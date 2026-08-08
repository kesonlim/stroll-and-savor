# Scraper

Monthly extraction of Singapore Airlines KrisFlyer Spontaneous Escapes
business-class deals, feeding the newsletter/carousel/story content
pipeline (see project [README](../README.md)).

## How it works

This isn't a traditional selector-based scraper — it's an agentic procedure
(`PROCEDURE.md`) run by Claude on a schedule, because:

- The primary source (SIA's own page) is a WAF-protected AEM site with no
  JSON API — extraction has to read rendered content, and needs to
  gracefully detect "not revealed yet" vs. a real parsing failure.
- The fallback source (MileLion) changes its table markup between posts
  occasionally — an LLM reading the table is more resilient to that than
  brittle CSS selectors.
- Every run is followed by a human review gate before anything downstream
  gets touched (see `PROCEDURE.md` step 8) — so extraction accuracy is
  backstopped either way, and it's worth spending that margin on format
  resilience rather than selector maintenance.

## Files

- **`PROCEDURE.md`** — the actual step-by-step instructions the scheduled
  routine follows: source order (SIA official → MileLion → One Mile at a
  Time), reveal-detection logic, business-class filtering, failure
  handling. Read this first.
- **`schema.json`** — JSON Schema for the output shape.
- **`samples/`** — extraction outputs, one per travel month
  (`<YYYY-MM>.json`). Includes manual test runs, not just scheduled fires.
- **`run-log.md`** — which source tier actually produced each month's data,
  tracked over time so `sia-official`'s real-world reliability is visible.

## Source order — why, briefly

Decided 2026-08-08 after weighing direct-scrape risk against the priority
of matching or beating MileLion's own publish speed:

1. SIA's page is stable and reused every month (confirmed), and its reveal
   cadence lines up with MileLion's own posting pattern (dated the 15th).
2. A raw HTTP scrape of SIA's page is expected to be blocked by its WAF; a
   rendering-browser fetch is not, based on interactive testing — but that
   hasn't been proven yet against unattended, cookie-less scheduled
   execution. Track this in `run-log.md`; demote `sia-official` in the
   order if it fails repeatedly in practice.
3. MileLion and One Mile at a Time both explicitly allow fetching article
   pages per `robots.txt`, publish same-day, and (for MileLion, confirmed)
   expose the full route table as structured data via an embedded Flourish
   visualisation rather than requiring prose parsing.

## Status

- [x] Source order decided and documented
- [x] Output schema defined
- [x] MileLion fallback tier built and tested end-to-end (`samples/2026-08.json`)
- [ ] SIA-official primary tier — not yet tested against a live (revealed)
      cycle; next reveal is expected mid-August 2026
- [ ] One Mile at a Time second-fallback tier — not yet needed/tested
- [ ] Scheduled cloud routine (RemoteTrigger) — procedure is written and
      ready to register, holding off on actually creating the recurring
      trigger until reviewed
