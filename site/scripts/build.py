"""Builds the full static site into site/dist/ from scraper/samples/*.json.
Usage: python3 site/scripts/build.py

Site IA (docs/growth-plan.md): root is a brand-general landing page;
Singapore Airlines Spontaneous Escapes content lives under
/singapore-airlines/spontaneous-escapes/.
"""
import datetime
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "site" / "templates"))
sys.path.insert(0, str(REPO_ROOT / "content" / "templates"))
sys.path.insert(0, str(REPO_ROOT / "content" / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "airlines" / "data"))

import landing  # noqa: E402
import spontaneous_escapes  # noqa: E402
import monthly_post  # noqa: E402
import airlines_index  # noqa: E402
import airline_entry  # noqa: E402
from chrome import SITE_URL  # noqa: E402
from web_artifact import month_label, SOURCE_LABEL  # noqa: E402
from entries import build_entries as build_airline_entries  # noqa: E402

DIST = REPO_ROOT / "site" / "dist"
BRAND = REPO_ROOT / "brand"
SE_PATH = "singapore-airlines/spontaneous-escapes"


def post_meta(data: dict) -> dict:
    label = month_label(data["travel_month"])
    source = SOURCE_LABEL.get(data.get("source"), data.get("source", "the source"))
    return {
        "slug": data["travel_month"],
        "eyebrow": f"Spontaneous Escapes — {label}",
        "title": f"{data.get('discount_pct', 30)}% off Saver Awards, business class",
        "meta": f"{len(data['deals'])} fares · book by {data['booking_window']['end']} · via {source}",
        "data": data,
    }


def copy_assets():
    assets_dir = DIST / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(BRAND / "website-style-guide.css", assets_dir / "style.css")
    fonts_src = BRAND / "fonts"
    fonts_dst = assets_dir / "fonts"
    if fonts_dst.exists():
        shutil.rmtree(fonts_dst)
    shutil.copytree(fonts_src, fonts_dst)
    favicon = BRAND / "logo-master" / "favicon.ico"
    if favicon.exists():
        shutil.copy(favicon, assets_dir / "favicon.ico")


def write_sitemap(url_paths: list):
    today = datetime.date.today().isoformat()
    urls_xml = "\n".join(
        f"  <url><loc>{SITE_URL}/{p}</loc><lastmod>{today}</lastmod></url>"
        for p in url_paths
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls_xml}\n"
        "</urlset>\n"
    )
    (DIST / "sitemap.xml").write_text(sitemap)


def write_robots():
    # Deliberately permissive -- docs/seo-standards.md: this project wants
    # maximum legitimate discoverability, the opposite of sites that block
    # AI crawlers. Allow-all covers GPTBot/ClaudeBot/PerplexityBot/etc.
    # without tracking every crawler's exact UA string.
    (DIST / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )


def write_llms_txt(posts: list, airline_entries: list):
    latest = posts[0]
    airline_lines = "\n".join(
        f"- [{e['name']}]({SITE_URL}/airlines/{e['slug']}/) ({e['iata']}, {e['alliance']})"
        for e in airline_entries
    )
    content = f"""# Stroll & Savor

> Independent tracker of travel deals and airline loyalty programs worth paying attention to, starting with Singapore Airlines KrisFlyer Spontaneous Escapes. Not affiliated with any airline, hotel, or attraction covered. Voice: numbers first, no hype -- exact routes, exact fare classes, no unverifiable claims.

## Singapore Airlines Spontaneous Escapes

Monthly business-class award fare list (30% off Saver Awards), published as close to Singapore Airlines' own reveal as possible.

- [Spontaneous Escapes tracker]({SITE_URL}/singapore-airlines/spontaneous-escapes/) -- section index, all months
- Latest: [{latest['title']}]({SITE_URL}/{SE_PATH}/{latest['slug']}/) -- {latest['meta']}

## Airlines glossary

{len(airline_entries)} airlines flying to/from Singapore Changi, covering Star Alliance, oneworld, and SkyTeam members so far (~86 airlines serve Changi in total; more coverage planned). Each entry: IATA code, alliance, hub, Changi check-in terminal, official site.

- [Airlines index]({SITE_URL}/airlines/)
{airline_lines}

## Notes for automated readers

- All content is static, server-rendered HTML -- no JavaScript required to read any page.
- Every page carries schema.org JSON-LD (Organization, BreadcrumbList, and Article/Organization as appropriate).
- Data sourcing: scraper/ and airlines/data/ in the source repo (github.com/kesonlim/stroll-and-savor) document exactly where each fact came from and when it was retrieved.
"""
    (DIST / "llms.txt").write_text(content)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    copy_assets()

    url_paths = [""]

    samples_dir = REPO_ROOT / "scraper" / "samples"
    sample_files = sorted(samples_dir.glob("*.json"), reverse=True)  # newest travel_month first
    if not sample_files:
        raise SystemExit("No scraper/samples/*.json found -- nothing to build")

    posts = []
    for f in sample_files:
        data = json.loads(f.read_text())
        meta = post_meta(data)
        posts.append(meta)

        post_dir = DIST / SE_PATH / meta["slug"]
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / "index.html").write_text(monthly_post.render(data))
        url_paths.append(f"{SE_PATH}/{meta['slug']}/")
        print(f"wrote /{SE_PATH}/{meta['slug']}/")

    se_dir = DIST / SE_PATH
    se_dir.mkdir(parents=True, exist_ok=True)
    (se_dir / "index.html").write_text(spontaneous_escapes.render(posts))
    url_paths.append(f"{SE_PATH}/")
    print(f"wrote /{SE_PATH}/")

    airline_entries = build_airline_entries()

    (DIST / "index.html").write_text(landing.render(posts[0], airline_count=len(airline_entries)))
    print("wrote /")

    airlines_dir = DIST / "airlines"
    for e in airline_entries:
        entry_dir = airlines_dir / e["slug"]
        entry_dir.mkdir(parents=True, exist_ok=True)
        (entry_dir / "index.html").write_text(airline_entry.render(e))
        url_paths.append(f"airlines/{e['slug']}/")
    (airlines_dir / "index.html").write_text(airlines_index.render(airline_entries))
    url_paths.append("airlines/")
    print(f"wrote /airlines/ ({len(airline_entries)} entries)")

    write_sitemap(url_paths)
    write_robots()
    write_llms_txt(posts, airline_entries)
    print(f"wrote /sitemap.xml, /robots.txt, /llms.txt ({len(url_paths)} URLs)")

    print(f"\nSite built at {DIST}")


if __name__ == "__main__":
    main()
