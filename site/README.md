# Site

The public Stroll & Savor site: a brand-general landing page plus
per-topic sections (currently just Singapore Airlines), deployed to
Cloudflare Pages. Live at **https://strollsavor.thethinkthank.com** (custom
domain confirmed working 2026-08-09) and
`https://stroll-and-savor.pages.dev`.

## Site structure (IA)

Full rationale in [`docs/growth-plan.md`](../docs/growth-plan.md). Root is
brand-general, not SIA-specific — SIA content lives under its own subpath
so the IA can hold other airlines/verticals later without a rename.

```
/                                            brand-general landing page
/singapore-airlines/spontaneous-escapes/     the monthly tracker (section landing + latest)
  <travel-month>/                            individual monthly posts
/airlines/                                   airline glossary index -- tiers 1+2 live (34 airlines: Star Alliance, oneworld, SkyTeam at Changi)
  <airline-slug>/                            individual airline entries
/hotels/  /attractions/                      [planned] SEO glossary, see docs/growth-plan.md
/news/                                       [planned] rewritten airline press releases
```

## Build

```
python3 site/scripts/build.py
```

Reads every `scraper/samples/*.json`, builds one monthly post per travel
month under `/singapore-airlines/spontaneous-escapes/<month>/`, that
section's own landing page, and the root landing page, into `site/dist/` —
a fully static, self-contained directory (brand CSS and fonts copied in
from `brand/`, no external requests at runtime).

## Deploy

```
npx wrangler pages deploy site/dist --project-name stroll-and-savor
```

Cloudflare Pages project: **stroll-and-savor**, account `kesonlim@gmail.com`.

**Custom domain**: attached manually via the Cloudflare dashboard (Workers
& Pages → stroll-and-savor → Custom domains) — `wrangler pages domain add`
doesn't exist in the installed wrangler version (4.120.0), and the direct
API-call fallback was blocked by Claude Code's auto-mode safety classifier
as a raw-credential-handling pattern. Confirmed resolving correctly
(landing page, SIA section, and a monthly post all checked) as of
2026-08-09.

**Note on caching**: after a deploy, the exact URL you were just looking at
may serve a stale edge-cached copy for a short time — a cache-busting query
string (`?cb=1`) or a moment's wait clears it. The deployment itself is
correct immediately; this is Cloudflare's edge cache, not a deploy failure.

## Structure

- `templates/chrome.py` — shared header/nav/footer wrapping every page,
  including the confirmed-live social links (Facebook/Instagram/
  TikTok/YouTube) and the nav (trimmed to sections that actually have
  content — add Guides/News once those ship).
- `templates/landing.py` — brand-general root: hero, "what we're
  tracking" (points at the SIA section), "follow along" (social grid),
  "how this gets made".
- `templates/spontaneous_escapes.py` — the
  `/singapore-airlines/spontaneous-escapes/` section landing page (this
  used to be the root landing page's content, before the IA restructure).
- `templates/monthly_post.py` — wraps `content/templates/web_artifact.py`'s
  `render_content` (the same full route-list content used for the
  standalone artifact in `content/posts/`) in site chrome, rather than
  duplicating that rendering logic.
- `scripts/build.py` — orchestrates everything above into `site/dist/`.
- `dist/` — build output, committed for the same reason `content/posts/`
  is: transparency/reproducibility of what's actually live. Regenerate with
  `build.py` rather than hand-editing.

## What's NOT here

- **`/hotels/`, `/attractions/`, `/news/`** — planned, not built.
  `/airlines/` tier 1 (15 Star Alliance members) is live; tiers 2+ and the
  other verticals are not. See [`docs/growth-plan.md`](../docs/growth-plan.md)
  for scope and sequencing.
- **No affiliate links on `/airlines/` yet** — the Klook affiliate link
  (live, tracked) is currently only on Spontaneous Escapes monthly posts,
  not on airline glossary pages. Bank card referrals (Citi first) also not
  implemented yet — mechanism differs from Klook (a personal
  identity-verified referral code, not a trackable link), see
  `docs/growth-plan.md`.
- **No newsletter/mailing list** — doesn't exist yet, out of scope until
  one does.
- **No social publishing automation** — Instagram/etc carousel and story
  content lives in `content/posts/<month>/`, downloaded and posted
  manually. See that folder's `caption.txt` / `*.caption.txt` files for
  proposed post copy.
- **No auto-deploy** — a new month's data landing (via the scheduled
  extraction routine) does not automatically rebuild or redeploy this
  site. Run `build.py` + `wrangler pages deploy` by hand after reviewing
  new content, consistent with the human-review-gate policy the rest of
  this project follows.
