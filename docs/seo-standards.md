# SEO & AI-discoverability standard

**Mandatory for every page in this repo** — landing, glossary entries,
blog/monthly posts, and anything added later. Referenced from the project
root `CLAUDE.md`. When building a new page type, work through the
checklist in "Before shipping a new page type" below before calling it
done.

**Canonical source: `~/.claude/SEO-GEO-STANDARDS.md`** (promoted global
2026-08-09, after this file proved out as the first working
implementation). This file was written first and is kept here as the
project-specific record — exact page types, the brand-voice tension notes
below, and the concrete build artifacts (`site/templates/chrome.py` etc.)
that implement it — but if the two ever disagree, the global file wins;
fix this one to match rather than the reverse. New general-purpose
practices get added to the global file directly, not duplicated here
first.

Decided 2026-08-09. Covers two overlapping but distinct goals:

- **Traditional SEO** — ranking in Google/Bing search results.
- **GEO (Generative Engine Optimization)** — being read, cited, and quoted
  correctly by AI answer engines and LLM web search (ChatGPT, Perplexity,
  Google AI Overviews, Claude, and the crawlers that feed them: GPTBot,
  ClaudeBot, PerplexityBot, Google-Extended, CCBot, and others). This is a
  newer, less standardized field than SEO, but the practices below are the
  well-evidenced ones, not speculation — several are things we already
  observed real sites doing during this project's own research (e.g.
  oneworld.com publishes `/llms.txt`; Changi and Star Alliance's own pages
  are plain server-rendered HTML with no JS-gated content).

The two goals mostly reinforce each other: clean semantic HTML, structured
data, and direct factual statements help both a Google crawler and an LLM
parsing the page for an answer. Where they'd ever conflict, favor
**clarity and correctness for a human reader first** — an SEO trick that
degrades the actual page is not worth it, and both Google and AI engines
increasingly penalize content that reads as written for a crawler rather
than a person.

## Why this project already has a head start

- **Fully static, server-rendered HTML** (`content/templates/`,
  `site/templates/`) — no client-side rendering gate, which several major
  AI crawlers (and some SEO crawlers) don't reliably execute. Nothing on
  this site requires JavaScript to see the actual content. Keep it that
  way — don't introduce a JS-rendered content path without a strong
  reason.
- **Self-hosted fonts, no external requests at runtime** — fast load,
  nothing for a privacy-conscious crawler to choke on.
- **Descriptive URL slugs already** (`/airlines/qatar-airways/`, not
  `/airlines/?id=14`) — keep doing this for every new section.
- **Sourced, dated data** (`airlines/data/*.json` note their source and
  retrieval date) — this discipline should extend to what's *visible on
  the page*, not just the source JSON (see "Show your sourcing" below).

## Per-page checklist (non-negotiable)

Every page's `<head>` must include:

1. **Unique `<title>`** — not a template repeated across pages. Include
   the specific entity/topic plus the brand name (`{Specific} — Stroll &
   Savor`, already the pattern in use).
2. **Unique `<meta name="description">`** — one to two sentences,
   specific to that page, front-loaded with the concrete fact (route
   count, airline name + IATA code, etc.) rather than generic brand copy.
3. **Canonical URL**: `<link rel="canonical" href="https://strollsavor.thethinkthank.com/...">`.
   Prevents duplicate-content ambiguity if a page is ever reachable at
   more than one path, and is a directness signal both Google and AI
   crawlers use to establish the authoritative version of a page.
4. **Open Graph**: `og:title`, `og:description`, `og:type`
   (`website` for index/landing pages, `article` for monthly
   posts/blog/news), `og:url`, `og:image` (where a relevant image exists
   — e.g. a monthly post's cover carousel slide).
5. **Twitter Card**: `twitter:card` (`summary_large_image` when an image
   exists, else `summary`), `twitter:title`, `twitter:description`.
6. **JSON-LD structured data** (`<script type="application/ld+json">`) —
   see "Structured data by page type" below. This is the single highest-
   leverage addition for both rich results and AI entity extraction; treat
   it as required, not optional polish.
7. **One `<h1>` per page**, matching the page's actual subject — never
   skip it, never use more than one, never use it for a generic site-wide
   label ("Stroll & Savor" as `<h1>` on every page would be wrong; each
   page's `<h1>` names *that page's* subject).
8. **Logical heading hierarchy** — `h2`s nest under the `h1`, `h3`s under
   relevant `h2`s. Don't skip levels for visual sizing reasons (use CSS for
   that, not the wrong tag).

## Structured data by page type

Schema.org JSON-LD, matched to what the page actually is:

- **Landing/section index pages** (`/`, `/airlines/`,
  `/singapore-airlines/spontaneous-escapes/`): `WebPage` or
  `CollectionPage`, plus a site-wide `Organization` block (name, url,
  logo, `sameAs` array of the confirmed social profiles) included once on
  the homepage at minimum.
- **Airline glossary entries**: `Organization` (schema.org has no
  dedicated "Airline" type) with `name`, `identifier` (IATA code),
  `url` (the airline's own official site — already verified per-entry,
  never guessed), and `sameAs` pointing back to it.
- **Monthly Spontaneous Escapes posts / future blog & news posts**:
  `Article` (or `BlogPosting` for genuinely editorial pieces once the news
  pipeline exists) with `headline`, `datePublished`, `description`, and
  `author`/`publisher` referencing the site's `Organization`.
- **Every page with a clear position in the site hierarchy**:
  `BreadcrumbList` (Home → section → page). Cheap to generate from the
  same `asset_prefix`/nav data already computed per page, high value for
  both Google's breadcrumb rich results and an AI crawler establishing
  where a page sits in the site.

Keep JSON-LD **factually identical to what's visibly on the page** — never
state something in structured data that isn't also readable by a human
visitor. Search engines and AI crawlers both penalize (or simply distrust)
structured data that contradicts visible content.

## Content-writing rules for AI extraction (GEO)

AI answer engines tend to extract and cite content that:

- **States the direct fact/answer first, elaboration after** — inverted-
  pyramid style. A reader (human or AI) skimming the first sentence of a
  section should get the actual answer, not throat-clearing.
  Already the house style (voice principle: "numbers do the persuading")
  — keep applying it deliberately to new page types, not just the deal
  lists it was originally written for.
- **Uses complete, standalone factual sentences** where possible — "Qatar
  Airways (QR) is a oneworld member hubbed at Doha" is more extractable
  and quotable than a sentence that only makes sense in context.
- **Shows its sourcing** — a visible "as of [date]" or a linked source is
  worth including on any page presenting a fact that could go stale
  (membership status, prices, schedules). This project already tracks
  `retrieved_at` in the data layer; surface it on-page where the fact is
  genuinely time-sensitive (e.g. alliance membership, which does change —
  see the Juneyao/Philippine Airlines partner-vs-member distinctions
  already documented in `docs/growth-plan.md`).
- **Avoids marketing adjectives doing the work numbers should** — this is
  already a brand voice rule for a different reason (credibility with the
  target reader), and it happens to also serve GEO: AI engines are trained
  to discount unverifiable superlative claims and favor concrete,
  checkable ones.

## Site-level technical requirements

- **`sitemap.xml`** at the site root, generated by `site/scripts/build.py`
  from the actual set of built pages (never hand-maintained — it must
  always match what's actually live). Referenced from `robots.txt`.
- **`robots.txt`** — explicitly permissive. This project's goal is
  maximum legitimate discoverability, the opposite of sites that block AI
  crawlers over content-scraping concerns. Default to `Allow: /` for all
  user-agents rather than enumerating individual AI bot names — an allow-
  all default already covers GPTBot/ClaudeBot/PerplexityBot/etc. without
  needing to track every crawler's exact UA string, which changes. Revisit
  only if a specific path ever needs to be excluded (there isn't one yet).
- **`llms.txt`** at the site root — a curated, plain-markdown overview of
  the site (what it is, its main sections, links to the most important
  pages) written for an LLM to read in one pass rather than crawling the
  whole site. This is an emerging, not-yet-universal convention, but
  costs little to maintain and several real sites already publish one
  (confirmed during this project's own research: oneworld.com serves
  `/llms.txt`). Regenerate it alongside the sitemap whenever the site
  structure changes meaningfully — stale entries here are worse than none.

## Before shipping a new page type

Run through this whenever a template for a *new kind* of page is built
(not needed again for a new *instance* of an existing page type — e.g. a
new airline entry reuses `airline_entry.py`'s already-compliant template):

1. Does it have a unique title + description drawn from real page data,
   not a hardcoded default?
2. Canonical URL, OG tags, Twitter Card — present and correct for this
   page's actual URL?
3. What schema.org type fits this content? (Check the list above first;
   if genuinely novel, pick the closest accurate schema.org type rather
   than skip structured data entirely.)
4. Does the page's own visible copy lead with the direct fact, or does it
   bury it under scene-setting?
5. Is every fact on the page traceable to a source, and is anything
   time-sensitive dated?
6. Added to `sitemap.xml` and (if it's a new top-level section) mentioned
   in `llms.txt`?

## Explicitly not done here

- No paid SEO tooling/audits (Ahrefs, SEMrush, etc.) — not in scope, this
  is a from-first-principles technical implementation.
- No keyword-density optimization or similar tactics that would compromise
  the "numbers do the persuading, no hype" voice — if a genuine conflict
  ever comes up between an SEO tactic and the brand voice, the voice wins;
  flag it rather than silently picking SEO.
- No AMP, no separate mobile site — the existing responsive static site is
  the only version; not revisited unless a real problem shows up.
