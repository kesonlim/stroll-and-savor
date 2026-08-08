# Website brand/style instructions

Framework-agnostic CSS tokens for the Stroll & Savor website, derived from
[`stroll-savor-ci-guide.html`](stroll-savor-ci-guide.html) (the brand guide —
treat it as the source of truth if this ever disagrees with it).

## What's here

- **`website-style-guide.css`** — drop-in stylesheet: `@font-face` rules,
  `:root` custom properties for color/type/texture, and base element styles
  (`body`, headings, `p`, `a`) plus a few utility classes (`.card`,
  `.divider-dashed`, `.text-rust`, `.invert`, etc).
- **`fonts/`** — the four self-hosted `.woff2` files the stylesheet points
  to (IBM Plex Sans 400/600, Space Mono 400, Courier Prime 700), extracted
  from the CI guide's embedded base64 so the website doesn't need to hit
  Google Fonts at runtime.

## How to use it

Copy `website-style-guide.css` and `fonts/` into the website project keeping
their relative position to each other (or adjust the `url()` paths in the
`@font-face` blocks), then import the stylesheet before any page-specific
CSS. It's plain CSS custom properties — works with a static site, Next.js
global CSS, Tailwind's `@layer base`, whatever the site ends up built with.

## Rules carried over from the CI guide (don't relitigate these per-page)

- **Five color tokens only** — `--paper`, `--ink`, `--rust`, `--teal`,
  `--rule`. Rust and teal are the only two allowed to carry meaning
  (discount/emphasis vs. secondary data); nothing else introduces a new hue.
- **Rust/teal at full strength are for large type and graphics only**
  (4.2–4.3:1 on paper — under AA for small text). Anywhere either sets text
  below ~18px — eyebrows, tags, section numbers, captions — use the
  text-safe pair (`--rust-text` / `--teal-text`, both 5.5:1+) instead. The
  stylesheet's `.text-rust` / `.text-teal` utilities already point at the
  safe pair; `.fill-rust` / `.fill-teal` are for the full-strength versions.
- **Paper-on-ink is the only sanctioned inversion** (`.invert`), reserved for
  dark UI moments — splash states, video end cards. Never invert to a rust
  or teal background fill.
- **Three typefaces, three fixed jobs** — Courier Prime for display/headlines,
  IBM Plex Sans for body copy, Space Mono for anything that's a number or
  reads like a stamped code (miles, dates, percentages, tags). If a design
  needs a fourth role, one of these three is being used wrong — don't add
  a font.
- **Dot-grid is background texture only** — never behind dense text blocks,
  where it fights legibility.
- **Dashed dividers and the route-line motif are semantic, not decorative** —
  a dashed rule separates a headline from its data; the route line always
  traces an actual route and is always rust.

## Not yet decided

This file only covers tokens — it doesn't pick a framework, hosting, or page
structure for the website itself. That's still open (see the project
[README](../README.md) roadmap).
