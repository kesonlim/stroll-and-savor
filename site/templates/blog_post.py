"""Blog post page: same content as the standalone web artifact
(content/templates/web_artifact.py's render_content), wrapped in real site
chrome (nav/footer) instead of a bare document."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "templates"))
from web_artifact import render_content, CONTENT_STYLE, month_label  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402

STYLE = f"""
  main {{ max-width: 900px; margin: 0 auto; padding: 3rem 1.75rem 6rem; }}
  {CONTENT_STYLE}
"""


def render(data: dict) -> str:
    label = month_label(data["travel_month"])
    body = f'<main>{render_content(data)}</main>'
    return page(
        title=f"Spontaneous Escapes — {label} — Stroll & Savor",
        description=f"Every business-class Spontaneous Escapes route for {label} travel, {data.get('discount_pct', 30)}% off Saver Awards.",
        body=body,
        asset_prefix="../../",
        extra_style=STYLE,
    )
