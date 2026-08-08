"""Instagram carousel slides: 1080x1350 (4:5). One cover, one deal slide per
curated pick, one closer. Minimal & punchy per CI guide section 06 --
monogram only (no wordmark), Space Mono for the miles figure, Courier Prime
for the route, heaviest use of the route-line motif in the whole system."""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from brand import CSS_PATH, MONOGRAM_INK, ROUTE_LINE_SVG, page  # noqa: E402

W, H = 1080, 1350

SLIDE_STYLE = """
  .canvas { padding: 88px 76px; display: flex; flex-direction: column; box-sizing: border-box; }
  .mono-mark { position: absolute; bottom: 64px; right: 76px; width: 56px; opacity: 0.85; }
  .mono-mark svg { display: block; width: 100%; height: auto; }
  .eyebrow-lg { font-family: var(--font-data); font-size: 28px; letter-spacing: 0.12em;
                text-transform: uppercase; color: var(--rust-text); }
  .route-line-motif { margin: 28px 0; }
  .route-line-motif svg { width: 220px; height: auto; }
"""


def month_label(travel_month: str) -> str:
    return datetime.strptime(travel_month, "%Y-%m").strftime("%B %Y")


def cover_slide(data: dict, pick_count: int) -> str:
    label = month_label(data["travel_month"])
    body = f"""
    <div class="eyebrow-lg">Spontaneous Escapes</div>
    <div class="route-line-motif">{ROUTE_LINE_SVG}</div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
      <div style="font-family:var(--font-display); font-weight:700; font-size:108px; line-height:1.05; color:var(--ink);">{label}</div>
      <div style="font-family:var(--font-body); font-size:36px; color:var(--ink-soft); margin-top:28px; max-width:22ch;">
        {data.get("discount_pct", 30)}% off Saver Awards, business class — {pick_count} picks this month
      </div>
    </div>
    <div style="font-family:var(--font-data); font-size:24px; color:var(--ink-soft); border-top:1px dashed var(--rule); padding-top:24px;">
      Book by {data["booking_window"]["end"]} &middot; Travel {data["travel_window"]["start"]} – {data["travel_window"]["end"]}
    </div>
    <div class="mono-mark">{MONOGRAM_INK}</div>
    """
    return page(W, H, body, extra_style=SLIDE_STYLE)


def deal_slide(deal: dict, index: int, total: int, region: str) -> str:
    body = f"""
    <div class="eyebrow-lg">{index:02d} / {total:02d} &mdash; {region}</div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
      <div style="font-family:var(--font-display); font-weight:700; font-size:80px; line-height:1.15; color:var(--ink); max-width:11ch;">
        {deal["route_label"]}
      </div>
      <div class="route-line-motif">{ROUTE_LINE_SVG}</div>
      <div style="font-family:var(--font-data); font-size:132px; color:var(--rust-text); line-height:1;">
        {deal["miles"]:,}<span style="font-size:48px;"> mi</span>
      </div>
    </div>
    <div style="font-family:var(--font-data); font-size:22px; color:var(--ink-soft); border-top:1px dashed var(--rule); padding-top:24px; max-width:80%;">
      Business class &middot; 30% off Saver Award
    </div>
    <div class="mono-mark">{MONOGRAM_INK}</div>
    """
    return page(W, H, body, extra_style=SLIDE_STYLE)


def closer_slide(data: dict) -> str:
    body = f"""
    <div class="eyebrow-lg">Spontaneous Escapes</div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
      <div style="font-family:var(--font-display); font-weight:700; font-size:64px; line-height:1.2; color:var(--ink); max-width:12ch;">
        Book by {data["booking_window"]["end"]}
      </div>
      <div style="font-family:var(--font-body); font-size:34px; color:var(--ink-soft); margin-top:24px; max-width:26ch;">
        Full list and live availability on singaporeair.com — discounts may run one direction only.
      </div>
    </div>
    <div class="route-line-motif">{ROUTE_LINE_SVG}</div>
    <div class="mono-mark">{MONOGRAM_INK}</div>
    """
    return page(W, H, body, extra_style=SLIDE_STYLE)
