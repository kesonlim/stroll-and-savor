import base64, pathlib

d = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/fonts")

def b64(name):
    return (d / f"{name}.b64").read_text().strip()

INSTRUMENT = b64("instrument")
PLEXSANS = b64("plexsans")
SPACEMONO = b64("spacemono")
COURIER = b64("courier_prime")

html = f"""<title>Stroll &amp; Savor — C &amp; F, and the space between them</title>
<style>
  @font-face {{ font-family: 'Instrument Serif'; src: url(data:font/woff2;base64,{INSTRUMENT}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'IBM Plex Sans'; src: url(data:font/woff2;base64,{PLEXSANS}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Space Mono'; src: url(data:font/woff2;base64,{SPACEMONO}) format('woff2'); font-weight: 400; font-display: swap; }}
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

  .finalists {{
    display: flex; gap: 0.6rem; margin: 1.8rem 0 4rem; flex-wrap: wrap;
  }}
  .finalists .pill {{
    font-family: 'Space Mono', monospace; font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase;
    border: 1px solid var(--rule); border-radius: 100px; padding: 0.4rem 0.9rem; color: var(--ink-soft);
  }}
  .finalists .pill b {{ color: var(--pine); }}

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

  .section-label {{
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-a);
    margin-bottom: 0.6rem;
  }}

  .dir-num {{
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--ink-soft);
    letter-spacing: 0.1em;
  }}
  .dir-name {{ font-size: clamp(1.9rem, 3.4vw, 2.6rem); margin: 0.2rem 0 0.5rem; letter-spacing: -0.01em; }}
  .dir-concept {{ max-width: 50ch; color: var(--ink-soft); font-size: 0.98rem; line-height: 1.55; margin-bottom: 2.2rem; }}
  .dir-concept .recipe {{ display: block; margin-top: 0.6rem; color: var(--ink); font-size: 0.85rem; }}
  .dir-concept .recipe b {{ font-weight: 700; }}

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

  /* C — Boarding Pass (finalist) */
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

  /* F — Field Notes (finalist) */
  .dirF .mock {{ background: #f1f0ea; border: 1px solid #d7d5c8;
    background-image: radial-gradient(circle, rgba(46,46,44,0.12) 1px, transparent 1px);
    background-size: 16px 16px;
  }}
  .dirF .mock .tag {{ background: #b4552f; color: #f8f6ee; }}
  .dirF .mock .route {{ font-family: 'Courier Prime', monospace; font-weight: 700; color: #2e2e2c; }}
  .dirF .mock .price .miles {{ color: #3e7c74; }}
  .dirF .mock .price .off {{ color: #b4552f; }}
  .dirF .mock .dates {{ border-top: 1px dashed #a9a696; color: #4a4a3f; }}
  .dirF .type-sample .wordmark {{ font-family: 'Courier Prime', monospace; font-weight: 700; color: #2e2e2c; }}
  .dirF .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #4a4a3f; }}

  /* G — Notebook Ticket: F's paper + shape, C's palette & headline */
  .dirG .mock {{ background: #f3f9f5; border: 1px solid #cfe6da;
    background-image: radial-gradient(circle, rgba(22,64,58,0.10) 1px, transparent 1px);
    background-size: 16px 16px;
  }}
  .dirG .mock::after {{
    content: ""; position: absolute; right: -14px; top: 50%; width: 28px; height: 28px;
    background: var(--paper); border-radius: 50%; transform: translateY(-50%);
    box-shadow: inset 0 0 0 1px #cfe6da;
  }}
  .dirG .mock .tag {{ background: #16403a; color: #eafaf1; }}
  .dirG .mock .route {{ font-family: 'Instrument Serif', serif; font-weight: 400; color: #16403a; }}
  .dirG .mock .price .miles {{ color: #16403a; }}
  .dirG .mock .price .off {{ color: #b4552f; }}
  .dirG .mock .dates {{ border-top: 1px dashed #a9c9bb; color: #2c5a4e; }}
  .dirG .type-sample .wordmark {{ font-family: 'Instrument Serif', serif; font-weight: 400; color: #16403a; }}
  .dirG .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #2c5a4e; }}

  /* H — Field Ticket: C's paper + punched shape, F's headline & rust accent */
  .dirH .mock {{ background: linear-gradient(155deg, #f5f3ec 0%, #ece8db 100%); border: 1px solid #dcd6c3; }}
  .dirH .mock::after {{
    content: ""; position: absolute; right: -14px; top: 50%; width: 28px; height: 28px;
    background: var(--paper); border-radius: 50%; transform: translateY(-50%);
    box-shadow: inset 0 0 0 1px #dcd6c3;
  }}
  .dirH .mock .tag {{ background: #b4552f; color: #f8f6ee; }}
  .dirH .mock .route {{ font-family: 'Courier Prime', monospace; font-weight: 700; color: #2e2e2c; }}
  .dirH .mock .price .miles {{ color: #3e7c74; }}
  .dirH .mock .price .off {{ color: #b4552f; }}
  .dirH .mock .dates {{ border-top: 1px dashed #c9c0a0; color: #4a4a3f; }}
  .dirH .type-sample .wordmark {{ font-family: 'Courier Prime', monospace; font-weight: 700; color: #2e2e2c; }}
  .dirH .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #4a4a3f; }}

  /* I — Dual Stamp: literal split-band card, both textures at once */
  .dirI .mock {{ background: #f2fbf6; border: 1px solid #bfe3cf; padding: 0; }}
  .dirI .mock .band-top {{
    background: linear-gradient(155deg, #f2fbf6 0%, #dcf1e6 100%);
    padding: 1.7rem 1.7rem 1rem;
    position: relative;
  }}
  .dirI .mock .band-top::after {{
    content: ""; position: absolute; right: -14px; top: 20px; width: 24px; height: 24px;
    background: var(--paper); border-radius: 50%;
    box-shadow: inset 0 0 0 1px #bfe3cf;
  }}
  .dirI .mock .tear {{
    border-top: 2px dashed #9dcdb2; position: relative;
  }}
  .dirI .mock .band-bottom {{
    background: #f1f0ea;
    background-image: radial-gradient(circle, rgba(46,46,44,0.12) 1px, transparent 1px);
    background-size: 14px 14px;
    padding: 1rem 1.7rem 1.5rem;
    flex: 1;
    display: flex; flex-direction: column; justify-content: flex-end;
  }}
  .dirI .mock .tag {{ background: #16403a; color: #eafaf1; }}
  .dirI .mock .route {{ font-family: 'Instrument Serif', serif; font-weight: 400; color: #16403a; }}
  .dirI .mock .price .miles {{ color: #16403a; }}
  .dirI .mock .price .off {{ color: #b4552f; }}
  .dirI .mock .dates {{ font-family: 'Courier Prime', monospace; font-weight: 700; font-size: 0.66rem; letter-spacing: 0.02em; line-height: 1.7; color: #2e2e2c; }}
  .dirI .mock .dates .k {{ font-family: 'Space Mono', monospace; font-weight: 400; opacity: 0.65; display: block; margin-bottom: 0.15rem; text-transform: uppercase; }}
  .dirI .type-sample .wordmark {{ font-family: 'Instrument Serif', serif; font-weight: 400; color: #16403a; }}
  .dirI .type-sample .wordmark span {{ font-family: 'Courier Prime', monospace; font-weight: 700; font-size: 0.6em; color: #b4552f; vertical-align: middle; margin-left: 0.3rem; }}
  .dirI .type-sample .lede {{ font-family: 'IBM Plex Sans', sans-serif; color: #4a4a3f; }}

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
    <p class="eyebrow">Stroll &amp; Savor — Brand Exploration, Round 3</p>
    <h1>Down to two. Here's the space between them.</h1>
    <p>C and F both tested well with the same Deliberate Collector reader — a ticket versus a field notebook, elegance versus rigor. Rather than picking one outright, here are three ways to blend them, each borrowing a different share from each side.</p>
    <div class="finalists">
      <span class="pill"><b>C</b> Boarding Pass — mint, punched ticket, Instrument Serif</span>
      <span class="pill"><b>F</b> Field Notes — dot-grid, pencil ink, Courier Prime</span>
    </div>
  </div>

  <div class="direction dirC">
    <span class="baseline-flag">Finalist</span>
    <div>
      <div class="dir-num">DIRECTION C</div>
      <h2 class="dir-name">Boarding Pass</h2>
      <p class="dir-concept">Mint and cream instead of navy, a punched-hole edge, and a monospace ticket code carrying the miles and dates like a fare stamp.</p>
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
          <p class="lede">Instrument Serif display, Plex Sans body, Space Mono for miles/dates.</p>
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

  <div class="direction dirF">
    <span class="baseline-flag">Finalist</span>
    <div>
      <div class="dir-num">DIRECTION F</div>
      <h2 class="dir-name">Field Notes</h2>
      <p class="dir-concept">A researcher's travel notebook — dot-grid paper, a rust route-line, a typewriter face for headlines. Feels like the reader's own tracking spreadsheet turned into something worth sharing.</p>
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
          <p class="lede">Courier Prime display, Plex Sans body, Space Mono for data.</p>
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

  <div class="direction dirG">
    <p class="section-label">Hybrid — leans Field Notes</p>
    <div>
      <div class="dir-num">DIRECTION G / 03</div>
      <h2 class="dir-name">Notebook Ticket</h2>
      <p class="dir-concept">F's dot-grid paper and rigor, tinted toward C's mint and punched-ticket silhouette. Reads as a field notebook that happens to be shaped like a boarding pass.
        <span class="recipe"><b>Recipe:</b> F's texture + shape hint from C · C's mint/pine palette, rust kept as the discount color · C's Instrument Serif headline</span>
      </p>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#f3f9f5;border:1px solid #cfe6da"></div><div class="label"><span class="name">Minted Grid</span>#F3F9F5</div></div>
          <div class="swatch"><div class="chip" style="background:#16403a"></div><div class="label"><span class="name">Pine Ink</span>#16403A</div></div>
          <div class="swatch"><div class="chip" style="background:#b4552f"></div><div class="label"><span class="name">Route Rust</span>#B4552F</div></div>
          <div class="swatch"><div class="chip" style="background:#cfe6da"></div><div class="label"><span class="name">Seafoam Dot</span>#CFE6DA</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor</div>
          <p class="lede">Instrument Serif for the route name, Space Mono for the fare detail — same pairing as C, on F's paper.</p>
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

  <div class="direction dirH">
    <p class="section-label">Hybrid — leans Boarding Pass</p>
    <div>
      <div class="dir-num">DIRECTION H / 03</div>
      <h2 class="dir-name">Field Ticket</h2>
      <p class="dir-concept">C's punched ticket shape and cream paper, carrying F's typewriter voice and rust route color instead of the stamp red. The plainer, more workmanlike sibling of C.
        <span class="recipe"><b>Recipe:</b> C's paper + punched shape · F's ink, teal &amp; rust palette · F's Courier Prime headline</span>
      </p>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#f5f3ec;border:1px solid #dcd6c3"></div><div class="label"><span class="name">Ticket Cream</span>#F5F3EC</div></div>
          <div class="swatch"><div class="chip" style="background:#2e2e2c"></div><div class="label"><span class="name">Pencil Ink</span>#2E2E2C</div></div>
          <div class="swatch"><div class="chip" style="background:#b4552f"></div><div class="label"><span class="name">Route Rust</span>#B4552F</div></div>
          <div class="swatch"><div class="chip" style="background:#3e7c74"></div><div class="label"><span class="name">Map Teal</span>#3E7C74</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor</div>
          <p class="lede">Courier Prime headline on a punched-ticket card — the notebook's voice, the ticket's shape.</p>
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

  <div class="direction dirI">
    <p class="section-label">Hybrid — literal 50/50</p>
    <div>
      <div class="dir-num">DIRECTION I / 03</div>
      <h2 class="dir-name">Dual Stamp</h2>
      <p class="dir-concept">No blending — an actual perforated split. The route lives on a torn-off ticket stub up top in C's voice; the fare log sits on dot-grid paper below in F's. One card, two textures, a dashed tear between them.
        <span class="recipe"><b>Recipe:</b> Top band = C in full · Bottom band = F in full · joined at a torn perforation</span>
      </p>
    </div>
    <div class="dir-grid">
      <div>
        <div class="swatches">
          <div class="swatch"><div class="chip" style="background:#dcf1e6;border:1px solid #bfe3cf"></div><div class="label"><span class="name">Mint (top)</span>#DCF1E6</div></div>
          <div class="swatch"><div class="chip" style="background:#f1f0ea;border:1px solid #d7d5c8"></div><div class="label"><span class="name">Dot-grid (bottom)</span>#F1F0EA</div></div>
          <div class="swatch"><div class="chip" style="background:#16403a"></div><div class="label"><span class="name">Pine Ink</span>#16403A</div></div>
          <div class="swatch"><div class="chip" style="background:#b4552f"></div><div class="label"><span class="name">Route Rust</span>#B4552F</div></div>
        </div>
        <div class="type-sample">
          <div class="wordmark">Stroll &amp; Savor<span>LOG</span></div>
          <p class="lede">Instrument Serif up top for the route, Courier Prime below for the fare log — each face stays in its own half.</p>
          <div class="meta">Instrument Serif + Courier Prime, split by section</div>
        </div>
      </div>
      <div class="mock">
        <div class="band-top">
          <span class="tag">Spontaneous Escape</span>
          <div class="route">Singapore → Tokyo<small>Business Class</small></div>
        </div>
        <div class="band-bottom tear">
          <div class="price"><span class="miles">100,500 mi</span><span class="off">−23% vs Saver</span></div>
          <div class="dates"><span class="k">Available this month</span>Aug 3 · 7 · 12 · 18 · 24 · 29</div>
        </div>
      </div>
    </div>
  </div>

  <p class="footer-note">G and H are single-surface blends (one paper, one palette, mixed fonts); I is a literal split card that keeps both languages fully intact. Pick C, F, one hybrid, or point me at a specific swap you want tried (e.g. "H's palette on C's headline") and I'll refine from there — then it becomes the token system for the monthly artifact, carousel, and story templates.</p>
</div>
"""

out = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/stroll-savor-moodboard.html")
out.write_text(html)
print("wrote", out, len(html), "chars")
