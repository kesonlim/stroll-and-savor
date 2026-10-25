"""KrisFlyer Spontaneous Escapes master dashboard, one page per travel month.

Restyled onto the Singapore Airlines corporate palette (Midnight Royal Blue /
California Gold), deliberately NOT the Stroll & Savor / Field Notes brand
system used elsewhere on the site. Does not reproduce SIA's "Bird of Gold"
logo or batik pattern -- generic motif and typographic homage only.

Layout and behaviour live in kfescapes/dashboard_body.html + dashboard.css
(split out of the original October 2026 page); {{TOKENS}} in the body are
filled per month from site/scripts/kfescapes_data.enrich(). build.py writes
every month to /singapore-airlines/spontaneous-escapes/<YYYY-MM>/dashboard/
and the newest month to /kfescapes/ as well.
"""
import html
import json
from pathlib import Path

from chrome import SITE_URL

_DIR = Path(__file__).resolve().parent / "kfescapes"
BODY = (_DIR / "dashboard_body.html").read_text()
STYLE = (_DIR / "dashboard.css").read_text()
SE_PATH = "singapore-airlines/spontaneous-escapes"

EXTRA_STYLE = """
    .archive-banner { background: #FFF7E6; border: 1px solid var(--sq-gold); border-radius: 10px;
      padding: 12px 16px; margin-bottom: 16px; font-size: 14px; color: var(--text-main); }
    .archive-banner a { color: var(--sq-navy); font-weight: 700; }
    .month-nav { margin-top: 18px; font-size: 13px; color: var(--text-muted); text-align: center; }
    .month-nav a { color: var(--sq-navy); }
    .month-nav b { color: var(--text-main); }
    .static-fares { margin-top: 18px; background: var(--card-bg); border: 1px solid var(--border);
      border-radius: 8px; padding: 10px 16px; font-size: 13px; }
    .static-fares summary { cursor: pointer; font-weight: 700; color: var(--sq-navy); }
    .static-fares table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12.5px; }
    .static-fares th, .static-fares td { text-align: left; padding: 5px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }
    .static-fares .static-wrap { overflow-x: auto; }
"""

CABIN_LABELS = {"Economy": "Economy", "Premium Economy": "Premium Economy",
                "Business": "Business Class", "Mixed": "Mixed (Econ Out + Biz In)"}
REGION_LABELS = {"South East Asia": "South East Asia", "North Asia": "North Asia (China / HK / TW / JP / KR)",
                 "West Asia & Africa": "West Asia & Africa", "Southwest Pacific": "Southwest Pacific / Australia",
                 "Europe": "Europe", "USA": "United States", "Other": "Other",
                 "Fifth Freedom": "Fifth-freedom (non-Singapore) sectors"}


def page_path(slug: str) -> str:
    return f"{SE_PATH}/{slug}/dashboard/"


def _js(value) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def _options(values: list, labels: dict) -> str:
    return "\n            ".join(
        f'<option value="{html.escape(v)}">{html.escape(labels.get(v, v))}</option>' for v in values)


def _static_fares(d: dict) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(r['route'])}</td><td>{html.escape(r['cabin'])}</td>"
        f"<td>{r['miles']:,}</td><td>{html.escape(r['flight_nos'])}</td>"
        f"<td>{html.escape(r['blackout_str'])}</td>"
        "</tr>"
        for r in d["rawSectors"])
    return (f'<details class="static-fares"><summary>Text version: all {len(d["rawSectors"])} '
            f'{html.escape(d["ctx"]["label"])} fares in one list</summary><div class="static-wrap"><table>'
            "<thead><tr><th>Route</th><th>Cabin</th><th>Miles (one-way)</th><th>Flights</th>"
            f"<th>Blackout dates</th></tr></thead><tbody>\n{rows}\n</tbody></table></div></details>")


def _month_nav(months: list, current: str, latest: str) -> str:
    links = []
    for m in months:
        href = "/kfescapes/" if m["slug"] == latest else "/" + page_path(m["slug"])
        links.append(f"<b>{m['label']}</b>" if m["slug"] == current else f'<a href="{href}">{m["label"]}</a>')
    return '<nav class="month-nav" aria-label="Other months">Every month: ' + " &middot; ".join(links) + "</nav>"


def render(d: dict, months: list, latest: dict, canonical_path: str) -> str:
    """d: kfescapes_data.enrich() output. months: [{slug, label}] oldest first.
    latest: the newest month's ctx. canonical_path: e.g. 'kfescapes/'."""
    ctx = d["ctx"]
    is_latest = ctx["slug"] == latest["slug"]
    raw, rts = d["rawSectors"], d["rtItineraries"]
    cabins_present = [c for c in ["Economy", "Premium Economy", "Business"] if any(r["cabin"] == c for r in raw)]
    cabin_opts = cabins_present + (["Mixed"] if any(r["cabin_type"] == "Mixed" for r in rts) else [])
    regions = list(dict.fromkeys(r["region"] for r in raw))

    banner = ""
    if not is_latest:
        banner = (f'<div class="archive-banner" role="note">Booking for these {ctx["label"]} fares closed on '
                  f'{ctx["book_by"]}. <a href="/kfescapes/">See the {latest["label"]} Spontaneous Escapes '
                  "&rarr;</a></div>")
    hint = f'<p class="region-hint">{html.escape(d["region_hint"])}</p>' if d["region_hint"] else ""

    tokens = {
        "MONTH_LABEL": ctx["label"], "MONTH_NAME": ctx["month_name"], "MON": ctx["mon"],
        "MON_UPPER": ctx["mon"].upper(), "LAST_DAY": str(ctx["last_day"]),
        "TRAVEL_RANGE": ctx["travel_range"], "BOOK_BY": ctx["book_by"], "DISCOUNT": str(ctx["discount"]),
        "N_SECTORS": str(len(raw)), "N_ITINERARIES": str(len(rts)),
        "N_DESTINATIONS": str(len({r["destination"] for r in rts})),
        "RAWSECTORS": _js(raw), "RTITINERARIES": _js(rts),
        "OUTBOUNDOPTIONS": _js(d["outboundOptions"]), "INBOUNDOPTIONS": _js(d["inboundOptions"]),
        "REGION_OPTIONS": _options(regions, REGION_LABELS), "CABIN_OPTIONS": _options(cabin_opts, CABIN_LABELS),
        "REGION_HINT": hint, "CLIMATE_NOTE": d["climate_note"], "SOURCE_NOTE": d["source_note"],
        "ARCHIVE_BANNER": banner, "STATIC_FARES": _static_fares(d),
        "MONTH_NAV": _month_nav(months, ctx["slug"], latest["slug"]),
    }
    body = BODY
    for k, v in tokens.items():
        body = body.replace("{{" + k + "}}", v)
    assert "{{" not in body, body[body.index("{{"):body.index("{{") + 40]

    cabin_words = ", ".join(cabins_present[:-1]) + (" and " if len(cabins_present) > 1 else "") + cabins_present[-1]
    title = f"KrisFlyer Spontaneous Escapes {ctx['label']} | Master Dashboard"
    desc = (f"All {len(raw)} Singapore Airlines KrisFlyer Spontaneous Escapes fares for {ctx['label']} "
            f"({cabin_words}), with blackout-date checking, filters and an open-jaw route builder.")
    canonical = f"{SITE_URL}/{canonical_path}"
    page = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc,
            "url": canonical, "isPartOf": {"@type": "WebSite", "name": "Stroll & Savor", "url": f"{SITE_URL}/"}}
    if d.get("fetched_at"):
        page["dateModified"] = d["fetched_at"][:10]
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Stroll & Savor", "item": f"{SITE_URL}/"},
        {"@type": "ListItem", "position": 2, "name": "Spontaneous Escapes", "item": f"{SITE_URL}/{SE_PATH}/"},
        {"@type": "ListItem", "position": 3, "name": f"{ctx['label']} dashboard", "item": canonical},
    ]}
    e = html.escape
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="KrisFlyer Spontaneous Escapes Tracker">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<script type="application/ld+json">{_js([page, crumbs])}</script>
<style>
{STYLE}
{EXTRA_STYLE}
</style>
</head>
<body>
{body}
</body></html>"""
