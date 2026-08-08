"""Monthly web artifact: full-width HTML page listing every business-class
route for the month, grouped by region. Text-dense, full three-typeface
system, dot-grid throughout -- per CI guide section 06's "Applying the
system" row for this surface."""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from brand import CSS_PATH, WORDMARK_INK, ROUTE_LINE_SVG  # noqa: E402
from curate import group_all_by_region, REGION_ORDER  # noqa: E402


def month_label(travel_month: str) -> str:
    return datetime.strptime(travel_month, "%Y-%m").strftime("%B %Y")


SOURCE_LABEL = {
    "sia-official": "the SIA website",
    "milelion": "MileLion",
    "onemileatatime": "One Mile at a Time",
}


def render(data: dict) -> str:
    travel_month = data["travel_month"]
    label = month_label(travel_month)
    groups = group_all_by_region(data["deals"])

    region_sections = []
    for region in REGION_ORDER + ["Other"]:
        rows = groups.get(region, [])
        if not rows:
            continue
        row_html = "\n".join(
            f'<div class="deal-row">'
            f'<span class="route">{d["route_label"]}</span>'
            f'<span class="miles data">{d["miles"]:,} mi</span>'
            f'<span class="deal-notes">{d.get("notes", "")}</span>'
            f'</div>'
            for d in rows
        )
        label_html = "Long-haul &amp; other" if region == "Other" else region
        region_sections.append(f"""
        <section class="region-block">
          <h3>{label_html}</h3>
          <div class="deal-list">{row_html}</div>
        </section>""")

    body = "".join(region_sections)

    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>Spontaneous Escapes — {label} — Stroll &amp; Savor</title>
<link rel="stylesheet" href="file://{CSS_PATH}">
<style>
  body {{ max-width: 900px; margin: 0 auto; padding: 4rem 1.75rem 6rem; }}
  .masthead {{ margin-bottom: 3rem; }}
  .masthead .mark {{ width: 260px; max-width: 60vw; margin-bottom: 1.6rem; }}
  .masthead .eyebrow {{ display: block; margin-bottom: 0.8rem; }}
  .masthead h1 {{ margin: 0 0 1rem; }}
  .masthead .window-row {{
    display: flex; gap: 1.6rem; flex-wrap: wrap; margin-top: 1.6rem;
    padding-top: 1.2rem; border-top: 1px dashed var(--rule);
    font-family: var(--font-data); font-size: 0.78rem; color: var(--ink-soft);
  }}
  .masthead .window-row b {{ color: var(--ink); font-weight: 400; }}
  .region-block {{ margin: 3rem 0; padding-top: 2rem; border-top: 1px solid var(--rule); }}
  .region-block h3 {{ font-family: var(--font-display); font-weight: 700; font-size: 1.3rem; margin-bottom: 1.2rem; }}
  .deal-list {{ display: flex; flex-direction: column; }}
  .deal-row {{
    display: grid; grid-template-columns: 1fr auto; gap: 0.2rem 1.2rem;
    padding: 0.9rem 0; border-bottom: 1px solid var(--rule);
    align-items: baseline;
  }}
  .deal-row .route {{ font-family: var(--font-display); font-weight: 700; font-size: 1rem; }}
  .deal-row .miles {{ font-size: 0.92rem; color: var(--rust-text); text-align: right; }}
  .deal-row .deal-notes {{ grid-column: 1 / -1; font-size: 0.76rem; color: var(--ink-soft); font-family: var(--font-data); }}
  footer {{ margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--rule); }}
</style>
</head>
<body>
  <div class="masthead">
    <div class="mark">{WORDMARK_INK}</div>
    <span class="eyebrow">Spontaneous Escapes — {label}</span>
    <h1>{data.get("discount_pct", 30)}% off Saver Awards, business class</h1>
    <p>Every business-class route on offer for {label} travel, straight from the source — extracted from {SOURCE_LABEL.get(data.get("source"), data.get("source", "the source"))}, no editorializing.</p>
    <div class="window-row">
      <span>Book by <b>{data["booking_window"]["end"]}</b></span>
      <span>Travel <b>{data["travel_window"]["start"]}</b> to <b>{data["travel_window"]["end"]}</b></span>
      <span>{len(data["deals"])} business-class fares listed</span>
    </div>
  </div>
  {body}
  <footer>
    <p>Discounts may apply in one direction only. Blackout dates and flight numbers are noted per route where given. Always confirm live availability on singaporeair.com before booking — this is a field note, not a booking engine.</p>
  </footer>
</body></html>"""


if __name__ == "__main__":
    import json
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".artifact.html")
    data = json.loads(src.read_text())
    out.write_text(render(data))
    print(f"wrote {out}")
