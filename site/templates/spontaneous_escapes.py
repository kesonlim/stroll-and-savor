"""Section landing page for /singapore-airlines/spontaneous-escapes/ --
this is the SIA-specific content that used to live at the site root, moved
here now that root is a brand-general landing page (docs/growth-plan.md)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "scripts"))
from brand import WORDMARK_INK, ROUTE_LINE_SVG  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402

ASSET_PREFIX = "../../"

STYLE = """
  .hero { max-width: 900px; margin: 0 auto; padding: 3rem 1.75rem 3rem; }
  .hero .mark { width: 260px; max-width: 60vw; margin-bottom: 1.6rem; }
  .hero h1 { font-size: clamp(1.7rem, 3vw, 2.3rem); margin: 0 0 1rem; max-width: 20ch; }
  .hero p.lede { font-size: 1.05rem; max-width: 56ch; color: var(--ink-soft); }
  .hero .route-line-motif { margin: 1.6rem 0 0; }
  .hero .route-line-motif svg { width: 200px; height: auto; }

  section { max-width: 900px; margin: 0 auto; padding: 2.6rem 1.75rem; border-top: 1px solid var(--rule); }
  section h2 { font-size: 1.3rem; margin-bottom: 1rem; }
  section p { max-width: 62ch; }

  .post-card {
    display: block; text-decoration: none; color: inherit;
    padding: 1.6rem 0; border-bottom: 1px solid var(--rule);
  }
  .post-card .eyebrow { font-family: var(--font-data); font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--rust-text); display: block; margin-bottom: 0.5rem; }
  .post-card h3 { font-family: var(--font-display); font-weight: 700; font-size: 1.3rem; margin: 0 0 0.4rem; }
  .post-card .meta { font-family: var(--font-data); font-size: 0.8rem; color: var(--ink-soft); }
"""


def render(posts: list) -> str:
    """`posts` newest first: [{slug, eyebrow, title, meta}, ...]"""
    latest = posts[0]
    older = posts[1:]

    older_html = ""
    if older:
        cards = "".join(f"""
        <a class="post-card" href="{p['slug']}/">
          <span class="eyebrow">{p['eyebrow']}</span>
          <h3>{p['title']}</h3>
          <span class="meta">{p['meta']}</span>
        </a>""" for p in older)
        older_html = f"""
    <section>
      <h2>Past months</h2>
      {cards}
    </section>"""

    body = f"""
    <div class="hero">
      <div class="mark">{WORDMARK_INK}</div>
      <span style="font-family:var(--font-data); font-size:0.76rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--rust-text);">
        Singapore Airlines
      </span>
      <h1>KrisFlyer Spontaneous Escapes, tracked every month.</h1>
      <p class="lede">
        Business-class award fares at 30% off, the moment Singapore Airlines reveals them.
        Numbers first, no hype — routes, miles, dates, straight from the source.
      </p>
      <div class="route-line-motif">{ROUTE_LINE_SVG}</div>
    </div>

    <section>
      <h2>Latest</h2>
      <a class="post-card" href="{latest['slug']}/">
        <span class="eyebrow">{latest['eyebrow']}</span>
        <h3>{latest['title']}</h3>
        <span class="meta">{latest['meta']}</span>
      </a>
    </section>
    {older_html}
    <section>
      <h2>How this gets made</h2>
      <p>
        The list is pulled and cross-checked within hours of Singapore Airlines' own
        reveal, filtered to business class only, and published without editorializing —
        the numbers are the point. Not a booking engine, not a travel agency — a field
        note, kept monthly.
      </p>
    </section>
    """
    return page(
        title="KrisFlyer Spontaneous Escapes — Stroll & Savor",
        description="Singapore Airlines KrisFlyer Spontaneous Escapes, business-class fares tracked monthly. Numbers first, no hype.",
        body=body,
        asset_prefix=ASSET_PREFIX,
        extra_style=STYLE,
    )
