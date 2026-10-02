"""Walking-tour video pipeline entry point (video/README.md).

  python3 video/scripts/run.py process "<shoot folder>"   # steps 1-3 for one shoot, now
  python3 video/scripts/run.py watch                      # launchd: auto-plan new shoots
  python3 video/scripts/run.py approve "<shoot folder>"   # steps 4-5: render 4K video & package for YouTube
"""
import datetime
import fcntl
import shutil
import sys

import analyze
import config
import drive
import ingest
import package
import plan
import render


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


def approve(shoot: str) -> None:
    job = config.SCRATCH / shoot
    out_dir = job / "out"
    plan_file = out_dir / "plan.json"

    if not plan_file.exists():
        print(f"[{shoot}] local plan not found; checking Drive '{config.OUTBOX}/{shoot}/plan.json'...")
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            drive.pull_file(shoot, "plan.json", out_dir)
        except Exception as e:
            sys.exit(f"Could not locate plan.json on local disk or Drive for '{shoot}': {e}")

    plan_data = json.loads(plan_file.read_text())

    print(f"[{shoot}] 4/5 render: cutting and compositing overlays ({len(plan_data.get('clips', []))} clips)")
    video_path = render.run(shoot, job, plan_data)

    print(f"[{shoot}] 5/5 package: generating YouTube metadata & timestamps")
    pkg_files = package.run(shoot, job, plan_data)

    plan_data["status"] = "rendered"
    plan_file.write_text(json.dumps(plan_data, indent=2, ensure_ascii=False))

    all_upload_files = [video_path, plan_file] + pkg_files
    print(f"[{shoot}] uploading completed video and publication package to Drive '{config.OUTBOX}/{shoot}/'...")
    drive.push_files(all_upload_files, shoot)
    print(f"[{shoot}] SUCCESS: 4K video rendered and uploaded to Drive with publication package.")


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
    elif cmd == "approve":
        approve(sys.argv[2])


if __name__ == "__main__":
    main()
