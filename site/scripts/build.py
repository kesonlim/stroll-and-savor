"""Builds the full static site into site/dist/ from scraper/samples/*.json.
Usage: python3 site/scripts/build.py

Site IA (docs/growth-plan.md): root is a brand-general landing page;
Singapore Airlines Spontaneous Escapes content lives under
/singapore-airlines/spontaneous-escapes/.
"""
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


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    copy_assets()

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
        print(f"wrote /{SE_PATH}/{meta['slug']}/")

    se_dir = DIST / SE_PATH
    se_dir.mkdir(parents=True, exist_ok=True)
    (se_dir / "index.html").write_text(spontaneous_escapes.render(posts))
    print(f"wrote /{SE_PATH}/")

    (DIST / "index.html").write_text(landing.render(posts[0]))
    print("wrote /")

    airline_entries = build_airline_entries()
    airlines_dir = DIST / "airlines"
    for e in airline_entries:
        entry_dir = airlines_dir / e["slug"]
        entry_dir.mkdir(parents=True, exist_ok=True)
        (entry_dir / "index.html").write_text(airline_entry.render(e))
    (airlines_dir / "index.html").write_text(airlines_index.render(airline_entries))
    print(f"wrote /airlines/ ({len(airline_entries)} entries)")

    print(f"\nSite built at {DIST}")


if __name__ == "__main__":
    main()
