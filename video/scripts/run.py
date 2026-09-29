"""Walking-tour video pipeline entry point (video/README.md).

  python3 video/scripts/run.py process "<shoot folder>"   # steps 1-3 for one shoot, now
  python3 video/scripts/run.py watch                      # launchd: auto-plan new shoots
  python3 video/scripts/run.py approve "<shoot folder>"   # steps 4-5 (not built yet)
"""
import datetime
import fcntl
import shutil
import sys

import analyze
import config
import drive
import ingest
import plan


def process(shoot: str) -> None:
    clips = drive.list_clips(shoot)
    if not clips:
        sys.exit(f"No video files in '{config.INBOX}/{shoot}'")
    job = config.SCRATCH / shoot
    job.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(config.SCRATCH).free
    biggest = max(c["size"] for c in clips)
    if free < biggest + 2e9:
        sys.exit(f"Need {biggest / 1e9:.1f} GB + 2 GB headroom free for the largest clip, only {free / 1e9:.1f} GB free")

    print(f"[{shoot}] 1/3 ingest ({len(clips)} clips)")
    clip_meta = ingest.run(shoot, job)
    print(f"[{shoot}] 2/3 analyze")
    analysis = analyze.run(shoot, job, clip_meta)
    print(f"[{shoot}] 3/3 plan")
    files = plan.run(shoot, job, clip_meta, analysis)
    drive.push_files(files, shoot)
    print(f"[{shoot}] plan uploaded to '{config.OUTBOX}/{shoot}/' -- review plan.md, then approve")


def watch() -> None:
    config.SCRATCH.mkdir(parents=True, exist_ok=True)
    lock = open(config.SCRATCH / ".watch.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return  # previous run still going
    since = datetime.datetime.fromisoformat(config.AUTO_SINCE).replace(tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    for s in drive.list_shoots():
        if s["created"] < since or drive.has_plan(s["name"]):
            continue
        clips = drive.list_clips(s["name"])
        if not clips:
            continue
        if now - max(c["modified"] for c in clips) < datetime.timedelta(minutes=config.STABLE_MINUTES):
            print(f"[{s['name']}] still uploading, will check again")
            continue
        process(s["name"])


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in {"process", "watch", "approve"}:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "watch":
        watch()
    elif len(sys.argv) < 3:
        sys.exit(f"usage: run.py {cmd} \"<shoot folder>\"")
    elif cmd == "process":
        process(sys.argv[2])
    else:
        sys.exit("approve (render + package) is the next build stage -- not implemented yet")


if __name__ == "__main__":
    main()
