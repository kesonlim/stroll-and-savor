# Video pipeline

Turns a raw walking-tour shoot into an edit plan, and (next build stage) a
finished video for the Stroll & Savor YouTube channel. Channel format is
long-form, lightly edited 4K walks, so "editing" here means trimming dead air
and adding chapters, place-name overlays and quiet background music, not
cutting a highlight reel.

## Flow

```
Drive: 01 - Footage/<shoot>/        (photos + clips, as uploaded)
  1 Ingest   pull one clip at a time -> ffprobe -> 720p proxy -> delete raw
  2 Analyze  freezedetect (standing still) + claude -p on frame contact sheets (place names)
  3 Plan     plan.json + plan.md + contact.jpg -> uploaded to the outbox
  --- you review and approve ---
  4 Render   (not built yet) re-pull originals, apply cuts, overlays, music
  5 Package  (not built yet) title/description/chapters draft
Drive: 02 - Edited Footage/01 - Edited by Claude/<shoot>/
```

One **shoot folder** = one video. Only video files (`.mov/.mp4/.m4v`) are
used; photos are ignored. Clips are ordered by capture time.

Nothing is uploaded to YouTube. Output sits in the Drive outbox for human
review, same human-review-gate policy as `content/` and `scraper/`.

## Setup (once)

```
brew install rclone ffmpeg
rclone config create gdrive drive scope=drive root_folder_id=1LMTImGgvO21L7fm-ynLW6Ly2LqL_eaCN
```

The second command opens a browser for Google sign-in. Use the account that
owns the footage tree. `claude` (Claude Code CLI) must be on `PATH`; place
naming runs through it headlessly, so no API key is needed.

## Use

```
python3 video/scripts/run.py process "89 - Kura Zen 26th Sep 2026"   # plan one shoot now
python3 video/scripts/run.py watch                                    # plan any new, finished-uploading shoots
```

`watch` only picks up shoot folders created on or after `AUTO_SINCE` in
`scripts/config.py`, so older shoots are never processed unless you name
them with `process`. A folder is treated as still uploading until none of its
clips changed for `STABLE_MINUTES`.

To change a plan, edit `plan.json` in the outbox folder (delete a cut to keep
that footage, rename or move a chapter), then approve. Approval (steps 4-5)
is the next build stage.

## Disk

Local work happens in `~/Library/Caches/stroll-savor-video/<shoot>/`
(override with `SSV_SCRATCH`). Only one raw clip is on disk at a time, next to
small proxies. `process` refuses to start unless the largest clip plus 2 GB
fits in free space.

## Known limits

- This Homebrew ffmpeg has no `drawtext`/libass, so step 4 will render
  overlays as PNGs with the brand fonts (headless Chrome, like
  `content/scripts/render.py`) and composite them with `overlay`.
- `FREEZE_NOISE` in `analyze.py` is untuned; handheld shake while standing
  still may hide pauses. Tune it on the first real shoot.
- Place names are only as good as what's visible plus GPS. Check the
  contact sheet before approving.
