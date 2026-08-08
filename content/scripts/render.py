"""Shared HTML -> PNG rendering via headless Chrome, same approach as
brand/scripts/render_platform_assets.py. Kept local-machine-only (uses this
Mac's installed Chrome) -- not meant to run inside the scheduled cloud
routine, which only produces data (see scraper/), not images."""
import subprocess
from pathlib import Path
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAD_PX = 100  # extra height requested then cropped away, absorbs any chrome/toolbar reservation quirks


def render_html_to_png(html: str, out_path: Path, width: int, height: int, transparent: bool = False):
    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_html = out_path.with_suffix(".render.html")
    raw_path = out_path.with_suffix(".raw.png")
    tmp_html.write_text(html)

    args = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
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
