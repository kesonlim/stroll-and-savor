"""Individual airline glossary page: /airlines/<slug>/. Structured facts +
one short genuine editorial paragraph per docs/growth-plan.md's
depth-per-page policy."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "scripts"))
from brand import MONOGRAM_INK, ROUTE_LINE_SVG  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402

ASSET_PREFIX = "../../"

STYLE = """
  main { max-width: 760px; margin: 0 auto; padding: 3rem 1.75rem 6rem; }
  .eyebrow { font-family: var(--font-data); font-size: 0.76rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--rust-text); display: block; margin-bottom: 0.8rem; }
  main h1 { margin: 0 0 0.6rem; }
  .subline { font-family: var(--font-data); font-size: 0.88rem; color: var(--ink-soft); }
  .route-line-motif { margin: 1.6rem 0 2rem; }
  .route-line-motif svg { width: 180px; height: auto; }

  .facts-table { width: 100%; border-collapse: collapse; margin: 2rem 0; }
  .facts-table tr { border-bottom: 1px solid var(--rule); }
  .facts-table tr:last-child { border-bottom: none; }
  .facts-table th, .facts-table td { text-align: left; padding: 0.7rem 0; font-size: 0.9rem; }
  .facts-table th { font-family: var(--font-data); font-weight: 400; color: var(--ink-soft); width: 40%; }
  .facts-table td { font-family: var(--font-body); }
  .facts-table a { color: var(--teal-text); }

  .blurb { font-size: 1rem; line-height: 1.7; max-width: 62ch; }
  .back-link { display: inline-block; margin-top: 2.5rem; font-family: var(--font-data);
    font-size: 0.82rem; color: var(--ink-soft); text-decoration: none; }
  .back-link:hover { color: var(--rust-text); }
"""


def render(entry: dict) -> str:
    body = f"""
    <main>
      <span class="eyebrow">Airlines &middot; Star Alliance</span>
      <h1>{entry['name']}</h1>
      <span class="subline">{entry['iata']} &middot; Star Alliance member since {entry['star_alliance_joined']} &middot; hub: {entry['hub']}</span>
      <div class="route-line-motif">{ROUTE_LINE_SVG}</div>

      <p class="blurb">{entry['blurb']}</p>

      <table class="facts-table">
        <tr><th>IATA code</th><td>{entry['iata']}</td></tr>
        <tr><th>Alliance</th><td>Star Alliance (member since {entry['star_alliance_joined']})</td></tr>
        <tr><th>Hub</th><td>{entry['hub']}</td></tr>
        <tr><th>Changi check-in</th><td>{entry['changi_terminal']}</td></tr>
        <tr><th>Official site</th><td><a href="{entry['website']}" rel="noopener" target="_blank">{entry['website'].replace('https://', '').replace('http://', '').rstrip('/')}</a></td></tr>
      </table>

      <a class="back-link" href="../">&larr; All airlines</a>
    </main>"""
    return page(
        title=f"{entry['name']} — Stroll & Savor",
        description=f"{entry['name']} ({entry['iata']}), Star Alliance member since {entry['star_alliance_joined']}, hubbed at {entry['hub']}.",
        body=body,
        asset_prefix=ASSET_PREFIX,
        extra_style=STYLE,
    )
