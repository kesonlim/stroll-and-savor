"""
Picks the featured routes for carousel/story content: best 3 distinct-city
routes per region, ranked by an internal miles-per-flight-hour value
heuristic.

The duration figures below are approximate typical SIA block times sourced
from general route knowledge, not from the extraction schema (which only
carries route/miles/dates/flight-numbers — see scraper/schema.json). They
exist ONLY to rank candidates against each other within a region; never
surface them as a displayed fact in generated content, since the brand's
"precision over hype" voice principle (see brand/stroll-savor-ci-guide.html
section 01) requires only verified numbers in anything user-facing.
"""
import json
import sys
from pathlib import Path

# Approximate one-way block hours, Singapore-origin. Deliberately excludes
# Los Angeles-Tokyo: a 5th-freedom oddity that isn't a "from Singapore"
# escape and doesn't fit any region bucket below.
ROUTE_HOURS = {
    "Denpasar": 2.583,
    "Jakarta": 1.75,
    "Kuala Lumpur": 1.083,
    "Medan": 1.333,
    "Surabaya": 2.167,
    "Bangkok": 2.333,
    "Hanoi": 2.917,
    "Phuket": 1.667,
    "Manila": 3.667,
    "Ho Chi Minh City": 1.75,
    "Hangzhou": 4.667,
    "Hong Kong": 3.917,
    "Beijing": 6.333,
    "Beijing Daxing": 6.333,
    "Shanghai": 5.083,
    "Ahmedabad": 5.667,
    "Chennai": 3.667,
    "Colombo": 3.5,
    "Dhaka": 3.833,
    "Cairns": 6.083,
}

REGION_OF = {
    "Denpasar": "Southeast Asia", "Jakarta": "Southeast Asia",
    "Kuala Lumpur": "Southeast Asia", "Medan": "Southeast Asia",
    "Surabaya": "Southeast Asia", "Bangkok": "Southeast Asia",
    "Hanoi": "Southeast Asia", "Phuket": "Southeast Asia",
    "Manila": "Southeast Asia", "Ho Chi Minh City": "Southeast Asia",
    "Hangzhou": "North Asia", "Hong Kong": "North Asia",
    "Beijing": "North Asia", "Beijing Daxing": "North Asia",
    "Shanghai": "North Asia",
    "Ahmedabad": "South Asia", "Chennai": "South Asia",
    "Colombo": "South Asia", "Dhaka": "South Asia",
    "Cairns": "Oceania",
}

REGION_ORDER = ["Southeast Asia", "North Asia", "South Asia", "Oceania"]


FOLD_CITY = {
    # Same city, different airport code -- fold so it only claims one
    # region slot instead of crowding out a genuinely distinct city.
    "Beijing Daxing": "Beijing",
}


def city_of(deal):
    """The non-Singapore endpoint of a route, regardless of direction."""
    raw = deal["destination"] if deal["origin"] == "Singapore" else deal["origin"]
    return FOLD_CITY.get(raw, raw)


def curate(deals, per_region=3):
    """Return up to `per_region` best-value distinct cities per region,
    each represented by one deal record (direction doesn't matter for
    display purposes since miles are identical both ways in this dataset)."""
    by_city = {}
    for d in deals:
        city = city_of(d)
        if city not in ROUTE_HOURS:
            continue  # unmapped (e.g. Los Angeles-Tokyo) -- excluded on purpose
        if city not in by_city:
            by_city[city] = d

    scored = []
    for city, d in by_city.items():
        value = d["miles"] / ROUTE_HOURS[city]
        scored.append((value, city, d))
    scored.sort(key=lambda t: t[0])

    picks = {r: [] for r in REGION_ORDER}
    for value, city, d in scored:
        region = REGION_OF[city]
        if len(picks[region]) < per_region:
            picks[region].append(d)

    return picks


def group_all_by_region(deals):
    """Every deal (both directions, nothing deduped), grouped by region and
    sorted by miles ascending within each region -- for the text-dense web
    artifact, which lists everything rather than a curated top set."""
    groups = {r: [] for r in REGION_ORDER}
    groups["Other"] = []
    for d in deals:
        region = REGION_OF.get(city_of(d), "Other")
        groups.setdefault(region, []).append(d)
    for region in groups:
        groups[region].sort(key=lambda d: d["miles"])
    return groups


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not src:
        print("usage: curate.py <scraper/samples/YYYY-MM.json>", file=sys.stderr)
        sys.exit(1)
    data = json.loads(src.read_text())
    picks = curate(data["deals"])
    total = 0
    for region in REGION_ORDER:
        print(f"\n{region}")
        for d in picks[region]:
            total += 1
            print(f"  {d['route_label']:30} {d['miles']:>7,} mi")
    print(f"\n{total} routes selected")
