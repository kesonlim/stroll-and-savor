"""Shared HTML -> PNG rendering via headless Chrome/Chromium, same approach
as brand/scripts/render_platform_assets.py. Browser location is
auto-detected (see find_browser) so this runs both on this Mac and inside
the scheduled cloud routine's environment, wherever a Chromium-family
browser happens to live there -- untested in the cloud context as of this
writing, see content/README.md."""
import glob
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image

PAD_PX = 100  # extra height requested then cropped away, absorbs any chrome/toolbar reservation quirks

_CANDIDATE_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # this Mac
    "/opt/pw-browsers/*/chrome-linux/chrome",  # Playwright-provisioned cloud sandboxes (glob)
    str(Path.home() / ".cache/ms-playwright/chromium-*/chrome-linux/chrome"),  # Playwright's default cache (glob)
]
_CANDIDATE_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]


class BrowserNotFoundError(RuntimeError):
    pass


def find_browser() -> str:
    env_override = os.environ.get("STROLL_SAVOR_CHROME")
    if env_override and Path(env_override).exists():
        return env_override

    for pattern in _CANDIDATE_PATHS:
        if "*" in pattern:
            matches = sorted(glob.glob(pattern))
            if matches:
                return matches[-1]
        elif Path(pattern).exists():
            return pattern

    for name in _CANDIDATE_NAMES:
        found = shutil.which(name)
        if found:
            return found

    raise BrowserNotFoundError(
        "No Chromium-family browser found (checked known Mac/Playwright paths, "
        "PATH lookups for google-chrome/chromium, and $STROLL_SAVOR_CHROME). "
        "Image rendering needs a real browser; set $STROLL_SAVOR_CHROME to an "
        "explicit binary path if one exists somewhere non-standard."
    )


def render_html_to_png(html: str, out_path: Path, width: int, height: int, transparent: bool = False):
    chrome = find_browser()
    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_html = out_path.with_suffix(".render.html")
    raw_path = out_path.with_suffix(".raw.png")
    tmp_html.write_text(html)

    args = [
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
        f"--screenshot={raw_path}",
        f"--window-size={width},{height + PAD_PX}",
        "--force-device-scale-factor=1",
    ]
    if transparent:
        args.append("--default-background-color=00000000")
    args.append(f"file://{tmp_html}")
    subprocess.run(args, check=True, capture_output=True)

    im = Image.open(raw_path)
    im.crop((0, 0, width, height)).save(out_path)
    raw_path.unlink()
    tmp_html.unlink()
