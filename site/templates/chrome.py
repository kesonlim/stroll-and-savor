"""Shared site chrome (head/nav/footer) wrapping every page. Asset paths
are relative to each page's own depth via `asset_prefix` (e.g. "" for
site root, "../../" for /singapore-airlines/spontaneous-escapes/,
"../../../" for /singapore-airlines/spontaneous-escapes/<month>/).

Implements docs/seo-standards.md's per-page checklist: canonical URL,
complete Open Graph + Twitter Card tags, and JSON-LD (a site-wide
Organization block on every page, plus an auto-generated BreadcrumbList
when `breadcrumbs` is given, plus whatever page-type-specific schema a
caller passes via `json_ld_extra`). See docs/seo-standards.md before
changing this -- it's the shared foundation every page's SEO compliance
depends on.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "scripts"))
from brand import MONOGRAM_INK  # noqa: E402

SITE_URL = "https://strollsavor.thethinkthank.com"

# Trim to what actually has content at each phase -- don't link to empty
# sections. Add "News" once that ships (see docs/growth-plan.md).
NAV_LINKS = [
    ("Home", ""),
    ("Singapore Airlines", "singapore-airlines/spontaneous-escapes/"),
    ("Airlines", "airlines/"),
]

SOCIAL_LINKS = [
    ("Facebook", "https://www.facebook.com/profile.php?id=61581034831451"),
    ("Instagram", "https://www.instagram.com/stroll_savor/"),
    ("TikTok", "https://www.tiktok.com/@stroll_savor"),
    ("YouTube", "https://www.youtube.com/@StrollAndSavor"),
]

ORGANIZATION_JSON_LD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Stroll & Savor",
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/assets/favicon.ico",
    "sameAs": [url for _, url in SOCIAL_LINKS],
}


def breadcrumb_json_ld(breadcrumbs: list) -> dict:
    """`breadcrumbs`: [(label, url_path), ...] from Home to the current
    page, url_path relative to site root (e.g. "airlines/qatar-airways/",
    "" for home)."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": label,
                "item": f"{SITE_URL}/{path}",
            }
            for i, (label, path) in enumerate(breadcrumbs)
        ],
    }


def page(
    title: str,
    description: str,
    body: str,
    asset_prefix: str = "",
    extra_style: str = "",
    og_image: str = "",
    url_path: str = "",
    og_type: str = "website",
    breadcrumbs: list = None,
    json_ld_extra: list = None,
) -> str:
    nav_html = "".join(
        f'<a href="{asset_prefix}{href}">{label}</a>' for label, href in NAV_LINKS
    )
    social_html = "".join(
        f'<a href="{url}" rel="noopener" target="_blank">{label}</a>' for label, url in SOCIAL_LINKS
    )
    canonical_url = f"{SITE_URL}/{url_path}"
    og_image_tag = f'<meta property="og:image" content="{og_image}">' if og_image else ""
    twitter_card_type = "summary_large_image" if og_image else "summary"

    json_ld_blocks = [ORGANIZATION_JSON_LD]
    if breadcrumbs:
        json_ld_blocks.append(breadcrumb_json_ld(breadcrumbs))
    if json_ld_extra:
        json_ld_blocks.extend(json_ld_extra)
    json_ld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>'
        for block in json_ld_blocks
    )

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:site_name" content="Stroll & Savor">
{og_image_tag}
<meta name="twitter:card" content="{twitter_card_type}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<link rel="icon" href="{asset_prefix}assets/favicon.ico">
<link rel="stylesheet" href="{asset_prefix}assets/style.css">
{json_ld_html}
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
