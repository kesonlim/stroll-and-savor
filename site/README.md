# Site

The public Stroll & Savor site: landing page + blog, deployed to Cloudflare
Pages at `strollsavor.thethinkthank.com`.

## Build

```
python3 site/scripts/build.py
```

Reads every `scraper/samples/*.json`, builds one blog post per travel month
plus a blog index and the landing page (which features the latest post),
into `site/dist/` — a fully static, self-contained directory (brand CSS and
fonts copied in from `brand/`, no external requests at runtime).

## Deploy

```
npx wrangler pages deploy site/dist --project-name stroll-and-savor
```

Cloudflare Pages project: **stroll-and-savor**, account `kesonlim@gmail.com`.
Production URL: `https://stroll-and-savor.pages.dev` (also reachable at
`strollsavor.thethinkthank.com` once the custom domain is attached — see
below).

**Custom domain**: `wrangler pages domain add` doesn't exist in the
installed wrangler version (4.120.0), and the direct Cloudflare API call
requires extracting the stored OAuth credential, which Claude Code's
auto-mode safety classifier blocks outright as a raw-credential-handling
pattern (reasonably so). Attach it manually instead: Cloudflare dashboard →
Workers & Pages → **stroll-and-savor** → Custom domains → add
`strollsavor.thethinkthank.com`. One-time step, ~30 seconds.

## Structure

- `templates/chrome.py` — shared header/nav/footer wrapping every page.
- `templates/landing.py` — the landing page (hero, "what this is", latest
  post callout, how-it-works). Content proposal and rationale live in
  project chat history (2026-08-09); update this file's docstring if that
  becomes stale.
- `templates/blog_index.py` — chronological post listing.
- `templates/blog_post.py` — wraps `content/templates/web_artifact.py`'s
  `render_content` (the same full route-list content used for the
  standalone artifact in `content/posts/`) in site chrome, rather than
  duplicating that rendering logic.
- `scripts/build.py` — orchestrates everything above into `site/dist/`.
- `dist/` — build output, committed for the same reason `content/posts/`
  is: transparency/reproducibility of what's actually live. Regenerate with
  `build.py` rather than hand-editing.

## What's NOT here

- **No newsletter/mailing list** — doesn't exist yet, out of scope until
  one does.
- **No social publishing** — Instagram/etc carousel and story content
  lives in `content/posts/<month>/`, downloaded and posted manually. See
  that folder's `caption.txt` / `*.caption.txt` files for proposed post
  copy.
- **No auto-deploy** — a new month's data landing (via the scheduled
  extraction routine) does not automatically rebuild or redeploy this
  site. Run `build.py` + `wrangler pages deploy` by hand after reviewing
  new content, consistent with the human-review-gate policy the rest of
  this project follows.
