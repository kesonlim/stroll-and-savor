"""Monthly Spontaneous Escapes post: same content as the standalone web
artifact (content/templates/web_artifact.py's render_content), wrapped in
site chrome. Lives at /singapore-airlines/spontaneous-escapes/<month>/."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "templates"))
from web_artifact import render_content, CONTENT_STYLE, month_label  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402
from affiliate import complete_the_trip_card, STYLE as AFFILIATE_STYLE  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import image_provider  # noqa: E402

ASSET_PREFIX = "../../../"

STYLE = f"""
  main {{ max-width: 900px; margin: 0 auto; padding: 2.5rem 1.75rem 6rem; }}
  {CONTENT_STYLE}
  {AFFILIATE_STYLE}
"""


def render(data: dict) -> str:
    label = month_label(data["travel_month"])
    title = f"Spontaneous Escapes — {label} — Stroll & Savor"
    description = f"Every business-class Spontaneous Escapes route for {label} travel, {data.get('discount_pct', 30)}% off Saver Awards."
    url_path = f"singapore-airlines/spontaneous-escapes/{data['travel_month']}/"

    hero_img = image_provider.resolve_image("flight", width=1200)
    hero_html = f"""
    <div style="margin-bottom:2.4rem; border-radius:14px; overflow:hidden; border:1px solid var(--rule); position:relative; background:#e2dfd6;">
      <img src="{hero_img['url']}" alt="{hero_img['alt']}" style="width:100%; height:auto; max-height:380px; object-fit:cover; display:block;">
      <div style="position:absolute; bottom:0; left:0; right:0; background:linear-gradient(transparent, rgba(12,19,34,0.8)); padding:1.2rem 1.6rem; color:#fff; display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:0.5rem;">
        <span style="font-family:var(--font-data); font-size:0.75rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--brass); font-weight:700;">KrisFlyer Spontaneous Escapes &bull; {label}</span>
        <span style="font-family:var(--font-data); font-size:0.68rem; color:rgba(255,255,255,0.7);">Photo by {hero_img['photographer']} &bull; Unsplash</span>
      </div>
    </div>
    """

    body = f'<main>{hero_html}{render_content(data)}{complete_the_trip_card()}</main>'

    article_json_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "image": hero_img["url"],
        "datePublished": data.get("generated_at"),
        "author": {"@type": "Organization", "name": "Stroll & Savor"},
        "publisher": {"@type": "Organization", "name": "Stroll & Savor"},
    }

    return page(
        title=title,
        description=description,
        body=body,
        asset_prefix=ASSET_PREFIX,
        extra_style=STYLE,
        og_image=hero_img["url"],
        url_path=url_path,
        og_type="article",
        breadcrumbs=[
            ("Home", ""),
            ("Flight Escapes", "singapore-airlines/spontaneous-escapes/"),
            (label, url_path),
        ],
        json_ld_extra=[article_json_ld],
    )
