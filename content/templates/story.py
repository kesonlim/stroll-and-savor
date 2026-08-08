"""Story/Reel graphic: 1080x1920 vertical, single deal per frame, largest
type sizes in the whole system per CI guide section 06. Space Mono-forward,
small monogram corner mark only (no wordmark -- there's no room and no need,
it's a single-serving frame meant to be swiped through fast)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from brand import MONOGRAM_INK, ROUTE_LINE_SVG, page  # noqa: E402

W, H = 1080, 1920

STORY_STYLE = """
  .canvas { padding: 140px 80px; display: flex; flex-direction: column; align-items: center;
            text-align: center; box-sizing: border-box; }
  .mono-mark { position: absolute; bottom: 72px; right: 80px; width: 64px; opacity: 0.85; }
  .mono-mark svg { display: block; width: 100%; height: auto; }
  .eyebrow-lg { font-family: var(--font-data); font-size: 30px; letter-spacing: 0.12em;
                text-transform: uppercase; color: var(--rust-text); }
"""


def deal_frame(deal: dict, data: dict) -> str:
    body = f"""
    <div class="eyebrow-lg">Spontaneous Escapes</div>
    <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:36px;">
      <div style="font-family:var(--font-display); font-weight:700; font-size:88px; line-height:1.2; color:var(--ink); max-width:11ch;">
        {deal["route_label"]}
      </div>
      {ROUTE_LINE_SVG.replace('width="120" height="40"', 'width="260" height="88"')}
      <div style="font-family:var(--font-data); font-size:196px; color:var(--rust-text); line-height:1;">
        {deal["miles"]:,}
      </div>
      <div style="font-family:var(--font-data); font-size:40px; color:var(--rust-text); margin-top:-24px;">miles</div>
      <div style="font-family:var(--font-body); font-size:32px; color:var(--ink-soft);">
        Business class &middot; {data.get("discount_pct", 30)}% off Saver Award
      </div>
    </div>
    <div style="font-family:var(--font-data); font-size:26px; color:var(--ink-soft); border-top:1px dashed var(--rule); padding-top:28px; width:100%;">
      Book by {data["booking_window"]["end"]}
    </div>
    <div class="mono-mark">{MONOGRAM_INK}</div>
    """
    return page(W, H, body, extra_style=STORY_STYLE)
