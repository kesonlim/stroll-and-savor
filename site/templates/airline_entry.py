"""Individual airline glossary page: /airlines/<slug>/. Structured facts +
one short genuine editorial paragraph per docs/growth-plan.md's
depth-per-page policy."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "content" / "scripts"))
from brand import MONOGRAM_INK, ROUTE_LINE_SVG  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import image_provider  # noqa: E402

ASSET_PREFIX = "../../"

STYLE = """
  main { max-width: 760px; margin: 0 auto; padding: 3rem 1.75rem 6rem; }
  .eyebrow { font-family: var(--font-data); font-size: 0.76rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--rust-text); display: block; margin-bottom: 0.8rem; }
  main h1 { margin: 0 0 0.6rem; }
  .subline { font-family: var(--font-data); font-size: 0.88rem; color: var(--ink-soft); }
  .airline-hero {
    margin: 1.8rem 0 2rem; border-radius: 14px; overflow: hidden;
    border: 1px solid var(--rule); position: relative; background: #e2dfd6;
  }
  .airline-hero img {
    width: 100%; height: auto; max-height: 320px; object-fit: cover; display: block;
  }
  .airline-hero .caption {
    position: absolute; bottom: 0; left: 0; right: 0;
    background: linear-gradient(transparent, rgba(12,19,34,0.8));
    padding: 1.1rem 1.4rem; color: #fff; display: flex;
    justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 0.5rem;
  }
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
    alliance_line = (
        f"{entry['alliance']} member since {entry['alliance_joined']}"
        if entry.get("alliance_joined") else f"{entry['alliance']} member"
    )
    alliance_fact = (
        f"{entry['alliance']} (member since {entry['alliance_joined']})"
        if entry.get("alliance_joined") else entry["alliance"]
    )

    hero_img = image_provider.resolve_image(entry.get("hub", entry["name"]), width=1100)

    body = f"""
    <main>
      <span class="eyebrow">Airlines &middot; {entry['alliance']}</span>
      <h1>{entry['name']}</h1>
      <span class="subline">{entry['iata']} &middot; {alliance_line} &middot; hub: {entry['hub']}</span>
      
      <div class="airline-hero">
        <img src="{hero_img['url']}" alt="{hero_img['alt']}" width="1100" height="320" loading="eager">
        <div class="caption">
          <span style="font-family:var(--font-data); font-size:0.75rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--brass); font-weight:700;">Hub &bull; {entry['hub']}</span>
          <span style="font-family:var(--font-data); font-size:0.68rem; color:rgba(255,255,255,0.75);">Photo by {hero_img['photographer']} &bull; Unsplash</span>
        </div>
      </div>

      <div class="route-line-motif">{ROUTE_LINE_SVG}</div>

      <p class="blurb">{entry['blurb']}</p>

      <table class="facts-table">
        <tr><th>IATA code</th><td>{entry['iata']}</td></tr>
        <tr><th>Alliance</th><td>{alliance_fact}</td></tr>
        <tr><th>Hub</th><td>{entry['hub']}</td></tr>
        <tr><th>Changi check-in</th><td>{entry['changi_terminal']}</td></tr>
        <tr><th>Official site</th><td><a href="{entry['website']}" rel="noopener" target="_blank">{entry['website'].replace('https://', '').replace('http://', '').rstrip('/')}</a></td></tr>
      </table>

      <a class="back-link" href="../">&larr; All airlines</a>
    </main>"""

    url_path = f"airlines/{entry['slug']}/"
    airline_json_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": entry["name"],
        "identifier": entry["iata"],
        "url": entry["website"],
        "sameAs": [entry["website"]],
    }

    return page(
        title=f"{entry['name']} — Stroll & Savor",
        description=f"{entry['name']} ({entry['iata']}), {alliance_line}, hubbed at {entry['hub']}.",
        body=body,
        asset_prefix=ASSET_PREFIX,
        extra_style=STYLE,
        og_image=hero_img["url"],
        url_path=url_path,
        og_type="website",
        breadcrumbs=[("Home", ""), ("Airlines", "airlines/"), (entry["name"], url_path)],
        json_ld_extra=[airline_json_ld],
    )
