"""High-resolution editorial image provider for Stroll & Savor.
Implements Option C (Curated stock photography via Unsplash CDN / API)
with automatic local caching, support for live Unsplash API searches,
and graceful fallback to flight & aerial photography (Option B).
"""
import json
import os
import urllib.request
import urllib.parse
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CACHE_FILE = DATA_DIR / "image_cache.json"
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")

# Curated, verified high-resolution editorial photography (Direction B aesthetics)
CURATED_IMAGES = {
    "tokyo": {
        "id": "photo-1503899036084-c55cdd92da26",
        "alt": "Tokyo after dark — glowing lanterns and traditional street alley",
        "photographer": "Jezael Melgoza",
        "city": "Tokyo, Japan",
    },
    "kyoto": {
        "id": "photo-1493976040374-85c8e12f0c0e",
        "alt": "Kyoto morning light along stone pavement and traditional pagodas",
        "photographer": "Sora Sagano",
        "city": "Kyoto, Japan",
    },
    "singapore": {
        "id": "photo-1565967511849-76a60a516170",
        "alt": "Singapore heritage shophouses and historic architecture",
        "photographer": "Victor",
        "city": "Singapore",
    },
    "flight": {
        "id": "photo-1436491865332-7a61a109cc05",
        "alt": "Airplane wing soaring over clouds at sunset — business class travel",
        "photographer": "NASA",
        "city": "Airborne",
    },
    "changi": {
        "id": "photo-1569154941061-e231b4725ef1",
        "alt": "Commercial airliner parked at modern airport terminal gate",
        "photographer": "Unsplash",
        "city": "Singapore Changi Airport",
    },
    "seoul": {
        "id": "photo-1538485399081-7191377e8241",
        "alt": "Vibrant Seoul night market and neon street food alleys",
        "photographer": "Ciaran O'Brien",
        "city": "Seoul, South Korea",
    },
    "frankfurt": {
        "id": "photo-1541872703-74c5e44368f9",
        "alt": "Frankfurt skyline and Main river bridge at dusk",
        "photographer": "Paul Fiedler",
        "city": "Frankfurt, Germany",
    },
    "paris": {
        "id": "photo-1502602898657-3e91760cbb34",
        "alt": "Classic Parisian boulevard and historic stone facades",
        "photographer": "Chris Karidis",
        "city": "Paris, France",
    },
    "sydney": {
        "id": "photo-1506973035872-a4ec16b8e8d9",
        "alt": "Sydney harbour and coastal walking trail at golden hour",
        "photographer": "Dan Freeman",
        "city": "Sydney, Australia",
    },
    "london": {
        "id": "photo-1513635269975-59663e0ac1ad",
        "alt": "London architecture and classic red telephone box in Westminster",
        "photographer": "Heidi Sandstrom",
        "city": "London, United Kingdom",
    },
    "new-york": {
        "id": "photo-1534430480872-3498386e7856",
        "alt": "Manhattan street grid and dusk cityscape",
        "photographer": "Kit Suman",
        "city": "New York, USA",
    },
    "zurich": {
        "id": "photo-1515488764276-beab7607c1e6",
        "alt": "Limmat river and old town architecture in Zurich",
        "photographer": "Henrique Ferreira",
        "city": "Zurich, Switzerland",
    },
    "san-francisco": {
        "id": "photo-1501594907352-04cda38ebc29",
        "alt": "Golden Gate bridge through Pacific sea mist",
        "photographer": "Joseph Barrientos",
        "city": "San Francisco, USA",
    },
    "hong-kong": {
        "id": "photo-1506318137071-a8e063b4bec0",
        "alt": "Victoria Harbour skyline illuminated at dusk",
        "photographer": "Florian Wehde",
        "city": "Hong Kong",
    },
    "bangkok": {
        "id": "photo-1508009603885-50cf7c579365",
        "alt": "Wat Arun temple spire illuminated over Chao Phraya River",
        "photographer": "Aleksandar Pasaric",
        "city": "Bangkok, Thailand",
    },
    "taipei": {
        "id": "photo-1552993873-0dd1110e025f",
        "alt": "Taipei 101 tower viewed from Elephant Mountain trail at sunset",
        "photographer": "Timo Volz",
        "city": "Taipei, Taiwan",
    },
    "rome": {
        "id": "photo-1552832230-c0197dd311b5",
        "alt": "Cobblestone streets and Roman architecture at golden hour",
        "photographer": "David Köhler",
        "city": "Rome, Italy",
    },
    "dubai": {
        "id": "photo-1512453979798-5ea266f8880c",
        "alt": "Dubai architectural skyline and futuristic towers",
        "photographer": "ZQ Lee",
        "city": "Dubai, UAE",
    },
    "doha": {
        "id": "photo-1568322445389-f64ac2515020",
        "alt": "Doha Corniche waterfront and illuminated skyline",
        "photographer": "Radoslaw Prekurat",
        "city": "Doha, Qatar",
    },
    "istanbul": {
        "id": "photo-1524231757912-21f4fe3a7200",
        "alt": "Hagia Sophia and Bosphorus strait at sunset",
        "photographer": "Anna Berdnik",
        "city": "Istanbul, Turkey",
    },
    "auckland": {
        "id": "photo-1507699622108-4be3abd695ad",
        "alt": "Auckland harbour and skyline from the water",
        "photographer": "Dan Freeman",
        "city": "Auckland, New Zealand",
    },
    "toronto": {
        "id": "photo-1507992781348-310259076fa0",
        "alt": "Toronto waterfront and CN Tower silhouette at dusk",
        "photographer": "Scott Webb",
        "city": "Toronto, Canada",
    },
    "delhi": {
        "id": "photo-1587474260584-136574528ed5",
        "alt": "India Gate in New Delhi under warm evening light",
        "photographer": "Raghav Bhasin",
        "city": "Delhi, India",
    },
    "mumbai": {
        "id": "photo-1570168007204-dfb528c6958f",
        "alt": "Gateway of India and waterfront in Mumbai",
        "photographer": "Siddhesh Mangela",
        "city": "Mumbai, India",
    },
    "beijing": {
        "id": "photo-1508804185872-d7badad00f7d",
        "alt": "Traditional historic imperial architecture in Beijing",
        "photographer": "Christian Lue",
        "city": "Beijing, China",
    },
}

KEYWORD_MAPPINGS = {
    # Airports & city codes
    "nrt": "tokyo",
    "hnd": "tokyo",
    "tyo": "tokyo",
    "icn": "seoul",
    "sel": "seoul",
    "fra": "frankfurt",
    "cdg": "paris",
    "syd": "sydney",
    "mel": "sydney",
    "sin": "singapore",
    "lhr": "london",
    "lgw": "london",
    "jfk": "new-york",
    "ewr": "new-york",
    "zrh": "zurich",
    "sfo": "san-francisco",
    "lax": "san-francisco",
    "hkg": "hong-kong",
    "bkk": "bangkok",
    "tpe": "taipei",
    "fco": "rome",
    "dxb": "dubai",
    "doh": "doha",
    "ist": "istanbul",
    "akl": "auckland",
    "yyz": "toronto",
    "del": "delhi",
    "bom": "mumbai",
    "pek": "beijing",
    "pkx": "beijing",
    # Airline hubs & names
    "ana": "tokyo",
    "all nippon": "tokyo",
    "japan airlines": "tokyo",
    "jal": "tokyo",
    "korean air": "seoul",
    "asiana": "seoul",
    "lufthansa": "frankfurt",
    "air france": "paris",
    "british airways": "london",
    "qantas": "sydney",
    "singapore airlines": "flight",
    "sia": "flight",
    "krisflyer": "flight",
    "spontaneous": "flight",
    "swiss": "zurich",
    "cathay": "hong-kong",
    "thai": "bangkok",
    "eva air": "taipei",
    "emirates": "dubai",
    "qatar": "doha",
    "turkish": "istanbul",
    "air new zealand": "auckland",
    "air canada": "toronto",
    "air india": "delhi",
    "air china": "beijing",
    "united": "san-francisco",
    "airlines": "changi",
}


def _load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            pass
    return {}


def _save_cache(cache: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def get_image_url(photo_id: str, width: int = 1200, quality: int = 80) -> str:
    """Build an optimized WebP CDN URL for an Unsplash photo ID."""
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={width}&q={quality}"


def _fetch_from_unsplash_api(query: str) -> dict | None:
    """Fetch a high-res landscape editorial photo using the Unsplash API."""
    if not UNSPLASH_ACCESS_KEY:
        return None
    try:
        url = (
            "https://api.unsplash.com/search/photos?"
            + urllib.parse.urlencode({
                "query": f"{query} travel city street editorial",
                "orientation": "landscape",
                "per_page": 1,
                "client_id": UNSPLASH_ACCESS_KEY,
            })
        )
        req = urllib.request.Request(url, headers={"User-Agent": "StrollAndSavor/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("results", [])
            if results:
                photo = results[0]
                return {
                    "id": photo["id"],
                    "alt": photo.get("alt_description") or f"{query} travel view",
                    "photographer": photo.get("user", {}).get("name", "Unsplash Contributor"),
                    "city": query.title(),
                }
    except Exception:
        pass
    return None


def resolve_image(key: str, width: int = 1200) -> dict:
    """Resolve an editorial image for a city, airline, or route slug."""
    clean_key = key.lower().strip()
    cache = _load_cache()

    if clean_key in cache:
        item = cache[clean_key].copy()
        item["url"] = get_image_url(item["id"], width=width)
        return item

    # Check curated catalog directly
    if clean_key in CURATED_IMAGES:
        item = CURATED_IMAGES[clean_key].copy()
        item["url"] = get_image_url(item["id"], width=width)
        cache[clean_key] = item
        _save_cache(cache)
        return item

    # Check if any curated city name appears in the query string
    for city_name, item_data in CURATED_IMAGES.items():
        if city_name != "flight" and city_name in clean_key:
            item = item_data.copy()
            item["url"] = get_image_url(item["id"], width=width)
            cache[clean_key] = item
            _save_cache(cache)
            return item

    # Check keyword mappings
    for code, mapped_key in KEYWORD_MAPPINGS.items():
        if code in clean_key:
            item = CURATED_IMAGES.get(mapped_key, CURATED_IMAGES["flight"]).copy()
            item["url"] = get_image_url(item["id"], width=width)
            cache[clean_key] = item
            _save_cache(cache)
            return item

    # If API key is available, query Unsplash
    api_result = _fetch_from_unsplash_api(clean_key)
    if api_result:
        api_result["url"] = get_image_url(api_result["id"], width=width)
        cache[clean_key] = api_result
        _save_cache(cache)
        return api_result

    # Fallback to flight/aerial view
    fallback = CURATED_IMAGES["flight"].copy()
    fallback["url"] = get_image_url(fallback["id"], width=width)
    return fallback
