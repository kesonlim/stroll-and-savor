# Stroll & Savor — Per-Platform Profile Pictures & Banners

Built from the locked master logo files (`stroll-savor-logo-master.zip`) and
the Field Notes CI guide. Avatars use the **monogram**; banners use the
**wordmark** on the dot-grid paper ground with the route-line motif —
consistent with the CI guide's "Applying the system" table.

## avatars/

| File | Upload as | Platform spec |
|---|---|---|
| `facebook-320.png` | Facebook Page profile picture | 320×320 (displays 170×170) |
| `instagram-320.png` | Instagram profile picture | 320×320 (displays ~110×110, circular) |
| `tiktok-200.png` | TikTok profile picture | 200×200 (circular) |
| `youtube-800.png` | YouTube channel picture | 800×800 (circular) |
| `linkedin-company-300.png` | LinkedIn Company Page logo | 300×300 |
| `linkedin-personal-400.png` | LinkedIn personal profile photo | 400×400 |
| `xiaohongshu-300.png` | Xiaohongshu (小红书) profile picture | ≈300×300 — **unofficial spec, verify in-app before upload** |
| `website-favicon-512.png` | Source for favicon generation | 512×512 master (already also delivered as `favicon.ico` in the logo master zip) |

All avatars are the monogram centered on the paper background color
(`#F1F0EA`) — safe for platforms that composite a circular mask over a
square upload (every platform in this list does).

## banners/

| File | Upload as | Platform spec |
|---|---|---|
| `facebook-cover-820x312.png` | Facebook Page cover photo | 820×312 desktop (640×360 is how mobile crops it — content stays centered so it survives that crop) |
| `youtube-banner-2560x1440.png` | YouTube channel art | 2560×1440 canvas; content is confined to the centered 1546×423 safe area so it's never cut off on any device |
| `linkedin-company-1128x191.png` | LinkedIn Company Page cover | 1128×191 — wordmark only, no tagline (no vertical room) |
| `linkedin-personal-1584x396.png` | LinkedIn personal banner | 1584×396 |
| `website-og-1200x630.png` | Website `<meta property="og:image">` / Twitter card | 1200×630 — this is the generic brand version; the monthly template (task queued) will generate a data-specific one per drop |

## Notes

- Instagram and TikTok have no cover/banner slot at all — profile picture is
  the only static brand surface there; everything else is the monthly
  carousel/story content itself.
- Xiaohongshu has no officially published spec. 300×300 matches how the app
  behaves in practice as of this writing, but confirm inside the app before
  the account actually launches — specs there have changed without notice
  before.
- These are the static, month-to-month-unchanging brand assets. The
  Spontaneous Escapes data itself (routes, miles, dates) lives in the
  monthly artifact/carousel/story templates, not here.
