"""Settings for the walking-tour video pipeline (video/README.md).

Drive is both ends: raw shoot folders are read from INBOX, plans and
finished edits are written to OUTBOX. Only one clip at a time is ever held
at full resolution on the local disk (SCRATCH).
"""
import os
from pathlib import Path

# rclone remote, created with root_folder_id = the footage tree root
# (Drive folder 1LMTImGgvO21L7fm-ynLW6Ly2LqL_eaCN), so paths below are
# relative to that root.
REMOTE = "gdrive"
INBOX = "01 - Footage"                                # Drive id 1YT8uwHFafRDaimUikFlrphr3gKQhGgZS
OUTBOX = "02 - Edited Footage/01 - Edited by Claude"  # Drive id 1GCph231Elb2UMG90VvEv2yhTrZvOlkz0

SCRATCH = Path(os.environ.get("SSV_SCRATCH", "~/Library/Caches/stroll-savor-video")).expanduser()

# The auto-watcher only picks up shoot folders created on/after this date,
# so the ~89 existing shoots are never processed unless named explicitly.
AUTO_SINCE = "2026-09-29"
# A folder counts as "done uploading" once no file in it changed for this long.
STABLE_MINUTES = 30

VIDEO_EXTS = {".mov", ".mp4", ".m4v"}

PROXY_HEIGHT = 720
FRAME_INTERVAL_S = 20        # one analysis frame per this many seconds of footage
SHEET_GRID = 3               # frames tiled SHEET_GRID x SHEET_GRID per contact sheet
FREEZE_MIN_S = 8             # standing still at least this long counts as dead air
TRIM_PAD_S = 1.5             # keep this much of each dead-air stretch on both sides
MIN_CHAPTER_S = 60           # merge place changes closer together than this
VISION_MODEL = "sonnet"      # claude -p --model alias
