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

ASSET_PREFIX = "../../../"

STYLE = f"""
  main {{ max-width: 900px; margin: 0 auto; padding: 3rem 1.75rem 6rem; }}
  {CONTENT_STYLE}
  {AFFILIATE_STYLE}
"""


def render(data: dict) -> str:
    label = month_label(data["travel_month"])
    title = f"Spontaneous Escapes — {label} — Stroll & Savor"
    description = f"Every business-class Spontaneous Escapes route for {label} travel, {data.get('discount_pct', 30)}% off Saver Awards."
    url_path = f"singapore-airlines/spontaneous-escapes/{data['travel_month']}/"
    body = f'<main>{render_content(data)}{complete_the_trip_card()}</main>'

    article_json_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
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
        url_path=url_path,
        og_type="article",
        breadcrumbs=[
            ("Home", ""),
            ("Singapore Airlines", "singapore-airlines/spontaneous-escapes/"),
            (label, url_path),
        ],
        json_ld_extra=[article_json_ld],
    )
