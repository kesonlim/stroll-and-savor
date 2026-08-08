"""Generate the full set of monthly posts (web artifact, carousel, story
frames, captions) from a scraper extract. Usage:

    python3 content/scripts/generate.py scraper/samples/2026-08.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "templates"))

from curate import curate, REGION_ORDER, city_of  # noqa: E402
from render import render_html_to_png  # noqa: E402
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


def main(src_path: str):
    src = Path(src_path)
    data = json.loads(src.read_text())
    travel_month = data["travel_month"]

    out_dir = REPO_ROOT / "content" / "posts" / travel_month
    carousel_dir = out_dir / "carousel"
    story_dir = out_dir / "story"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    story_dir.mkdir(parents=True, exist_ok=True)

    picks = curate(data["deals"])
    flat = flatten_picks(picks)
    print(f"Curated {len(flat)} routes across {sum(1 for r in REGION_ORDER if picks[r])} regions")

    # --- Web artifact ---
    artifact_html = web_artifact.render(data)
    (out_dir / "web-artifact.html").write_text(artifact_html)
    print(f"wrote {out_dir / 'web-artifact.html'}")

    # --- Carousel ---
    cover_html = carousel.cover_slide(data, len(flat))
    render_html_to_png(cover_html, carousel_dir / "00-cover.png", carousel.W, carousel.H)

    for i, (deal, region) in enumerate(flat, start=1):
        html = carousel.deal_slide(deal, i, len(flat), region)
        render_html_to_png(html, carousel_dir / f"{i:02d}-deal.png", carousel.W, carousel.H)

    closer_html = carousel.closer_slide(data)
    render_html_to_png(closer_html, carousel_dir / f"{len(flat) + 1:02d}-closer.png", carousel.W, carousel.H)
    print(f"wrote {len(flat) + 2} carousel slides to {carousel_dir}")

    (carousel_dir / "caption.txt").write_text(captions.carousel_caption(data, flat))

    # --- Story frames (same curated set, one frame each) ---
    for i, (deal, region) in enumerate(flat, start=1):
        html = story.deal_frame(deal, data)
        slug = city_of(deal).lower().replace(" ", "-")
        render_html_to_png(html, story_dir / f"{i:02d}-{slug}.png", story.W, story.H)
        cap = captions.story_caption(deal, data)
        (story_dir / f"{i:02d}-{slug}.caption.txt").write_text(cap)
    print(f"wrote {len(flat)} story frames to {story_dir}")

    # --- Index / review notes ---
    index_lines = [
        f"# {travel_month} posts — generated for human review",
        "",
        "Nothing here has been published. Review before posting anywhere",
        "(per scraper/PROCEDURE.md step 8's human review gate).",
        "",
        f"- `web-artifact.html` — full {len(data['deals'])}-route list",
        f"- `carousel/` — {len(flat) + 2} slides (cover + {len(flat)} picks + closer) + `caption.txt`",
        f"- `story/` — {len(flat)} single-deal frames, each with its own `.caption.txt`",
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
    if len(sys.argv) < 2:
        print("usage: generate.py <scraper/samples/YYYY-MM.json>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
