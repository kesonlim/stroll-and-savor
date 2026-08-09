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
- `site/` — the public website (brand-general landing page + per-topic sections + `/airlines/` glossary), deployed to Cloudflare Pages. See [`site/README.md`](site/README.md).
- `airlines/data/` — researched source data backing the airline glossary (Changi's full airline list, Star Alliance membership, per-entry content).
- `docs/growth-plan.md` — the growth/monetization/SEO roadmap: site IA, monetization plan, SEO glossary plan, news pipeline plan, sequencing.
- `.claude/skills/design-taste-frontend/` — anti-slop frontend design skill (sourced from `Leonxlnx/taste-skill`), available to any Claude Code session working in this repo.

## Status

- [x] Logo system selected and locked
- [x] Master logo file set produced
- [x] Brand/corporate identity guide written
- [x] Per-platform profile pictures & banners produced
- [x] Website brand/style instructions (CSS tokens)
- [~] Scraper for Spontaneous Escapes business class promos — procedure built, MileLion fallback tested end-to-end; SIA-direct primary tier not yet validated against a live cycle
- [x] Monthly artifact / carousel / story templates — built and run end-to-end against real August 2026 data, see [`content/README.md`](content/README.md)
- [x] Monthly extraction automation (RemoteTrigger, fires around the 15th–18th) — live, see [`scraper/README.md`](scraper/README.md#scheduled-routine). Content generation (`content/`) is now chained onto the same routine (browser-availability in that environment is unvalidated — degrades gracefully to text-only if no browser is found).
- [x] Public site — live at `https://strollsavor.thethinkthank.com` (custom domain confirmed working) and `https://stroll-and-savor.pages.dev`. Brand-general landing page at root; Singapore Airlines Spontaneous Escapes content at `/singapore-airlines/spontaneous-escapes/`. Deploys are manual, not wired to the extraction routine, per the review-gate policy.
- [x] Growth/monetization/SEO roadmap — see [`docs/growth-plan.md`](docs/growth-plan.md). Social accounts (Facebook/Instagram/TikTok/YouTube) confirmed live and linked from the site.
- [~] SEO glossary — `/airlines/` tiers 1+2 live: 34 airlines (15 Star Alliance + 10 oneworld + 9 SkyTeam) flying to/from Changi, including SIA itself. Tier 3 (the remaining ~52 of Changi's 86 with no major alliance) and `/hotels/`, `/attractions/` not started.
- [ ] News pipeline (rewritten airline press releases) — planned, not built. Singapore Airlines only, first.
- [ ] Affiliate integration — planned (Klook/OTA first), not implemented.
- [ ] Social media posting — carousel/story images + proposed captions are generated (`content/posts/<month>/`) but posted manually; no publishing automation.
- [ ] Newsletter/mailing list — doesn't exist yet.
