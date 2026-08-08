"""Landing page. Content sections per the proposal in project chat
(2026-08-09): hero, what-this-is, latest-post callout, how-it-works.
No social links yet -- accounts aren't confirmed live."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "scripts"))
from brand import WORDMARK_INK, ROUTE_LINE_SVG  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402

STYLE = """
  .hero { max-width: 980px; margin: 0 auto; padding: 4rem 1.75rem 3rem; }
  .hero .mark { width: 300px; max-width: 65vw; margin-bottom: 1.6rem; }
  .hero h1 { font-size: clamp(1.8rem, 3.2vw, 2.6rem); margin: 0 0 1rem; max-width: 18ch; }
  .hero p.lede { font-size: 1.1rem; max-width: 52ch; color: var(--ink-soft); }
  .hero .route-line-motif { margin: 1.8rem 0 0; }
  .hero .route-line-motif svg { width: 200px; height: auto; }

  section { max-width: 980px; margin: 0 auto; padding: 3rem 1.75rem; border-top: 1px solid var(--rule); }
  section h2 { font-size: 1.4rem; margin-bottom: 1rem; }
  section p { max-width: 62ch; }

  .latest-card {
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 14px;
    padding: 2rem 2.2rem; display: flex; flex-direction: column; gap: 0.8rem;
    text-decoration: none; color: inherit; margin-top: 1.4rem;
  }
  .latest-card .eyebrow { font-family: var(--font-data); font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--rust-text); }
  .latest-card h3 { font-family: var(--font-display); font-weight: 700; font-size: 1.6rem; margin: 0; }
  .latest-card .meta { font-family: var(--font-data); font-size: 0.82rem; color: var(--ink-soft); }
  .latest-card .cta { font-family: var(--font-data); font-size: 0.82rem; color: var(--teal-text); margin-top: 0.4rem; }

  .principles-mini { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap: 1.2rem; margin-top: 1.4rem; }
  .principles-mini .p { font-size: 0.9rem; }
  .principles-mini .p b { display: block; color: var(--ink); margin-bottom: 0.3rem; font-family: var(--font-display); font-weight: 700; font-size: 0.98rem; }
"""


def render(latest_post: dict) -> str:
    body = f"""
    <div class="hero">
      <div class="mark">{WORDMARK_INK}</div>
      <span style="font-family:var(--font-data); font-size:0.78rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--rust-text);">
        Field notes for the deliberate collector
      </span>
      <h1>Singapore Airlines Spontaneous Escapes, tracked every month.</h1>
      <p class="lede">
        Business-class award fares at 30% off, the moment Singapore Airlines reveals them.
        Numbers first, no hype — routes, miles, dates, straight from the source.
      </p>
      <div class="route-line-motif">{ROUTE_LINE_SVG}</div>
    </div>

    <section>
      <h2>What this is</h2>
      <p>
        KrisFlyer Spontaneous Escapes drops a new list of discounted award routes on the
        15th of every month, business class included. This site tracks it — full route
        list, business-class fares only, published as close to the reveal as we can
        manage. Not a booking engine, not a travel agency — a field note, kept monthly.
      </p>
    </section>

    <section>
      <h2>Latest</h2>
      <a class="latest-card" href="blog/{latest_post['slug']}/">
        <span class="eyebrow">{latest_post['eyebrow']}</span>
        <h3>{latest_post['title']}</h3>
        <span class="meta">{latest_post['meta']}</span>
        <span class="cta">Read the full list &rarr;</span>
      </a>
    </section>

    <section>
      <h2>How this gets made</h2>
      <p>
        The list is pulled and cross-checked within hours of Singapore Airlines' own
        reveal, filtered to business class only, and published without editorializing —
        the numbers are the point.
      </p>
      <div class="principles-mini">
        <div class="p"><b>Numbers do the persuading</b>Miles, taxes, dates. No adjectives standing in for a good fare.</div>
        <div class="p"><b>Precision over hype</b>Exact routes, exact fare classes. If a deal is one-direction only, we say so.</div>
        <div class="p"><b>Published monthly</b>One list, one cadence, every month this promotion runs.</div>
      </div>
    </section>
    """
    return page(
        title="Stroll & Savor — Singapore Airlines Spontaneous Escapes, tracked monthly",
        description="Business-class Spontaneous Escapes fares from Singapore Airlines, tracked and published monthly. Numbers first, no hype.",
        body=body,
        asset_prefix="",
        extra_style=STYLE,
    )
