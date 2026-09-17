# Growth, monetization & SEO plan

Originally decided 2026-08-09 via a structured design-tree interview.
**Superseded in large part by a 2026-09-11 strategy reset** (also a
structured `grilling` interview — see project chat history for full
round-by-round reasoning), after real research showed the interim
deal-alert redesign was modeled on the wrong genre of site. This doc is
the durable record — update it as decisions change rather than treating
it as a point-in-time snapshot that drifts from reality.

## Where things stand today (2026-09-11)

- Field Notes brand system, fully specified (`brand/`) — **now scoped to
  social media only**, not the website (see reset below).
- SIA Spontaneous Escapes tracked monthly: extraction (`scraper/`), content
  generation (`content/`), airline glossary (`airlines/`) — all kept, all
  infrastructure, unaffected by the visual/positioning reset.
- Social accounts, confirmed live:
  - Facebook: https://www.facebook.com/profile.php?id=61581034831451
  - Instagram: https://www.instagram.com/stroll_savor/
  - TikTok: https://www.tiktok.com/@stroll_savor
  - YouTube: https://www.youtube.com/@StrollAndSavor
- Mailing list (Buttondown signup) and OTA affiliate links (Klook) are
  live. No ad network integration, no credit-card affiliate relationship
  yet (see "Citi correction" below — this was never actually live).
- The site's static-HTML-via-Python-f-strings build (`site/templates/`,
  `site/scripts/build.py`) is being **replaced by an Astro migration**
  (see below) — do not build new templates in the old pattern.

## 2026-09-11 strategy reset — what changed and why

**The problem.** The prior session's homepage redesign was modeled on
Going.com — a deal-alert "subscription" site (Premium/Elite tiers,
$49-199/yr). But Stroll & Savor's actual business model is affiliate +
ads, not subscription. Copying a subscription site's visual conventions
while running a different business model was a genre mismatch, and it's
why the redesign didn't feel right even though it was well-executed on
its own terms.

**The correction, researched not guessed:**

- **Superior-margin travel monetization models, ranked**: credit-card/
  finance affiliate has by far the highest EPC in the travel/finance
  niche ($100-300+ CPA per approved card vs. 2-8% commission and ~1-3%
  conversion for OTA affiliate, vs. $3-15 RPM for display ads). This is
  literally The Points Guy's entire business, and the same playbook
  MileLion (this project's own scraper fallback source) runs in this
  exact market. Subscription (Going's model) has the best long-term LTV
  but is the hardest to bootstrap solo and doesn't fit a "generic
  consumer" positioning — explicitly not pursued.
- **Sequencing given that ranking**: OTA affiliate (Klook, already live)
  + display ads on programmatic content are the *volume/ease-of-scale*
  layer (low barrier, low margin, but easy to turn on and scales with
  content volume). Credit-card/finance affiliate is the *profit engine*,
  entered via a lower-barrier network (CardRatings-style) before
  graduating to direct issuer deals, once there's real traffic to show —
  exactly TPG/MileLion's own path.
- **Site positioning**: broadens from a narrow "deal tracker" to a real
  points/travel-deals **content hub** in the TPG mold — deals + card
  guides + airline/program reference content, no single "hero product."
  A narrow tracker caps traffic at one source (SIA's monthly reveal) and
  gives card issuers nothing to call "finance-relevant" beyond one
  recurring post.
- **Design role model, researched via a live homepage audit**: not
  Skyscanner (pure search-utility, no editorial content — building that
  hero would mean competing with the OTAs you're earning commission
  from), but a **TPG + NerdWallet hybrid**: TPG's editorial grid +
  "BEST FOR X" affiliate card-offer modules, NerdWallet's ranked
  "best of" list pages. No live flight-search form anywhere on the site.
- **Field Notes brand identity** (Courier Prime/IBM Plex Sans/Space Mono,
  warm paper background) moves to **social media only** — a deliberate
  split, not a demotion. The website needs generic, mass-market,
  instantly-recognizable design; social content can still stand out with
  a distinct identity since it's a different consumption context.
- **Citi referral correction**: `docs/growth-plan.md` previously implied
  a live Citi referral link. There isn't one — what's real is that
  Citibank SG's personal-referral program pays S$150/referral (researched
  2026-08-09); enrollment hasn't happened yet. Card-guide content
  launches without live card-affiliate links until real relationships
  (Citi enrollment, then CardRatings-style network, then direct issuers)
  exist.

## Tech stack: Astro migration

The existing static-HTML-via-Python-f-string approach (`site/templates/*.py`
generating raw HTML strings) is being replaced with **Astro + file-based
content collections**, deployed to Cloudflare Pages same as today.

**Why**: researched, not a preference call — the documented 2026 best
practice is *"use a headless CMS when you have a dedicated content team
that needs a visual editor... use file-based content when your team is
technical or works with AI agents"* (Cosmic JS, Astro vs Next.js
comparison). That's exactly this project's situation: no editor team,
content and code both produced by Claude Code sessions. Astro is also the
documented default for SEO-heavy, mostly-static content sites specifically
because it's pre-rendered by default. Concretely, this also fixes a real
maintainability problem the old approach had: content, layout, and copy
were all mixed together inside Python f-strings generating raw HTML,
which made the last redesign painful (CSS specificity bugs, giant string
blocks). Content becomes typed Markdown/YAML/JSON in git (same
human-review-gate workflow as today); presentation becomes reusable
`.astro` components.

**Migration is mechanical for existing content**: airline glossary data
(`airlines/data/entries.py` + JSON files) and SIA Spontaneous Escapes
posts (`scraper/samples/*.json`) both go from Python dicts to Markdown/
YAML frontmatter — no re-authoring, no content loss.

## Site structure (IA)

URL structure **stays stable** — it already has real (if early) search
history and there's no functional reason to reset it:

```
/                                  brand-general hub homepage (TPG+NerdWallet hybrid design)
/singapore-airlines/
  spontaneous-escapes/             the existing monthly tracker
    <travel-month>/                individual monthly posts
/airlines/                         glossary: every airline serving Singapore (34 live)
  <airline-slug>/
/cards/                            [new] credit-card guides ("best miles cards in Singapore," per-card pages)
/hotels/                           [planned, later] glossary: hotel chains, Singapore first
  <chain-slug>/
/attractions/                      [planned, later] glossary: attractions, Singapore first
  <attraction-slug>/
/blog/  (or /news/ + /guides/)     [new] editorial stream — deal analysis, card guides as articles,
                                    rewritten SIA press releases. One content model, dated posts,
                                    TPG-style. Absorbs the previously-separate "news pipeline" plan.
```

New sections get added to the existing tree; nothing gets renamed.

## Homepage design direction

**Role model, from a live structural audit of TPG, Skyscanner, and
NerdWallet (2026-09-11):**

- **The Points Guy** — magazine-first: editorial article grid (bylines,
  read times, category tags) with commerce inserted as distinct bordered
  "offer" modules (superlative label + card image + terms + CTA), plus a
  points-valuation reference table and a card-filter/comparison tool.
- **Skyscanner** — utility-first: a search form *is* the hero, almost no
  editorial content, a long tail of programmatic city/route link tiles
  below. **Explicitly not the model for Stroll & Savor** — a live
  flight-search hero is a large technical build that also competes with
  the OTAs paying commission through this site.
- **NerdWallet** — ranked "best of" list pages (card image + rating +
  short "why we like it" + fee summary), no narrative voice, ratings and
  disclosures next to every commerce unit.

**Stroll & Savor's homepage**: TPG's editorial-grid rhythm and
superlative-labeled card-offer modules, NerdWallet's ranked "best of"
structure for card-guide pages specifically, no search-form hero.

## Content pillars (priority order)

1. **Deals** — existing SIA Spontaneous Escapes tracker, widen beyond SIA
   (see "Widening the scraper" below).
2. **Airline/loyalty glossary** — existing, 34 of 86 Changi airlines live,
   continue tiering (see SEO plan below, unchanged in substance).
3. **Card guides** — new. Evergreen editorial ranking content ("best miles
   credit cards in Singapore," individual card pages), built now without
   live affiliate links where none exist yet. Prioritized ahead of the
   news pipeline because it's the direct path to the card-affiliate
   profit engine and it's a durable SEO asset (doesn't go stale monthly
   the way a deal post does).
4. **Points valuation reference** — new, TPG-style "what's a mile worth"
   table. Lower priority, natural follow-on once card guides exist.
5. **News/blog** — the previously-planned SIA press-release rewrite
   pipeline, now folded into the general editorial/blog stream rather
   than a separate section. Lowest priority of the five (was already
   unstarted).

## Content & research agent architecture

Two-stage pipeline, both stages are just scoped Claude Code passes, not
new infrastructure:

```
research agent → structured findings (JSON/YAML, no prose)
              → content agent → Astro content collection entry + social assets
              → human review (existing gate, unchanged)
              → publish
```

- **Research agent**: evolution of `scraper/`. Watches known sources
  (airline newsrooms, MileLion/OMAAT/TPG, card issuer rate pages) and
  outputs structured data only. Two modes: **scheduled** (cloud routine,
  like the existing `⚡ SS_Escapes_Monthly_Extract`) for predictable
  recurring checks, **on-demand** (an invoked subagent) for irregular
  research tasks. **Cadence: daily** for the scheduled mode.
- **Content agent**: evolution of `content/scripts/generate.py`. Consumes
  a research agent's structured findings, never invents facts, produces
  an Astro content entry plus matching social assets.
- **Widening the scraper** (first research-agent task): identify which
  other airlines/loyalty programs relevant to a Singapore-based audience
  run comparable trackable promos, so "Deals" stops being SIA-only. Not
  yet scoped — do this before building the monitoring-agent or reviving
  the full news pipeline; one new system at a time.

## Social distribution

**Pipeline scope, sequenced**: (a) extend the existing carousel/story/
caption generator (`content/`) to new content types as they get built —
smallest lift, same pattern, new content sources. (b) Add real posting
automation — currently 100% manual, this unlocks consistent cadence. (c)
Add video generation for TikTok/YouTube — most novel/expensive, last.

**Publish flow: queued-and-approve, never full auto-publish** — consistent
with every other human-review gate already established in this project;
social posts are public and permanent in a way that's awkward to walk
back.

**Posting mechanism**: direct platform APIs, not a unified provider —
Postiz/Ayrshare-style tools were evaluated (Postiz self-hosted is free;
Ayrshare's $149+/mo is priced for agencies managing many client brands,
not a single brand) but tabled in favor of direct integrations, revisited
only if maintaining several direct integrations becomes a real burden.

**Platform priority — audience-first, not build-ease-first.** An initial
"start with whatever's easiest to integrate" pass (Threads + X) was
**corrected** after checking actual Singapore platform-usage data: X has
the lowest ad-engagement of any platform measured in Singapore (0.5%),
and Threads doesn't register in Singapore-specific stats at all. Stroll &
Savor's audience is explicitly Singapore-biased (inbound visitors +
outbound Singapore-based travelers), so fit had to come before ease:

1. **Instagram** — strongest reach (65.9% of SG internet users) + the
   existing carousel/story content is already built for this exact
   format. Start the Meta app review now (2-4 week queue) in parallel
   with building everything else, since nothing blocks on it.
2. **Facebook** — same Meta app as Instagram, near-zero extra setup once
   approved, already has a live presence to feed.
3. **TikTok** — highest engagement in Singapore specifically (4.2% ad
   engagement, most time-in-app of any platform measured). Gated on video
   generation; bump ahead of YouTube once that exists.
4. **XiaoHongShu** — no official API for foreign creators exists (only
   unofficial/session-based tools), so automation isn't realistically on
   the table yet. But it's the **primary destination-research platform
   for Chinese travelers considering Singapore** (60%+ discover
   destinations there, ~50% have booked from what they saw) — exactly the
   inbound-tourist half of this project's target audience. **Start
   posting manually now**, don't wait for automation that has no clean
   path.
5. **YouTube** — after TikTok, also needs video.
6. **Deprioritized / skipped for now**: X, Threads, Bluesky, LinkedIn —
   weak Singapore audience fit for this brand. Bluesky specifically: real
   and growing (43.5M registered users) but no evidence of an established
   travel/points community there; revisit only if that changes.

## Monetization plan

**Sequencing, updated per the 2026-09-11 reset**: OTA affiliate + display
ads as the volume/ease-of-scale layer, credit-card/finance affiliate as
the actual profit engine, entered incrementally:

- **OTA/activity affiliates (live now)** — Klook, no minimum-traffic
  requirement, commission 2–20% depending on category. Contextual
  placement on deal pages.
- **Credit-card/finance affiliate (the priority profit engine, not yet
  live)** — sequencing: (1) enroll in Citibank SG's personal-referral
  program (S$150/referral, confirmed rate, not yet enrolled), (2) apply
  to a lower-barrier aggregator network (CardRatings-style) once card
  guide content exists to demonstrate "finance relevance," (3) graduate
  to direct issuer relationships as traffic grows — the exact path TPG
  and MileLion both walked. Top-tier programs are gated on traffic/
  authority; card guides (see content pillars) are the asset that
  unlocks this.
- **Travel insurance affiliates** — unchanged, lower priority, revisit
  once there's a "before you book" content moment to attach it to.
- **Google AdSense / display ads** — unchanged: confined to reference/
  utility pages only (`/airlines/`, `/hotels/`, `/attractions/`,
  `/blog/`), never on deal-tracking pages. Don't turn on until there's
  real traffic to justify it.
- **Sponsored/partner content** — unchanged, no policy needed until asked.
- **Premium tier** — explicitly **not pursued** (was previously "possible
  future lever"). Research showed subscription is the wrong fit for a
  generic-consumer-positioned affiliate/ads business and the hardest
  model to bootstrap solo; if revisited, that would be a deliberate
  future decision, not a default assumption.

## SEO plan: programmatic glossary

Unchanged in substance from the original plan — still a legitimate,
well-precedented strategy, still airlines-first before hotels/attractions,
still tiered. Continues under the Astro migration (glossary entries become
typed content collection items rather than Python dicts, same data, same
editorial bar).

**Scope sizing**: Changi Airport's official passenger list has 86
airlines (`airlines/data/changi-airlines.json`).

**Tier 1, shipped**: 15 Star Alliance members (Air Canada, Air China, Air
India, Air New Zealand, All Nippon Airways, Asiana Airlines, Ethiopian
Airlines, EVA Air, Lufthansa, Shenzhen Airlines, Singapore Airlines, Swiss
International Air Lines, Thai Airways, Turkish Airlines, United Airlines).

**Tier 2, shipped**: 19 oneworld/SkyTeam members — see git history /
`airlines/data/oneworld-skyteam-members.json` for the full breakdown.

**Tier 3, not yet scoped**: the remaining ~52 of Changi's 86 airlines with
no major alliance membership.

**Not yet done**: internal linking between glossary entries and
Spontaneous Escapes/deal routes (now has a much more natural link target
once the hub has more sections — reconsider during the Astro rebuild), and
tier 3 scoping.

## Phased roadmap (post-reset)

Numbered by dependency order, not calendar date.

1. **Astro scaffold + content migration** — set up Astro project, content
   collection schemas, port existing airline glossary + SIA post data
   mechanically. *(starting now)*
2. **Homepage rebuild** — TPG+NerdWallet hybrid design, editorial grid +
   card-offer modules, no search hero.
3. **Card guide content** — 1-2 evergreen "best miles credit cards in
   Singapore" pages, editorial-only (no live affiliate links yet).
4. **Widen the scraper** — research which other programs to track beyond
   SIA.
5. **Social pipeline, phase 1** — extend carousel/story/caption generator
   to new content types; start Meta app review (Instagram/Facebook) in
   parallel; start manual XiaoHongShu posting now.
6. **Social pipeline, phase 2** — posting automation (queued-and-approve)
   for Instagram + Facebook once Meta review clears.
7. **Airline glossary tier 3** — remaining ~52 airlines, can run in
   parallel with the above.
8. **Credit-card affiliate enrollment** — Citi personal referral first,
   then a CardRatings-style network once card guide content + real
   traffic exist.
9. **Video generation + TikTok/YouTube posting automation** — after (5)
   proves out the pipeline on simpler formats.
10. **Reference-page ad integration (AdSense)** — once `/airlines/` and/or
    `/blog/` have real traffic.
11. **Hotels + attractions glossaries** — deferred until (7) validates the
    content-depth/effort tradeoff.

## Explicitly not decided / deferred

- Sponsored/partner content policy (no policy needed until it comes up).
- Whether/how to expand the glossary beyond Singapore-scoped.
- Unified social-posting provider (Postiz/Ayrshare) — tabled in favor of
  direct platform integrations; revisit only if direct-integration
  maintenance becomes a real burden.
- X, Threads, Bluesky, LinkedIn as distribution channels — deprioritized
  for weak Singapore audience fit, not ruled out permanently.
- Premium/subscription tier — explicitly not pursued per the 2026-09-11
  research, not a default to revisit without a fresh deliberate decision.

## KrisFlyer master dashboard + kfescapes.thethinkthank.com (2026-09-18)

A separate, more ambitious monthly asset from the core roadmap above:
a full interactive dashboard covering every Singapore Airlines KrisFlyer
Spontaneous Escapes promotional sector (all 92 one-way sectors + 42
official round-trip itineraries), with live blackout-date checking,
region/cabin/weather filters, a collapsible custom open-jaw route
builder, and a column customizer. Source files (HTML + an engineering
handoff doc) are supplied out of band each month once Singapore Airlines
publishes that month's promotion (around the 15th); Claude restyles them
onto the Field Notes brand system (`site/templates/krisflyer_dashboard_*.py`,
generated via a one-shot color-remap transform script, never hand-typed
given the embedded data size) and publishes at
`/singapore-airlines/spontaneous-escapes/<YYYY-MM>/dashboard/`. Each
month gets its own template module (e.g. `krisflyer_dashboard_2026_11.py`)
so past months stay live rather than being overwritten.

**kfescapes.thethinkthank.com** is a second custom domain on the same
`stroll-and-savor` Cloudflare Pages project (not a separate project) that
shows the current month's dashboard as its landing page, with full
Stroll & Savor branding kept. Since one Pages project serves identical
static output to every custom domain attached to it, `functions/index.js`
(a Cloudflare Pages Function matching the root route) does host-based
routing: requests with `Host: kfescapes.thethinkthank.com` are served
`/_kfescapes-landing/index.html` instead of the normal landing page;
every other host falls through unchanged. `site/scripts/build.py` writes
that alias file from whichever `krisflyer_dashboard_*` module is current
— update that one call each month, not `functions/index.js`.

**Still needs a manual step:** attaching `kfescapes.thethinkthank.com` as
a custom domain to the `stroll-and-savor` Pages project in the Cloudflare
dashboard (Workers & Pages → stroll-and-savor → Custom domains → Add).
No Cloudflare API token is configured in this environment and this
wrangler version has no CLI command for it, so it hasn't been done yet —
until it is, the domain won't resolve and the Function's host check can't
be exercised end-to-end (verified locally via `context.next()` fallthrough
and the `/_kfescapes-landing/` alias file being reachable instead).
