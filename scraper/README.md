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
      cycle; next reveal is expected mid-August 2026 (this routine's first
      live fire)
- [ ] One Mile at a Time second-fallback tier — not yet needed/tested
- [x] Scheduled cloud routine (RemoteTrigger) — live as of 2026-08-08

## Scheduled routine

- **Name**: `⚡ SS_Escapes_Monthly_Extract` (id `trig_01QhQcNpgm11HAxTdwE98dw8`)
- **Cron**: `20 1,2,3,4,5,6 15,16,17,18 * *` (UTC) — fires hourly, 9:20am
  through 2:20pm Singapore time, on the **15th through 18th** of each
  month.
- **Why days 15–18, not just 15–16**: MileLion's own SEAT-tool writeup
  states SIA releases "on the 15th of each month, **or the next working
  day**." All three of our reference data points (May/June/July 2026
  reveals) happened to land on weekdays, so that rule was untested until
  now — **August 15, 2026 is a Saturday**, so this routine's very first
  live fire is also the first real test of the weekend-shift behavior. Day
  range 15–18 covers every possible shift case: a Sunday 15th shifts to
  Monday the 16th; a Saturday 15th shifts to Monday the 17th; an 18th
  buffer day covers a Monday public holiday stacking on top of a weekend
  15th. Each fire is idempotent (no-ops once `samples/<travel_month>.json`
  exists for the month), so the extra days/hours cost nothing but a quick
  no-op check.
- **Why hourly, not every 30 min**: the platform enforces a 1-hour minimum
  fire interval per trigger; every-30-min was rejected outright by the API.
- **Timing basis — a proxy, not confirmed**: the 9am–2:20pm SGT window is
  based on MileLion's article `datePublished` timestamps (11:34, 11:38,
  11:47 SGT across three past reveals) — that's when the *blogger* posted
  after noticing the page change, not a first-party SIA timestamp. Actual
  SIA reveal time could be earlier. Wayback Machine access is blocked in
  this environment, so this couldn't be verified more precisely; treat the
  window as a best-effort estimate and widen it in `run-log.md` if actual
  fires show the reveal happening outside it.
- **Notifications**: push, on completion of every fire (including no-ops) —
  this is the cue for the human review gate (`PROCEDURE.md` step 8).
- **First live fire**: 2026-08-15, 09:20 SGT.
