"""Fetches one month of KrisFlyer Spontaneous Escapes fares (all cabins) for the
dashboard at strollsavor.com/kfescapes/, and fills in climate averages for any
destination that doesn't have them yet.

Usage:
    python3 site/scripts/kfescapes_fetch.py 2026-11
    python3 site/scripts/kfescapes_fetch.py 2026-11 --source-url <MileLion article> --flourish 30470106,30470108

The MileLion article URL, booking/travel windows and discount default to
scraper/samples/<YYYY-MM>.json (written earlier by the monthly extraction
routine, see scraper/PROCEDURE.md). Flourish table ids default to every
flourish visualisation embedded in that article; each table's own title must
name the month being fetched, so a stale table from last month is rejected.

Writes site/data/kfescapes/<YYYY-MM>.json and updates climate.json, then
prints what the dashboard will still show as "-" (unknown flight numbers,
cities missing from cities.json). Those are warnings, not failures -- the
month still publishes.
"""
import argparse
import calendar
import datetime
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kfescapes_data  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = kfescapes_data.DATA_DIR
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
CABIN_HEADERS = {"business": "Business", "premium economy": "Premium Economy", "py": "Premium Economy",
                 "economy": "Economy"}


def get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def balanced_json(html: str, marker: str) -> dict:
    """JSON object literal right after `marker`, found by brace matching (the
    embed isn't valid JSON as a whole, and the object holds nested braces)."""
    start = html.index("{", html.index(marker) + len(marker))
    depth, in_str, esc = 0, False, False
    for j in range(start, len(html)):
        c = html[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(html[start:j + 1])
    raise ValueError(f"unbalanced JSON after {marker!r}")


def fetch_table(vid: str, month_label: str) -> tuple:
    html = get(f"https://flo.uri.sh/visualisation/{vid}/embed?auto=1")
    title = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
    title = title.group(1).strip() if title else ""
    if month_label.lower() not in title.lower():
        raise SystemExit(f"Flourish {vid} is titled {title!r}, not {month_label} -- stale or wrong table")
    header = balanced_json(html, "_Flourish_data_column_names =")["rows"]["columns"][1]
    cabin = CABIN_HEADERS.get(header.strip().lower())
    if cabin is None:
        m = re.search(r"\(([^)]+)\)\s*$", title)
        cabin = CABIN_HEADERS.get((m.group(1) if m else "").strip().lower())
    if cabin is None:
        raise SystemExit(f"Flourish {vid}: can't tell the cabin from column {header!r} / title {title!r}")
    sectors = []
    for r in balanced_json(html, "_Flourish_data =")["rows"]:
        cols = r.get("columns", [])
        if len(cols) < 2 or " to " not in str(cols[0]) or not str(cols[1]).strip():
            continue
        origin, dest = (x.strip() for x in str(cols[0]).split(" to ", 1))
        fnos = re.findall(r"SQ\s*\d+", str(cols[2]) if len(cols) > 2 else "")
        sectors.append({
            "origin": origin,
            "destination": dest,
            "cabin": cabin,
            "miles": int(re.sub(r"[^\d]", "", str(cols[1]))),
            "flight_nos": [f.replace(" ", "") for f in fnos],
            "blackout": str(cols[3]).strip() if len(cols) > 3 and cols[3] else "-",
        })
    return {"flourish_id": vid, "title": title, "cabin": cabin, "rows": len(sectors)}, sectors


def default_windows(travel_month: str) -> dict:
    year, month = map(int, travel_month.split("-"))
    prev = datetime.date(year, month, 1) - datetime.timedelta(days=1)
    return {
        "booking_window": {"start": prev.replace(day=15).isoformat(), "end": prev.isoformat()},
        "travel_window": {"start": f"{travel_month}-01",
                          "end": f"{travel_month}-{calendar.monthrange(year, month)[1]:02d}"},
    }


def climate_for(lat: float, lon: float) -> dict:
    """12 monthly averages from 2015-2024 daily records (Open-Meteo archive, ERA5)."""
    url = ("https://archive-api.open-meteo.com/v1/archive"
           f"?latitude={lat}&longitude={lon}&start_date=2015-01-01&end_date=2024-12-31"
           "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,sunshine_duration,daylight_duration"
           "&timezone=auto")
    for attempt in range(4):
        try:
            d = json.loads(get(url, timeout=90))["daily"]
            break
        except urllib.error.HTTPError as e:
            # Free tier is rate-limited per minute; a 10-year pull is a heavy call.
            if e.code != 429 or attempt == 3:
                raise
            time.sleep(65)
    acc = {m: {"hi": [], "lo": [], "wet": 0, "rain": 0.0, "sun": 0.0, "day": 0.0} for m in range(1, 13)}
    for i, day in enumerate(d["time"]):
        a = acc[int(day[5:7])]
        if d["temperature_2m_max"][i] is not None:
            a["hi"].append(d["temperature_2m_max"][i])
            a["lo"].append(d["temperature_2m_min"][i])
        a["rain"] += d["precipitation_sum"][i] or 0
        if (d["precipitation_sum"][i] or 0) >= 1:
            a["wet"] += 1
        a["sun"] += d["sunshine_duration"][i] or 0
        a["day"] += d["daylight_duration"][i] or 0
    return {str(m): {"low": round(sum(a["lo"]) / len(a["lo"]), 1),
                     "high": round(sum(a["hi"]) / len(a["hi"]), 1),
                     "rain_mm": round(a["rain"] / 10),
                     "wet_days": round(a["wet"] / 10, 1),
                     "sun_ratio": round(a["sun"] / a["day"], 2) if a["day"] else 0}
            for m, a in acc.items()}


def fill_climate(cities_needed: set) -> None:
    path = DATA_DIR / "climate.json"
    climate = json.loads(path.read_text()) if path.exists() else {}
    cities = json.loads((DATA_DIR / "cities.json").read_text())
    for name in sorted(cities_needed):
        canon, entry = kfescapes_data.resolve_city(cities, name)
        if canon in climate or not entry or "lat" not in entry:
            continue
        try:
            months = climate_for(entry["lat"], entry["lon"])
        except (urllib.error.URLError, KeyError, ValueError) as e:
            print(f"WARNING climate lookup failed for {canon} ({e}); its weather shows as missing")
            continue
        climate[canon] = {"lat": entry["lat"], "lon": entry["lon"],
                          "source": "Open-Meteo historical weather API (ERA5), daily 2015-2024, CC BY 4.0",
                          "months": months}
        print(f"  climate: added {canon}")
        path.write_text(json.dumps(climate, indent=1, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("travel_month", help="YYYY-MM")
    ap.add_argument("--source-url")
    ap.add_argument("--flourish", help="comma-separated Flourish visualisation ids")
    args = ap.parse_args()

    ym = args.travel_month
    year, month = map(int, ym.split("-"))
    label = f"{calendar.month_name[month]} {year}"
    sample_path = REPO_ROOT / "scraper" / "samples" / f"{ym}.json"
    sample = json.loads(sample_path.read_text()) if sample_path.exists() else {}
    source_url = args.source_url or sample.get("source_url")
    if not source_url:
        raise SystemExit(f"No --source-url and no source_url in {sample_path}")

    if args.flourish:
        ids = [x.strip() for x in args.flourish.split(",") if x.strip()]
    else:
        ids = list(dict.fromkeys(re.findall(r"(?:flo\.uri\.sh|public\.flourish\.studio)/visualisation/(\d+)",
                                            get(source_url))))
    if not ids:
        raise SystemExit(f"No Flourish tables found in {source_url} -- pass --flourish ids")

    tables, sectors = [], []
    for vid in ids:
        meta, rows = fetch_table(vid, label)
        tables.append(meta)
        sectors.extend(rows)
        print(f"  {meta['cabin']}: {meta['rows']} sectors (Flourish {vid})")
    if not sectors:
        raise SystemExit("Tables fetched but no sectors parsed")

    windows = default_windows(ym)
    data = {
        "travel_month": ym,
        "source": "milelion",
        "source_url": source_url,
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "booking_window": sample.get("booking_window", windows["booking_window"]),
        "travel_window": sample.get("travel_window", windows["travel_window"]),
        "discount_pct": sample.get("discount_pct", 30),
        "tables": tables,
        "sectors": sectors,
    }
    out = DATA_DIR / f"{ym}.json"
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {out.relative_to(REPO_ROOT)} ({len(sectors)} sectors)")

    needed = {s["destination"] if s["origin"] == "Singapore" else s["origin"] for s in sectors}
    needed |= {s["destination"] for s in sectors if "Singapore" not in (s["origin"], s["destination"])}
    fill_climate(needed)

    gaps = kfescapes_data.enrich(data)["gaps"]
    for key, what in [("unknown_cities", "cities missing from cities.json (region 'Other', no weather)"),
                      ("missing_climate", "cities with no climate data"),
                      ("unknown_flights", "flight numbers with no known times (shown as '-')")]:
        if gaps[key]:
            print(f"WARNING {len(gaps[key])} {what}: {', '.join(gaps[key])}")


if __name__ == "__main__":
    main()
