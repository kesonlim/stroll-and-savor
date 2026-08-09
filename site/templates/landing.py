"""Brand-general root landing page (docs/growth-plan.md). Not SIA-specific
-- that content lives at /singapore-airlines/spontaneous-escapes/. Points
to whatever sections actually have content (currently just Singapore
Airlines) and to the confirmed-live social accounts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "scripts"))
from brand import WORDMARK_INK, ROUTE_LINE_SVG  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page, SOCIAL_LINKS  # noqa: E402

STYLE = """
  .hero { max-width: 980px; margin: 0 auto; padding: 4rem 1.75rem 3rem; }
  .hero .mark { width: 300px; max-width: 65vw; margin-bottom: 1.6rem; }
  .hero h1 { font-size: clamp(1.8rem, 3.2vw, 2.6rem); margin: 0 0 1rem; max-width: 20ch; }
  .hero p.lede { font-size: 1.1rem; max-width: 52ch; color: var(--ink-soft); }
  .hero .route-line-motif { margin: 1.8rem 0 0; }
  .hero .route-line-motif svg { width: 200px; height: auto; }

  section { max-width: 980px; margin: 0 auto; padding: 3rem 1.75rem; border-top: 1px solid var(--rule); }
  section h2 { font-size: 1.4rem; margin-bottom: 1rem; }
  section p { max-width: 62ch; }

  .tracking-card {
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 14px;
    padding: 2rem 2.2rem; display: flex; flex-direction: column; gap: 0.8rem;
    text-decoration: none; color: inherit; margin-top: 1.4rem;
  }
  .tracking-card .eyebrow { font-family: var(--font-data); font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--rust-text); }
  .tracking-card h3 { font-family: var(--font-display); font-weight: 700; font-size: 1.5rem; margin: 0; }
  .tracking-card .meta { font-family: var(--font-data); font-size: 0.82rem; color: var(--ink-soft); }
  .tracking-card .cta { font-family: var(--font-data); font-size: 0.82rem; color: var(--teal-text); margin-top: 0.4rem; }

  .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 1rem; margin-top: 1.4rem; }
  .social-grid a {
    display: block; text-decoration: none; color: var(--ink);
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px;
    padding: 1.2rem 1.3rem; font-family: var(--font-display); font-weight: 700; font-size: 1rem;
  }
  .social-grid a:hover { border-color: var(--rust-soft); }

  .principles-mini { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap: 1.2rem; margin-top: 1.4rem; }
  .principles-mini .p { font-size: 0.9rem; }
  .principles-mini .p b { display: block; color: var(--ink); margin-bottom: 0.3rem; font-family: var(--font-display); font-weight: 700; font-size: 0.98rem; }
"""


def render(latest_tracker: dict) -> str:
    social_html = "".join(
        f'<a href="{url}" rel="noopener" target="_blank">{label}</a>' for label, url in SOCIAL_LINKS
    )
    body = f"""
    <div class="hero">
      <div class="mark">{WORDMARK_INK}</div>
      <span style="font-family:var(--font-data); font-size:0.78rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--rust-text);">
        Field notes for the deliberate collector
      </span>
      <h1>Travel value, tracked with precision.</h1>
      <p class="lede">
        We track the travel deals and loyalty programs worth paying attention to —
        numbers first, no hype. Routes, miles, dates, straight from the source.
      </p>
      <div class="route-line-motif">{ROUTE_LINE_SVG}</div>
    </div>

    <section>
      <h2>What we're tracking</h2>
      <a class="tracking-card" href="singapore-airlines/spontaneous-escapes/">
        <span class="eyebrow">{latest_tracker['eyebrow']}</span>
        <h3>{latest_tracker['title']}</h3>
        <span class="meta">{latest_tracker['meta']}</span>
        <span class="cta">See the tracker &rarr;</span>
      </a>
    </section>

    <section>
      <h2>Follow along</h2>
      <p>New lists go up on Instagram and TikTok first, usually within hours of the reveal.</p>
      <div class="social-grid">{social_html}</div>
    </section>

    <section>
      <h2>How this gets made</h2>
      <p>
        Every list is pulled and cross-checked against the source, filtered to what
        actually matters, and published without editorializing.
      </p>
      <div class="principles-mini">
        <div class="p"><b>Numbers do the persuading</b>Miles, taxes, dates. No adjectives standing in for a good fare.</div>
        <div class="p"><b>Precision over hype</b>Exact routes, exact fare classes. If a deal is one-direction only, we say so.</div>
        <div class="p"><b>Published on a cadence</b>One list, one cadence, every cycle we track.</div>
      </div>
    </section>
    """
    return page(
        title="Stroll & Savor — Travel value, tracked with precision",
        description="Field notes on travel deals and loyalty programs worth paying attention to — starting with Singapore Airlines KrisFlyer Spontaneous Escapes.",
        body=body,
        asset_prefix="",
        extra_style=STYLE,
    )
