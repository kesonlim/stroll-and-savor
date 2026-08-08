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

`content/scripts/render.py` shells out to a Chromium-family browser in
headless mode to screenshot HTML at an exact pixel canvas size — same
approach as `brand/scripts/render_platform_assets.py`. The browser location
is auto-detected (`render.find_browser`) across known Mac/Playwright paths,
a `google-chrome`/`chromium` PATH lookup, and an `$STROLL_SAVOR_CHROME`
override — so it works locally on this Mac and *should* work inside the
scheduled cloud routine's environment too, but **that hasn't been proven
yet** (see "Wired into the extraction routine" below).

If no browser is found, `generate.py` degrades gracefully rather than
failing: it still writes `web-artifact.html` and all caption `.txt` files
(neither needs a browser), skips the PNGs, and says so plainly in that
run's `README.md` — including the exact command to run locally afterward
to fill in the images.

## Wired into the extraction routine

The `⚡ SS_Escapes_Monthly_Extract` cloud routine (see
`scraper/README.md`'s "Scheduled routine" section) now also runs
`content/scripts/generate.py` after a successful extraction, in the same
fire, and commits/pushes whatever it produces alongside the extracted data.

This is the routine's first attempt at finding a browser in that
environment — genuinely untested before this. Expected outcomes going
forward:
- **Browser found**: full carousel/story PNGs land automatically, same as
  a local run.
- **No browser found**: `web-artifact.html` and captions still land
  automatically (already useful — captions are most of the manual writing
  work), and `content/posts/<travel_month>/README.md` says exactly what to
  run locally to add images. Not a failure, just a partial win.

Check `content/posts/<travel_month>/README.md` after the first live fire
(2026-08-15) to see which of these actually happened, and update this
section once it's known rather than left as a prediction.

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
- [x] Wired into the extraction routine (`⚡ SS_Escapes_Monthly_Extract`
      now runs `generate.py` after a successful extraction) — untested
      against a live fire as of this writing; first real signal comes
      2026-08-15
- [ ] Actually posting anything — still fully manual, by design (review
      gate); no publishing automation exists yet
