"""Brand-general root landing page (docs/growth-plan.md). Not SIA-specific
-- that content lives at /singapore-airlines/spontaneous-escapes/. Points
to whatever sections actually have content (currently just Singapore
Airlines) and to the confirmed-live social accounts.

Visual direction: deal-alert/newsletter style (Going.com primary anchor,
Thrifty Traveler/Dollar Flight Club for card punch), decided 2026-08-11.
Scoped to this page only via the `theme-dealfeed` body class -- every
CSS custom property it touches is redefined at that scope, so
brand/website-style-guide.css (and every other page, still Field Notes)
is untouched. See docs/seo-standards.md for the shared SEO contract this
still has to satisfy.

Field Notes (Courier Prime / IBM Plex Sans / Space Mono, warm paper bg)
stays the identity for social media posts -- content/templates/ -- by
deliberate choice, not oversight.
"""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page, SOCIAL_LINKS  # noqa: E402

# TODO(user): replace once you've created the account -- I can't create
# accounts on your behalf. Sign up at buttondown.com, then swap this for
# your real username (Q10 of the 2026-08-11 redesign decision).
BUTTONDOWN_USERNAME = "strollsavor"

GOOGLE_FONTS_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
"""

STYLE = """
  /* ---- Deal-feed theme tokens, scoped to this page only ---- */
  body.theme-dealfeed {
    --paper: #fcfcfa;
    --paper-2: #f5f4f0;
    --ink: #1c1b18;
    --ink-soft: #6b6862;
    --rule: #e6e3da;
    --rust-deep: #7a3a1f;
    --font-display: 'Inter', ui-sans-serif, system-ui, sans-serif;
    --font-body: 'Inter', ui-sans-serif, system-ui, sans-serif;
    --font-data: 'Inter', ui-sans-serif, system-ui, sans-serif;
    background-image: none;
    font-feature-settings: "tnum" 1;
  }
  body.theme-dealfeed h1, body.theme-dealfeed h2 { letter-spacing: -0.02em; }
  body.theme-dealfeed p { color: var(--ink-soft); }
  body.theme-dealfeed a { color: var(--rust-text); }
  body.theme-dealfeed a:hover { color: var(--rust-deep); }
  body.theme-dealfeed .site-header { padding-top: 1.6rem; }
  body.theme-dealfeed .site-header .brand span { font-weight: 800; }
  body.theme-dealfeed .site-header nav a { font-weight: 500; text-transform: none; letter-spacing: 0; }
  body.theme-dealfeed .site-header nav a:hover { color: var(--rust-text); }
  body.theme-dealfeed .site-footer { border-top-color: var(--rule); }

  .hero { max-width: 720px; margin: 0 auto; padding: 3.4rem 1.75rem 3rem; }

  .tracking-strip {
    display: inline-flex; align-items: center; gap: 0.55rem;
    font-size: 0.82rem; font-weight: 500; color: var(--ink-soft);
    background: var(--paper-2); border: 1px solid var(--rule);
    border-radius: 999px; padding: 0.4rem 0.9rem 0.4rem 0.7rem;
    margin-bottom: 1.6rem;
  }
  .tracking-strip .dot {
    width: 7px; height: 7px; border-radius: 50%; background: var(--rust);
    flex-shrink: 0;
  }
  @media (prefers-reduced-motion: no-preference) {
    .tracking-strip .dot { animation: pulse 2.4s ease-in-out infinite; }
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(180, 85, 47, 0.35); }
    50% { opacity: 0.7; box-shadow: 0 0 0 5px rgba(180, 85, 47, 0); }
  }

  .hero h1 {
    font-size: clamp(2.1rem, 1.4rem + 3vw, 3.2rem);
    font-weight: 800; line-height: 1.1; margin: 0 0 1.1rem; max-width: 22ch;
  }
  .hero p.lede { font-size: 1.12rem; line-height: 1.55; max-width: 46ch; margin-bottom: 1.8rem; }

  .email-capture { display: flex; gap: 0.6rem; max-width: 420px; flex-wrap: wrap; }
  .email-capture input[type=email] {
    flex: 1 1 220px; min-width: 0; padding: 0.85rem 1rem; font-size: 1rem;
    font-family: var(--font-body); border: 1.5px solid var(--rule); border-radius: 9px;
    background: var(--paper); color: var(--ink);
  }
  .email-capture input[type=email]:focus-visible {
    outline: 2px solid var(--rust); outline-offset: 2px; border-color: var(--rust);
  }
  .email-capture button {
    padding: 0.85rem 1.35rem; font-size: 1rem; font-weight: 700; font-family: var(--font-body);
    background: var(--rust); color: #fff; border: none; border-radius: 9px; cursor: pointer;
    white-space: nowrap;
  }
  .email-capture button:hover { background: var(--rust-deep); }
  .email-capture button:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
  .fine-print { font-size: 0.8rem; color: var(--ink-soft); margin: 0.6rem 0 0; }

  section.dealfeed-section { max-width: 980px; margin: 0 auto; padding: 3rem 1.75rem; border-top: 1px solid var(--rule); }
  section.dealfeed-section > .section-head { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; margin-bottom: 1.6rem; flex-wrap: wrap; }
  section.dealfeed-section h2 { font-size: 1.5rem; font-weight: 800; margin: 0; }
  section.dealfeed-section > .section-head a { font-size: 0.9rem; font-weight: 600; white-space: nowrap; }

  .deal-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.1rem; }
  .deal-card {
    background: var(--paper); border: 1px solid var(--rule); border-radius: 16px;
    padding: 1.6rem 1.7rem; display: flex; flex-direction: column; gap: 0.7rem;
    text-decoration: none; color: inherit; transition: border-color 0.15s ease, transform 0.15s ease;
  }
  .deal-card:hover { border-color: var(--rust-soft); transform: translateY(-2px); }
  .deal-card .badge {
    align-self: flex-start; background: var(--rust); color: #fff; font-weight: 800;
    font-size: 0.85rem; padding: 0.28rem 0.65rem; border-radius: 6px;
  }
  .deal-card .badge.muted { background: var(--ink-soft); }
  .deal-card h3 { font-size: 1.2rem; font-weight: 700; margin: 0; color: var(--ink); }
  .deal-card .stat { font-size: 1.5rem; font-weight: 800; color: var(--ink); }
  .deal-card .stat small { font-size: 0.95rem; font-weight: 500; color: var(--ink-soft); }
  .deal-card .meta { font-size: 0.86rem; color: var(--ink-soft); }
  .deal-card .cta { font-weight: 700; font-size: 0.92rem; margin-top: 0.3rem; }
  .deal-card.placeholder { border-style: dashed; justify-content: center; align-items: flex-start; }
  .deal-card.placeholder h3 { color: var(--ink-soft); font-weight: 600; }

  .principles-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: 1.4rem; }
  .principles-grid .p b { display: block; color: var(--ink); margin-bottom: 0.35rem; font-family: var(--font-display); font-weight: 700; font-size: 1.02rem; }
  .principles-grid .p span { font-size: 0.92rem; color: var(--ink-soft); }

  .glossary-teaser {
    display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 16px;
    padding: 1.8rem 2rem; flex-wrap: wrap;
  }
  .glossary-teaser .copy { max-width: 46ch; }
  .glossary-teaser h2 { font-size: 1.25rem; margin: 0 0 0.4rem; }
  .glossary-teaser p { margin: 0; }
  .glossary-teaser a.button {
    flex-shrink: 0; background: var(--ink); color: var(--paper); text-decoration: none;
    font-weight: 700; padding: 0.75rem 1.3rem; border-radius: 9px; font-size: 0.92rem;
  }
  .glossary-teaser a.button:hover { background: var(--rust-deep); color: #fff; }

  .social-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 1rem; }
  .social-grid a {
    display: block; text-decoration: none; color: var(--ink);
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 16px;
    padding: 1.1rem 1.3rem; font-weight: 700; font-size: 1rem;
  }
  .social-grid a:hover { border-color: var(--rust-soft); }
"""


def _email_form(username: str, form_id: str) -> str:
    return f"""
      <form action="https://buttondown.com/api/emails/embed-subscribe/{username}"
            method="post" target="popupwindow" class="email-capture" id="{form_id}"
            onsubmit="window.open('https://buttondown.com/{username}', 'popupwindow')">
        <input type="email" name="email" placeholder="you@email.com" required aria-label="Email address">
        <button type="submit">Get alerts</button>
      </form>
      <p class="fine-print">One email per deal that clears the bar. No spam, unsubscribe anytime.</p>
    """


def render(latest_tracker: dict, airline_count: int = 0) -> str:
    social_html = "".join(
        f'<a href="{url}" rel="noopener" target="_blank">{label}</a>' for label, url in SOCIAL_LINKS
    )

    data = latest_tracker["data"]
    deals = data["deals"]
    routes = len(deals)
    min_miles = min(d["miles"] for d in deals)
    source_labels = {
        "sia_direct": "Singapore Airlines directly",
        "milelion": "MileLion",
        "omaat": "One Mile at a Time",
    }
    source = source_labels.get(data.get("source"), data.get("source", "the source"))
    book_by = datetime.strptime(data["booking_window"]["end"], "%Y-%m-%d").strftime("%-d %b %Y")

    deal_card = f"""
      <a class="deal-card" href="singapore-airlines/spontaneous-escapes/{latest_tracker['slug']}/">
        <span class="badge">{data.get('discount_pct', 30)}% off</span>
        <h3>SIA KrisFlyer Spontaneous Escapes</h3>
        <span class="stat">{routes} routes <small>from {min_miles:,} miles</small></span>
        <span class="meta">Business class, book by {book_by}.<br>Verified via {source}.</span>
        <span class="cta">See every route &rarr;</span>
      </a>
    """
    placeholder_card = """
      <div class="deal-card placeholder">
        <span class="badge muted">More soon</span>
        <h3>We're expanding past Singapore Airlines</h3>
        <span class="meta">More loyalty programs are getting tracked as we add them. Use the form above to hear first.</span>
      </div>
    """

    body = f"""
    <div class="hero">
      <span class="tracking-strip"><span class="dot"></span>Tracking SIA KrisFlyer Spontaneous Escapes, {routes} routes live</span>
      <h1>Deals worth your miles, tracked live.</h1>
      <p class="lede">
        Exact routes, exact miles, exact dates. We flag a deal the moment
        it's actually worth booking. No hype, no guesswork.
      </p>
      {_email_form(BUTTONDOWN_USERNAME, 'hero-alerts')}
    </div>

    <section class="dealfeed-section">
      <div class="section-head">
        <h2>Latest deals</h2>
        <a href="singapore-airlines/spontaneous-escapes/">All Spontaneous Escapes posts &rarr;</a>
      </div>
      <div class="deal-grid">
        {deal_card}
        {placeholder_card}
      </div>
    </section>

    <section class="dealfeed-section">
      <h2>How we work</h2>
      <div class="principles-grid">
        <div class="p"><b>Numbers do the persuading</b><span>Miles, taxes, dates. No adjectives standing in for a good fare.</span></div>
        <div class="p"><b>Precision over hype</b><span>Exact routes, exact fare classes. If a deal is one-direction only, we say so.</span></div>
        <div class="p"><b>Sourced, not spun</b><span>Every list is cross-checked against the airline's own reveal before it goes up.</span></div>
      </div>
    </section>

    <section class="dealfeed-section">
      <div class="glossary-teaser">
        <div class="copy">
          <h2>{airline_count} airlines flying Changi, decoded</h2>
          <p>Alliance, hub, terminal, official site. The reference you check before you book.</p>
        </div>
        <a class="button" href="airlines/">Browse the glossary &rarr;</a>
      </div>
    </section>

    <section class="dealfeed-section">
      <h2>Follow along</h2>
      <p>New lists go up on Instagram and TikTok first, usually within hours of the reveal.</p>
      <div class="social-grid">{social_html}</div>
    </section>
    """
    return page(
        title="Stroll & Savor - Travel deals, tracked with precision",
        description="We track the travel deals and loyalty programs worth paying attention to: exact routes, exact miles, exact dates. Starting with Singapore Airlines KrisFlyer Spontaneous Escapes.",
        body=body,
        asset_prefix="",
        extra_style=STYLE,
        url_path="",
        og_type="website",
        breadcrumbs=[("Home", "")],
        body_class="theme-dealfeed",
        head_extra=GOOGLE_FONTS_HEAD,
    )