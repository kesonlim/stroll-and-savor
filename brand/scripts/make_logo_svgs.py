import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

FONT_PATH = "/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/fonts/courier_prime.ttf"
OUT_DIR = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/logo-master/svg")
OUT_DIR.mkdir(parents=True, exist_ok=True)

font = TTFont(FONT_PATH)
glyph_set = font.getGlyphSet()
cmap = font.getBestCmap()
upm = font["head"].unitsPerEm
ascent = font["hhea"].ascent
descent = font["hhea"].descent  # negative

def text_to_path(text, extra_tracking=0):
    """Return (path_d, total_width, ascent, descent) with glyphs laid left-to-right at baseline y=0, x growing right."""
    x = 0
    segments = []
    for ch in text:
        if ch == " ":
            gname = cmap.get(ord(" "))
        else:
            gname = cmap.get(ord(ch))
        if gname is None:
            gname = ".notdef"
        glyph = glyph_set[gname]
        pen = SVGPathPen(glyph_set)
        glyph.draw(pen)
        d = pen.getCommands()
        if d:
            segments.append(f'<g transform="translate({x},0)"><path d="{d}"/></g>')
        x += glyph.width + extra_tracking
    total_width = x - extra_tracking if segments else x
    return "\n".join(segments), x, ascent, descent

def build_svg(text, out_name, color, tracking=0, pad_ratio=0.12):
    body, width, asc, desc = text_to_path(text, extra_tracking=tracking)
    height = asc - desc
    pad = int(height * pad_ratio)
    vb_w = width + pad * 2
    vb_h = height + pad * 2
    # flip Y (font Y-up -> SVG Y-down), origin baseline at (pad, pad+asc)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" fill="{color}">
<g transform="translate({pad},{pad + asc}) scale(1,-1)">
{body}
</g>
</svg>
'''
    (OUT_DIR / out_name).write_text(svg)
    print(out_name, "viewBox", vb_w, vb_h)

INK = "#2e2e2c"
PAPER = "#f1f0ea"
RUST = "#b4552f"

# --- Wordmark: "stroll & savor" as two-tone (ampersand in rust) needs split build ---
def build_wordmark(out_name, base_color, amp_color, bg=None):
    pre, x1, asc, desc = text_to_path("stroll ", extra_tracking=0)
    amp, x2, _, _ = text_to_path("&", extra_tracking=0)
    post, x3, _, _ = text_to_path(" savor", extra_tracking=0)
    height = asc - desc
    pad = int(height * 0.12)
    total_w = x1 + x2 + x3
    vb_w = total_w + pad * 2
    vb_h = height + pad * 2
    bgrect = f'<rect x="0" y="0" width="{vb_w}" height="{vb_h}" fill="{bg}"/>' if bg else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}">
{bgrect}
<g transform="translate({pad},{pad + asc}) scale(1,-1)">
<g fill="{base_color}">{pre}</g>
<g fill="{amp_color}" transform="translate({x1},0)">{amp}</g>
<g fill="{base_color}" transform="translate({x1 + x2},0)">{post}</g>
</g>
</svg>
'''
    (OUT_DIR / out_name).write_text(svg)
    print(out_name, "viewBox", vb_w, vb_h)

build_wordmark("wordmark-ink-on-transparent.svg", INK, RUST, bg=None)
build_wordmark("wordmark-paper-on-transparent.svg", PAPER, "#e08a67", bg=None)
build_wordmark("wordmark-ink-on-paper.svg", INK, RUST, bg=PAPER)
build_wordmark("wordmark-paper-on-ink.svg", PAPER, "#e08a67", bg=INK)

# --- Monogram: "s&s" ---
def build_monogram(out_name, base_color, amp_color, bg=None):
    s1, x1, asc, desc = text_to_path("s")
    amp, x2, _, _ = text_to_path("&")
    s2, x3, _, _ = text_to_path("s")
    height = asc - desc
    pad = int(height * 0.12)
    total_w = x1 + x2 + x3
    vb_w = total_w + pad * 2
    vb_h = height + pad * 2
    bgrect = f'<rect x="0" y="0" width="{vb_w}" height="{vb_h}" fill="{bg}"/>' if bg else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}">
{bgrect}
<g transform="translate({pad},{pad + asc}) scale(1,-1)">
<g fill="{base_color}">{s1}</g>
<g fill="{amp_color}" transform="translate({x1},0)">{amp}</g>
<g fill="{base_color}" transform="translate({x1 + x2},0)">{s2}</g>
</g>
</svg>
'''
    (OUT_DIR / out_name).write_text(svg)
    print(out_name, "viewBox", vb_w, vb_h)

build_monogram("monogram-ink-on-transparent.svg", INK, RUST, bg=None)
build_monogram("monogram-paper-on-transparent.svg", PAPER, "#e08a67", bg=None)
build_monogram("monogram-ink-on-paper.svg", INK, RUST, bg=PAPER)
build_monogram("monogram-paper-on-ink.svg", PAPER, "#e08a67", bg=INK)

print("done")
