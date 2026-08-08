import base64, pathlib

d = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/fonts")

def b64(name):
    return (d / f"{name}.b64").read_text().strip()

INSTRUMENT = b64("instrument")
PLEXSANS = b64("plexsans")
SPACEMONO = b64("spacemono")
ARCHIVO = b64("archivo_narrow")
DOMINE = b64("domine")
COURIER = b64("courier_prime")

html = f"""<title>Stroll &amp; Savor — Visual Directions, Round 2</title>
<style>
  @font-face {{ font-family: 'Instrument Serif'; src: url(data:font/woff2;base64,{INSTRUMENT}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'IBM Plex Sans'; src: url(data:font/woff2;base64,{PLEXSANS}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Space Mono'; src: url(data:font/woff2;base64,{SPACEMONO}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Archivo Narrow'; src: url(data:font/woff2;base64,{ARCHIVO}) format('woff2'); font-weight: 700; font-display: swap; }}
  @font-face {{ font-family: 'Domine'; src: url(data:font/woff2;base64,{DOMINE}) format('woff2'); font-weight: 700; font-display: swap; }}
  @font-face {{ font-family: 'Courier Prime'; src: url(data:font/woff2;base64,{COURIER}) format('woff2'); font-weight: 700; font-display: swap; }}

  :root {{
    --paper: #faf6ee;
    --ink: #2b2620;
    --ink-soft: #6b6255;
    --rule: #e4dbc9;
    --accent-a: #d9603f;
    --pine: #16403a;
  }}

  * {{ box-sizing: border-box; }}
  html {{ background: var(--paper); }}
  body {{
    background: var(--paper);
    color: var(--ink);
    font-family: 'IBM Plex Sans', ui-sans-serif, system-ui, sans-serif;
    margin: 0;
    padding: 0 0 6rem;
    -webkit-font-smoothing: antialiased;
  }}

  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 4rem 1.75rem 0; }}

  .intro {{ max-width: 760px; margin-bottom: 3rem; }}
  .eyebrow {{
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-a);
    margin: 0 0 1rem;
  }}
  .intro h1 {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-weight: 400;
    font-size: clamp(2.2rem, 4.4vw, 3.3rem);
    line-height: 1.08;
    margin: 0 0 1.1rem;
    text-wrap: balance;
  }}
  .intro p {{
    font-size: 1.05rem;
    line-height: 1.65;
    color: var(--ink-soft);
    margin: 0 0 0.6rem;
    max-width: 64ch;
  }}

  .persona {{
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0 1.4rem;
    background: #fff;
    border: 1px solid var(--rule);
    border-radius: 16px;
    padding: 1.5rem 1.7rem;
    margin: 2rem 0 4rem;
    max-width: 760px;
  }}
  .persona .badge {{
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: var(--pine);
    color: #eafaf1;
    padding: 0.3rem 0.6rem;
    border-radius: 100px;
    height: fit-content;
    grid-row: 1;
  }}
  .persona h3 {{ margin: 0 0 0.4rem; font-size: 1.15rem; grid-column: 2; }}
  .persona p {{ grid-column: 2; margin: 0; font-size: 0.93rem; line-height: 1.55; color: var(--ink-soft); }}
  .persona .stats {{ grid-column: 2; display: flex; gap: 1.4rem; flex-wrap: wrap; margin-top: 0.9rem; font-family: 'Space Mono', monospace; font-size: 0.72rem; color: var(--ink); }}
  .persona .stats b {{ display: block; font-size: 0.62rem; font-weight: 400; letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink-soft); margin-bottom: 0.15rem; }}

  .baseline-flag {{
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-family: 'Space Mono', monospace; font-size: 0.66rem; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--pine); margin-bottom: 0.6rem;
  }}
  .baseline-flag::before {{ content: "●"; font-size: 0.55rem; }}

  .direction {{
    margin-bottom: 5.5rem;
    padding-top: 3rem;
    border-top: 1px solid var(--rule);
  }}
  .direction:first-of-type {{ border-top: none; padding-top: 0; }}

  .dir-num {{
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--ink-soft);
    letter-spacing: 0.1em;
  }}
  .dir-name {{ font-size: clamp(1.9rem, 3.4vw, 2.6rem); margin: 0.2rem 0 0.5rem; letter-spacing: -0.01em; }}
  .dir-concept {{ max-width: 48ch; color: var(--ink-soft); font-size: 0.98rem; line-height: 1.55; margin-bottom: 2.2rem; }}

  .dir-grid {{
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    gap: 2.5rem;
    align-items: start;
  }}
  @media (max-width: 860px) {{ .dir-grid {{ grid-template-columns: 1fr; }} }}

  .swatches {{ display: flex; gap: 0.6rem; margin-bottom: 1.6rem; flex-wrap: wrap; }}
  .swatch {{ flex: 1 1 90px; min-width: 84px; }}
  .swatch .chip {{ height: 64px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.06); }}
  .swatch .label {{ font-family: 'Space Mono', monospace; font-size: 0.68rem; margin-top: 0.4rem; color: var(--ink-soft); line-height: 1.3; }}
  .swatch .name {{ display: block; color: var(--ink); font-size: 0.72rem; font-weight: 700; font-family: 'IBM Plex Sans', sans-serif; margin-bottom: 0.1rem; }}

  .type-sample {{ margin-bottom: 1.6rem; }}
  .type-sample .wordmark {{ font-size: 2.5rem; line-height: 1; margin-bottom: 0.5rem; }}
  .type-sample .lede {{ font-size: 1.02rem; line-height: 1.5; max-width: 44ch; }}
  .type-sample .meta {{ font-family: 'Space Mono', monospace; font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-soft); margin-top: 0.7rem; }}

  .mock {{
    border-radius: 20px;
    padding: 1.7rem;
    aspect-ratio: 4 / 5;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 18px 40px -22px rgba(0,0,0,0.28);
  }}
  .mock .tag {{
    align-self: flex-start;
    font-family: 'Space Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.35rem 0.65rem;
    border-radius: 100px;
  }}
  .mock .route {{ font-size: clamp(1.5rem, 3vw, 2rem); line-height: 1.08; margin: 1.1rem 0 0.3rem; }}
  .mock .route small {{ display: block; font-size: 0.62em; font-weight: 400; opacity: 0.7; }}
  .mock .price {{ display: flex; align-items: baseline; gap: 0.5rem; margin-top: 0.6rem; }}
  .mock .price .miles {{ font-family: 'Space Mono', monospace; font-size: 1.15rem; font-weight: 700; }}
  .mock .price .off {{ font-size: 0.72rem; font-family: 'Space Mono', monospace; }}
  .mock .dates {{ font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 0.03em; line-height: 1.6; padding-top: 0.9rem; margin-top: 0.9rem; }}
  .mock .dates .k {{ opacity: 0.65; display: block; margin-bottom: 0.15rem; }}

  /* C — Boarding Pass (baseline) */
  .dirC .mock {{ background: linear-gradient(155deg, #f2fbf6 0%, #dcf1e6 100%); border: 1px solid #bfe3cf; }}
  .dirC .mock::after {{
    content: ""; position: absolute; right: -14px; top: 50%; width: 28px; height: 28px;
    background: var(--paper); border-radius: 50%; transform: translateY(-50%);
    box-shadow: inset 0 0 0 1px #bfe3cf;
  }}
  .dirC .mock .tag {{ background: #16403a; color: #eafaf1; }}
  .dirC .mock .route {{ font-family: 'Instrument Serif', serif; font-weight: 400; color: #16403a; }}
  .dirC .mock .price .miles {{ color: #16403a; }}
  .dirC .mock .price .off {{ color: #d9603f; }}
  .dirC .mock .dates {{ border-top: 1px dashed #9dcdb2; color: #2c5a4e; }}
  .dirC .type-sample .wordmark {{ font-family: 'Instrument Serif', serif; font-weight: 400; color: #16403a; }}
  .dirC .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #2c5a4e; }}

  /* D — Flight Log */
  .dirD .mock {{ background: linear-gradient(160deg, #f3f1e9 0%, #e7e2d3 100%); border: 1px solid #d8d0b8;
    background-image:
      linear-gradient(160deg, #f3f1e9 0%, #e7e2d3 100%),
      repeating-linear-gradient(0deg, transparent, transparent 27px, rgba(43,40,35,0.05) 27px, rgba(43,40,35,0.05) 28px);
  }}
  .dirD .mock .tag {{ background: #e8a33d; color: #2b2823; }}
  .dirD .mock .route {{ font-family: 'Archivo Narrow', sans-serif; font-weight: 700; text-transform: uppercase; letter-spacing: 0.01em; color: #2b2823; }}
  .dirD .mock .price .miles {{ color: #4a6fa5; }}
  .dirD .mock .price .off {{ color: #c1671f; }}
  .dirD .mock .dates {{ border-top: 1px dashed #c9c0a0; color: #5a5644; }}
  .dirD .type-sample .wordmark {{ font-family: 'Archivo Narrow', sans-serif; font-weight: 700; text-transform: uppercase; letter-spacing: 0.02em; color: #2b2823; }}
  .dirD .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #55503f; }}

  /* E — Luggage Tag */
  .dirE .mock {{ background: linear-gradient(155deg, #f1e3c8 0%, #e6d0a4 100%); border: 1px solid #d3b981; }}
  .dirE .mock::before {{
    content: ""; position: absolute; left: 50%; top: 14px; width: 46px; height: 12px;
    border: 2px solid rgba(59,42,28,0.35); border-radius: 8px; transform: translateX(-50%);
  }}
  .dirE .mock {{ padding-top: 2.6rem; }}
  .dirE .mock .tag {{ background: #b5432c; color: #f8ecd8; }}
  .dirE .mock .route {{ font-family: 'Domine', serif; font-weight: 700; color: #3b2a1c; }}
  .dirE .mock .price .miles {{ color: #5c7a5a; }}
  .dirE .mock .price .off {{ color: #b5432c; }}
  .dirE .mock .dates {{ border-top: 1px dashed #c9ad82; color: #6b5636; }}
  .dirE .type-sample .wordmark {{ font-family: 'Domine', serif; font-weight: 700; color: #3b2a1c; }}
  .dirE .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #5a4a34; }}

  /* F — Field Notes */
  .dirF .mock {{ background: #f1f0ea; border: 1px solid #d7d5c8;
    background-image:
      radial-gradient(circle, rgba(46,46,44,0.12) 1px, transparent 1px);
    background-size: 16px 16px;
  }}
  .dirF .mock .tag {{ background: #b4552f; color: #f8f6ee; }}
  .dirF .mock .route {{ font-family: 'Courier Prime', monospace; font-weight: 700; color: #2e2e2c; }}
  .dirF .mock .price .miles {{ color: #3e7c74; }}
  .dirF .mock .price .off {{ color: #b4552f; }}
  .dirF .mock .dates {{ border-top: 1px dashed #a9a696; color: #4a4a3f; }}
  .dirF .type-sample .wordmark {{ font-family: 'Courier Prime', monospace; font-weight: 700; color: #2e2e2c; }}
  .dirF .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #4a4a3f; }}

  .footer-note {{
    max-width: 760px;
    margin: 0 auto;
    padding: 0 1.75rem;
    font-size: 0.92rem;
    line-height: 1.6;
    color: var(--ink-soft);
    border-top: 1px solid var(--rule);
    padding-top: 2rem;
  }}
  .footer-note b {{ color: var(--ink); }}
</style>

<div class="wrap">
  <div class="intro">
    <p class="eyebrow">Stroll &amp; Savor — Brand Exploration, Round 2</p>
    <h1>Boarding Pass, plus three more objects the same collector would keep.</h1>
    <p>Direction C is confirmed as the baseline. Below: who it's for, then three more directions built for that same reader — each one borrows from a different real travel object, the way C borrowed from the ticket stub.</p>
  </div>

  <div class="persona">
    <span class="badge">Persona</span>
    <h3>The Deliberate Collector</h3>
    <p>Late 20s–mid 50s, skews male, works in a field that rewards systems-thinking — finance, engineering, tech, consulting. Treats a miles balance like a portfolio: researched, tracked, optimized. Reads FlyerTalk threads and r/churning, not just Instagram. Distrusts glossy "luxury travel" marketing but will absolutely screenshot a well-formatted deal table. The trip itself matters less than proof the strategy worked — collects the win the way others collect watches, film cameras, or vinyl: precision objects with a bit of ritual attached. Direction C landed because it treats a promo listing with the same respect as the numbers deserve, rather than burying them in lifestyle gloss.</p>
    <div class="stats">
      <span><b>Age band</b>30–55</span>
      <span><b>Skew</b>~70% male</span>
      <span><b>Mindset</b>optimizer, not spender</span>
      <span><b>Trusts</b>data over adjectives</span>
    </div>
  </div>

  <div class="direction dirC">
    <span class="baseline-flag">Confirmed baseline</span>
    <div>
      <div class="dir-num">DIRECTION C</div>
      <h2 class="dir-name">Boarding Pass</h2>
      <p class="dir-concept">Mint and cream instead of navy, a punched-hole edge, and a monospace ticket code carrying the miles and dates like a fare stamp. Elegant, a little vintage, unmistakably a travel document rather than an ad.</p>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#f2fbf6;border:1px solid #bfe3cf"></div><div class="label"><span class="name">Mint Paper</span>#F2FBF6</div></div>
          <div class="swatch"><div class="chip" style="background:#16403a"></div><div class="label"><span class="name">Pine Ink</span>#16403A</div></div>
          <div class="swatch"><div class="chip" style="background:#d9603f"></div><div class="label"><span class="name">Stamp Red</span>#D9603F</div></div>
          <div class="swatch"><div class="chip" style="background:#dcf1e6"></div><div class="label"><span class="name">Seafoam</span>#DCF1E6</div></div>
          <div class="swatch"><div class="chip" style="background:#9dcdb2"></div><div class="label"><span class="name">Perforation</span>#9DCDB2</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor</div>
          <p class="lede">Instrument Serif for display, IBM Plex Sans for body, Space Mono for miles/dates.</p>
          <div class="meta">Instrument Serif 400 / Plex Sans 400 / Space Mono 400</div>
        </div>
      </div>
      <div class="mock">
        <span class="tag">Spontaneous Escape</span>
        <div class="route">Singapore → Tokyo<small>Business Class</small></div>
        <div>
          <div class="price"><span class="miles">100,500 mi</span><span class="off">−23% vs Saver</span></div>
          <div class="dates"><span class="k">Available this month</span>Aug 3 · 7 · 12 · 18 · 24 · 29</div>
        </div>
      </div>
    </div>
  </div>

  <div class="direction dirD">
    <div>
      <div class="dir-num">DIRECTION D / 03</div>
      <h2 class="dir-name">Flight Log</h2>
      <p class="dir-concept">A pilot's logbook page, not a cockpit dashboard — ruled paper, amber instrument-warning accent instead of navy, a condensed placard face for the route. Reads as the record of someone who actually flies, tracking every leg.</p>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#f3f1e9;border:1px solid #d8d0b8"></div><div class="label"><span class="name">Log Paper</span>#F3F1E9</div></div>
          <div class="swatch"><div class="chip" style="background:#2b2823"></div><div class="label"><span class="name">Graphite</span>#2B2823</div></div>
          <div class="swatch"><div class="chip" style="background:#e8a33d"></div><div class="label"><span class="name">Instrument Amber</span>#E8A33D</div></div>
          <div class="swatch"><div class="chip" style="background:#4a6fa5"></div><div class="label"><span class="name">Steel Blue</span>#4A6FA5</div></div>
          <div class="swatch"><div class="chip" style="background:#e7e2d3"></div><div class="label"><span class="name">Ruled Line</span>#E7E2D3</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">STROLL &amp; SAVOR</div>
          <p class="lede">Archivo Narrow for display — condensed, technical, placard-like. Plex Sans stays for body; Space Mono for the log entries.</p>
          <div class="meta">Archivo Narrow 700 / Plex Sans 400 / Space Mono 400</div>
        </div>
      </div>
      <div class="mock">
        <span class="tag">Spontaneous Escape</span>
        <div class="route">Singapore → Tokyo<small>Business Class</small></div>
        <div>
          <div class="price"><span class="miles">100,500 mi</span><span class="off">−23% vs Saver</span></div>
          <div class="dates"><span class="k">Available this month</span>Aug 3 · 7 · 12 · 18 · 24 · 29</div>
        </div>
      </div>
    </div>
  </div>

  <div class="direction dirE">
    <div>
      <div class="dir-num">DIRECTION E / 03</div>
      <h2 class="dir-name">Luggage Tag</h2>
      <p class="dir-concept">Kraft-paper warmth and a postmark red, styled after the string-tied trunk tags from air travel's golden age. The most "keepsake" of the four — a route sounds like a destination worth bragging about, not just a fare code.</p>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#f1e3c8;border:1px solid #d3b981"></div><div class="label"><span class="name">Kraft</span>#F1E3C8</div></div>
          <div class="swatch"><div class="chip" style="background:#3b2a1c"></div><div class="label"><span class="name">Ink Brown</span>#3B2A1C</div></div>
          <div class="swatch"><div class="chip" style="background:#b5432c"></div><div class="label"><span class="name">Postmark Red</span>#B5432C</div></div>
          <div class="swatch"><div class="chip" style="background:#5c7a5a"></div><div class="label"><span class="name">Tag Green</span>#5C7A5A</div></div>
          <div class="swatch"><div class="chip" style="background:#c9ad82"></div><div class="label"><span class="name">Twine Tan</span>#C9AD82</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor</div>
          <p class="lede">Domine for display — sturdy, stamped, a little vintage-label. Plex Sans and Space Mono carry the fare detail underneath.</p>
          <div class="meta">Domine 700 / Plex Sans 400 / Space Mono 400</div>
        </div>
      </div>
      <div class="mock">
        <span class="tag">Spontaneous Escape</span>
        <div class="route">Singapore → Tokyo<small>Business Class</small></div>
        <div>
          <div class="price"><span class="miles">100,500 mi</span><span class="off">−23% vs Saver</span></div>
          <div class="dates"><span class="k">Available this month</span>Aug 3 · 7 · 12 · 18 · 24 · 29</div>
        </div>
      </div>
    </div>
  </div>

  <div class="direction dirF">
    <div>
      <div class="dir-num">DIRECTION F / 03</div>
      <h2 class="dir-name">Field Notes</h2>
      <p class="dir-concept">A researcher's travel notebook — dot-grid paper, a rust route-line, a typewriter face for headlines. Feels like the reader's own tracking spreadsheet turned into something worth sharing, which is close to the truth of how this audience actually works.</p>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#f1f0ea;border:1px solid #d7d5c8"></div><div class="label"><span class="name">Dot-grid Paper</span>#F1F0EA</div></div>
          <div class="swatch"><div class="chip" style="background:#2e2e2c"></div><div class="label"><span class="name">Pencil Ink</span>#2E2E2C</div></div>
          <div class="swatch"><div class="chip" style="background:#b4552f"></div><div class="label"><span class="name">Route Rust</span>#B4552F</div></div>
          <div class="swatch"><div class="chip" style="background:#3e7c74"></div><div class="label"><span class="name">Map Teal</span>#3E7C74</div></div>
          <div class="swatch"><div class="chip" style="background:#d7d5c8"></div><div class="label"><span class="name">Grid Dot</span>#D7D5C8</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor</div>
          <p class="lede">Courier Prime for display — typewriter cadence, field-journal honesty. Plex Sans for body, Space Mono for data so it doesn't compete with the headline mono.</p>
          <div class="meta">Courier Prime 700 / Plex Sans 400 / Space Mono 400</div>
        </div>
      </div>
      <div class="mock">
        <span class="tag">Spontaneous Escape</span>
        <div class="route">Singapore → Tokyo<small>Business Class</small></div>
        <div>
          <div class="price"><span class="miles">100,500 mi</span><span class="off">−23% vs Saver</span></div>
          <div class="dates"><span class="k">Available this month</span>Aug 3 · 7 · 12 · 18 · 24 · 29</div>
        </div>
      </div>
    </div>
  </div>

  <p class="footer-note">All four (C, D, E, F) target the same Deliberate Collector persona through a different physical object. Pick one to lock as the final system, or mix (e.g. E's kraft palette with C's punched-ticket shape) — next step after that is applying it to the actual monthly artifact, carousel, and story templates.</p>
</div>
"""

out = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/stroll-savor-moodboard.html")
out.write_text(html)
print("wrote", out, len(html), "chars")
