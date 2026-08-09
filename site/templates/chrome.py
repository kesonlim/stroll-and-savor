"""Shared site chrome (head/nav/footer) wrapping every page. Asset paths
are relative to each page's own depth via `asset_prefix` (e.g. "" for
site root, "../../" for /singapore-airlines/spontaneous-escapes/,
"../../../" for /singapore-airlines/spontaneous-escapes/<month>/)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "scripts"))
from brand import MONOGRAM_INK  # noqa: E402

# Trim to what actually has content at each phase -- don't link to empty
# sections. Add "Guides" (glossary) and "News" once those ship (see
# docs/growth-plan.md).
NAV_LINKS = [
    ("Home", ""),
    ("Singapore Airlines", "singapore-airlines/spontaneous-escapes/"),
]

SOCIAL_LINKS = [
    ("Facebook", "https://www.facebook.com/profile.php?id=61581034831451"),
    ("Instagram", "https://www.instagram.com/stroll_savor/"),
    ("TikTok", "https://www.tiktok.com/@stroll_savor"),
    ("YouTube", "https://www.youtube.com/@StrollAndSavor"),
]


def page(title: str, description: str, body: str, asset_prefix: str = "", extra_style: str = "", og_image: str = "") -> str:
    nav_html = "".join(
        f'<a href="{asset_prefix}{href}">{label}</a>' for label, href in NAV_LINKS
    )
    social_html = "".join(
        f'<a href="{url}" rel="noopener" target="_blank">{label}</a>' for label, url in SOCIAL_LINKS
    )
    og_tag = f'<meta property="og:image" content="{og_image}">' if og_image else ""
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
{og_tag}
<link rel="icon" href="{asset_prefix}assets/favicon.ico">
<link rel="stylesheet" href="{asset_prefix}assets/style.css">
<style>
  .site-header {{
    max-width: 980px; margin: 0 auto; padding: 2rem 1.75rem 0;
    display: flex; align-items: center; justify-content: space-between;
  }}
  .site-header .brand {{ display: flex; align-items: center; gap: 0.6rem; text-decoration: none; }}
  .site-header .brand svg {{ width: 28px; height: auto; display: block; }}
  .site-header .brand span {{ font-family: var(--font-display); font-weight: 700; font-size: 1.1rem; color: var(--ink); }}
  .site-header nav {{ display: flex; gap: 1.6rem; font-family: var(--font-data); font-size: 0.82rem; }}
  .site-header nav a {{ color: var(--ink-soft); text-decoration: none; }}
  .site-header nav a:hover {{ color: var(--rust-text); }}
  .site-footer {{
    max-width: 980px; margin: 5rem auto 0; padding: 2rem 1.75rem 3rem;
    border-top: 1px solid var(--rule); font-family: var(--font-data);
    font-size: 0.76rem; color: var(--ink-soft); display: flex;
    justify-content: space-between; flex-wrap: wrap; gap: 1rem;
  }}
  .site-footer .social {{ display: flex; gap: 1.2rem; }}
  .site-footer .social a {{ color: var(--ink-soft); text-decoration: none; }}
  .site-footer .social a:hover {{ color: var(--rust-text); }}
  {extra_style}
</style>
</head>
<body>
  <header class="site-header">
    <a class="brand" href="{asset_prefix}">{MONOGRAM_INK}<span>stroll &amp; savor</span></a>
    <nav>{nav_html}</nav>
  </header>
  {body}
  <footer class="site-footer">
    <span>Stroll &amp; Savor — independent, not affiliated with any airline, hotel, or attraction we cover.</span>
    <span class="social">{social_html}</span>
  </footer>
</body></html>"""
