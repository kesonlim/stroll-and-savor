import base64, pathlib

d = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/fonts")

def b64(name):
    return (d / f"{name}.b64").read_text().strip()

PLEXSANS = b64("plexsans")
SPACEMONO = b64("spacemono")
COURIER = b64("courier_prime")

html = f"""<title>Stroll &amp; Savor — Logo Directions</title>
<style>
  @font-face {{ font-family: 'IBM Plex Sans'; src: url(data:font/woff2;base64,{PLEXSANS}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Space Mono'; src: url(data:font/woff2;base64,{SPACEMONO}) format('woff2'); font-weight: 400; font-display: swap; }}
  @font-face {{ font-family: 'Courier Prime'; src: url(data:font/woff2;base64,{COURIER}) format('woff2'); font-weight: 700; font-display: swap; }}

  :root {{
    --paper: #f1f0ea;
    --paper-2: #faf9f5;
    --ink: #2e2e2c;
    --ink-soft: #6d6a5f;
    --rule: #d7d5c8;
    --rust: #b4552f;
    --teal: #3e7c74;
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
    background-image: radial-gradient(circle, rgba(46,46,44,0.09) 1px, transparent 1px);
    background-size: 18px 18px;
  }}

  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 4rem 1.75rem 0; }}

  .eyebrow {{
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--rust);
    margin: 0 0 1rem;
  }}
  .intro h1 {{
    font-family: 'Courier Prime', monospace;
    font-weight: 700;
    font-size: clamp(2rem, 4vw, 2.9rem);
    line-height: 1.15;
    margin: 0 0 1.1rem;
    text-wrap: balance;
    max-width: 20ch;
  }}
  .intro p {{
    font-size: 1.02rem;
    line-height: 1.65;
    color: var(--ink-soft);
    margin: 0 0 0.6rem;
    max-width: 62ch;
  }}

  .locked {{
    display: flex; align-items: center; gap: 0.7rem;
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 100px;
    padding: 0.5rem 1rem; margin: 1.6rem 0 3.6rem; width: fit-content;
    font-family: 'Space Mono', monospace; font-size: 0.72rem; color: var(--ink-soft);
  }}
  .locked .dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--teal); }}
  .locked b {{ color: var(--ink); font-weight: 700; }}
  .locked .swb {{ display: inline-flex; gap: 3px; }}
  .locked .swb span {{ width: 12px; height: 12px; border-radius: 3px; }}

  .concept {{ margin-bottom: 5.5rem; padding-top: 3rem; border-top: 1px solid var(--rule); }}
  .concept:first-of-type {{ border-top: none; padding-top: 0; }}
  .c-num {{ font-family: 'Space Mono', monospace; font-size: 0.75rem; color: var(--ink-soft); letter-spacing: 0.1em; }}
  .c-name {{ font-size: clamp(1.7rem, 3vw, 2.3rem); margin: 0.2rem 0 0.5rem; font-family: 'Courier Prime', monospace; }}
  .c-desc {{ max-width: 56ch; color: var(--ink-soft); font-size: 0.97rem; line-height: 1.55; margin-bottom: 2.2rem; }}

  .stage {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.4rem;
    align-items: end;
  }}
  .tile {{
    background: var(--paper-2);
    border: 1px solid var(--rule);
    border-radius: 14px;
    padding: 1.2rem;
    display: flex; flex-direction: column; align-items: center; gap: 0.9rem;
  }}
  .tile .cap {{ font-family: 'Space Mono', monospace; font-size: 0.64rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-soft); text-align: center; }}

  .avatar {{
    width: 96px; height: 96px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    background: var(--paper); border: 1px solid var(--rule);
    overflow: hidden;
  }}
  .favicon-tab {{
    display: flex; align-items: center; gap: 0.5rem;
    background: #e7e5db; border-radius: 8px 8px 0 0; padding: 0.4rem 0.7rem 0.4rem 0.5rem;
    font-family: 'IBM Plex Sans'; font-size: 0.68rem; color: var(--ink-soft);
    border: 1px solid var(--rule); border-bottom: none;
  }}
  .favicon-tab .fav {{ width: 16px; height: 16px; flex-shrink: 0; }}
  .lockup {{
    display: flex; align-items: center; gap: 0.7rem;
    background: var(--paper); border: 1px solid var(--rule); border-radius: 10px;
    padding: 0.9rem 1.2rem; width: 100%;
  }}
  .lockup .mark {{ width: 34px; height: 34px; flex-shrink: 0; }}
  .lockup .word {{ font-family: 'Courier Prime', monospace; font-weight: 700; font-size: 1.05rem; color: var(--ink); white-space: nowrap; }}
  .lockup .word .amp {{ color: var(--rust); }}

  .wordmark-only {{ font-family: 'Courier Prime', monospace; font-weight: 700; font-size: 1.8rem; color: var(--ink); text-align: center; }}
  .wordmark-only .amp {{ color: var(--rust); }}
  .wordmark-only .dot {{ color: var(--teal); font-size: 0.6em; vertical-align: middle; }}

  .footer-note, .platform-table {{
    max-width: 900px; margin: 0 auto; padding: 0 1.75rem;
  }}
  .footer-note {{
    font-size: 0.92rem; line-height: 1.6; color: var(--ink-soft);
    border-top: 1px solid var(--rule); padding-top: 2rem; margin-top: 0;
    max-width: 760px;
  }}
  .footer-note b {{ color: var(--ink); }}

  .platform-table {{ margin-bottom: 4rem; }}
  .platform-table h2 {{ font-family: 'Courier Prime', monospace; font-size: 1.5rem; margin-bottom: 0.4rem; }}
  .platform-table > p {{ color: var(--ink-soft); font-size: 0.95rem; max-width: 62ch; margin-bottom: 1.6rem; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--paper-2); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; font-size: 0.86rem; }}
  .table-scroll {{ overflow-x: auto; border-radius: 10px; }}
  th, td {{ text-align: left; padding: 0.7rem 0.9rem; border-bottom: 1px solid var(--rule); white-space: nowrap; }}
  th {{ font-family: 'Space Mono', monospace; font-size: 0.68rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-soft); background: var(--paper); }}
  td.num {{ font-family: 'Space Mono', monospace; font-variant-numeric: tabular-nums; }}
  tr:last-child td {{ border-bottom: none; }}
  .flag {{ display: inline-block; margin-left: 0.4rem; font-family: 'Space Mono', monospace; font-size: 0.62rem; color: var(--rust); border: 1px solid var(--rust); border-radius: 4px; padding: 0.05rem 0.3rem; }}
</style>

<div class="wrap">
  <p class="eyebrow">Stroll &amp; Savor — Logo Exploration</p>
  <div class="intro">
    <h1>Four ways to mark a field notebook.</h1>
    <p>Built on the locked Field Notes system — dot-grid paper, pencil ink, route rust, map teal, Courier Prime for anything that has to act like a headline. Each concept is shown at the sizes it'll actually live at: a round profile picture, a browser-tab favicon, and a horizontal lockup for the website header and banners.</p>
  </div>
  <div class="locked">
    <span class="dot"></span> <b>Locked system:</b> Field Notes
    <span class="swb">
      <span style="background:#f1f0ea;border:1px solid #d7d5c8"></span>
      <span style="background:#2e2e2c"></span>
      <span style="background:#b4552f"></span>
      <span style="background:#3e7c74"></span>
    </span>
    Courier Prime / Plex Sans / Space Mono
  </div>

  <!-- A: Pure Wordmark -->
  <div class="concept">
    <div class="c-num">CONCEPT A / 04</div>
    <h2 class="c-name">Field Mark</h2>
    <p class="c-desc">Type, unadorned — lowercase Courier Prime, wide tracking, the ampersand pulled into rust so the two halves of the name read as distinct entries in the same notebook. No icon: relies entirely on the typewriter voice to be recognizable, the way a well-set masthead works without a crest.</p>
    <div class="stage">
      <div class="tile">
        <div class="avatar"><span class="wordmark-only" style="font-size:0.85rem;line-height:1.15">stroll<br><span class="amp">&amp;</span> savor</span></div>
        <div class="cap">Profile picture</div>
      </div>
      <div class="tile">
        <div class="favicon-tab">
          <svg class="fav" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#2e2e2c"/><text x="16" y="21" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="16" fill="#f1f0ea">s&amp;s</text></svg>
          strollandsavor.com
        </div>
        <div class="cap">Browser favicon</div>
      </div>
      <div class="tile" style="flex:1 1 260px">
        <div class="lockup"><span class="word">stroll <span class="amp">&amp;</span> savor</span></div>
        <div class="cap">Website header lockup</div>
      </div>
    </div>
  </div>

  <!-- B: Path Mark -->
  <div class="concept">
    <div class="c-num">CONCEPT B / 04</div>
    <h2 class="c-name">Trail Mark</h2>
    <p class="c-desc">A dotted trail that curls into an S and lands on a solid pin — the walk (stroll) ending at a place worth stopping (savor). Doubles as an icon on its own wherever the wordmark won't fit, and as the initial "S" whenever it's paired with type.</p>
    <div class="stage">
      <div class="tile">
        <div class="avatar">
          <svg viewBox="0 0 100 100" width="64" height="64">
            <path d="M30 22 C55 22 20 40 45 48 C70 56 35 72 62 78" fill="none" stroke="#b4552f" stroke-width="5" stroke-linecap="round" stroke-dasharray="0.5 11"/>
            <circle cx="62" cy="78" r="6" fill="#3e7c74"/>
          </svg>
        </div>
        <div class="cap">Profile picture</div>
      </div>
      <div class="tile">
        <div class="favicon-tab">
          <svg class="fav" viewBox="0 0 32 32">
            <rect width="32" height="32" rx="6" fill="#f1f0ea"/>
            <path d="M9 7 C18 7 7 13 15 15 C23 17 11 23 20 25" fill="none" stroke="#b4552f" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.2 3.6"/>
            <circle cx="20" cy="25" r="2.4" fill="#3e7c74"/>
          </svg>
          strollandsavor.com
        </div>
        <div class="cap">Browser favicon</div>
      </div>
      <div class="tile" style="flex:1 1 260px">
        <div class="lockup">
          <svg class="mark" viewBox="0 0 100 100"><path d="M30 22 C55 22 20 40 45 48 C70 56 35 72 62 78" fill="none" stroke="#b4552f" stroke-width="6" stroke-linecap="round" stroke-dasharray="0.5 12"/><circle cx="62" cy="78" r="7" fill="#3e7c74"/></svg>
          <span class="word">stroll <span class="amp">&amp;</span> savor</span>
        </div>
        <div class="cap">Website header lockup</div>
      </div>
    </div>
  </div>

  <!-- C: Stamp Monogram -->
  <div class="concept">
    <div class="c-num">CONCEPT C / 04</div>
    <h2 class="c-name">Field Stamp</h2>
    <p class="c-desc">A monogram inside a dashed rubber-stamp ring, with tick marks at the compass points like a surveyor's stamp — reads as something a well-used passport would collect. The strongest of the four at very small sizes (favicon, TikTok's circular crop) because it's a closed, contained shape.</p>
    <div class="stage">
      <div class="tile">
        <div class="avatar">
          <svg viewBox="0 0 100 100" width="72" height="72">
            <circle cx="50" cy="50" r="42" fill="none" stroke="#2e2e2c" stroke-width="2.5" stroke-dasharray="1 6" stroke-linecap="round"/>
            <line x1="50" y1="3" x2="50" y2="11" stroke="#b4552f" stroke-width="2.5"/>
            <line x1="50" y1="89" x2="50" y2="97" stroke="#b4552f" stroke-width="2.5"/>
            <line x1="3" y1="50" x2="11" y2="50" stroke="#b4552f" stroke-width="2.5"/>
            <line x1="89" y1="50" x2="97" y2="50" stroke="#b4552f" stroke-width="2.5"/>
            <text x="50" y="59" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="30" fill="#2e2e2c">S&amp;S</text>
          </svg>
        </div>
        <div class="cap">Profile picture</div>
      </div>
      <div class="tile">
        <div class="favicon-tab">
          <svg class="fav" viewBox="0 0 32 32">
            <circle cx="16" cy="16" r="14" fill="#f1f0ea" stroke="#2e2e2c" stroke-width="1" stroke-dasharray="0.4 2.4"/>
            <text x="16" y="21" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="12" fill="#b4552f">SS</text>
          </svg>
          strollandsavor.com
        </div>
        <div class="cap">Browser favicon</div>
      </div>
      <div class="tile" style="flex:1 1 260px">
        <div class="lockup">
          <svg class="mark" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="42" fill="none" stroke="#2e2e2c" stroke-width="3" stroke-dasharray="1 7" stroke-linecap="round"/>
            <text x="50" y="60" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="32" fill="#2e2e2c">S&amp;S</text>
          </svg>
          <span class="word">stroll <span class="amp">&amp;</span> savor</span>
        </div>
        <div class="cap">Website header lockup</div>
      </div>
    </div>
  </div>

  <!-- D: Standalone Icon (extracted from B) -->
  <div class="concept">
    <div class="c-num">CONCEPT D / 04</div>
    <h2 class="c-name">Waypoint</h2>
    <p class="c-desc">The pin from Concept B, standing alone as a pure app-icon mark — no wordmark dependency at all. Meant to pair with A's typeset wordmark for everyday use (icon for avatars, wordmark for headers) rather than compete with it, similar to how a lot of publications split "icon" and "logotype" into two separate assets.</p>
    <div class="stage">
      <div class="tile">
        <div class="avatar" style="background:#2e2e2c">
          <svg viewBox="0 0 100 100" width="56" height="56">
            <circle cx="50" cy="38" r="20" fill="none" stroke="#f1f0ea" stroke-width="6"/>
            <path d="M50 58 L50 88" stroke="#f1f0ea" stroke-width="6" stroke-linecap="round" stroke-dasharray="0.5 10"/>
            <circle cx="50" cy="38" r="7" fill="#b4552f"/>
          </svg>
        </div>
        <div class="cap">Profile picture (inverted)</div>
      </div>
      <div class="tile">
        <div class="favicon-tab">
          <svg class="fav" viewBox="0 0 32 32">
            <rect width="32" height="32" rx="6" fill="#2e2e2c"/>
            <circle cx="16" cy="12" r="6.5" fill="none" stroke="#f1f0ea" stroke-width="2"/>
            <path d="M16 18.5 L16 27" stroke="#f1f0ea" stroke-width="2" stroke-linecap="round" stroke-dasharray="0.2 3"/>
            <circle cx="16" cy="12" r="2.4" fill="#b4552f"/>
          </svg>
          strollandsavor.com
        </div>
        <div class="cap">Browser favicon</div>
      </div>
      <div class="tile" style="flex:1 1 260px">
        <div class="lockup" style="background:#2e2e2c">
          <svg class="mark" viewBox="0 0 100 100">
            <circle cx="50" cy="38" r="20" fill="none" stroke="#f1f0ea" stroke-width="7"/>
            <path d="M50 58 L50 88" stroke="#f1f0ea" stroke-width="7" stroke-linecap="round" stroke-dasharray="0.5 12"/>
            <circle cx="50" cy="38" r="8" fill="#b4552f"/>
          </svg>
          <span class="word" style="color:#f1f0ea">stroll <span class="amp" style="color:#e08a67">&amp;</span> savor</span>
        </div>
        <div class="cap">Dark lockup (app splash / banner overlay)</div>
      </div>
    </div>
  </div>

  <p class="footer-note">Pick one outright, or split roles the way D suggests — an icon mark for avatars/app icons and a wordmark for headers/banners don't have to be the same asset. Once a direction (or pairing) is picked, it becomes the master logo file set, and the corporate identity rollout below can start.</p>

  <div class="concept" style="margin-top:4.5rem;">
    <p class="section-locked-eyebrow" style="font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--teal);margin-bottom:0.6rem;">Locked</p>
    <div>
      <div class="c-num">FINAL SYSTEM</div>
      <h2 class="c-name">Field Mark — with a companion monogram</h2>
      <p class="c-desc">Concept A is the primary logo everywhere it can be set in full: website header, banners, long-form content, the carousel/story templates it already matches in voice. For the small circular contexts where two lines of type won't survive the crop — TikTok, Instagram, the browser favicon — a compact "s&amp;s" monogram in the same Courier Prime cuts in as the avatar-only mark. Same typeface, same restraint, no separate icon language to maintain.</p>
    </div>
    <div class="stage">
      <div class="tile">
        <div class="avatar"><span class="wordmark-only" style="font-size:1.4rem">s<span class="amp">&amp;</span>s</span></div>
        <div class="cap">Profile picture — monogram</div>
      </div>
      <div class="tile">
        <div class="favicon-tab">
          <svg class="fav" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#2e2e2c"/><text x="16" y="21" text-anchor="middle" font-family="Courier Prime, monospace" font-weight="700" font-size="15" fill="#f1f0ea">s&amp;s</text></svg>
          strollandsavor.com
        </div>
        <div class="cap">Browser favicon — monogram</div>
      </div>
      <div class="tile" style="flex:1 1 260px">
        <div class="lockup"><span class="word">stroll <span class="amp">&amp;</span> savor</span></div>
        <div class="cap">Website header — full wordmark</div>
      </div>
    </div>
  </div>

  <div class="platform-table" style="margin-top:4.5rem;">
    <h2>Where this logo actually has to fit</h2>
    <p>For the full CI rollout — profile pictures, banners, and website — each platform crops and displays differently. Reference sizes below; upload at the largest figure and let the platform downscale, never upscale a small export.</p>
    <div class="table-scroll">
    <table>
      <thead>
        <tr><th>Platform</th><th>Profile / avatar</th><th>Cover / banner</th><th>Notes</th></tr>
      </thead>
      <tbody>
        <tr><td>Facebook Page</td><td class="num">320×320 px (displays 170×170)</td><td class="num">820×312 px desktop / 640×360 mobile</td><td>Banner center-crops hardest on mobile — keep the mark centered.</td></tr>
        <tr><td>Instagram</td><td class="num">320×320 px (displays ~110×110, circular)</td><td class="num">n/a — Highlight covers 161×161 px if used</td><td>No banner slot; profile crop is a hard circle.</td></tr>
        <tr><td>TikTok</td><td class="num">200×200 px (circular)</td><td class="num">n/a</td><td>No banner; icon-only marks (C or D) read best here.</td></tr>
        <tr><td>YouTube</td><td class="num">800×800 px (circular)</td><td class="num">2560×1440 px, safe area 1546×423 centered</td><td>Banner safe area is the only zone visible on every device — keep logo/text inside it.</td></tr>
        <tr><td>LinkedIn (Company Page)</td><td class="num">300×300 px</td><td class="num">1128×191 px</td><td>Very short banner strip — a horizontal lockup (B/D) fits better than a stacked one.</td></tr>
        <tr><td>LinkedIn (Personal, if used)</td><td class="num">400×400 px</td><td class="num">1584×396 px</td><td>—</td></tr>
        <tr><td>Xiaohongshu (小红书)<span class="flag">verify</span></td><td class="num">≈300×300 px (circular)</td><td class="num">n/a</td><td>No official published spec — app-enforced crop, similar to Instagram in practice. Confirm inside the app closer to launch.</td></tr>
        <tr><td>Website (favicon)</td><td class="num">512×512 px master → 32×32 / 16×16</td><td class="num">OG/share image 1200×630 px</td><td>Master the icon at 512px and export down; a monogram or icon mark (C/D) survives 16px better than a wordmark.</td></tr>
      </tbody>
    </table>
    </div>
  </div>
</div>
"""

out = pathlib.Path("/tmp/claude-0/-home-user-kesonlim-github-com/3fd2b48e-d022-57fd-8d65-871181c56cb9/scratchpad/stroll-savor-logos.html")
out.write_text(html)
print("wrote", out, len(html), "chars")
