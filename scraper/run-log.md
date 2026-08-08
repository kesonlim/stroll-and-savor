# Run log

Tracks which source tier actually produced each month's extract, so drift in
`sia-official`'s reliability (see `PROCEDURE.md`'s "known open risk") is
visible over time rather than silently masked. Update on every run,
including manual test runs.

| Date | Travel month | Source used | Routes | Notes |
|---|---|---|---|---|
| 2026-08-08 | 2026-08 | milelion (test) | 37 | Manual test run, not a scheduled fire. SIA's own page was between reveal cycles (showed the "revealed soon" placeholder for Sept) so step 1–2 of `PROCEDURE.md` were exercised but step 3 (live SIA extraction) is still unvalidated. Fallback to MileLion worked cleanly via its embedded Flourish table — see `samples/2026-08.json`. |
