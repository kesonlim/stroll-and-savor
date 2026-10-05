"""Brand-general root landing page (docs/growth-plan.md).
Redesigned to Direction B: The Global Modern Editorial (Monocle / Afar style).
Unifies the two core pillars: Slow Culinary Urban Walks and High-Value Flight Intelligence.
"""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import image_provider  # noqa: E402
from chrome import page, SOCIAL_LINKS  # noqa: E402

BUTTONDOWN_USERNAME = "klim"

GOOGLE_FONTS_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,400;1,600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
"""

STYLE = """
  /* ---- Global Modern Editorial (Direction B) ---- */
  body.theme-editorial {
    --paper: #f6f5f0;
    --paper-2: #ffffff;
    --paper-dark: #0c1322;
    --ink: #0f172a;
    --ink-soft: #475569;
    --rule: #e2dfd6;
    --brass: #c89446;
    --brass-deep: #966a23;
    --brass-soft: #f5e9d5;
    --navy: #0c1322;
    --font-display: 'Playfair Display', Georgia, serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-data: 'Space Mono', monospace;
    background-color: var(--paper);
    color: var(--ink);
  }

  .masthead-strip {
    max-width: 1040px; margin: 0 auto; padding: 1rem 2rem 0;
    display: flex; align-items: center; justify-content: space-between;
    font-family: var(--font-data); font-size: 0.68rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--ink-soft);
    border-bottom: 1px solid var(--rule); padding-bottom: 0.75rem;
  }
  .masthead-strip .vol { font-weight: 700; color: var(--brass-deep); }

  .hero {
    max-width: 1040px; margin: 0 auto; padding: 4.5rem 2rem 3.5rem;
  }
  .hero-eyebrow {
    display: inline-flex; align-items: center; gap: 0.6rem;
    font-family: var(--font-data); font-size: 0.76rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--brass-deep); font-weight: 700;
    margin-bottom: 1.4rem;
  }
  .hero-eyebrow .dot {
    width: 8px; height: 8px; border-radius: 50%; background: var(--brass);
    display: inline-block;
  }
  @media (prefers-reduced-motion: no-preference) {
    .hero-eyebrow .dot { animation: pulse-brass 2.2s infinite; }
  }
  @keyframes pulse-brass {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.25); }
  }

  .hero h1 {
    font-family: var(--font-display);
    font-size: clamp(2.4rem, 1.8rem + 3.2vw, 4.2rem);
    font-weight: 900; line-height: 1.08; letter-spacing: -0.01em;
    color: var(--ink); margin: 0 0 1.5rem; max-width: 20ch;
  }
  .hero p.lede {
    font-size: clamp(1.1rem, 1rem + 0.5vw, 1.3rem);
    line-height: 1.6; color: var(--ink-soft); max-width: 44ch;
    margin: 0 0 2.2rem; font-weight: 400;
  }

  .hero-dispatch-box {
    background: var(--paper-2); border: 1px solid var(--rule);
    border-left: 3px solid var(--brass); border-radius: 12px;
    padding: 1.6rem 2rem; max-width: 580px; box-shadow: 0 8px 30px rgba(15, 23, 42, 0.03);
  }
  .hero-dispatch-box .box-title {
    font-family: var(--font-display); font-size: 1.15rem; font-weight: 700;
    color: var(--ink); margin: 0 0 0.35rem;
  }
  .hero-dispatch-box p {
    font-size: 0.88rem; color: var(--ink-soft); margin: 0 0 1.2rem; line-height: 1.5;
  }
  .email-capture { display: flex; gap: 0.6rem; flex-wrap: wrap; }
  .email-capture input[type=email] {
    flex: 1 1 240px; min-width: 0; padding: 0.85rem 1.1rem; font-size: 0.95rem;
    font-family: var(--font-body); border: 1px solid var(--rule); border-radius: 8px;
    background: var(--paper); color: var(--ink); outline: none; transition: border-color 0.15s ease;
  }
  .email-capture input[type=email]:focus {
    border-color: var(--brass); background: #fff;
  }
  .email-capture button {
    padding: 0.85rem 1.5rem; font-size: 0.92rem; font-weight: 700;
    font-family: var(--font-body); background: var(--ink); color: #fff;
    border: none; border-radius: 8px; cursor: pointer; transition: background 0.15s ease;
  }
  .email-capture button:hover { background: var(--brass-deep); }

  /* Sections */
  section.editorial-section {
    max-width: 1040px; margin: 0 auto; padding: 4rem 2rem;
    border-top: 1px solid var(--rule);
  }
  .section-eyebrow {
    font-family: var(--font-data); font-size: 0.72rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--brass-deep); font-weight: 700; margin-bottom: 0.5rem;
  }
  .section-header-row {
    display: flex; align-items: baseline; justify-content: space-between;
    gap: 1rem; margin-bottom: 2.2rem; flex-wrap: wrap;
  }
  .section-header-row h2 {
    font-family: var(--font-display); font-size: 2.2rem; font-weight: 800;
    margin: 0; color: var(--ink); letter-spacing: -0.01em;
  }
  .section-header-row a.view-all {
    font-family: var(--font-body); font-weight: 600; font-size: 0.9rem;
    color: var(--brass-deep); text-decoration: none;
  }
  .section-header-row a.view-all:hover { text-decoration: underline; }

  /* Departure Board Flight Card */
  .flight-radar-card {
    background: var(--paper-dark); color: #fff; border-radius: 16px;
    padding: 2.4rem 2.6rem; margin-bottom: 2rem;
    position: relative; overflow: hidden;
    box-shadow: 0 16px 40px rgba(12, 19, 34, 0.12);
  }
  .flight-radar-card::after {
    content: ""; position: absolute; top: 0; right: 0; width: 300px; height: 100%;
    background: radial-gradient(circle at top right, rgba(200, 148, 70, 0.15), transparent 70%);
    pointer-events: none;
  }
  .flight-radar-card .card-top {
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12); padding-bottom: 1.2rem;
    margin-bottom: 1.8rem; flex-wrap: wrap; gap: 1rem;
  }
  .flight-radar-card .tag-badge {
    background: var(--brass); color: #0c1322; font-family: var(--font-data);
    font-size: 0.74rem; font-weight: 700; letter-spacing: 0.08em;
    padding: 0.35rem 0.8rem; border-radius: 6px; text-transform: uppercase;
  }
  .flight-radar-card .date-indicator {
    font-family: var(--font-data); font-size: 0.78rem; color: rgba(255, 255, 255, 0.6);
  }
  .flight-radar-card h3 {
    font-family: var(--font-display); font-size: 2.1rem; font-weight: 700;
    margin: 0 0 0.8rem; color: #fff; line-height: 1.2;
  }
  .flight-radar-card p.summary {
    font-size: 1.05rem; line-height: 1.6; color: rgba(255, 255, 255, 0.75);
    max-width: 58ch; margin: 0 0 2rem;
  }
  .flight-route-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem; margin-bottom: 2rem;
  }
  .flight-route-chip {
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px; padding: 1rem 1.2rem; display: flex; flex-direction: column; gap: 0.25rem;
  }
  .flight-route-chip .sector {
    font-family: var(--font-data); font-size: 0.85rem; font-weight: 700;
    letter-spacing: 0.05em; color: var(--brass);
  }
  .flight-route-chip .destination { font-size: 0.95rem; font-weight: 600; color: #fff; }
  .flight-route-chip .miles { font-family: var(--font-data); font-size: 0.78rem; color: rgba(255, 255, 255, 0.55); }

  .flight-radar-card .action-row {
    display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;
  }
  .button-brass {
    background: var(--brass); color: #0c1322; text-decoration: none;
    font-weight: 700; font-size: 0.94rem; padding: 0.85rem 1.6rem;
    border-radius: 8px; transition: transform 0.15s ease, background 0.15s ease;
  }
  .button-brass:hover { background: #dcb065; transform: translateY(-1px); }
  .button-outline {
    background: transparent; border: 1px solid rgba(255, 255, 255, 0.25);
    color: #fff; text-decoration: none; font-weight: 600; font-size: 0.92rem;
    padding: 0.85rem 1.4rem; border-radius: 8px; transition: border-color 0.15s ease;
  }
  .button-outline:hover { border-color: #fff; }

  /* Urban Walks Grid */
  .walks-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.6rem; margin-top: 1rem;
  }
  .walk-card {
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 16px;
    overflow: hidden; text-decoration: none; color: inherit;
    display: flex; flex-direction: column; justify-content: space-between;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .walk-card:hover {
    transform: translateY(-4px); box-shadow: 0 16px 36px rgba(15, 23, 42, 0.08);
  }
  .walk-card .card-thumb {
    width: 100%; height: 210px; overflow: hidden; position: relative; background: #e2dfd6;
  }
  .walk-card .card-thumb img {
    width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; display: block;
  }
  .walk-card:hover .card-thumb img {
    transform: scale(1.05);
  }
  .walk-card .card-content {
    padding: 1.8rem 1.7rem; display: flex; flex-direction: column; flex: 1; justify-content: space-between;
  }
  .walk-card .card-label {
    font-family: var(--font-data); font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase; color: var(--brass-deep);
    margin-bottom: 0.7rem;
  }
  .walk-card h3 {
    font-family: var(--font-display); font-size: 1.45rem; font-weight: 800;
    margin: 0 0 0.8rem; line-height: 1.25; color: var(--ink);
  }
  .walk-card p {
    font-size: 0.94rem; line-height: 1.6; color: var(--ink-soft); margin: 0 0 1.5rem;
  }
  .walk-card .meta-footer {
    display: flex; justify-content: space-between; align-items: center;
    border-top: 1px solid var(--rule); padding-top: 1rem;
    font-family: var(--font-data); font-size: 0.76rem; color: var(--ink-soft);
  }

  /* Airlines Directory Teaser with Photography */
  .directory-teaser {
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 16px;
    overflow: hidden; display: flex; justify-content: space-between;
    align-items: stretch; gap: 0; flex-wrap: wrap;
  }
  .directory-teaser .copy {
    padding: 2.8rem 3rem; flex: 1 1 360px; max-width: 58ch;
    display: flex; flex-direction: column; justify-content: center;
  }
  .directory-teaser .teaser-image {
    flex: 1 1 300px; min-height: 260px; position: relative; overflow: hidden; background: #e2dfd6;
  }
  .directory-teaser .teaser-image img {
    width: 100%; height: 100%; object-fit: cover; display: block;
  }
  .directory-teaser h3 {
    font-family: var(--font-display); font-size: 1.8rem; font-weight: 800;
    margin: 0 0 0.6rem; color: var(--ink);
  }
  .directory-teaser p { margin: 0; font-size: 1rem; line-height: 1.6; color: var(--ink-soft); }

  /* Manifesto / Principles Grid */
  .principles-row {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.8rem; margin-top: 1.5rem;
  }
  .principle-box {
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px;
    padding: 1.8rem;
  }
  .principle-box .num {
    font-family: var(--font-data); font-size: 0.8rem; font-weight: 700;
    color: var(--brass-deep); margin-bottom: 0.6rem; display: block;
  }
  .principle-box h4 {
    font-family: var(--font-display); font-size: 1.25rem; font-weight: 700;
    margin: 0 0 0.5rem; color: var(--ink);
  }
  .principle-box p {
    font-size: 0.92rem; line-height: 1.6; color: var(--ink-soft); margin: 0;
  }

  @media (max-width: 768px) {
    .masthead-strip {
      padding: 0.8rem 1.2rem; font-size: 0.64rem;
      flex-direction: column; gap: 0.35rem; align-items: flex-start;
      line-height: 1.4;
    }
    .hero { padding: 2.2rem 1.25rem 1.8rem; }
    .hero h1 {
      font-size: clamp(1.55rem, 1.25rem + 1.8vw, 1.95rem);
      line-height: 1.16; word-break: break-word;
    }
    .hero-dispatch-box { padding: 1.4rem 1.1rem; }
    .flight-radar-card { padding: 1.6rem 1.2rem; }
    .flight-radar-card .card-top {
      flex-direction: column; align-items: flex-start; gap: 0.6rem;
    }
    .flight-radar-card h3 {
      font-size: 1.35rem; word-break: break-word; line-height: 1.25;
    }
    .flight-route-grid { grid-template-columns: 1fr; }
    .section-header-row h2 { font-size: 1.65rem; }
    .walks-grid { grid-template-columns: 1fr; }
    .directory-teaser { padding: 1.8rem 1.2rem; flex-direction: column; align-items: flex-start; }
    .directory-teaser a.button-brass { width: 100%; text-align: center; }
  }
"""


def _email_form(username: str, form_id: str) -> str:
    return f"""
      <form action="https://buttondown.com/api/emails/embed-subscribe/{username}"
            method="post" target="popupwindow" class="email-capture" id="{form_id}"
            onsubmit="window.open('https://buttondown.com/{username}', 'popupwindow')">
        <input type="email" name="email" placeholder="Enter your email" required aria-label="Email address">
        <button type="submit">Join the Dispatch</button>
      </form>
    """


def render(latest_tracker: dict, airline_count: int = 0) -> str:
    data = latest_tracker["data"]
    deals = data["deals"]
    routes = len(deals)
    min_miles = min(d["miles"] for d in deals)
    today_date = datetime.now().date()
    book_end_date = datetime.strptime(data["booking_window"]["end"], "%Y-%m-%d").date()
    is_cycle_ended = today_date > book_end_date

    if is_cycle_ended:
        status_tag = "NEXT CYCLE: MID-OCTOBER"
        status_headline = "Singapore Airlines Spontaneous Escapes"
        status_sub = "Discounted 30% Saver Awards across Business & Economy. The next drop is expected ~15 October 2026 for November flights. Review our 92-sector planner while awaiting the drop."
        date_badge = "Expected ~15 Oct 2026"
    else:
        status_tag = "30% OFF SAVER AWARDS"
        status_headline = "KrisFlyer Spontaneous Escapes Active"
        status_sub = f"Currently tracking {routes} discounted routes starting from {min_miles:,} miles in Business class."
        date_badge = f"Book by {data['booking_window']['end']}"

    tokyo_img = image_provider.resolve_image("tokyo", width=800)
    kyoto_img = image_provider.resolve_image("kyoto", width=800)
    sg_img = image_provider.resolve_image("singapore", width=800)
    changi_img = image_provider.resolve_image("changi", width=900)

    body = f"""
    <div class="masthead-strip">
      <span class="vol">Issue 01 &bull; Autumn 2026</span>
      <span>The Art of Departure &amp; The Slow Walk</span>
      <span>Dispatches from Singapore, Tokyo &amp; Beyond</span>
    </div>

    <div class="hero">
      <div class="hero-eyebrow">
        <span class="dot"></span>
        <span>Independent Travel &bull; Field Notes</span>
      </div>
      <h1>Where Slow Urban Walks Meet High-Value Flight Intelligence.</h1>
      <p class="lede">
        We map the quiet back-alley food trails worth lingering in, and decode the airline loyalty sweet spots that get you there in business class for 30% fewer miles.
      </p>

      <div class="hero-dispatch-box">
        <div class="box-title">The Departure Dispatch</div>
        <p>Curated pedestrian walking guides, quiet neighborhood supper spots, and immediate alerts whenever high-value redemption seats drop.</p>
        {_email_form(BUTTONDOWN_USERNAME, 'hero-alerts')}
      </div>
    </div>

    <!-- Section 1: Flight Intelligence Desk -->
    <section class="editorial-section">
      <div class="section-eyebrow">01 / Flight Intelligence</div>
      <div class="section-header-row">
        <h2>Spontaneous Escapes Radar</h2>
        <a class="view-all" href="singapore-airlines/spontaneous-escapes/">View All Escapes Reports &rarr;</a>
      </div>

      <div class="flight-radar-card">
        <div class="card-top">
          <span class="tag-badge">{status_tag}</span>
          <span class="date-indicator">{date_badge}</span>
        </div>
        <h3>{status_headline}</h3>
        <p class="summary">{status_sub}</p>

        <div class="flight-route-grid">
          <div class="flight-route-chip">
            <span class="sector">SIN &rarr; NRT / HND</span>
            <span class="destination">Tokyo, Japan</span>
            <span class="miles">36,400 miles Business</span>
          </div>
          <div class="flight-route-chip">
            <span class="sector">SIN &rarr; ICN</span>
            <span class="destination">Seoul, Korea</span>
            <span class="miles">36,400 miles Business</span>
          </div>
          <div class="flight-route-chip">
            <span class="sector">SIN &rarr; FRA / LHR</span>
            <span class="destination">Frankfurt / London</span>
            <span class="miles">72,450 miles Business</span>
          </div>
          <div class="flight-route-chip">
            <span class="sector">SIN &rarr; SYD / MEL</span>
            <span class="destination">Sydney / Melbourne</span>
            <span class="miles">47,950 miles Business</span>
          </div>
        </div>

        <div class="action-row">
          <a class="button-brass" href="singapore-airlines/spontaneous-escapes/2026-10/dashboard/">Open 92-Sector Master Dashboard &rarr;</a>
          <a class="button-outline" href="singapore-airlines/spontaneous-escapes/{latest_tracker['slug']}/">Past Month Breakdown</a>
        </div>
      </div>
    </section>

    <!-- Section 2: Curated Urban Walks -->
    <section class="editorial-section" id="walks">
      <div class="section-eyebrow">02 / Field Guides</div>
      <div class="section-header-row">
        <h2>Curated Urban Walks</h2>
        <a class="view-all" href="https://www.youtube.com/@StrollAndSavor" target="_blank" rel="noopener">Watch 4K Walking Films &rarr;</a>
      </div>

      <div class="walks-grid">
        <article class="walk-card">
          <div class="card-thumb">
            <img src="{tokyo_img['url']}" alt="{tokyo_img['alt']}" loading="lazy" width="600" height="340">
          </div>
          <div class="card-content">
            <div>
              <div class="card-label">Tokyo, Japan &bull; Night Walk</div>
              <h3>Tokyo After Dark: Shinjuku Alleys &amp; Late-Night Ramen</h3>
              <p>From the glowing lanterns of Omoide Yokocho to the quiet residential backstreets of Yanaka. A 6-kilometer pedestrian guide to Tokyo's best standing sake bars and midnight broths.</p>
            </div>
            <div class="meta-footer">
              <span>6.2 km walk &bull; 4 food stops</span>
              <span style="color:var(--brass-deep); font-weight:700;">Field Guide &rarr;</span>
            </div>
          </div>
        </article>

        <article class="walk-card">
          <div class="card-thumb">
            <img src="{kyoto_img['url']}" alt="{kyoto_img['alt']}" loading="lazy" width="600" height="340">
          </div>
          <div class="card-content">
            <div>
              <div class="card-label">Kyoto, Japan &bull; Morning Trail</div>
              <h3>Dawn Along Shirakawa Canal: Pour-Overs &amp; Heritage Bakeries</h3>
              <p>Walking the stone paths of Gion at 6:00 AM before the tour buses arrive. We map the third-generation kissatens, matcha roasters, and unheralded artisanal sourdough stalls.</p>
            </div>
            <div class="meta-footer">
              <span>4.8 km walk &bull; 3 coffee stops</span>
              <span style="color:var(--brass-deep); font-weight:700;">Field Guide &rarr;</span>
            </div>
          </div>
        </article>

        <article class="walk-card">
          <div class="card-thumb">
            <img src="{sg_img['url']}" alt="{sg_img['alt']}" loading="lazy" width="600" height="340">
          </div>
          <div class="card-content">
            <div>
              <div class="card-label">Singapore &bull; Heritage Corridor</div>
              <h3>The Spice Corridors: Joo Chiat Shophouses to Little India</h3>
              <p>An architectural and culinary cross-section through Singapore's vibrant heritage districts. Traditional kopi gu you, charcoal popiah, and twilight roti prata stops.</p>
            </div>
            <div class="meta-footer">
              <span>5.5 km walk &bull; 5 culinary stops</span>
              <span style="color:var(--brass-deep); font-weight:700;">Field Guide &rarr;</span>
            </div>
          </div>
        </article>
      </div>
    </section>

    <!-- Section 3: Airlines Directory -->
    <section class="editorial-section">
      <div class="section-eyebrow">03 / Changi Airport Terminal Reference</div>
      <div class="directory-teaser">
        <div class="copy">
          <h3>{airline_count} Global Airlines Operating Changi, Decoded.</h3>
          <p>Alliance alignments (Star Alliance, oneworld, SkyTeam), dedicated terminal maps, lounge access rules, and loyalty program transfer partners. The reference you check before you book.</p>
          <div style="margin-top:1.8rem;">
            <a class="button-brass" href="airlines/">Explore the Airline Glossary &rarr;</a>
          </div>
        </div>
        <div class="teaser-image">
          <img src="{changi_img['url']}" alt="{changi_img['alt']}" loading="lazy" width="800" height="500">
        </div>
      </div>
    </section>

    <!-- Section 4: Editorial Code -->
    <section class="editorial-section">
      <div class="section-eyebrow">04 / Our Editorial Standard</div>
      <div class="section-header-row">
        <h2>How We Work</h2>
      </div>
      <div class="principles-row">
        <div class="principle-box">
          <span class="num">01 / METRICS FIRST</span>
          <h4>Numbers Do the Persuading</h4>
          <p>Exact miles, exact taxes, exact dates. No generic travel-blogger adjectives standing in for a genuine redemption deal.</p>
        </div>
        <div class="principle-box">
          <span class="num">02 / ON FOOT AUTHENTICITY</span>
          <h4>Walked, Timed &amp; Eaten</h4>
          <p>Every urban route is walked at human pace. We only feature eateries, coffee houses, and bakeries where we've personally paid and dined.</p>
        </div>
        <div class="principle-box">
          <span class="num">03 / UNSPONSORED INTEGRITY</span>
          <h4>Zero Airline or Hotel PR</h4>
          <p>No free stays, no junkets, no sponsored airline tickets. Independent reporting for discerning travelers.</p>
        </div>
      </div>
    </section>
    """
    return page(
        title="Stroll & Savor — Urban Walks & Flight Intelligence",
        description="Curated slow urban walks, neighborhood culinary guides, and insider airline loyalty intelligence. Track Singapore Airlines KrisFlyer Spontaneous Escapes with precision.",
        body=body,
        asset_prefix="",
        extra_style=STYLE,
        url_path="",
        og_type="website",
        breadcrumbs=[("Home", "")],
        body_class="theme-editorial",
        head_extra=GOOGLE_FONTS_HEAD,
    )