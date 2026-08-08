import subprocess, pathlib, json
from PIL import Image

BASE = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad")
SVG = BASE / "logo-master" / "svg"
PNG = BASE / "logo-master" / "png"
PNG.mkdir(parents=True, exist_ok=True)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# This headless Chrome build reserves a fixed 87px band at the bottom of every
# screenshot regardless of content or window size (verified empirically).
# Work around it by requesting extra height and cropping the reserved band off.
HEADLESS_BOTTOM_BUG_PX = 87

def _shoot(html, out_path, width, height, transparent):
    tmp_html = BASE / f"_render_tmp_{out_path.stem}.html"
    tmp_html.write_text(html)
    raw_path = BASE / f"_raw_{out_path.stem}.png"
    args = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
        f"--screenshot={raw_path}",
        f"--window-size={width},{height + HEADLESS_BOTTOM_BUG_PX}",
    ]
    if transparent:
        args.append("--default-background-color=00000000")
    args.append(f"file://{tmp_html}")
    subprocess.run(args, check=True, capture_output=True)
    im = Image.open(raw_path)
    im.crop((0, 0, width, height)).save(out_path)
    raw_path.unlink()
    tmp_html.unlink()

def render(svg_path, out_path, width, height, transparent=True):
    html = f"""<html><head><style>
html,body{{margin:0;padding:0;overflow:hidden;background:transparent;}}
img{{display:block;width:{width}px;height:{height}px;}}
</style></head><body>
<img src="file://{svg_path}">
</body></html>"""
    _shoot(html, out_path, width, height, transparent)

def render_square(svg_path, out_path, size, bg_color=None, safe_ratio=0.66):
    """Center the mark in a square canvas at safe_ratio of the square, with optional bg fill."""
    bg_style = bg_color if bg_color else "transparent"
    ar = svg_aspect(svg_path.name)
    inner_w = size * safe_ratio
    inner_h = inner_w / ar
    if inner_h > size * safe_ratio:
        inner_h = size * safe_ratio
        inner_w = inner_h * ar
    left = (size - inner_w) / 2
    top = (size - inner_h) / 2
    html = f"""<html><head><style>
html,body{{margin:0;padding:0;overflow:hidden;}}
.canvas{{position:relative;width:{size}px;height:{size}px;background:{bg_style};}}
img{{position:absolute;left:{left}px;top:{top}px;width:{inner_w}px;height:{inner_h}px;}}
</style></head><body>
<div class="canvas"><img src="file://{svg_path}"></div>
</body></html>"""
    _shoot(html, out_path, size, size, bg_color is None)

def svg_aspect(svg_file):
    txt = (SVG / svg_file).read_text()
    vb = txt.split('viewBox="')[1].split('"')[0]
    _, _, w, h = [float(v) for v in vb.split()]
    return w / h

PAPER = "#f1f0ea"
INK = "#2e2e2c"

MASTER_SIZE = 1024
DOWNSIZES = [512, 320, 200, 180, 32, 16]

sq_masters = [
    ("monogram-ink-on-transparent.svg", "avatar-transparent", None),
    ("monogram-ink-on-transparent.svg", "avatar-on-paper", PAPER),
    ("monogram-paper-on-transparent.svg", "avatar-on-ink", INK),
]

for svg_file, out_stem, bg in sq_masters:
    master_path = PNG / f"{out_stem}-{MASTER_SIZE}.png"
    render_square(SVG / svg_file, master_path, MASTER_SIZE, bg_color=bg, safe_ratio=0.74)
    print(master_path.name, MASTER_SIZE, "x", MASTER_SIZE, "bg=", bg)
    master_im = Image.open(master_path)
    for size in DOWNSIZES:
        if size == MASTER_SIZE:
            continue
        resized = master_im.resize((size, size), Image.LANCZOS)
        out_name = f"{out_stem}-{size}.png"
        resized.save(PNG / out_name)
        print(" ->", out_name, size, "x", size)

jobs = []
# Wordmark: wide lockup, for banners/headers, transparent + on backgrounds
word_ar = svg_aspect("wordmark-ink-on-transparent.svg")
for width in [2400, 1200, 800, 400]:
    h = round(width / word_ar)
    jobs.append(("wordmark-ink-on-transparent.svg", f"wordmark-transparent-w{width}.png", width, h, True))
    jobs.append(("wordmark-paper-on-transparent.svg", f"wordmark-transparent-w{width}-forDark.png", width, h, True))
for width in [1600]:
    h = round(width / word_ar)
    jobs.append(("wordmark-ink-on-paper.svg", f"wordmark-on-paper-w{width}.png", width, h, False))
    jobs.append(("wordmark-paper-on-ink.svg", f"wordmark-on-ink-w{width}.png", width, h, False))

for svg_file, out_name, w, h, transparent in jobs:
    render(SVG / svg_file, PNG / out_name, w, h, transparent)
    print(out_name, w, "x", h)

print("done rendering", len(jobs) + len(sq_masters) * len(DOWNSIZES), "pngs")
