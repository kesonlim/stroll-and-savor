"""Step 1 -- Ingest: pull each clip, probe it, make a 720p proxy, drop the raw.

Only one full-resolution clip is ever on local disk at a time; the render
step re-pulls originals later. Writes <job>/clips.json in timeline order.
"""
import json
import subprocess
from pathlib import Path

import config
import drive


def probe(path: Path) -> dict:
    info = json.loads(subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout)
    tags = info["format"].get("tags", {})
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    num, den = video.get("avg_frame_rate", "0/1").split("/")
    return {
        "duration": float(info["format"]["duration"]),
        # iPhone footage carries local capture time + GPS in Apple tags
        "created": tags.get("com.apple.quicktime.creationdate") or tags.get("creation_time"),
        "location": tags.get("com.apple.quicktime.location.ISO6709"),
        "width": video["width"],
        "height": video["height"],
        "fps": round(int(num) / int(den), 3) if int(den) else None,
    }


def make_proxy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-hwaccel", "videotoolbox", "-i", str(src),
        "-vf", f"scale=-2:{config.PROXY_HEIGHT},format=yuv420p",
        "-c:v", "h264_videotoolbox", "-b:v", "2500k",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(dst),
    ], check=True)


def run(shoot: str, job: Path) -> list:
    clips_file = job / "clips.json"
    done = {c["name"]: c for c in json.loads(clips_file.read_text())} if clips_file.exists() else {}

    for clip in drive.list_clips(shoot):
        name = clip["name"]
        if name in done:
            continue
        print(f"  ingest {name} ({clip['size'] / 1e9:.1f} GB)")
        raw = drive.pull_clip(shoot, name, job / "raw")
        proxy = job / "proxies" / f"{Path(name).stem}.mp4"
        try:
            meta = probe(raw)
            make_proxy(raw, proxy)
        finally:
            raw.unlink(missing_ok=True)
        done[name] = {"name": name, "proxy": str(proxy.relative_to(job)), **meta}
        # checkpoint after every clip so an interrupted run resumes here
        clips_file.write_text(json.dumps(_ordered(done), indent=2))

    clips = _ordered(done)
    clips_file.write_text(json.dumps(clips, indent=2))
    return clips


def _ordered(done: dict) -> list:
    # capture time first, filename as tiebreak (IMG_0001 < IMG_0002)
    return sorted(done.values(), key=lambda c: (c["created"] or "", c["name"]))
