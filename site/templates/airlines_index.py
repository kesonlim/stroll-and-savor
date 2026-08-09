"""Airline glossary index: /airlines/. Currently tier 1 only (Star
Alliance members flying to/from Changi) -- see docs/growth-plan.md for
the tiering plan toward all 86 Changi airlines."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402

STYLE = """
  main { max-width: 900px; margin: 0 auto; padding: 3rem 1.75rem 6rem; }
  main h1 { margin-bottom: 0.6rem; }
  main > p { max-width: 62ch; margin-bottom: 2.4rem; }
  .airline-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px,1fr)); gap: 1rem; }
  .airline-card {
    display: block; text-decoration: none; color: inherit;
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px;
    padding: 1.2rem 1.3rem;
  }
  .airline-card:hover { border-color: var(--rust-soft); }
  .airline-card .iata { font-family: var(--font-data); font-size: 0.72rem; color: var(--rust-text);
    text-transform: uppercase; letter-spacing: 0.08em; }
  .airline-card h2 { font-family: var(--font-display); font-weight: 700; font-size: 1.05rem; margin: 0.3rem 0 0; }
  .airline-card .hub { font-family: var(--font-data); font-size: 0.76rem; color: var(--ink-soft); margin-top: 0.4rem; display: block; }
"""


def render(entries: list) -> str:
    cards = "".join(f"""
    <a class="airline-card" href="{e['slug']}/">
      <span class="iata">{e['iata']}</span>
      <h2>{e['name']}</h2>
      <span class="hub">{e['hub']}</span>
    </a>""" for e in entries)

    body = f"""
    <main>
      <h1>Airlines</h1>
      <p>
        Star Alliance members flying to and from Singapore Changi — the airlines
        most relevant to redeeming and earning KrisFlyer miles. Starting with
        Star Alliance; more of Changi's ~86 airlines to follow.
      </p>
      <div class="airline-grid">{cards}</div>
    </main>"""
    return page(
        title="Airlines — Stroll & Savor",
        description="Star Alliance member airlines flying to and from Singapore Changi, relevant to KrisFlyer miles redemption and earning.",
        body=body,
        asset_prefix="../",
        extra_style=STYLE,
    )
