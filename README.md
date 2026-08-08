# Stroll & Savor

Brand system and (upcoming) automation for a monthly newsletter/social presence covering Singapore Airlines "Spontaneous Escapes" business class deals.

## What's here

- `brand/` — the Field Notes brand system: corporate identity guide, logo exploration and final lockup, master logo file set (SVG/PNG/ICO), and per-platform profile pictures & banners.
  - `stroll-savor-ci-guide.html` — the full brand guide (colors, type, logo usage, voice).
  - `stroll-savor-logos.html` — logo concept exploration and the final locked system.
  - `stroll-savor-moodboard.html` — early direction/moodboard exploration.
  - `logo-master/` — final logo files (SVG source, PNG exports, favicon).
  - `platform-assets/` — avatars and banners sized per platform (Instagram, Facebook, LinkedIn, YouTube, TikTok, Xiaohongshu, website OG image).
  - `website-style-guide.css` / `website-style-guide.md` — framework-agnostic CSS tokens for the website, derived from the CI guide.
  - `fonts/` — self-hosted `.woff2` files (IBM Plex Sans, Space Mono, Courier Prime) backing the website style guide.
  - `scripts/` — Python build scripts used to generate the HTML guide and render the PNG/ICO assets, kept for reproducibility.
- `scraper/` — the monthly Spontaneous Escapes business-class extraction procedure, output schema, and test runs. See [`scraper/README.md`](scraper/README.md).
- `content/` — web artifact / carousel / story templates and generated monthly posts, built from `brand/` and fed by `scraper/`. See [`content/README.md`](content/README.md).
- `.claude/skills/design-taste-frontend/` — anti-slop frontend design skill (sourced from `Leonxlnx/taste-skill`), available to any Claude Code session working in this repo.

## Status

- [x] Logo system selected and locked
- [x] Master logo file set produced
- [x] Brand/corporate identity guide written
- [x] Per-platform profile pictures & banners produced
- [x] Website brand/style instructions (CSS tokens)
- [~] Scraper for Spontaneous Escapes business class promos — procedure built, MileLion fallback tested end-to-end; SIA-direct primary tier not yet validated against a live cycle
- [x] Monthly artifact / carousel / story templates — built and run end-to-end against real August 2026 data, see [`content/README.md`](content/README.md)
- [x] Monthly extraction automation (RemoteTrigger, fires around the 15th–18th) — live, see [`scraper/README.md`](scraper/README.md#scheduled-routine). Generating content (`content/`) and actually publishing it are still manual/separate steps.
