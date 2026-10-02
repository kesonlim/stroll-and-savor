"""Step 4 -- Render: assemble trimmed clips and composite brand overlays.

Flow:
  1. For each clip, compute kept segments by inverting cuts from plan.json.
  2. Pull one raw clip at a time from Drive, extract trimmed segments, and delete the raw clip.
  3. Concatenate all trimmed segments via ffmpeg concat demuxer.
  4. Generate branded 4K lower-third PNG overlays for every chapter landmark.
  5. Composite overlays using ffmpeg into the final 4K video.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import config
import drive

REPO_ROOT = Path(__file__).resolve().parents[2]


def find_browser() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        str(Path.home() / ".cache/ms-playwright/chromium-*/chrome-linux/chrome"),
    ]
    for p in candidates:
        if "*" in p:
            m = sorted(glob.glob(p))
            if m:
                return m[-1]
        elif Path(p).exists():
            return p
    for name in ["google-chrome", "google-chrome-stable", "chromium"]:
        found = shutil.which(name)
        if found:
            return found
    return "google-chrome"


def get_encoder() -> tuple:
    """Return best available video encoder and bitrate flags."""
    try:
        out = subprocess.run(["ffmpeg", "-encoders"], capture_output=True, text=True, check=True).stdout
        if "h264_videotoolbox" in out:
            return ("h264_videotoolbox", ["-b:v", "45M"])
        if "libx264" in out:
            return ("libx264", ["-crf", "18", "-preset", "veryfast"])
    except Exception:
        pass
    return ("libx264", ["-crf", "18", "-preset", "veryfast"])


def get_clip_duration(clip_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(clip_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def get_clip_dimensions(clip_path: Path) -> tuple:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=s=x:p=0", str(clip_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    parts = res.stdout.strip().split("x")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    return 3840, 2160


def compute_keeps(clip_duration: float, cuts: list) -> list:
    """Invert cuts [start, end] into kept intervals [start, end]."""
    if not cuts:
        return [(0.0, clip_duration)]
    
    sorted_cuts = sorted(cuts, key=lambda c: c["start"])
    keeps = []
    curr = 0.0
    for c in sorted_cuts:
        c_start = max(0.0, c["start"])
        c_end = min(clip_duration, c["end"])
        if c_start > curr + 0.3:
            keeps.append((curr, c_start))
        curr = max(curr, c_end)
    if curr < clip_duration - 0.3:
        keeps.append((curr, clip_duration))
    return keeps


def render_overlay_png(text: str, out_png: Path, width: int = 3840, height: int = 2160) -> None:
    """Render a transparent 4K lower-third card with Field Notes typography."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    html_file = out_png.with_suffix(".html")
    
    html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@700&family=IBM+Plex+Sans:wght@600;700&family=Space+Mono:wght@400;700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: {width}px;
    height: {height}px;
    background: transparent;
    overflow: hidden;
    position: relative;
  }}
  .lower-third {{
    position: absolute;
    left: 120px;
    bottom: 120px;
    display: inline-flex;
    flex-direction: column;
    gap: 12px;
    background: rgba(241, 240, 234, 0.94);
    border: 2px solid #d7d5c8;
    border-radius: 24px;
    padding: 28px 48px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
    max-width: 1400px;
  }}
  .eyebrow {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Space Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    color: #994827;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }}
  .dot {{
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #b4552f;
  }}
  .title {{
    font-family: 'Courier Prime', monospace;
    font-size: 54px;
    font-weight: 700;
    color: #2e2e2c;
    line-height: 1.15;
  }}
</style>
</head>
<body>
  <div class="lower-third">
    <div class="eyebrow"><span class="dot"></span>Stroll &amp; Savor &middot; Singapore</div>
    <div class="title">{text}</div>
  </div>
</body>
</html>"""
    html_file.write_text(html)
    
    browser = find_browser()
    raw_png = out_png.with_suffix(".raw.png")
    cmd = [
        browser, "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--screenshot={raw_png}",
        f"--window-size={width},{height}",
        "--default-background-color=00000000",
        f"file://{html_file}"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if raw_png.exists():
        raw_png.rename(out_png)
    if html_file.exists():
        html_file.unlink()


def run(shoot: str, job: Path, plan: dict) -> Path:
    out_dir = job / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = job / "render_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    
    clips = plan["clips"]
    all_cuts = plan.get("cuts", [])
    cuts_by_clip = {}
    for c in all_cuts:
        cuts_by_clip.setdefault(c["clip"], []).append(c)

    encoder, enc_args = get_encoder()
    print(f"[{shoot}] Using video encoder: {encoder}")

    chunk_files = []
    raw_dir = job / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # 1. Download one clip at a time, extract keeps, delete raw
    width, height = 3840, 2160
    for clip_idx, clip_name in enumerate(clips):
        print(f"[{shoot}] Processing clip {clip_idx + 1}/{len(clips)}: {clip_name}")
        local_raw = drive.pull_clip(shoot, clip_name, raw_dir)
        try:
            dur = get_clip_duration(local_raw)
            width, height = get_clip_dimensions(local_raw)
            clip_cuts = cuts_by_clip.get(clip_name, [])
            keeps = compute_keeps(dur, clip_cuts)

            for keep_idx, (start, end) in enumerate(keeps):
                chunk_name = f"chunk_{clip_idx:03d}_{keep_idx:03d}.mp4"
                chunk_path = work_dir / chunk_name
                trim_cmd = [
                    "ffmpeg", "-y", "-v", "error",
                    "-ss", str(round(start, 3)), "-to", str(round(end, 3)),
                    "-i", str(local_raw),
                    "-c:v", encoder, *enc_args,
                    "-c:a", "aac", "-b:a", "192k",
                    str(chunk_path)
                ]
                subprocess.run(trim_cmd, check=True)
                chunk_files.append(chunk_path)
        finally:
            if local_raw.exists():
                local_raw.unlink()

    if not chunk_files:
        raise RuntimeError("No video chunks generated from keep segments")

    # 2. Concat all chunks
    concat_list_file = work_dir / "concat_list.txt"
    concat_lines = [f"file '{c.resolve()}'" for c in chunk_files]
    concat_list_file.write_text("\n".join(concat_lines))

    assembled_video = work_dir / "assembled.mp4"
    print(f"[{shoot}] Concatenating {len(chunk_files)} segments...")
    concat_cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_list_file),
        "-c", "copy", str(assembled_video)
    ]
    subprocess.run(concat_cmd, check=True)

    # 3. Generate overlays
    overlays = plan.get("overlays", [])
    overlay_pngs = []
    if overlays:
        print(f"[{shoot}] Generating {len(overlays)} brand overlays ({width}x{height})...")
        for i, ov in enumerate(overlays):
            ov_png = work_dir / f"overlay_{i:03d}.png"
            render_overlay_png(ov["text"], ov_png, width=width, height=height)
            overlay_pngs.append((ov_png, ov["at"], ov.get("duration", 5)))

    # 4. Composite overlays
    final_output = out_dir / f"{shoot} - 4K Walk.mp4"
    if overlay_pngs:
        print(f"[{shoot}] Applying overlays to assembled video...")
        inputs = ["-i", str(assembled_video)]
        filter_parts = []
        last_v = "0:v"
        for i, (png_path, at, dur) in enumerate(overlay_pngs):
            inputs.extend(["-i", str(png_path)])
            out_v = f"v{i+1}"
            filter_parts.append(
                f"[{last_v}][{i+1}:v]overlay=0:0:enable='between(t,{at},{at+dur})':format=auto[{out_v}]"
            )
            last_v = out_v

        filter_complex = ";".join(filter_parts)
        comp_cmd = [
            "ffmpeg", "-y", "-v", "error",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", f"[{last_v}]", "-map", "0:a?",
            "-c:v", encoder, *enc_args,
            "-c:a", "copy",
            str(final_output)
        ]
        subprocess.run(comp_cmd, check=True)
    else:
        shutil.copy(assembled_video, final_output)

    # Clean up work dir to reclaim space
    shutil.rmtree(work_dir, ignore_errors=True)
    print(f"[{shoot}] Render complete: {final_output}")
    return final_output
