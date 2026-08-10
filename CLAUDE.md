# Stroll & Savor — project instructions

Project-specific instructions for any Claude Code session working in this
repo. These apply in addition to (and where more specific, take precedence
within this repo over) any global/user-level instructions.

## SEO & AI-discoverability — mandatory for every page

**Every page created in this repo — glossary entries, blog/monthly posts,
landing pages, anything added later — must follow
[`docs/seo-standards.md`](docs/seo-standards.md), which points to the
canonical global standard at `~/.claude/SEO-GEO-STANDARDS.md`.** This is
not optional polish; treat it the same as the brand voice rules or the
human-review-gate policy that already govern this project.

The short version (full detail, reasoning, and a pre-ship checklist in the
doc itself):

- Unique title + meta description per page, drawn from real page data.
- Canonical URL, complete Open Graph tags, Twitter Card tags.
- Schema.org JSON-LD structured data, matched to the actual page type
  (`Organization` for airlines, `Article` for posts, `BreadcrumbList`
  everywhere there's a clear hierarchy).
- One `<h1>`, logical heading nesting, no skipped levels.
- Content leads with the direct fact, sourced and dated where the fact is
  time-sensitive — this is also already the house brand voice ("numbers do
  the persuading"), so it's rarely extra work, just discipline.
- Stay fully static/server-rendered — no content gated behind
  client-side JS, since several major AI crawlers don't execute it.
- `sitemap.xml`, `robots.txt`, and `llms.txt` are all generated
  automatically by `site/scripts/build.py` from the actual built pages —
  never hand-edit them, and never let a new section skip being included
  (check `build.py`'s `url_paths` list and `write_llms_txt` cover it).

When building a genuinely new page *type* (not a new instance of an
existing one), run the "Before shipping a new page type" checklist in
`docs/seo-standards.md` before considering it done.

## Other durable references

- [`docs/growth-plan.md`](docs/growth-plan.md) — site IA, monetization
  plan, SEO glossary scope/sequencing, news pipeline plan.
- [`brand/stroll-savor-ci-guide.html`](brand/stroll-savor-ci-guide.html) —
  the Field Notes brand system (colors, type, voice). Source of truth for
  anything visual or tonal; if this file and any other doc disagree, this
  one wins.
- [`site/README.md`](site/README.md), [`content/README.md`](content/README.md),
  [`scraper/README.md`](scraper/README.md) — how each subsystem's build/
  deploy pipeline actually works.
