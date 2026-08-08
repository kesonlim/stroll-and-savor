"""Generate the full set of monthly posts (web artifact, carousel, story
frames, captions) from a scraper extract. Usage:

    python3 content/scripts/generate.py scraper/samples/2026-08.json [--force]

Data/caption/HTML output (web artifact, captions) never needs a browser and
always gets written. PNG rendering (carousel/story images) needs a
Chromium-family browser (see render.find_browser) -- if none is found,
those steps are skipped with a clear note in the index rather than failing
the whole run, so this stays safe to call from an environment that may not
have a browser (e.g. the scheduled cloud routine, untested as of this
writing -- see content/README.md)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "templates"))

from curate import curate, REGION_ORDER, city_of  # noqa: E402
from render import render_html_to_png, find_browser, BrowserNotFoundError  # noqa: E402
import web_artifact  # noqa: E402
import carousel  # noqa: E402
import story  # noqa: E402
import captions  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def flatten_picks(picks: dict) -> list:
    flat = []
    for region in REGION_ORDER:
        for d in picks[region]:
            flat.append((d, region))
    return flat


def main(src_path: str, force: bool = False):
    src = Path(src_path)
    data = json.loads(src.read_text())
    travel_month = data["travel_month"]

    out_dir = REPO_ROOT / "content" / "posts" / travel_month
    if out_dir.exists() and not force:
        print(f"{out_dir} already exists -- nothing to do (pass --force to regenerate)")
        return
    carousel_dir = out_dir / "carousel"
    story_dir = out_dir / "story"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    story_dir.mkdir(parents=True, exist_ok=True)

    try:
        browser = find_browser()
        print(f"using browser: {browser}")
    except BrowserNotFoundError as e:
        browser = None
        print(f"WARNING: {e}\nWill still produce web-artifact.html and captions, but no PNGs this run.")

    picks = curate(data["deals"])
    flat = flatten_picks(picks)
    print(f"Curated {len(flat)} routes across {sum(1 for r in REGION_ORDER if picks[r])} regions")

    # Single source of truth for per-pick numbering/slugs, so a caption and
    # its matching image always share the same base filename regardless of
    # whether the image-rendering step ran this time.
    numbered = [(i, f"{i:02d}-{city_of(deal).lower().replace(' ', '-')}", deal, region)
                for i, (deal, region) in enumerate(flat, start=1)]

    # --- Web artifact (no browser needed) ---
    artifact_html = web_artifact.render(data)
    (out_dir / "web-artifact.html").write_text(artifact_html)
    print(f"wrote {out_dir / 'web-artifact.html'}")

    # --- Captions (no browser needed) ---
    (carousel_dir / "caption.txt").write_text(captions.carousel_caption(data, flat))
    for i, slug, deal, region in numbered:
        (story_dir / f"{slug}.caption.txt").write_text(captions.story_caption(deal, data))

    # --- Carousel + story PNGs (browser required) ---
    images_rendered = 0
    if browser:
        cover_html = carousel.cover_slide(data, len(flat))
        render_html_to_png(cover_html, carousel_dir / "00-cover.png", carousel.W, carousel.H)
        images_rendered += 1

        for i, slug, deal, region in numbered:
            html = carousel.deal_slide(deal, i, len(flat), region)
            render_html_to_png(html, carousel_dir / f"{i:02d}-deal.png", carousel.W, carousel.H)
            images_rendered += 1

        closer_html = carousel.closer_slide(data)
        render_html_to_png(closer_html, carousel_dir / f"{len(flat) + 1:02d}-closer.png", carousel.W, carousel.H)
        images_rendered += 1
        print(f"wrote {images_rendered} carousel slides to {carousel_dir}")

        for i, slug, deal, region in numbered:
            html = story.deal_frame(deal, data)
            render_html_to_png(html, story_dir / f"{slug}.png", story.W, story.H)
            images_rendered += 1
        print(f"wrote {len(flat)} story frames to {story_dir}")

    # --- Index / review notes ---
    index_lines = [
        f"# {travel_month} posts — generated for human review",
        "",
        "Nothing here has been published. Review before posting anywhere",
        "(per scraper/PROCEDURE.md step 8's human review gate).",
        "",
    ]
    if browser:
        index_lines += [
            f"- `web-artifact.html` — full {len(data['deals'])}-route list",
            f"- `carousel/` — {len(flat) + 2} slides (cover + {len(flat)} picks + closer) + `caption.txt`",
            f"- `story/` — {len(flat)} single-deal frames, each with its own `.caption.txt`",
        ]
    else:
        index_lines += [
            f"- `web-artifact.html` — full {len(data['deals'])}-route list",
            "- **No carousel/story PNGs this run** — no Chromium-family browser was found in "
            "this environment. Captions were still generated (`carousel/caption.txt`, "
            "`story/*.caption.txt`) so copy is ready; run "
            f"`python3 content/scripts/generate.py {src} --force` on a machine with a "
            "browser (e.g. locally) to fill in the images.",
        ]
    index_lines += [
        "",
        "## Curated picks (best 3 per region by internal miles/hour value ranking)",
        "",
    ]
    for region in REGION_ORDER:
        if not picks[region]:
            continue
        index_lines.append(f"**{region}**")
        for d in picks[region]:
            index_lines.append(f"- {d['route_label']} — {d['miles']:,} mi")
        index_lines.append("")

    (out_dir / "README.md").write_text("\n".join(index_lines))
    print(f"wrote {out_dir / 'README.md'}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--force"]
    if len(args) < 1:
        print("usage: generate.py <scraper/samples/YYYY-MM.json> [--force]", file=sys.stderr)
        sys.exit(1)
    main(args[0], force="--force" in sys.argv)
