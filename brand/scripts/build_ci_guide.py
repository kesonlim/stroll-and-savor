import base64, pathlib

d = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/fonts")
svgdir = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/logo-master/svg")

def b64(name):
    return (d / f"{name}.b64").read_text().strip()

def svg(name):
    return (svgdir / name).read_text()

PLEXSANS = b64("plexsans")
PLEXSANS_600 = b64("plexsans_600")
SPACEMONO = b64("spacemono")
COURIER = b64("courier_prime")

WORDMARK_INK = svg("wordmark-ink-on-transparent.svg")
MONOGRAM_INK = svg("monogram-ink-on-transparent.svg")
MONOGRAM_PAPER = svg("monogram-paper-on-transparent.svg")

html = f"""<title>Stroll &amp; Savor — Brand Guide</title>
<style>
  @font-face {{ font-family: 'IBM Plex Sans'; src: url(data:font/woff2;base64,{PLEXSANS}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'IBM Plex Sans'; src: url(data:font/woff2;base64,{PLEXSANS_600}) format('woff2'); font-weight: 600; font-display: swap; }}
  @font-face {{ font-family: 'Space Mono'; src: url(data:font/woff2;base64,{SPACEMONO}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Courier Prime'; src: url(data:font/woff2;base64,{COURIER}) format('woff2'); font-weight: 700; font-display: swap; }}

  :root {{
    --paper: #f1f0ea;
    --paper-2: #faf9f5;
    --ink: #2e2e2c;
    --ink-soft: #6d6a5f;
    --rule: #d7d5c8;
    --rust: #b4552f;
    --rust-soft: #e0a583;
    --rust-text: #994827;
    --teal: #3e7c74;
    --teal-text: #346962;
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
    background-image: radial-gradient(circle, rgba(46,46,44,0.08) 1px, transparent 1px);
    background-size: 18px 18px;
  }}

  .wrap {{ max-width: 980px; margin: 0 auto; padding: 4rem 1.75rem 0; }}

  .cover {{ margin-bottom: 5rem; }}
  .cover .eyebrow {{
    font-family: 'Space Mono', monospace; font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--rust-text); margin: 0 0 1.4rem;
  }}
  .cover .wordmark-slot svg {{ width: 340px; max-width: 70vw; height: auto; display: block; margin-bottom: 1.6rem; }}
  .cover h1 {{ font-family: 'Courier Prime', monospace; font-weight: 700; font-size: clamp(1.5rem, 3vw, 2rem); margin: 0 0 1rem; }}
  .cover p {{ max-width: 62ch; color: var(--ink-soft); font-size: 1.02rem; line-height: 1.6; }}
  .cover .meta-row {{ display: flex; gap: 1.6rem; flex-wrap: wrap; margin-top: 1.8rem; padding-top: 1.4rem; border-top: 1px solid var(--rule); font-family: 'Space Mono', monospace; font-size: 0.72rem; color: var(--ink-soft); }}
  .cover .meta-row b {{ color: var(--ink); font-weight: 400; }}

  section {{ margin-bottom: 5rem; padding-top: 3rem; border-top: 1px solid var(--rule); }}
  .sec-num {{ font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--rust-text); letter-spacing: 0.1em; margin-bottom: 0.5rem; }}
  h2 {{ font-family: 'Courier Prime', monospace; font-weight: 700; font-size: clamp(1.5rem, 2.6vw, 2rem); margin: 0 0 1.2rem; }}
  h3 {{ font-family: 'IBM Plex Sans', sans-serif; font-weight: 600; font-size: 1.02rem; margin: 2rem 0 0.7rem; }}
  h3:first-of-type {{ margin-top: 0; }}
  p {{ font-size: 0.98rem; line-height: 1.65; color: var(--ink-soft); max-width: 68ch; margin: 0 0 1rem; }}
  p b {{ color: var(--ink); font-weight: 600; }}

  .principles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: 1.2rem; margin-top: 1.4rem; }}
  .principle {{ background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px; padding: 1.2rem 1.3rem; }}
  .principle .k {{ font-family: 'Space Mono', monospace; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--rust-text); margin-bottom: 0.5rem; display: block; }}
  .principle h4 {{ margin: 0 0 0.5rem; font-size: 0.98rem; font-weight: 600; }}
  .principle p {{ font-size: 0.88rem; margin: 0; }}

  .dodont {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem; }}
  @media (max-width: 700px) {{ .dodont {{ grid-template-columns: 1fr; }} }}
  .dodont .box {{ border-radius: 12px; padding: 1rem 1.2rem; font-size: 0.88rem; }}
  .dodont .do {{ background: rgba(62,124,116,0.08); border: 1px solid rgba(62,124,116,0.3); }}
  .dodont .dont {{ background: rgba(180,85,47,0.06); border: 1px solid rgba(180,85,47,0.28); }}
  .dodont .tag {{ font-family: 'Space Mono', monospace; font-size: 0.66rem; letter-spacing: 0.08em; text-transform: uppercase; display: block; margin-bottom: 0.5rem; }}
  .dodont .do .tag {{ color: var(--teal-text); }}
  .dodont .dont .tag {{ color: var(--rust-text); }}
  .dodont .line {{ font-family: 'IBM Plex Sans', sans-serif; color: var(--ink); margin: 0.3rem 0; }}

  .logo-stage {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.4rem; margin: 1.4rem 0 2rem; }}
  @media (max-width: 700px) {{ .logo-stage {{ grid-template-columns: 1fr; }} }}
  .logo-card {{ background: var(--paper-2); border: 1px solid var(--rule); border-radius: 14px; padding: 2rem; display: flex; flex-direction: column; align-items: center; gap: 1rem; }}
  .logo-card svg {{ width: 220px; height: auto; }}
  .logo-card.mono svg {{ width: 100px; }}
  .logo-card .cap {{ font-family: 'Space Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-soft); text-align: center; }}

  .clearspace {{ position: relative; background: var(--paper-2); border: 1px dashed var(--rule); border-radius: 14px; padding: 2.4rem; display: flex; align-items: center; justify-content: center; margin: 1.4rem 0 2rem; }}
  .clearspace .inner {{ position: relative; padding: 1.6em; border: 1px dashed var(--rust-soft); }}
  .clearspace .inner svg {{ width: 200px; height: auto; display: block; }}
  .clearspace .inner::after {{ content: "clear space = height of lowercase 's'"; position: absolute; bottom: -1.8rem; left: 50%; transform: translateX(-50%); white-space: nowrap; font-family: 'Space Mono', monospace; font-size: 0.62rem; color: var(--ink-soft); }}

  .swatch-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px,1fr)); gap: 1rem; margin: 1.4rem 0 2rem; }}
  .swatch {{ border-radius: 12px; overflow: hidden; border: 1px solid var(--rule); }}
  .swatch .chip {{ height: 88px; }}
  .swatch .info {{ background: var(--paper-2); padding: 0.8rem 1rem; }}
  .swatch .name {{ font-weight: 600; font-size: 0.88rem; margin-bottom: 0.15rem; }}
  .swatch .hex {{ font-family: 'Space Mono', monospace; font-size: 0.76rem; color: var(--ink-soft); }}
  .swatch .role {{ font-size: 0.78rem; color: var(--ink-soft); margin-top: 0.4rem; line-height: 1.4; }}

  .type-row {{ display: flex; flex-direction: column; gap: 1.6rem; margin: 1.4rem 0 2rem; }}
  .type-item {{ background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px; padding: 1.4rem 1.6rem; }}
  .type-item .role-tag {{ font-family: 'Space Mono', monospace; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--rust-text); margin-bottom: 0.6rem; display: block; }}
  .type-item .sample {{ font-size: 1.9rem; line-height: 1.2; margin-bottom: 0.5rem; }}
  .type-item .meta {{ font-family: 'Space Mono', monospace; font-size: 0.74rem; color: var(--ink-soft); }}
  .courier {{ font-family: 'Courier Prime', monospace; font-weight: 700; }}
  .plex {{ font-family: 'IBM Plex Sans', sans-serif; }}
  .plex.semi {{ font-weight: 600; }}
  .mono {{ font-family: 'Space Mono', monospace; }}

  .scale-table {{ width: 100%; border-collapse: collapse; margin-top: 0.6rem; font-size: 0.86rem; }}
  .scale-table th, .scale-table td {{ text-align: left; padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--rule); }}
  .scale-table th {{ font-family: 'Space Mono', monospace; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-soft); }}
  .scale-table td.num {{ font-family: 'Space Mono', monospace; font-variant-numeric: tabular-nums; }}

  .motif-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap: 1rem; margin: 1.4rem 0 2rem; }}
  .motif {{ background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px; padding: 1.2rem; }}
  .motif .swimg {{ height: 70px; border-radius: 8px; margin-bottom: 0.8rem; border: 1px solid var(--rule); }}
  .motif h4 {{ margin: 0 0 0.4rem; font-size: 0.92rem; }}
  .motif p {{ margin: 0; font-size: 0.82rem; }}

  .apply-table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.86rem; background: var(--paper-2); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; }}
  .apply-table th, .apply-table td {{ text-align: left; padding: 0.75rem 0.9rem; border-bottom: 1px solid var(--rule); vertical-align: top; }}
  .apply-table th {{ font-family: 'Space Mono', monospace; font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-soft); background: var(--paper); }}
  .apply-table tr:last-child td {{ border-bottom: none; }}
  .table-scroll {{ overflow-x: auto; border-radius: 10px; }}

  .filelist {{ background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px; padding: 1.4rem 1.6rem; margin-top: 1rem; }}
  .filelist .row {{ display: flex; justify-content: space-between; gap: 1rem; padding: 0.5rem 0; border-bottom: 1px solid var(--rule); font-size: 0.86rem; }}
  .filelist .row:last-child {{ border-bottom: none; }}
  .filelist .path {{ font-family: 'Space Mono', monospace; color: var(--ink); }}
  .filelist .status {{ font-family: 'Space Mono', monospace; font-size: 0.7rem; color: var(--ink-soft); white-space: nowrap; }}
  .filelist .status.done {{ color: var(--teal-text); }}
  .filelist .status.next {{ color: var(--rust-text); }}

  footer {{ max-width: 68ch; }}
</style>

<div class="wrap">

  <div class="cover">
    <p class="eyebrow">Brand Guide — v1.0</p>
    <div class="wordmark-slot">{WORDMARK_INK}</div>
    <h1>The Field Notes system, written down.</h1>
    <p>This is the reference for everything Stroll &amp; Savor puts into the world — logo, color, type, texture, voice — and how each piece behaves differently across static brand assets (profile pictures, banners, the website) versus the monthly generated content (the Spontaneous Escapes artifact, carousel, and story graphics). Built on the Field Notes direction: a researcher's travel notebook, not an airline ad.</p>
    <div class="meta-row">
      <span><b>Persona</b> — The Deliberate Collector</span>
      <span><b>Direction</b> — Field Notes</span>
      <span><b>Logo</b> — Field Mark + companion monogram</span>
    </div>
  </div>

  <section>
    <p class="sec-num">01</p>
    <h2>Foundation</h2>

    <h3>Who this is for</h3>
    <p>Late 20s to mid-50s, skews male, works in a field that rewards systems-thinking — finance, engineering, tech, consulting. Treats a miles balance like a portfolio: researched, tracked, optimized. Reads FlyerTalk and r/churning, not just Instagram. Distrusts glossy "luxury travel" marketing but will screenshot a well-formatted deal table without hesitation. The trip matters less than proof the strategy worked. Every design and copy decision below should read as credible to that person first — everything else is secondary.</p>

    <h3>Voice principles</h3>
    <div class="principles">
      <div class="principle">
        <span class="k">01</span>
        <h4>Numbers do the persuading</h4>
        <p>Lead with miles, taxes, dates, percentage saved. Adjectives ("incredible," "unmissable") are a tell that the numbers aren't good enough to stand alone.</p>
      </div>
      <div class="principle">
        <span class="k">02</span>
        <h4>Write like a field note, not an ad</h4>
        <p>Short, declarative, slightly clipped. Present tense. It's a record of something found, not a pitch for something sold.</p>
      </div>
      <div class="principle">
        <span class="k">03</span>
        <h4>Precision over hype</h4>
        <p>Exact dates, exact routes, exact fare classes. "Business class deals" is vague; "SIN–NRT, Spontaneous Escapes, 100,500mi" is the actual content.</p>
      </div>
      <div class="principle">
        <span class="k">04</span>
        <h4>Respect the reader's intelligence</h4>
        <p>No exclamation points doing the excitement's job. No "you won't believe." If the deal is good, the number says so.</p>
      </div>
    </div>

    <div class="dodont">
      <div class="box do">
        <span class="tag">Do</span>
        <p class="line">"SIN → HND, Business, 100,500mi + S$92. Available Aug 3, 7, 12, 18, 24, 29."</p>
      </div>
      <div class="box dont">
        <span class="tag">Don't</span>
        <p class="line">"You won't BELIEVE this incredible business class deal to Tokyo!! 😱✈️"</p>
      </div>
    </div>
  </section>

  <section>
    <p class="sec-num">02</p>
    <h2>Logo</h2>
    <p>Two marks, two jobs. The <b>wordmark</b> is the primary logo — use it anywhere there's room to set it in full. The <b>monogram</b> is the avatar-only mark — small, circular, or square surfaces only. They are not interchangeable; using the wordmark somewhere it gets crushed into a circle, or the monogram somewhere it could be the full name, both read as a mistake.</p>

    <div class="logo-stage">
      <div class="logo-card">
        {WORDMARK_INK}
        <span class="cap">Wordmark — website header, banners, long-form content</span>
      </div>
      <div class="logo-card mono">
        {MONOGRAM_INK}
        <span class="cap">Monogram — profile pictures, favicons, app icons</span>
      </div>
    </div>

    <h3>Clear space &amp; minimum size</h3>
    <div class="clearspace">
      <div class="inner">{MONOGRAM_INK}</div>
    </div>
    <p>Keep clear space around either mark equal to at least the height of the lowercase "s" on every side — don't crowd it against edges, text, or other logos. Never run the wordmark narrower than ~120px on screen, or the monogram smaller than ~24px (below that, both blur into noise; a single "s" fallback is documented in the master file README for anything smaller).</p>

    <h3>Rules</h3>
    <div class="dodont">
      <div class="box do">
        <span class="tag">Do</span>
        <p class="line">Use the transparent SVG/PNG variants and let the destination's own background show through.</p>
        <p class="line">Keep the ampersand in rust, always — it's the one fixed color accent in the mark.</p>
      </div>
      <div class="box dont">
        <span class="tag">Dont</span>
        <p class="line">Stretch, skew, rotate, drop-shadow, or outline either mark.</p>
        <p class="line">Recolor the wordmark or monogram outside ink/paper/rust.</p>
      </div>
    </div>
  </section>

  <section>
    <p class="sec-num">03</p>
    <h2>Color</h2>
    <p>Five tokens, no exceptions. Rust and teal are the only two colors allowed to carry meaning (discount/emphasis vs. secondary data) — nothing else in the system introduces a new hue.</p>

    <div class="swatch-row">
      <div class="swatch">
        <div class="chip" style="background:#f1f0ea"></div>
        <div class="info"><div class="name">Paper</div><div class="hex">#F1F0EA</div><div class="role">Base ground for nearly everything — dot-grid texture sits on top of this.</div></div>
      </div>
      <div class="swatch">
        <div class="chip" style="background:#2e2e2c"></div>
        <div class="info"><div class="name">Ink</div><div class="hex">#2E2E2C</div><div class="role">Primary text and the wordmark's default color. Also used as a dark background variant.</div></div>
      </div>
      <div class="swatch">
        <div class="chip" style="background:#b4552f"></div>
        <div class="info"><div class="name">Route Rust</div><div class="hex">#B4552F</div><div class="role">The one accent. Discounts, the logo's ampersand, anything that needs to be found first.</div></div>
      </div>
      <div class="swatch">
        <div class="chip" style="background:#3e7c74"></div>
        <div class="info"><div class="name">Map Teal</div><div class="hex">#3E7C74</div><div class="role">Secondary data color — miles figures, links, anything that's informative but not the headline number.</div></div>
      </div>
      <div class="swatch">
        <div class="chip" style="background:#d7d5c8"></div>
        <div class="info"><div class="name">Grid Dot</div><div class="hex">#D7D5C8</div><div class="role">Hairlines, dividers, the dot-grid texture itself. Never used as a text color.</div></div>
      </div>
    </div>

    <h3>Pairing</h3>
    <p>Ink on paper is the default for all body copy — it's the highest-contrast, most-used pairing in the system. Rust and teal both sit on paper for accents/data, never as large background fills (they're too saturated to read as calm at that scale). Paper-on-ink is the only sanctioned inversion, reserved for dark UI moments (splash states, video end cards) — don't invert to rust or teal backgrounds.</p>

    <h3>Text-safe variants</h3>
    <p>Route Rust and Map Teal at full strength are <b>4.3:1</b> and <b>4.2:1</b> against paper — enough for large type (a headline, the logo's ampersand) but just under WCAG AA's 4.5:1 floor for small text. Anywhere either color sets small text directly — eyebrows, section numbers, tags, status labels — use the darkened text-safe pair below instead. Same hue, same role, just legible at caption size.</p>
    <div class="swatch-row">
      <div class="swatch">
        <div class="chip" style="background:#994827"></div>
        <div class="info"><div class="name">Rust (text-safe)</div><div class="hex">#994827</div><div class="role">5.6:1 on paper. Use for any rust text below ~18px.</div></div>
      </div>
      <div class="swatch">
        <div class="chip" style="background:#346962"></div>
        <div class="info"><div class="name">Teal (text-safe)</div><div class="hex">#346962</div><div class="role">5.5:1 on paper. Use for any teal text below ~18px.</div></div>
      </div>
    </div>
  </section>

  <section>
    <p class="sec-num">04</p>
    <h2>Typography</h2>
    <p>Three typefaces, three jobs, never swapped. If a design needs a fourth role, it's using one of these three wrong, not missing a font.</p>

    <div class="type-row">
      <div class="type-item">
        <span class="role-tag">Display / headlines — Courier Prime Bold</span>
        <div class="sample courier">stroll &amp; savor</div>
        <div class="meta">Typewriter cadence, field-journal honesty. Route names, section headers, anything acting as a masthead.</div>
      </div>
      <div class="type-item">
        <span class="role-tag">Body — IBM Plex Sans</span>
        <div class="sample plex">Available this month: Aug 3, 7, 12, 18, 24, 29.</div>
        <div class="meta">Everything the reader actually reads at length — captions, descriptions, this guide. 600 weight for emphasis/subheads within body copy.</div>
      </div>
      <div class="type-item">
        <span class="role-tag">Data — Space Mono</span>
        <div class="sample mono">100,500 mi · &minus;23% vs Saver</div>
        <div class="meta">Miles, taxes, dates, percentages, ticket-style labels — anything that's a number or reads like a stamped code.</div>
      </div>
    </div>

    <h3>Scale</h3>
    <div class="table-scroll">
    <table class="scale-table">
      <thead><tr><th>Role</th><th>Typeface / weight</th><th>Size (web)</th><th>Use</th></tr></thead>
      <tbody>
        <tr><td>H1 / cover headline</td><td>Courier Prime 700</td><td class="num">32&ndash;48px</td><td>Page titles, artifact mastheads</td></tr>
        <tr><td>H2 / section</td><td>Courier Prime 700</td><td class="num">24&ndash;32px</td><td>Section breaks</td></tr>
        <tr><td>Subhead</td><td>Plex Sans 600</td><td class="num">15&ndash;17px</td><td>In-body emphasis, card titles</td></tr>
        <tr><td>Body</td><td>Plex Sans 400</td><td class="num">15&ndash;16px</td><td>Running text</td></tr>
        <tr><td>Data / label</td><td>Space Mono 400</td><td class="num">11&ndash;18px</td><td>Miles, dates, tags, captions</td></tr>
      </tbody>
    </table>
    </div>
  </section>

  <section>
    <p class="sec-num">05</p>
    <h2>Texture &amp; motifs</h2>
    <p>The system has three recurring graphic devices beyond logo/color/type. Used consistently, they're what makes a card recognizable as Stroll &amp; Savor before you've read a word of it.</p>

    <div class="motif-grid">
      <div class="motif">
        <div class="swimg" style="background:#f1f0ea;background-image:radial-gradient(circle, rgba(46,46,44,0.18) 1.5px, transparent 1.5px);background-size:16px 16px;"></div>
        <h4>Dot-grid</h4>
        <p>16&ndash;18px spacing, low opacity. Background texture only &mdash; never behind dense text blocks where it'd fight legibility.</p>
      </div>
      <div class="motif">
        <div class="swimg" style="background:var(--paper-2);border-top:2px dashed #b4552f;display:flex;align-items:center;justify-content:center;"><span class="mono" style="font-size:0.7rem;color:#6d6a5f">dashed rule</span></div>
        <h4>Dashed dividers</h4>
        <p>Separates a headline from its data (route from miles/dates). Reads as a tear-off line, not decoration.</p>
      </div>
      <div class="motif">
        <div class="swimg" style="background:var(--paper-2);display:flex;align-items:center;justify-content:center;">
          <svg width="90" height="30" viewBox="0 0 90 30"><path d="M4 15 C25 15 20 25 45 15 C65 7 70 20 86 15" fill="none" stroke="#b4552f" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0.2 5"/></svg>
        </div>
        <h4>Route line</h4>
        <p>A dotted path, always rust, always with intent (an actual route/journey) &mdash; never a generic squiggle for decoration's sake.</p>
      </div>
    </div>
  </section>

  <section>
    <p class="sec-num">06</p>
    <h2>Applying the system</h2>
    <p>Static brand assets and the monthly generated content share every token above, but lean on different pieces of it — a profile picture has one job (be recognizable at 32px), a carousel slide has a different one (stop a scroll, then hold up to a close read).</p>

    <div class="table-scroll">
    <table class="apply-table">
      <thead><tr><th>Surface</th><th>Primary mark</th><th>Type emphasis</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Profile picture / favicon</td><td>Monogram</td><td>&mdash;</td><td>No text beyond the mark itself; relies on ink/rust contrast at small size.</td></tr>
        <tr><td>Website header / banner</td><td>Wordmark</td><td>Courier Prime</td><td>Full lockup, generous clear space, paper background.</td></tr>
        <tr><td>Monthly web artifact</td><td>Wordmark (masthead)</td><td>Courier Prime headline, Plex body</td><td>Full three-typeface system, dot-grid texture throughout.</td></tr>
        <tr><td>Carousel slides</td><td>Monogram or none</td><td>Space Mono for miles/dates, Courier Prime for route</td><td>Minimal &amp; punchy per the content brief &mdash; top deals only, heaviest use of the route-line motif.</td></tr>
        <tr><td>Story / Reel graphic</td><td>Monogram, small corner mark</td><td>Space Mono-forward</td><td>Vertical, single deal per frame, largest type sizes in the system.</td></tr>
        <tr><td>Long-form infographic</td><td>Wordmark at top</td><td>Full scale, most text-dense surface</td><td>Closest to the web artifact's density, built for a static share.</td></tr>
      </tbody>
    </table>
    </div>
  </section>

  <section>
    <p class="sec-num">07</p>
    <h2>File reference</h2>
    <p>Where each piece of this system actually lives.</p>
    <div class="filelist">
      <div class="row"><span class="path">stroll-savor-logo-master.zip</span><span class="status done">Delivered</span></div>
      <div class="row"><span class="path">This brand guide (Field Notes v1.0)</span><span class="status done">This document</span></div>
      <div class="row"><span class="path">stroll-savor-platform-assets.zip (avatars + banners)</span><span class="status done">Delivered</span></div>
      <div class="row"><span class="path">Website favicon set, OG image</span><span class="status done">Delivered — in platform-assets.zip</span></div>
      <div class="row"><span class="path">Website CSS tokens &amp; style instructions</span><span class="status next">Next</span></div>
      <div class="row"><span class="path">Monthly artifact / carousel / story templates</span><span class="status next">Queued</span></div>
    </div>
  </section>

  <footer>
    <p>This is v1.0 &mdash; expect it to firm up once the per-platform assets and website are built against it and any edge cases surface. Treat it as the source of truth over any individual asset if the two ever disagree.</p>
  </footer>

</div>
"""

out = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/stroll-savor-ci-guide.html")
out.write_text(html)
print("wrote", out, len(html), "chars")
