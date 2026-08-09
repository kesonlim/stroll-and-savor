"""Tier-1 airline glossary entries: Star Alliance members flying to/from
Changi (see docs/growth-plan.md, airlines/data/star-alliance-members.json).

Fields sourced from verified data (star-alliance-members.json,
changi-airlines.json) plus hand-authored hub/blurb text. Hub cities are
long-stable, well-known facts (not scraped, not expected to need a
citation) -- Star Alliance join dates and Changi terminal info ARE scraped
and verified, kept exactly as sourced.

Blurb policy (docs/growth-plan.md): one short genuine paragraph in brand
voice per airline -- what's actually useful to know for a KrisFlyer/Star
Alliance redemption angle, not generic "world-class service" marketing
copy. No hype adjectives, no unverifiable time-sensitive claims (award
chart specifics, route counts) that would go stale and violate the
brand's "precision over hype" rule.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

_star = json.loads((DATA_DIR / "star-alliance-members.json").read_text())
_changi = json.loads((DATA_DIR / "changi-airlines.json").read_text())
_changi_by_name = {a["name"]: a for a in _changi["airlines"]}

# name in entries below -> (iata, joined date already in star data, website)
JOINED = {
    "Air Canada": "May 1997", "Air China": "Dec 2007", "Air India": "Jul 2014",
    "Air New Zealand": "May 1999", "All Nippon Airways": "Oct 1999",
    "Asiana Airlines": "Mar 2003", "Ethiopian Airlines": "Dec 2011",
    "EVA Air": "Jun 2013", "Lufthansa": "May 1997", "Shenzhen Airlines": "Nov 2012",
    "Singapore Airlines": "Apr 2000", "Swiss International Air Lines": "Apr 2006",
    "Thai Airways": "May 1997", "Turkish Airlines": "Apr 2008", "United Airlines": "May 1997",
}

CHANGI_TERMINAL = {
    "Air Canada": "T2, Row 12, Door 8", "Air China": "T1, Row 4, Door 1",
    "Air India": "T2, Row 10, Door 7", "Air New Zealand": "T3, Row 8, Door 6",
    "All Nippon Airways": "T2, Row 7-8, Door 5-6", "Asiana Airlines": "T3, Row 8, Door 6",
    "Ethiopian Airlines": "T2, Row 12, Door 8", "EVA Air": "T3, Row 8, Door 6",
    "Lufthansa": "T2, Row 4-5, Door 2", "Shenzhen Airlines": "T1, Row 4, Door 1",
    "Singapore Airlines": "T2, Row 3/5/6, Door 3 & T3, Row 3-4, Door 3",
    "Swiss International Air Lines": "T2, Row 4-5, Door 2", "Thai Airways": "T2, Row 8, Door 6",
    "Turkish Airlines": "T1, Row 9, Door 4", "United Airlines": "T2, Row 1, Door 1",
}

HUB = {
    "Air Canada": "Toronto Pearson",
    "Air China": "Beijing (Capital & Daxing)",
    "Air India": "Delhi & Mumbai",
    "Air New Zealand": "Auckland",
    "All Nippon Airways": "Tokyo Haneda & Narita",
    "Asiana Airlines": "Seoul Incheon",
    "Ethiopian Airlines": "Addis Ababa",
    "EVA Air": "Taipei Taoyuan",
    "Lufthansa": "Frankfurt & Munich",
    "Shenzhen Airlines": "Shenzhen",
    "Singapore Airlines": "Singapore Changi",
    "Swiss International Air Lines": "Zurich & Geneva",
    "Thai Airways": "Bangkok Suvarnabhumi",
    "Turkish Airlines": "Istanbul",
    "United Airlines": "Chicago O'Hare, Houston, Newark, San Francisco (multi-hub)",
}

BLURB = {
    "Air Canada": "Air Canada's own frequent-flyer currency is Aeroplan, but as a Star Alliance partner its wide Canadian and US network is most useful redeeming KrisFlyer miles onward from a North American gateway.",
    "Air China": "China's flag carrier — mainly relevant as a same-alliance connector into interior Chinese cities Singapore Airlines doesn't serve directly.",
    "Air India": "A Star Alliance member since 2014, useful for onward connections across India's domestic network beyond SIA's own India routes.",
    "Air New Zealand": "The natural Star Alliance connector onward from Australia/NZ gateways into the Pacific and New Zealand's domestic network.",
    "All Nippon Airways": "ANA's first and business class cabins are frequently cited among the strongest Star Alliance redemptions available, and it runs the widest domestic Japan network of any Star Alliance carrier.",
    "Asiana Airlines": "A Star Alliance anchor in Korea, useful for onward domestic Korean connections beyond Incheon.",
    "Ethiopian Airlines": "Africa's largest Star Alliance network by a wide margin — the default connector for onward African itineraries booked with KrisFlyer miles.",
    "EVA Air": "Taiwan's Star Alliance carrier, hubbed at Taipei Taoyuan — a common short-to-mid-haul redemption from Singapore with a well-regarded business class product.",
    "Lufthansa": "Star Alliance's founding European anchor — the most common connector for onward continental Europe itineraries redeemed with KrisFlyer miles.",
    "Shenzhen Airlines": "A newer Star Alliance member (joined 2012), covering secondary Chinese cities that neither SIA nor Air China reach directly.",
    "Singapore Airlines": "The reason this site exists — SIA's own KrisFlyer program is the frequent-flyer currency every list here is priced in.",
    "Swiss International Air Lines": "Part of the Lufthansa Group, hubbed at Zurich and Geneva — a clean connector into the Alps and a Star Alliance mainstay in Central Europe.",
    "Thai Airways": "A near-neighbour Star Alliance carrier, useful for onward connections across Thailand and mainland Southeast Asia.",
    "Turkish Airlines": "One of the largest route networks in Star Alliance — Istanbul is a genuine one-stop connector to much of Europe, the Middle East, and Africa.",
    "United Airlines": "The widest Star Alliance footprint across North America — the default connector for onward US domestic itineraries.",
}


def slug(name: str) -> str:
    return (
        name.lower()
        .replace(" & ", "-")
        .replace("'", "")
        .replace(" ", "-")
    )


def build_entries() -> list:
    entries = []
    for name in _star["tier_1_at_changi"]:
        changi = _changi_by_name.get("SWISS International Airlines" if name == "Swiss International Air Lines" else name)
        entries.append({
            "name": name,
            "slug": slug(name),
            "iata": changi["iata"] if changi else None,
            "star_alliance_joined": JOINED[name],
            "changi_terminal": CHANGI_TERMINAL[name],
            "hub": HUB[name],
            "website": _star["member_websites"][name],
            "blurb": BLURB[name],
        })
    return entries


if __name__ == "__main__":
    for e in build_entries():
        print(f"{e['slug']:32} {e['iata']:3} {e['name']}")
