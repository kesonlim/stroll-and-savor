# Run log

Tracks which source tier actually produced each month's extract, so drift in
`sia-official`'s reliability (see `PROCEDURE.md`'s "known open risk") is
visible over time rather than silently masked. Update on every run,
including manual test runs.

| Date | Travel month | Source used | Routes | Notes |
|---|---|---|---|---|
| 2026-08-08 | 2026-08 | milelion (test) | 37 | Manual test run, not a scheduled fire. SIA's own page was between reveal cycles (showed the "revealed soon" placeholder for Sept) so step 1–2 of `PROCEDURE.md` were exercised but step 3 (live SIA extraction) is still unvalidated. Fallback to MileLion worked cleanly via its embedded Flourish table — see `samples/2026-08.json`. |
| 2026-08-15 | 2026-09 | **none — failed** | 0 | First live scheduled fire. New failure mode not previously anticipated: this scheduled/cloud session's network egress proxy returned a hard 403 (org policy denial, confirmed via `/__agentproxy/status` → `recentRelayFailures`, kind `connect_rejected`) for **all three** source domains — `www.singaporeair.com`, `milelion.com`, and `onemileatatime.com` — plus the Flourish CDN (`flo.uri.sh`) that tier 2's table-extraction step depends on. This is not the SIA-WAF risk `PROCEDURE.md` flagged (that was about tier 1 only, and about JS-rendering not raw fetches) — it's a broader allowlist-style block on this session that stops every tier including the two proven-working ones. Confirmed via WebSearch (which does not go through this proxy) that the promotion **has** already been revealed (MileLion article dated 2026-08-14, "Singapore Airlines KrisFlyer Spontaneous Escapes for September 2026 announced"; booking by 31 Aug 2026, travel 1–30 Sep 2026, 30% off) — so this is a real access failure, not a "not yet revealed" wait case. Did not fabricate a `deals` table from WebSearch's prose summary since it lacks per-route business-class miles figures. No `samples/2026-09.json` written; content generation (step 6) skipped. Needs either a network-policy allowlist fix for this environment, or a manual interactive run. |
