# Monthly extraction procedure

Run this on the 15th of each month, **or the next working day if the 15th
falls on a weekend** — per MileLion's own SEAT-tool writeup, SIA's release
cadence has this exception built in, and it applies to August 2026's cycle
specifically (the 15th is a Saturday, so the reveal may land on the 17th
instead). The scheduled cloud routine (see `scraper/README.md`'s "Scheduled
routine" section) covers this by firing across the 15th–18th, not just the
15th–16th. This doc is the literal prompt/checklist that routine follows —
read it top to bottom, in order, and stop at the first step that succeeds.

## Source order (decided 2026-08-08, see project history for the reasoning)

1. **SIA official page** (primary) — first-party, fastest possible, but
   unvalidated against unattended cloud execution as of this writing.
2. **MileLion** (fallback) — reliably same-day, clean tables, `robots.txt`
   allows fetching article pages.
3. **One Mile at a Time** (second fallback) — same allowance, used only if
   both of the above fail or disagree badly.

Every run must record which tier actually produced the data (`source` field
in the output — see `schema.json`), so drift in reliability is visible over
time rather than silently masked.

## Steps

1. **Fetch SIA's page with a rendering browser, not a raw HTTP client.**
   URL: `https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/kf-promo/kfescapes/`
   Use a tool that executes JS and renders the DOM (e.g. the Browser MCP /
   Playwright-equivalent available in this environment) — a bare `curl`/
   `requests` fetch is expected to be blocked by the WAF in front of this
   AEM site and should not be attempted.

2. **Check whether this month's list is actually live.** The page shows a
   placeholder ("...will be revealed soon... catch us again mid of this
   month...") when between cycles. If that placeholder text is present,
   the reveal hasn't happened yet:
   - Retry every ~2 hours for the rest of the day.
   - If still not revealed by end of day, retry once more the following
     morning.
   - If still not revealed after 48h total, stop and fall back to step 4
     (do not wait indefinitely — SIA's cadence could shift).

3. **If the list is live**, read the rendered page content and extract
   every business-class row into the `schema.json` shape. Set
   `"source": "sia-official"`. Skip to step 6.

4. **Fallback: fetch MileLion.** Search `milelion.com` for this month's
   "KrisFlyer Spontaneous Escapes for [travel month] announced" post
   (published the 15th of the prior month). **The full route table is not
   in the article's page text** — MileLion embeds it as a Flourish
   visualisation iframe (`Business & Economy Class` table). Do not rely on
   the article prose ("My picks for this month"), which only lists a
   partial highlight selection.

   To get the full table (confirmed working 2026-08-08, see
   `scraper/samples/2026-08.json`):
   1. Load the article in a rendering browser and find the two
      `flo.uri.sh/visualisation/<id>/embed` iframe URLs via
      `document.querySelectorAll('iframe')` — the one whose surrounding
      heading says "Business & Economy Class" is the one that matters
      (there's a second, separate one for Premium Economy).
   2. Fetch `https://flo.uri.sh/visualisation/<id>/embed?auto=1` directly
      (plain HTTP fetch is fine for this endpoint — it's Flourish's CDN,
      not SIA's WAF).
   3. In that HTML, find the third inline `<script>` block and extract the
      `_Flourish_data = {...}` object (balanced-brace scan — it's a JS
      object literal, not strict JSON, though in practice the `rows` value
      itself parses as JSON). Columns are
      `["Route", "Economy", "Flight Nos.", "Blackout", "Business", "Flight Nos.", "Blackout"]`
      — a business-class value of `"-"` means no business award on that
      route this cycle; exclude those rows.
   4. Route strings are formatted `"X to Y"` — split on `" to "` to get
      origin/destination. Watch for city names that could contain "to"
      (none observed so far, but don't assume it'll never happen).

   Set `"source": "milelion"`.

5. **If MileLion also fails or its table looks incomplete** (e.g. fewer
   than ~5 routes, or missing the business-class column entirely), fetch
   the equivalent One Mile at a Time post as a second fallback. Set
   `"source": "onemileatatime"`.

6. **Business-class filter.** Only include rows where the source explicitly
   shows a business-class miles figure. Routes offered only in economy/
   premium economy for that cycle are excluded from `deals`, not zeroed out.

7. **Write the output** as JSON matching `scraper/schema.json`, saved to
   `scraper/samples/<travel_month>.json` (e.g. `scraper/samples/2026-09.json`).

8. **Human review gate.** Do not feed this output into any newsletter/
   carousel/story template automatically. Notify the project owner that the
   extract is ready for a quick glance, with the source tier and route count
   in the notification (e.g. "12 business-class routes extracted from
   sia-official for Sept 2026 travel — ready to review").

## Failure handling

If every source in the chain fails (step 5 also fails, or nothing resembling
the promotion is found anywhere after the 48h retry window): stop, do not
guess or fabricate data, and notify the project owner directly that this
month's automated pull failed and needs a manual check.

## Known open risk

Step 1's reliability against an unattended, scheduled (non-interactive)
cloud execution has not yet been proven — it worked in an interactive
session (see `scraper/samples/` test run), but WAF behavior can differ for
traffic with no prior session/cookies. Track actual monthly outcomes in
`scraper/run-log.md` (source tier used each month) — if `sia-official`
fails repeatedly, demote it below MileLion in the order rather than keep
retrying a path that doesn't work in practice.
