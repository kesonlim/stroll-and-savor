import base64, pathlib

d = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/fonts")

def b64(name):
    return (d / f"{name}.b64").read_text().strip()

FRAUNCES = b64("fraunces")
KARLA = b64("karla")
BRICOLAGE = b64("bricolage")
NEWSREADER = b64("newsreader")
INSTRUMENT = b64("instrument")
PLEXSANS = b64("plexsans")
SPACEMONO = b64("spacemono")

html = f"""<title>Stroll &amp; Savor — Visual Directions</title>
<style>
  @font-face {{ font-family: 'Fraunces'; src: url(data:font/woff2;base64,{FRAUNCES}) format('woff2'); font-weight: 600; font-display: swap; }}
  @font-face {{ font-family: 'Karla'; src: url(data:font/woff2;base64,{KARLA}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Bricolage Grotesque'; src: url(data:font/woff2;base64,{BRICOLAGE}) format('woff2'); font-weight: 700; font-display: swap; }}
  @font-face {{ font-family: 'Newsreader'; src: url(data:font/woff2;base64,{NEWSREADER}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Instrument Serif'; src: url(data:font/woff2;base64,{INSTRUMENT}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'IBM Plex Sans'; src: url(data:font/woff2;base64,{PLEXSANS}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Space Mono'; src: url(data:font/woff2;base64,{SPACEMONO}) format('woff2'); font-weight: 400; font-display: swap; }}

  :root {{
    --paper: #faf6ee;
    --ink: #2b2620;
    --ink-soft: #6b6255;
    --rule: #e4dbc9;
    --card: #ffffff;
    --accent-a: #d9603f;
    --accent-b: #2f6f5e;
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

  .intro {{ max-width: 720px; margin-bottom: 4rem; }}
  .eyebrow {{
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-a);
    margin: 0 0 1rem;
  }}
  .intro h1 {{
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 600;
    font-size: clamp(2.2rem, 4.4vw, 3.4rem);
    line-height: 1.05;
    margin: 0 0 1.1rem;
    text-wrap: balance;
    letter-spacing: -0.01em;
  }}
  .intro p {{
    font-size: 1.05rem;
    line-height: 1.65;
    color: var(--ink-soft);
    margin: 0 0 0.6rem;
    max-width: 62ch;
  }}
  .intro .brief {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1.6rem;
    margin-top: 1.6rem;
    padding-top: 1.4rem;
    border-top: 1px solid var(--rule);
    font-size: 0.85rem;
    color: var(--ink-soft);
  }}
  .intro .brief b {{ color: var(--ink); font-weight: 600; }}

  .direction {{
    margin-bottom: 5.5rem;
    padding-top: 3rem;
    border-top: 1px solid var(--rule);
  }}
  .direction:first-of-type {{ border-top: none; padding-top: 0; }}

  .dir-head {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 2rem;
    flex-wrap: wrap;
    margin-bottom: 2.2rem;
  }}
  .dir-num {{
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--ink-soft);
    letter-spacing: 0.1em;
  }}
  .dir-name {{ font-size: clamp(1.9rem, 3.4vw, 2.6rem); margin: 0.2rem 0 0.5rem; letter-spacing: -0.01em; }}
  .dir-concept {{ max-width: 46ch; color: var(--ink-soft); font-size: 0.98rem; line-height: 1.55; }}

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
  .type-sample .wordmark {{ font-size: 2.6rem; line-height: 1; margin-bottom: 0.5rem; }}
  .type-sample .lede {{ font-size: 1.05rem; line-height: 1.5; max-width: 44ch; }}
  .type-sample .meta {{ font-family: 'Space Mono', monospace; font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-soft); margin-top: 0.7rem; }}

  /* ---- mock card: shared skeleton, themed per-direction ---- */
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
  .mock .route {{
    font-size: clamp(1.5rem, 3vw, 2rem);
    line-height: 1.08;
    margin: 1.1rem 0 0.3rem;
  }}
  .mock .route small {{ display: block; font-size: 0.62em; font-weight: 400; opacity: 0.7; }}
  .mock .price {{ display: flex; align-items: baseline; gap: 0.5rem; margin-top: 0.6rem; }}
  .mock .price .miles {{ font-family: 'Space Mono', monospace; font-size: 1.15rem; font-weight: 700; }}
  .mock .price .off {{ font-size: 0.72rem; font-family: 'Space Mono', monospace; }}
  .mock .dates {{ font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 0.03em; line-height: 1.6; padding-top: 0.9rem; margin-top: 0.9rem; }}
  .mock .dates .k {{ opacity: 0.65; display: block; margin-bottom: 0.15rem; }}

  /* A — Golden Hour */
  .dirA .mock {{ background: linear-gradient(165deg, #fff8ec 0%, #fbead9 60%, #f7ddc4 100%); border: 1px solid #f0dcbf; }}
  .dirA .mock .tag {{ background: #d9603f; color: #fff8ec; }}
  .dirA .mock .route {{ font-family: 'Fraunces', serif; font-weight: 600; color: #3a2c1f; }}
  .dirA .mock .price .miles {{ color: #2f6f5e; }}
  .dirA .mock .price .off {{ color: #d9603f; }}
  .dirA .mock .dates {{ border-top: 1px dashed #dcc6a4; color: #6b5a44; }}
  .dirA .type-sample .wordmark {{ font-family: 'Fraunces', serif; font-weight: 600; color: #3a2c1f; }}
  .dirA .type-sample .lede {{ font-family: 'Karla', sans-serif; color: #52463a; }}

  /* B — Market Stroll */
  .dirB .mock {{ background: linear-gradient(160deg, #fff3d1 0%, #ffe1a8 100%); border: 1px solid #f3d488; }}
  .dirB .mock .tag {{ background: #c1392b; color: #fff3d1; }}
  .dirB .mock .route {{ font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; color: #2e3b1f; }}
  .dirB .mock .price .miles {{ color: #4c6b2a; }}
  .dirB .mock .price .off {{ color: #c1392b; }}
  .dirB .mock .dates {{ border-top: 1px dashed #e0bd6a; color: #6a5a26; }}
  .dirB .type-sample .wordmark {{ font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; color: #2e3b1f; }}
  .dirB .type-sample .lede {{ font-family: 'Newsreader', serif; font-style: italic; color: #4d4222; }}

  /* C — Boarding Pass */
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

  .footer-note {{
    max-width: 720px;
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
    <p class="eyebrow">Stroll &amp; Savor — Brand Exploration, Round 1</p>
    <h1>Three ways to say "we found you a business class deal" without sounding like an airline.</h1>
    <p>Built against the brief: mixed audience of miles nerds and aspirational travelers, warm and personal in tone, light and bright rather than moody, and no generic airline navy. Each direction is shown against a real Spontaneous Escapes card, since that's the actual unit of content every month.</p>
    <div class="brief">
      <span><b>Audience</b> — miles hobbyists + aspirational dreamers</span>
      <span><b>Tone</b> — warm, personal</span>
      <span><b>Light</b> — bright, not moody</span>
      <span><b>Scope</b> — lifestyle brand, deals is one pillar</span>
    </div>
  </div>

  <div class="direction dirA">
    <div class="dir-head">
      <div>
        <div class="dir-num">DIRECTION A / 03</div>
        <h2 class="dir-name">Golden Hour</h2>
        <p class="dir-concept">A travel-journal warmth — like a postcard written at a café table. Terracotta and deep teal read as considered rather than corporate; the serif gives it the feel of a personal recommendation, not a promo blast.</p>
      </div>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#faf6ee;border:1px solid #eadfc9"></div><div class="label"><span class="name">Paper</span>#FAF6EE</div></div>
          <div class="swatch"><div class="chip" style="background:#3a2c1f"></div><div class="label"><span class="name">Ink</span>#3A2C1F</div></div>
          <div class="swatch"><div class="chip" style="background:#d9603f"></div><div class="label"><span class="name">Terracotta</span>#D9603F</div></div>
          <div class="swatch"><div class="chip" style="background:#2f6f5e"></div><div class="label"><span class="name">Deep Teal</span>#2F6F5E</div></div>
          <div class="swatch"><div class="chip" style="background:#f0dcbf"></div><div class="label"><span class="name">Sand</span>#F0DCBF</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor</div>
          <p class="lede">Fraunces for display — a warm, slightly old-fashioned serif with soft ink-trap curves. Karla for body copy: rounded, legible, unfussy.</p>
          <div class="meta">Fraunces 600 / Karla 400</div>
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

  <div class="direction dirB">
    <div class="dir-head">
      <div>
        <div class="dir-num">DIRECTION B / 03</div>
        <h2 class="dir-name">Market Stroll</h2>
        <p class="dir-concept">Butter-yellow and tomato-red, borrowed from a Saturday food market, not a boarding gate. A bold contemporary display face carries the "stop scrolling" energy the brief asked for; an italic serif body keeps it from tipping into pure hype.</p>
      </div>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#fff3d1;border:1px solid #f3d488"></div><div class="label"><span class="name">Butter</span>#FFF3D1</div></div>
          <div class="swatch"><div class="chip" style="background:#2e3b1f"></div><div class="label"><span class="name">Olive Ink</span>#2E3B1F</div></div>
          <div class="swatch"><div class="chip" style="background:#c1392b"></div><div class="label"><span class="name">Tomato</span>#C1392B</div></div>
          <div class="swatch"><div class="chip" style="background:#4c6b2a"></div><div class="label"><span class="name">Sage</span>#4C6B2A</div></div>
          <div class="swatch"><div class="chip" style="background:#ffe1a8"></div><div class="label"><span class="name">Apricot</span>#FFE1A8</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor</div>
          <p class="lede">Bricolage Grotesque for display — chunky, current, built for a thumbnail. Newsreader italic for body: a diary-entry cadence for captions.</p>
          <div class="meta">Bricolage Grotesque 700 / Newsreader 400 italic</div>
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

  <div class="direction dirC">
    <div class="dir-head">
      <div>
        <div class="dir-num">DIRECTION C / 03</div>
        <h2 class="dir-name">Boarding Pass</h2>
        <p class="dir-concept">Leans into the travel-document object itself — mint and cream instead of navy, with a punched-hole edge and a monospace ticket code. Elegant serif headline keeps it from reading as a novelty ticket stub; it's the most "collectible" of the three.</p>
      </div>
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
          <p class="lede">Instrument Serif for display — thin, elegant, a little vintage-ticket. IBM Plex Sans for body, Space Mono for miles/dates so numbers read like a real fare stamp.</p>
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

  <p class="footer-note">Reply with a direction letter, a mix ("A's palette with C's ticket-code detail"), or a fourth path entirely — this is a first pass to react to, not a final. Once one lands, it becomes the token system for the monthly artifact, carousel, and story graphic.</p>
</div>
"""

out = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/stroll-savor-moodboard.html")
out.write_text(html)
print("wrote", out, len(html), "chars")
