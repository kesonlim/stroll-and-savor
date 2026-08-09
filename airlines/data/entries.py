"""Airline glossary entries, tiers 1 and 2 (see docs/growth-plan.md):
Star Alliance, oneworld, and SkyTeam members flying to/from Changi.

Fields sourced from verified data (star-alliance-members.json,
oneworld-skyteam-members.json, changi-airlines.json -- including Changi
terminal, now stored centrally there rather than duplicated here) plus
hand-authored hub/blurb text. Hub cities are long-stable, well-known facts
(not scraped, not expected to need a citation) -- alliance join dates and
Changi terminal info ARE scraped/verified, kept exactly as sourced.
Star Alliance join dates were captured during tier-1 research; oneworld/
SkyTeam join dates were not (would need another research pass) -- so tier-2
entries show alliance membership without a join date rather than a
fabricated one.

Blurb policy (docs/growth-plan.md): one short genuine paragraph in brand
voice per airline -- what's actually useful to know for a KrisFlyer/
alliance redemption angle, not generic "world-class service" marketing
copy. No hype adjectives, no unverifiable time-sensitive claims (award
chart specifics, route counts) that would go stale and violate the
brand's "precision over hype" rule.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

_star = json.loads((DATA_DIR / "star-alliance-members.json").read_text())
_ow_st = json.loads((DATA_DIR / "oneworld-skyteam-members.json").read_text())
_changi = json.loads((DATA_DIR / "changi-airlines.json").read_text())
_changi_by_name = {a["name"]: a for a in _changi["airlines"]}

# Changi's name for a given entry, where it differs from the alliance
# site's own naming.
CHANGI_NAME_OVERRIDE = {
    "Swiss International Air Lines": "SWISS International Airlines",
}

ALLIANCE = {}
for _n in _star["tier_1_at_changi"]:
    ALLIANCE[_n] = "Star Alliance"
for _e in _ow_st["oneworld_at_changi"]:
    ALLIANCE[_e["name"]] = "oneworld"
for _e in _ow_st["skyteam_at_changi"]:
    ALLIANCE[_e["name"]] = "SkyTeam"

JOINED = {
    "Air Canada": "May 1997", "Air China": "Dec 2007", "Air India": "Jul 2014",
    "Air New Zealand": "May 1999", "All Nippon Airways": "Oct 1999",
    "Asiana Airlines": "Mar 2003", "Ethiopian Airlines": "Dec 2011",
    "EVA Air": "Jun 2013", "Lufthansa": "May 1997", "Shenzhen Airlines": "Nov 2012",
    "Singapore Airlines": "Apr 2000", "Swiss International Air Lines": "Apr 2006",
    "Thai Airways": "May 1997", "Turkish Airlines": "Apr 2008", "United Airlines": "May 1997",
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
    "British Airways": "London Heathrow",
    "Cathay Pacific": "Hong Kong",
    "Fiji Airways": "Nadi",
    "Finnair": "Helsinki",
    "Japan Airlines": "Tokyo Haneda & Narita",
    "Malaysia Airlines": "Kuala Lumpur",
    "Oman Air": "Muscat",
    "Qantas Airways": "Sydney, Melbourne, Brisbane & Perth (multi-hub)",
    "Qatar Airways": "Doha",
    "SriLankan Airlines": "Colombo",
    "Air France": "Paris Charles de Gaulle",
    "China Airlines": "Taipei Taoyuan",
    "China Eastern Airlines": "Shanghai",
    "Garuda Indonesia": "Jakarta & Denpasar",
    "KLM Royal Dutch Airlines": "Amsterdam Schiphol",
    "Korean Air": "Seoul Incheon",
    "Saudia Airlines": "Jeddah & Riyadh",
    "Vietnam Airlines": "Hanoi & Ho Chi Minh City",
    "Xiamen Airlines": "Xiamen",
}

WEBSITE = {
    **_star["member_websites"],
    "British Airways": "https://www.britishairways.com/",
    "Cathay Pacific": "https://www.cathaypacific.com/",
    "Fiji Airways": "https://www.fijiairways.com/",
    "Finnair": "https://www.finnair.com/",
    "Japan Airlines": "https://www.jal.com/en/",
    "Malaysia Airlines": "https://www.malaysiaairlines.com/",
    "Oman Air": "https://www.omanair.com/",
    "Qantas Airways": "https://www.qantas.com/",
    "Qatar Airways": "https://www.qatarairways.com/",
    "SriLankan Airlines": "https://www.srilankan.com/",
    "Air France": "https://www.airfrance.com/",
    "China Airlines": "https://www.china-airlines.com/",
    "China Eastern Airlines": "https://www.ceair.com/",
    "Garuda Indonesia": "https://www.garuda-indonesia.com/",
    "KLM Royal Dutch Airlines": "https://www.klm.com/",
    "Korean Air": "https://www.koreanair.com/",
    "Saudia Airlines": "https://www.saudia.com/",
    "Vietnam Airlines": "https://www.vietnamairlines.com/",
    "Xiamen Airlines": "https://www.xiamenair.com/",
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
    "British Airways": "oneworld's UK anchor — the default connector for onward continental Europe and UK domestic itineraries via Heathrow.",
    "Cathay Pacific": "Hong Kong's flag carrier and a longtime oneworld member — a strong short-haul pick from Singapore with a well-regarded business class product.",
    "Fiji Airways": "The direct route into Fiji and the wider South Pacific on this list — a oneworld member covering a niche none of the other airlines here reach.",
    "Finnair": "The natural oneworld connector into Northern Europe via Helsinki, historically positioned as a fast polar route between Asia and Europe.",
    "Japan Airlines": "JAL's premium cabins are frequently mentioned in the same breath as ANA's (Star Alliance) — between the two, Tokyo is well covered regardless of which alliance a KrisFlyer redemption favours.",
    "Malaysia Airlines": "The closest oneworld hub to Singapore, useful for onward connections across Malaysia and into oneworld's wider network.",
    "Oman Air": "A smaller Gulf carrier in oneworld, useful mainly as a connector into Oman itself rather than a major onward hub.",
    "Qantas Airways": "oneworld's Australian anchor — the default connector for onward Australian domestic itineraries.",
    "Qatar Airways": "One of oneworld's largest route networks — Doha is a genuine one-stop connector to much of Europe, Africa, and the Americas, and its business class is frequently cited as a benchmark redemption.",
    "SriLankan Airlines": "A near-neighbour oneworld carrier, useful for onward connections across Sri Lanka and South India.",
    "Air France": "SkyTeam's French anchor, sister carrier to KLM under the same parent group — the most common SkyTeam connector for onward continental Europe.",
    "China Airlines": "Taiwan's SkyTeam option, a direct alternative to EVA Air (Star Alliance) on the same Taipei route.",
    "China Eastern Airlines": "SkyTeam's Shanghai anchor, useful for onward connections across eastern China.",
    "Garuda Indonesia": "Indonesia's flag carrier and SkyTeam's Southeast Asian anchor, useful for onward connections across the Indonesian archipelago beyond what SIA and Scoot serve directly.",
    "KLM Royal Dutch Airlines": "Air France's sister carrier under the same group — the other common SkyTeam connector into continental Europe, via Amsterdam.",
    "Korean Air": "SkyTeam's Korean anchor, sharing Incheon with Star Alliance's Asiana Airlines — the two carriers are in the process of merging.",
    "Saudia Airlines": "Saudi Arabia's flag carrier, useful mainly as a connector into the Kingdom rather than a major onward hub for this audience.",
    "Vietnam Airlines": "A near-neighbour SkyTeam carrier, useful for onward connections across Vietnam beyond SIA's own direct routes.",
    "Xiamen Airlines": "A regional SkyTeam option covering a Chinese city Singapore Airlines doesn't serve directly.",
}

TIER = {}
for _n in _star["tier_1_at_changi"]:
    TIER[_n] = 1
for _e in _ow_st["oneworld_at_changi"] + _ow_st["skyteam_at_changi"]:
    TIER[_e["name"]] = 2


def slug(name: str) -> str:
    return (
        name.lower()
        .replace(" & ", "-")
        .replace("'", "")
        .replace(" ", "-")
    )


def build_entries() -> list:
    names = list(_star["tier_1_at_changi"])
    names += [e["name"] for e in _ow_st["oneworld_at_changi"]]
    names += [e["name"] for e in _ow_st["skyteam_at_changi"]]

    entries = []
    for name in names:
        changi_name = CHANGI_NAME_OVERRIDE.get(name, name)
        changi = _changi_by_name[changi_name]
        entries.append({
            "name": name,
            "slug": slug(name),
            "iata": changi["iata"],
            "alliance": ALLIANCE[name],
            "alliance_joined": JOINED.get(name),
            "changi_terminal": changi["changi_terminal"],
            "hub": HUB[name],
            "website": WEBSITE[name],
            "blurb": BLURB[name],
            "tier": TIER[name],
        })
    return entries


if __name__ == "__main__":
    for e in build_entries():
        print(f"tier{e['tier']} {e['slug']:32} {e['iata']:3} {e['alliance']:14} {e['name']}")
