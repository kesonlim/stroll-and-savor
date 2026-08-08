"""Shared brand primitives for content templates: paths, inlined SVG marks,
and an HTML page skeleton wired to brand/website-style-guide.css."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BRAND_DIR = REPO_ROOT / "brand"
CSS_PATH = BRAND_DIR / "website-style-guide.css"
SVG_DIR = BRAND_DIR / "logo-master" / "svg"

MONOGRAM_INK = (SVG_DIR / "monogram-ink-on-transparent.svg").read_text()
MONOGRAM_PAPER = (SVG_DIR / "monogram-paper-on-transparent.svg").read_text()
WORDMARK_INK = (SVG_DIR / "wordmark-ink-on-transparent.svg").read_text()
WORDMARK_PAPER = (SVG_DIR / "wordmark-paper-on-transparent.svg").read_text()

ROUTE_LINE_SVG = (
    '<svg width="120" height="40" viewBox="0 0 90 30" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4 15 C25 15 20 25 45 15 C65 7 70 20 86 15" fill="none" '
    'stroke="var(--rust)" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0.2 5"/>'
    '</svg>'
)


def page(width: int, height: int, body: str, extra_style: str = "", background: str = "var(--paper)") -> str:
    """A self-contained HTML page at an exact pixel canvas size, brand CSS
    already linked. `body` is raw inner HTML for a fixed-size canvas div."""
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{CSS_PATH}">
<style>
  html, body {{ margin: 0; padding: 0; overflow: hidden; }}
  .canvas {{
    width: {width}px; height: {height}px;
    background: {background};
    position: relative;
    overflow: hidden;
  }}
  {extra_style}
</style>
</head>
<body><div class="canvas">{body}</div></body></html>"""
