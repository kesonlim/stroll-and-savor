# Growth, monetization & SEO plan

Decided 2026-08-09 via a structured design-tree interview (see project chat
history for the full round-by-round reasoning). This doc is the durable
record — update it as decisions change rather than treating it as a
point-in-time snapshot that drifts from reality.

## Where things stand today

- Field Notes brand system, fully specified (`brand/`).
- SIA Spontaneous Escapes tracked monthly: extraction (`scraper/`), content
  generation (`content/`), and a live site (`site/`) — currently living at
  the site root, being restructured (see below).
- Social accounts, confirmed live:
  - Facebook: https://www.facebook.com/profile.php?id=61581034831451
  - Instagram: https://www.instagram.com/stroll_savor/
  - TikTok: https://www.tiktok.com/@stroll_savor
  - YouTube: https://www.youtube.com/@StrollAndSavor
- No mailing list, no ad network integration, no affiliate links live yet.

## Site structure (IA)

The root domain (`strollsavor.thethinkthank.com`) is a **general Stroll &
Savor brand landing page** — not SIA-specific. SIA content moves to a
subpath so the IA can hold other airlines/verticals alongside it without a
rename.

```
/                                  brand-general landing page
/singapore-airlines/
  spontaneous-escapes/             the existing monthly tracker (moved from root)
    <travel-month>/                individual monthly posts (was /blog/<month>/)
/airlines/                         [planned] glossary: every airline serving Singapore
  <airline-slug>/
/hotels/                           [planned, later] glossary: hotel chains, Singapore first
  <chain-slug>/
/attractions/                      [planned, later] glossary: attractions, Singapore first
  <attraction-slug>/
/news/                             [planned] rewritten/reframed airline press releases
  <post-slug>/
```

Root nav (once restructured): **Home** / **Singapore Airlines** / **Blog**
(news) / **Guides** (glossary, once it exists) — trim to what actually has
content at each phase rather than linking to empty sections.

## Monetization plan

**Sequencing: monetize in parallel with growth, but light-touch.** Two
affiliate categories checked and confirmed low-barrier enough to integrate
early rather than waiting for meaningful traffic:

- **OTA/activity affiliates (priority 1)** — Klook has no minimum-traffic
  requirement and no website requirement to join; commission 2–20%
  depending on category (tours/hotels ~6.5%, attractions ~5%). Natural
  first placement: a Klook/Pelago-style link on the Spontaneous Escapes
  page, which already primes visitors toward post-booking activities (the
  SIA source page itself features Pelago activity suggestions).
- **Bank card referrals (priority 2, added incrementally)** — Singapore
  issuers (Citi confirmed: S$150/referral) run these as personal
  referral/MGM programs, not a formal affiliate network — same model
  MileLion uses. Requires signing up individually per bank; add one at a
  time as enrolled, not a single integration.
- **Travel insurance affiliates** — relevant given Spontaneous Escapes
  fares are explicitly non-cancellable (SIA's own T&Cs recommend insurance)
  — natural contextual fit, lower priority than the above two, revisit
  once the site has a "before you book" content moment to attach it to.
- **Google AdSense / display ads** — **confined to reference/utility pages
  only** (`/airlines/`, `/hotels/`, `/attractions/`, `/news/`) — **never**
  on deal-tracking pages (home, `/singapore-airlines/spontaneous-escapes/`
  and its monthly posts). Those are the trust-critical surface; the brand
  voice (persona "distrusts glossy travel marketing," no-hype principles)
  is the product there, and ad clutter undercuts it directly. Reference
  pages are lookup-utility in nature and can carry ads without the same
  cost. Don't turn this on until there's real traffic to justify it.
- **Sponsored/partner content** — not ruled out, but no policy needed
  until someone actually asks; revisit if/when relevant.
- **Premium tier** — a possible future lever (faster/deeper deal
  analysis, similar to MileLion's own SEAT tool), explicitly deferred, not
  part of the current roadmap.

## SEO plan: programmatic glossary

Legitimate, well-precedented strategy in this niche (deal/points blogs and
travel aggregators do this routinely) — but only if pages carry real
value, not thin templated shells (both a copyright/quality constraint on
scraped content and a real SEO risk: search engines actively penalize
low-value duplicate content).

**Sequencing**: airlines first, Singapore-scoped, before hotels/attractions
(explicitly deferred — do not start those until airlines is shipped and
validated).

**Depth per page**: structured data (routes served, alliance, cabin
classes, booking links) **plus one short genuine editorial paragraph per
airline in the established brand voice** — not a pure data template, not
full long-form. Matches the pattern already used for the monthly blog post
(data template + light editorial framing in the masthead).

**Scope sizing** (researched 2026-08-09, corrects this doc's earlier
"several dozen" guess): Changi Airport's official passenger airline list
has **86 airlines** — see `airlines/data/changi-airlines.json` (name +
IATA code, sourced from
`changiairport.com/en/fly/airline-information/passenger.html`). That's a
meaningfully bigger hand-review commitment than "several dozen," so build
in **tiers** rather than all 86 at once:

1. **Star Alliance members** (SIA's own alliance — most relevant to a
   KrisFlyer-focused audience deciding where to redeem/earn miles) first.
2. **Major codeshare/oneworld/SkyTeam partners** relevant to Singapore
   routes next.
3. **Everything else** last, and possibly with a lighter per-entry bar
   once the format is proven on the higher-priority tiers.

**Tier 1, confirmed 2026-08-09**: cross-referencing Star Alliance's official
26-member list (`airlines/data/star-alliance-members.json`) against the
Changi 86 gives **15 airlines**: Air Canada, Air China, Air India, Air New
Zealand, All Nippon Airways, Asiana Airlines, Ethiopian Airlines, EVA Air,
Lufthansa, Shenzhen Airlines, Singapore Airlines, Swiss International Air
Lines, Thai Airways, Turkish Airlines, United Airlines. A tight, manageable
first batch. (Note: Juneyao Air is a Star Alliance *Connecting Partner* at
Changi, not a full member — different mileage rules, deliberately excluded
from this tier rather than conflated with it.)

**Technical approach**: extends the existing Python-template-generation
pattern (`content/templates/`, `site/templates/`) rather than introducing
a new stack.

**Tier 1 shipped 2026-08-09**: all 15 entries live at `/airlines/<slug>/`
plus an index at `/airlines/` (added to site nav). Data + hand-authored
blurbs in `airlines/data/entries.py`, templates in
`site/templates/airline_entry.py` / `airlines_index.py`. Includes
Singapore Airlines itself (deliberately — it's the reason the site
exists, and leaving it out of an otherwise-complete tier would be its own
kind of inconsistency).

**Not yet done, for tier 2+**: sitemap.xml generation, internal linking
(glossary entries should cross-link to relevant Spontaneous Escapes routes
where applicable — not built for tier 1 since there's no natural link
target per-airline yet), and deciding the tier-2 list (other
alliance/codeshare partners at Changi).

## News pipeline (press-release rewrite)

**Scope: start narrow — Singapore Airlines only.** Validates the
rewrite pipeline actually produces genuinely transformative content before
investing in a multi-airline tracker. SIA's newsroom/press-release archive
is browsable at a stable URL pattern
(`singaporeair.com/en_UK/sg/corporate/newsroom/press-release/`), already
confirmed reachable during earlier research in this project.

**Architecture**: reuse the proven `scraper/`-style pattern — a
cloud-scheduled routine that checks the newsroom page/RSS feed, and on a
new release, runs a rewrite pass before anything publishes.

**Hard constraint, not a nice-to-have**: rewritten posts must be
genuinely transformative — real framing, analysis, "what this means for
Spontaneous Escapes / for the deliberate collector," not paraphrased
press-release copy. This isn't just good practice — it's a operating
requirement (verbatim reproduction of source material beyond a short
attributed quote isn't something this pipeline can do), and it's also the
difference between content that ranks and thin duplicate content that
gets penalized. Every generated post needs a human review pass before
publishing, same as everything else in this project — no exception for
"it's just a rewrite."

**Not yet designed**: the actual prompt/procedure for the rewrite step,
and whether it needs an explicit "here's what changed vs. last time"
diffing step to avoid re-processing unchanged pages. Design this when the
narrow SIA-only version is actually being built, not speculatively now.

## Social conversion

Site ships with a config-driven social-links component (footer, and a
prominent block on deal pages) — now pointing at the four confirmed live
accounts above. The mechanism (not yet built): what specifically pulls a
reader from "reading the Spontaneous Escapes list" to "follows on
Instagram" — likely a soft CTA near the bottom of each monthly post
("this month's list as a carousel — see it on Instagram") rather than a
generic header icon, since that ties the ask to content the reader just
found valuable. Design the actual CTA copy/placement when building the
next monthly post, not abstractly now.

## Phased roadmap

Numbered by dependency order, not by calendar date — some phases can run
in parallel once their prerequisites land.

1. **Site IA restructure** — brand-general root landing page, SIA content
   moved to `/singapore-airlines/spontaneous-escapes/`, live social links
   wired in. *(in progress as of this doc's writing)*
2. **First affiliate integration** — Klook (or equivalent OTA/activity
   affiliate) link placed contextually on the Spontaneous Escapes page.
   Low effort, no traffic prerequisite — do this early.
3. **Airline glossary, Singapore-scoped** — research the actual airline
   list, build the template (structured data + short editorial paragraph
   per entry), human-review each entry, publish. Add `/airlines/` to nav
   once it has real content, not before.
4. **SIA news pipeline (narrow)** — press-release tracker + rewrite
   routine for Singapore Airlines only, human-reviewed before publish. Add
   `/news/` to nav once validated.
5. **Bank card referral links** — added incrementally as you personally
   enroll in each issuer's program (Citi first, given the confirmed S$150
   referral rate).
6. **Reference-page ad integration (AdSense)** — only once `/airlines/`
   and/or `/news/` have enough real traffic to be worth it; confined to
   those sections per the ad philosophy above.
7. **Hotels + attractions glossaries** — explicitly deferred until (3) is
   shipped and its content-depth/effort tradeoff is validated in practice.
8. **Broaden the news pipeline** beyond SIA, if (4) proves out.

## Explicitly not decided / deferred

- Premium tier (mentioned as a future possibility, not designed).
- Sponsored/partner content policy (no policy needed until it comes up).
- Whether/how to expand the glossary beyond Singapore-scoped once the
  Singapore version is validated.
- Exact CTA design for social conversion (deferred to when building that
  content, not designed in the abstract).
