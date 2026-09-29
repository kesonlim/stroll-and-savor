"""Step 3 -- Plan: turn analysis into an editable, human-approved edit plan.

Writes to <job>/out/:
  plan.json   -- machine-readable; edit it to change cuts/chapters before approving
  plan.md     -- the same plan for a human read, incl. a paste-ready chapter list
  contact.jpg -- one frame per chapter, for a glance-check of place names
Nothing renders until you approve (video/README.md).
"""
import json
import subprocess
from pathlib import Path

import config


def fmt(t: float) -> str:
    t = int(round(t))
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def build_cuts(analysis: dict, clips: list) -> list:
    cuts = []
    for f in analysis["freezes"]:
        start, end = f["start"] + config.TRIM_PAD_S, f["end"] - config.TRIM_PAD_S
        if end > start:
            cuts.append({"clip": f["clip"], "start": round(start, 2), "end": round(end, 2),
                         "reason": f"standing still {f['end'] - f['start']:.0f}s"})
    # 2+ consecutive vision-flagged frames (lens blocked, pocket shot)
    run = []
    for f in analysis["frames"] + [None]:
        if f and f["dead_air"] and (not run or run[-1]["clip"] == f["clip"]):
            run.append(f)
            continue
        if len(run) >= 2:
            cuts.append({"clip": run[0]["clip"], "start": run[0]["clip_t"],
                         "end": run[-1]["clip_t"] + config.FRAME_INTERVAL_S, "reason": "nothing on screen"})
        run = [f] if f and f["dead_air"] else []
    order = [c["name"] for c in clips]
    return sorted(_merge(cuts), key=lambda c: (order.index(c["clip"]), c["start"]))


def _merge(cuts: list) -> list:
    merged = []
    for c in sorted(cuts, key=lambda c: (c["clip"], c["start"])):
        if merged and merged[-1]["clip"] == c["clip"] and c["start"] <= merged[-1]["end"]:
            merged[-1]["end"] = max(merged[-1]["end"], c["end"])
            merged[-1]["reason"] += f"; {c['reason']}"
        else:
            merged.append(dict(c))
    return merged


def edited_time(t: float, cuts: list, offsets: dict) -> float:
    """Map a raw-timeline time to where it lands after cuts are applied."""
    removed = 0.0
    for c in cuts:
        c0, c1 = offsets[c["clip"]] + c["start"], offsets[c["clip"]] + c["end"]
        if c1 <= t:
            removed += c1 - c0
        elif c0 < t:
            removed += t - c0
    return max(0.0, t - removed)


def build_chapters(analysis: dict, cuts: list) -> list:
    chapters = []
    for f in analysis["frames"]:
        if f["dead_air"]:
            continue
        at = edited_time(f["t"], cuts, analysis["offsets"])
        if not chapters:
            chapters.append({"at": 0, "title": f["place"], "clip": f["clip"], "clip_t": f["clip_t"]})
        elif f["place"] != chapters[-1]["title"] and at - chapters[-1]["at"] >= config.MIN_CHAPTER_S:
            chapters.append({"at": round(at, 1), "title": f["place"], "clip": f["clip"], "clip_t": f["clip_t"]})
    return chapters


def contact_sheet(job: Path, clips: list, chapters: list, out: Path) -> None:
    tmp = job / "chapter_frames"
    tmp.mkdir(exist_ok=True)
    for old in tmp.glob("*.jpg"):
        old.unlink()
    proxies = {c["name"]: job / c["proxy"] for c in clips}
    for i, ch in enumerate(chapters):
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-ss", str(ch["clip_t"] + 1), "-i", str(proxies[ch["clip"]]),
            "-frames:v", "1", "-vf", "scale=480:-2", str(tmp / f"ch_{i:03d}.jpg"),
        ], check=True)
    cols = min(4, len(chapters))
    rows = -(-len(chapters) // cols)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(tmp / "ch_%03d.jpg"),
        "-vf", f"tile={cols}x{rows}:padding=6:color=white", "-frames:v", "1", "-q:v", "3", str(out),
    ], check=True)


def run(shoot: str, job: Path, clips: list, analysis: dict) -> list:
    out = job / "out"
    out.mkdir(exist_ok=True)
    cuts = build_cuts(analysis, clips)
    chapters = build_chapters(analysis, cuts)
    raw_len = sum(c["duration"] for c in clips)
    cut_len = sum(c["end"] - c["start"] for c in cuts)

    plan = {
        "shoot": shoot,
        "status": "awaiting_approval",
        "clips": [c["name"] for c in clips],
        "raw_duration": round(raw_len, 1),
        "edited_duration": round(raw_len - cut_len, 1),
        "cuts": cuts,
        "chapters": [{"at": c["at"], "title": c["title"]} for c in chapters],
        "overlays": [{"at": c["at"], "text": c["title"], "duration": 5} for c in chapters],
        "music": {"source": "YouTube Audio Library", "track": None, "volume_db": -22},
    }
    (out / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False))

    lines = [
        f"# Edit plan: {shoot}",
        "",
        f"{len(clips)} clip(s), {fmt(raw_len)} raw -> **{fmt(raw_len - cut_len)} edited** "
        f"({len(cuts)} cuts removing {fmt(cut_len)}).",
        "",
        "## Chapters (paste into the YouTube description)",
        "",
        *[f"{fmt(c['at'])} {c['title']}" for c in chapters],
        "",
    ]
    if len(chapters) < 3:
        lines += ["> YouTube needs at least 3 chapters to show them -- add some in plan.json.", ""]
    lines += [
        "## Cuts",
        "",
        "| Clip | From | To | Why |",
        "|---|---|---|---|",
        *[f"| {c['clip']} | {fmt(c['start'])} | {fmt(c['end'])} | {c['reason']} |" for c in cuts],
        "",
        "## To approve",
        "",
        "Edit plan.json in this Drive folder if anything is wrong (delete a cut to keep that footage,",
        "rename a chapter title, move a chapter's `at`), then run:",
        "",
        f"    python3 video/scripts/run.py approve \"{shoot}\"",
        "",
    ]
    (out / "plan.md").write_text("\n".join(lines))

    if chapters:
        contact_sheet(job, clips, chapters, out / "contact.jpg")
    return sorted(out.iterdir())
