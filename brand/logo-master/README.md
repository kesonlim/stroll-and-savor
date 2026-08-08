# Stroll & Savor — Master Logo File Set

Locked system: **Field Notes** — dot-grid paper `#F1F0EA`, pencil ink `#2E2E2C`,
route rust `#B4552F`, map teal `#3E7C74`. Wordmark and monogram both set in
**Courier Prime Bold**, converted to true vector outlines (no font dependency —
these files open and print correctly with zero font installed).

## Two marks, two jobs

- **Wordmark** (`stroll & savor`) — the primary logo. Use it anywhere there's
  room to set it in full: website header, banners, long-form content, video
  end cards.
- **Monogram** (`s&s`) — the avatar-only mark. Use it wherever the surface is
  small and circular/square: profile pictures, favicons, app icons. It will
  not read cleanly as literal text below ~24px on screen — that's expected
  even from real brands; if a specific placement needs to work at 16px,
  consider falling back to a single lowercase "s" set the same way.

Don't invent a third mark or stretch one into the other's job — that split is
the whole point of having two assets.

## File map

```
svg/                                   Vector masters (font-independent, infinitely scalable)
  wordmark-ink-on-transparent.svg      Primary — ink text, transparent background
  wordmark-paper-on-transparent.svg    For dark backgrounds — paper-colored text, transparent bg
  wordmark-ink-on-paper.svg            Ink text, opaque paper background baked in
  wordmark-paper-on-ink.svg            Paper text, opaque ink background baked in
  monogram-ink-on-transparent.svg      Same four variants, for the "s&s" monogram
  monogram-paper-on-transparent.svg
  monogram-ink-on-paper.svg
  monogram-paper-on-ink.svg

png/                                   Raster exports, rendered from the SVGs at 2x+ the target size
  wordmark-transparent-w{2400,1200,800,400}.png          Ink wordmark, transparent, for light backgrounds
  wordmark-transparent-w{2400,1200,800,400}-forDark.png  Paper wordmark, transparent, for dark backgrounds
  wordmark-on-paper-w1600.png                            Opaque paper background baked in
  wordmark-on-ink-w1600.png                               Opaque ink background baked in
  avatar-transparent-{1024,512,320,200,180,32,16}.png     Monogram, transparent background
  avatar-on-paper-{...}.png                                Monogram, opaque paper background baked in
  avatar-on-ink-{...}.png                                  Monogram, opaque ink background baked in

favicon.ico                            16/32/48/64px multi-resolution, ink-on-ink-background monogram
```

## Usage rules

- **Clear space**: keep empty space around either mark equal to at least the
  height of the wordmark's lowercase "s" on every side. Don't crowd it against
  edges or other content.
- **Minimum size**: wordmark shouldn't run narrower than ~120px wide on
  screen. Monogram shouldn't run smaller than ~24px — below that, switch to
  the single-"s" fallback described above.
- **Backgrounds**: use the transparent variants whenever the destination
  surface's own background is known and correct (website, template
  designed for it). Use the "-on-paper" / "-on-ink" baked-background variants
  only when you need a flat, self-contained image file with no possibility of
  the background disappearing (e.g. pasting into a doc or slide).
- **Color**: never recolor the ampersand away from rust, and never render the
  wordmark or monogram in any color outside the locked palette above.
- **Don't**: stretch, skew, rotate, add a drop shadow/outline, or set the
  wordmark in a different weight/typeface than the one baked into these
  vectors.

## Regenerating or extending

Masters were built by converting Courier Prime Bold glyphs to path outlines
with `fontTools`, then rasterized via headless Chromium. If new sizes or
color variants are needed later, regenerate from the SVGs in `svg/` rather
than re-rastering from an existing PNG, to avoid compounding quality loss.
