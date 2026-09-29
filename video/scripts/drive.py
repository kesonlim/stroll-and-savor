"""Thin rclone wrappers -- the only module that talks to Google Drive."""
import datetime
import json
import subprocess
from pathlib import Path

import config


def _remote(path: str) -> str:
    return f"{config.REMOTE}:{path}"


def _lsjson(path: str, *flags: str) -> list:
    out = subprocess.run(
        ["rclone", "lsjson", _remote(path), *flags],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out or "[]")


def _parse_time(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def list_shoots() -> list:
    """Shoot folders in the inbox: [{name, created}] (created = Drive btime)."""
    shoots = []
    for d in _lsjson(config.INBOX, "--dirs-only", "--metadata"):
        btime = (d.get("Metadata") or {}).get("btime") or d["ModTime"]
        shoots.append({"name": d["Name"], "created": _parse_time(btime)})
    return shoots


def list_clips(shoot: str) -> list:
    """Video files in a shoot folder: [{name, size, modified}], photos ignored."""
    return [
        {"name": f["Name"], "size": f["Size"], "modified": _parse_time(f["ModTime"])}
        for f in _lsjson(f"{config.INBOX}/{shoot}", "--files-only")
        if Path(f["Name"]).suffix.lower() in config.VIDEO_EXTS
    ]


def has_plan(shoot: str) -> bool:
    try:
        return any(f["Name"] == "plan.json" for f in _lsjson(f"{config.OUTBOX}/{shoot}", "--files-only"))
    except subprocess.CalledProcessError:  # outbox folder doesn't exist yet
        return False


def pull_clip(shoot: str, clip: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["rclone", "copyto", _remote(f"{config.INBOX}/{shoot}/{clip}"), str(dest_dir / clip)],
        check=True,
    )
    return dest_dir / clip


def push_files(files: list, shoot: str) -> None:
    for f in files:
        subprocess.run(
            ["rclone", "copyto", str(f), _remote(f"{config.OUTBOX}/{shoot}/{Path(f).name}")],
            check=True,
        )
