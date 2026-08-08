"""Blog index: chronological list of every published monthly post."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402

STYLE = """
  main { max-width: 900px; margin: 0 auto; padding: 3rem 1.75rem 6rem; }
  main h1 { margin-bottom: 0.6rem; }
  main > p { max-width: 60ch; margin-bottom: 2.4rem; }
  .post-card {
    display: block; text-decoration: none; color: inherit;
    padding: 1.8rem 0; border-bottom: 1px solid var(--rule);
  }
  .post-card .eyebrow { font-family: var(--font-data); font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--rust-text); display: block; margin-bottom: 0.5rem; }
  .post-card h2 { font-family: var(--font-display); font-weight: 700; font-size: 1.4rem; margin: 0 0 0.4rem; }
  .post-card .meta { font-family: var(--font-data); font-size: 0.8rem; color: var(--ink-soft); }
"""


def render(posts: list) -> str:
    """`posts` newest first: [{slug, eyebrow, title, meta}, ...]"""
    cards = "".join(f"""
    <a class="post-card" href="{p['slug']}/">
      <span class="eyebrow">{p['eyebrow']}</span>
      <h2>{p['title']}</h2>
      <span class="meta">{p['meta']}</span>
    </a>""" for p in posts)

    body = f"""
    <main>
      <h1>Blog</h1>
      <p>The full Spontaneous Escapes business-class list, published monthly — straight from the source, no editorializing.</p>
      {cards}
    </main>"""
    return page(
        title="Blog — Stroll & Savor",
        description="Every monthly Spontaneous Escapes business-class list, published as close to Singapore Airlines' own reveal as we can manage.",
        body=body,
        asset_prefix="../",
        extra_style=STYLE,
    )
