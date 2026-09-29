"""Step 2 -- Analyze: find dead air (ffmpeg) and name places (vision model).

Dead air  = ffmpeg freezedetect on the proxy (standing still, blocked view).
Places    = one frame every FRAME_INTERVAL_S, tiled into GRIDxGRID contact
            sheets, read by `claude -p` (headless Claude Code, no API key
            needed). A cell's position encodes its timestamp, so frames need
            no burned-in labels (this ffmpeg build has no drawtext).

Writes <job>/analysis.json.
"""
import json
import re
import subprocess
from pathlib import Path

import config

SHEETS_PER_CALL = 12
FREEZE_NOISE = "0.003"   # freezedetect noise tolerance; raise if handheld shake hides pauses


def detect_freezes(proxy: Path) -> list:
    err = subprocess.run([
        "ffmpeg", "-hide_banner", "-i", str(proxy), "-an",
        "-vf", f"fps=4,scale=320:-2,freezedetect=n={FREEZE_NOISE}:d={config.FREEZE_MIN_S}",
        "-f", "null", "-",
    ], capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", err)]
    return [{"start": s, "end": e} for s, e in zip(starts, ends)]


def make_sheets(proxy: Path, out_dir: Path, prefix: str) -> list:
    out_dir.mkdir(parents=True, exist_ok=True)
    g = config.SHEET_GRID
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(proxy), "-an",
        "-vf", f"fps=1/{config.FRAME_INTERVAL_S},scale=480:-2,tile={g}x{g}:padding=4",
        "-q:v", "4", str(out_dir / f"{prefix}_%03d.jpg"),
    ], check=True)
    return sorted(out_dir.glob(f"{prefix}_*.jpg"))


PROMPT = """You are logging a walking-tour video for the YouTube channel Stroll & Savor.
Shoot folder: "{shoot}"

Each image below is a contact sheet of {g}x{g} video frames, read left-to-right,
top-to-bottom (cell 0 = top-left). Unused trailing cells are black -- skip them.
{manifest}

Read every sheet with the Read tool. For each non-black cell, report:
- place: the most specific place name you can support from what is visible
  (street signs, shopfronts, landmarks) plus the shoot name and GPS hint.
  Prefer a real name ("Haji Lane", "Tekka Centre hawker stalls") over a
  description. If you genuinely can't tell, reuse the previous cell's place.
  Never invent a name you can't support.
- kind: one of street, market, food, shop, park, transit, indoor, other
- dead_air: true only if the frame shows nothing worth watching
  (lens blocked, pointing at the ground, pocket shot)

Reply with ONLY a JSON array, no prose:
[{{"sheet": "<file name>", "cell": 0, "place": "...", "kind": "street", "dead_air": false}}, ...]
"""


def name_places(shoot: str, job: Path, sheets: list, hint: dict) -> list:
    results = []
    for i in range(0, len(sheets), SHEETS_PER_CALL):
        batch = sheets[i:i + SHEETS_PER_CALL]
        manifest = "\n".join(
            f"- {s.name}  (clip {hint[s]['clip']}, GPS {hint[s]['location'] or 'unknown'})"
            for s in batch
        )
        if results:
            manifest += f"\n(The previous batch ended at: {results[-1]['place']})"
        print(f"  vision: sheets {i + 1}-{i + len(batch)} of {len(sheets)}")
        out = subprocess.run(
            ["claude", "-p", PROMPT.format(shoot=shoot, g=config.SHEET_GRID, manifest=manifest),
             "--model", config.VISION_MODEL, "--output-format", "json", "--allowedTools", "Read"],
            cwd=job / "sheets", check=True, capture_output=True, text=True,
        ).stdout
        text = json.loads(out)["result"]
        results.extend(json.loads(text[text.index("["): text.rindex("]") + 1]))
    return results


def run(shoot: str, job: Path, clips: list) -> dict:
    sheets, hint, offsets, freezes = [], {}, {}, []
    t0 = 0.0
    for n, clip in enumerate(clips):
        offsets[clip["name"]] = t0
        proxy = job / clip["proxy"]
        print(f"  analyze {clip['name']}")
        freezes += [{"clip": clip["name"], **f} for f in detect_freezes(proxy)]
        for idx, s in enumerate(make_sheets(proxy, job / "sheets", f"c{n:02d}")):
            sheets.append(s)
            hint[s] = {"clip": clip["name"], "location": clip["location"], "index": idx}
        t0 += clip["duration"]

    per_sheet = config.SHEET_GRID ** 2
    by_name = {s.name: s for s in sheets}
    frames = []
    for r in name_places(shoot, job, sheets, hint):
        s = by_name.get(Path(r["sheet"]).name)
        if s is None:
            continue
        h = hint[s]
        clip_t = (h["index"] * per_sheet + int(r["cell"])) * config.FRAME_INTERVAL_S
        frames.append({
            "t": round(offsets[h["clip"]] + clip_t, 2), "clip": h["clip"], "clip_t": clip_t,
            "place": r["place"], "kind": r.get("kind", "other"), "dead_air": bool(r.get("dead_air")),
        })

    analysis = {"frames": sorted(frames, key=lambda f: f["t"]), "freezes": freezes, "offsets": offsets}
    (job / "analysis.json").write_text(json.dumps(analysis, indent=2))
    return analysis
