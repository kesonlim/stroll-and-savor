# Content

Templates and generated monthly posts for Spontaneous Escapes business-class
deals, built from the Field Notes brand system (`brand/`) and fed by
`scraper/samples/<travel_month>.json`.

## Pipeline

```
python3 content/scripts/generate.py scraper/samples/<travel_month>.json
```

Produces, under `content/posts/<travel_month>/`:

- **`web-artifact.html`** — full text-dense list of every business-class
  fare that month, grouped by region. Full three-typeface system, dot-grid
  throughout — the CI guide's "most text-dense surface."
- **`carousel/`** — cover + one slide per curated pick + closer, 1080×1350
  (Instagram feed/carousel size), plus one `caption.txt` for the whole post.
- **`story/`** — one 1080×1920 vertical frame per curated pick, each with
  its own `.caption.txt`.
- **`README.md`** — index of what was generated and which routes were
  curated, for the human review pass.

**Nothing here auto-publishes.** Generated output sits under
`content/posts/` for review — matches the human-review-gate policy already
established for the scraper (`scraper/PROCEDURE.md` step 8).

## How curation works

Carousel and story content features a curated subset, not the full list
(per CI guide section 06: "top deals only" for these surfaces). Curation
logic lives in `content/scripts/curate.py`:

- Best 3 distinct-city routes per region (Southeast Asia, North Asia, South
  Asia, Oceania), ranked by an internal miles-per-flight-hour value
  heuristic.
- Flight duration figures backing that heuristic are approximate (typical
  SIA block times, not from the extraction schema) and used **only** to
  rank candidates against each other — never displayed as a claimed fact in
  generated content, since only schema-verified numbers (route, miles,
  dates) are shown to the reader. This keeps curation logic and the brand's
  "precision over hype" voice rule from conflicting.
- Routes with no region mapping (e.g. a 5th-freedom oddity like a
  Los Angeles–Tokyo segment) are excluded from curated picks but still
  appear in the full web artifact under "Long-haul & other."

## Rendering

`content/scripts/render.py` shells out to this Mac's local Chrome in
headless mode to screenshot HTML at an exact pixel canvas size — same
approach as `brand/scripts/render_platform_assets.py`. **Local-machine
only** — this does not run inside the scheduled cloud routine, which only
produces data (see `scraper/README.md`), not images.

## Files

- `templates/web_artifact.py`, `templates/carousel.py`, `templates/story.py`
  — HTML generators per surface.
- `scripts/brand.py` — shared brand primitives (CSS path, inlined SVG
  marks, page skeleton).
- `scripts/curate.py` — region/value curation logic.
- `scripts/captions.py` — caption copy in the established voice.
- `scripts/render.py` — HTML → PNG.
- `scripts/generate.py` — orchestrates all of the above end to end.

## Status

- [x] Web artifact template
- [x] Carousel template (cover/deal/closer) + renderer
- [x] Story template
- [x] Caption copy generator
- [x] First real run: `posts/2026-08/` — generated from the July 15 2026
      release (August 2026 travel), MileLion-sourced (`scraper/samples/2026-08.json`)
- [ ] Actually posting anything — still fully manual, by design (review
      gate); no publishing automation exists yet
