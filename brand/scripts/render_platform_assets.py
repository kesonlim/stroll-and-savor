import subprocess, pathlib
from PIL import Image

BASE = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad")
SVG = BASE / "logo-master" / "svg"
OUT = BASE / "platform-assets"
(OUT / "avatars").mkdir(parents=True, exist_ok=True)
(OUT / "banners").mkdir(parents=True, exist_ok=True)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
HEADLESS_BOTTOM_BUG_PX = 87  # fixed reservation bug in this Chrome build, verified empirically

PAPER = "#f1f0ea"
INK = "#2e2e2c"
RUST = "#b4552f"
TEAL = "#3e7c74"
RULE = "#d7d5c8"

def svg_aspect(path):
    txt = path.read_text()
    vb = txt.split('viewBox="')[1].split('"')[0]
    _, _, w, h = [float(v) for v in vb.split()]
    return w / h

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

def render_html(html, out_path, width, height, transparent=False):
    _shoot(html, out_path, width, height, transparent)

def render_square_avatar(svg_path, out_path, size, bg_color, safe_ratio=0.74):
    ar = svg_aspect(svg_path)
    inner_w = size * safe_ratio
    inner_h = inner_w / ar
    left = (size - inner_w) / 2
    top = (size - inner_h) / 2
    html = f"""<html><head><style>
html,body{{margin:0;padding:0;overflow:hidden;}}
.canvas{{position:relative;width:{size}px;height:{size}px;background:{bg_color};}}
img{{position:absolute;left:{left}px;top:{top}px;width:{inner_w}px;height:{inner_h}px;}}
</style></head><body>
<div class="canvas"><img src="file://{svg_path}"></div>
</body></html>"""
    render_html(html, out_path, size, size, transparent=(bg_color == "transparent"))

# ---- Avatars: exact sizes each platform actually asks for ----
AVATAR_SIZES = {
    "facebook-320.png": 320,
    "instagram-320.png": 320,
    "tiktok-200.png": 200,
    "youtube-800.png": 800,
    "linkedin-company-300.png": 300,
    "linkedin-personal-400.png": 400,
    "xiaohongshu-300.png": 300,
    "website-favicon-512.png": 512,
}
for name, size in AVATAR_SIZES.items():
    render_square_avatar(SVG / "monogram-ink-on-transparent.svg", OUT / "avatars" / name, size, PAPER)
    print("avatar:", name, size)

print("done avatars")

# ---- Banners: composed, dot-grid ground + wordmark + route-line + tagline ----
WORDMARK_SVG = (SVG / "wordmark-ink-on-transparent.svg").read_text()
TAGLINE = "spontaneous escapes &middot; business class &middot; every month"

FONT_DIR = BASE / "fonts"
def b64(name):
    return (FONT_DIR / f"{name}.b64").read_text().strip()

FONT_FACES = f"""
@font-face {{ font-family:'Courier Prime'; src:url(data:font/woff2;base64,{b64('courier_prime')}) format('woff2'); font-weight:700; }}
@font-face {{ font-family:'Space Mono'; src:url(data:font/woff2;base64,{b64('spacemono')}) format('woff2'); font-weight:400; }}
"""

ROUTE_LINE = """<svg viewBox="0 0 300 60" preserveAspectRatio="none" style="width:100%;height:100%;">
<path d="M4 40 C60 40 50 15 110 30 C160 42 180 10 230 24 C260 32 270 15 296 20"
fill="none" stroke="#b4552f" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0.2 7"/>
</svg>"""

def render_banner(out_name, width, height, safe_w=None, safe_h=None, wordmark_scale=1.0, show_tagline=True, show_routeline=True):
    safe_w = safe_w or width
    safe_h = safe_h or height
    word_w = min(safe_w * 0.62, 520 * wordmark_scale)
    html = f"""<html><head><style>
{FONT_FACES}
html,body{{margin:0;padding:0;overflow:hidden;}}
.canvas{{position:relative;width:{width}px;height:{height}px;background:{PAPER};
  background-image:radial-gradient(circle, rgba(46,46,44,0.09) 1px, transparent 1px);
  background-size:18px 18px;}}
.safe{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:{safe_w}px;height:{safe_h}px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;}}
.wordmark{{width:{word_w}px;}}
.wordmark svg{{width:100%;height:auto;display:block;}}
.tagline{{font-family:'Space Mono',monospace;font-size:{max(11, safe_h*0.045):.0f}px;letter-spacing:0.08em;text-transform:uppercase;color:#6d6a5f;white-space:nowrap;}}
.routeline{{width:{min(safe_w*0.5, 300)}px;height:{min(safe_h*0.18, 40)}px;opacity:0.9;}}
</style></head><body>
<div class="canvas">
  <div class="safe">
    <div class="wordmark">{WORDMARK_SVG}</div>
    {'<div class="tagline">' + TAGLINE + '</div>' if show_tagline else ''}
    {'<div class="routeline">' + ROUTE_LINE + '</div>' if show_routeline else ''}
  </div>
</div>
</body></html>"""
    render_html(html, OUT / "banners" / out_name, width, height, transparent=False)
    print("banner:", out_name, width, "x", height)

# Facebook cover: 820x312, safe zone accounts for profile pic overlap bottom-left in practice,
# but we keep centered since crop varies mobile/desktop.
render_banner("facebook-cover-820x312.png", 820, 312, safe_w=680, safe_h=230, wordmark_scale=0.85)

# YouTube channel art: 2560x1440 canvas, only the centered 1546x423 safe area is guaranteed visible everywhere.
render_banner("youtube-banner-2560x1440.png", 2560, 1440, safe_w=1546, safe_h=423, wordmark_scale=1.3)

# LinkedIn company page banner: 1128x191 — very short, no tagline/routeline (no room).
render_banner("linkedin-company-1128x191.png", 1128, 191, safe_w=900, safe_h=150, wordmark_scale=0.6, show_tagline=False, show_routeline=False)

# LinkedIn personal banner: 1584x396
render_banner("linkedin-personal-1584x396.png", 1584, 396, safe_w=1300, safe_h=300, wordmark_scale=0.9)

# Website OG / share image: 1200x630
render_banner("website-og-1200x630.png", 1200, 630, safe_w=980, safe_h=460, wordmark_scale=1.0)

print("done banners")

