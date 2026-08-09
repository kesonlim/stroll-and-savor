"""Affiliate placement components. First slot: OTA/activity affiliate
(Klook priority, per docs/growth-plan.md) on the monthly Spontaneous
Escapes post -- the highest-intent moment, right after someone's read the
route list, mirroring how SIA's own promo page nudges toward Pelago
activities in the same spot.

PLACEHOLDER LINK: KLOOK_URL below is Klook's real, working, non-affiliate
Singapore page -- safe to ship as-is, just not tracked/monetized yet.
Swap in the real affiliate tracking link once enrolled (Klook's affiliate
program has no minimum-traffic requirement, confirmed 2026-08-09 -- see
docs/growth-plan.md). Do not fabricate a tracking ID or "aff_id"-style
query param; leave this plain until a real one exists.
"""

KLOOK_URL = "https://www.klook.com/en-SG/"

STYLE = """
  .affiliate-card {
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 14px;
    padding: 1.8rem 2rem; margin: 3rem 0; display: flex; flex-direction: column; gap: 0.6rem;
  }
  .affiliate-card .eyebrow { font-family: var(--font-data); font-size: 0.7rem; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--rust-text); }
  .affiliate-card p { margin: 0; max-width: 60ch; }
  .affiliate-card .cta { font-family: var(--font-data); font-size: 0.86rem; color: var(--teal-text); text-decoration: none; }
  .affiliate-card .cta:hover { color: var(--teal); }
  .affiliate-card .disclosure { font-family: var(--font-data); font-size: 0.7rem; color: var(--ink-soft); }
"""


def complete_the_trip_card() -> str:
    return f"""
    <div class="affiliate-card">
      <span class="eyebrow">Complete the trip</span>
      <p>Booked a Spontaneous Escapes fare? Activities and tours at most of these destinations are bookable separately, sometimes cheaper than airline add-ons.</p>
      <a class="cta" href="{KLOOK_URL}" rel="noopener sponsored" target="_blank">Browse activities on Klook &rarr;</a>
      <span class="disclosure">Stroll &amp; Savor may earn a commission on bookings made through this link, at no extra cost to you.</span>
    </div>"""
