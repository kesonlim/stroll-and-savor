"""Monthly data for the KrisFlyer Spontaneous Escapes dashboard (strollsavor.com/kfescapes/).

site/data/kfescapes/<YYYY-MM>.json holds one month's sectors exactly as the
source published them (written by kfescapes_fetch.py). This module joins them
with the reference files beside them -- cities.json (region), flights.json
(known SQ schedules), climate.json (10-year daily averages) -- into the four
arrays the dashboard page renders.

Nothing is guessed: a flight number not in flights.json gets no times or
duration (shown as "-" on the page) until someone adds it there.

A month file with an "enriched" key (2026-10, built by hand before this
pipeline existed) already carries the four arrays and is passed through as-is.
"""
import calendar
import datetime
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "kfescapes"
CABINS = ["Economy", "Premium Economy", "Business"]
REGION_ORDER = ["South East Asia", "North Asia", "West Asia & Africa", "Southwest Pacific",
                "Europe", "USA", "Other", "Fifth Freedom"]
MONTH_RE = re.compile(r"(?i)\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b|\b20\d\d\b")


def clean(text) -> str:
    """Scraped text is inserted into the page via innerHTML, so strip anything
    HTML-significant. Route names and blackout lists never legitimately use
    these characters."""
    return re.sub(r"[<>\"'`]", "", str(text)).strip()


def _read(name: str, default=None):
    path = DATA_DIR / name
    return json.loads(path.read_text()) if path.exists() else default


def _region_rank(region: str) -> int:
    return REGION_ORDER.index(region) if region in REGION_ORDER else 99


def month_files() -> list:
    """Month data files, oldest first."""
    return sorted(DATA_DIR.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9].json"))


def resolve_city(cities: dict, name: str):
    """(canonical name, entry or None), following same_as aliases."""
    entry = cities.get(name)
    if entry and "same_as" in entry:
        return entry["same_as"], cities.get(entry["same_as"])
    return name, entry


def parse_blackout(text: str, last_day: int) -> list:
    """'1-3, 8-10, 19 Nov 2026' -> [1, 2, 3, 8, 9, 10, 19]. '-' or empty -> []."""
    if not text or text.strip() in {"-", "–", "—"} or "none" in text.lower():
        return []
    days = set()
    for lo, hi in re.findall(r"(\d{1,2})(?:\s*[-–—]\s*(\d{1,2}))?", MONTH_RE.sub(" ", text)):
        lo = int(lo)
        hi = int(hi) if hi else lo
        days.update(d for d in range(lo, hi + 1) if 1 <= d <= last_day)
    return sorted(days)


def day_ranges(days: list, mon: str) -> str:
    if not days:
        return "None"
    ranges, start, prev = [], days[0], days[0]
    for d in days[1:] + [None]:
        if d is not None and d == prev + 1:
            prev = d
            continue
        ranges.append(f"{start}–{prev} {mon}" if start != prev else f"{start} {mon}")
        if d is not None:
            start = prev = d
    return ", ".join(ranges)


def fmt_dur(minutes):
    if minutes is None:
        return "-"
    return f"{minutes // 60}h {minutes % 60:02d}m"


def schedule_band(times: list) -> str:
    known = sorted(t for t in times if t)
    if not known:
        return "-"
    hour = int(known[0][:2])
    if 5 <= hour < 12:
        return "Morning / Midday"
    if 12 <= hour < 18:
        return "Afternoon / Evening"
    return "Evening / Night"


def describe_climate(c: dict):
    """(weather text, weather_type) from one climate.json month entry.

    Rain is judged on the monthly total: ERA5 counts light drizzle on most
    tropical days, so "wet days" overstates rain, and its sunshine figure
    runs high everywhere -- it's only trusted relative to other cities."""
    high, rain, sun = c["high"], c["rain_mm"], c["sun_ratio"]
    feel = ("Hot" if high >= 30 else "Warm" if high >= 25 else "Mild" if high >= 18
            else "Cool" if high >= 10 else "Cold")
    wet = ("frequent rain" if rain >= 150 else "some rain" if rain >= 80
           else "light rain" if rain >= 30 else "mostly dry")
    if rain >= 150:
        kind = "Rainy"
    elif sun >= 0.7 or rain < 40:
        kind = "Sunny"
    else:
        kind = "Cloudy"
    return f"{feel}, {wet} (~{rain} mm in the month)", kind


def month_context(data: dict) -> dict:
    year, month = map(int, data["travel_month"].split("-"))
    last_day = calendar.monthrange(year, month)[1]
    name = calendar.month_name[month]
    mon = calendar.month_abbr[month]
    book_end = datetime.date.fromisoformat(data["booking_window"]["end"])
    return {
        "slug": data["travel_month"],
        "year": year,
        "month": month,
        "month_name": name,
        "mon": mon,
        "label": f"{name} {year}",
        "last_day": last_day,
        "travel_range": f"1 – {last_day} {mon} {year}",
        "book_by": f"{book_end.day} {calendar.month_abbr[book_end.month]} {book_end.year}",
        "discount": data.get("discount_pct", 30),
    }


def _flight_cells(flight_nos: list, flights: dict):
    """dep_time / arr_time strings in the format the October dashboard used."""
    deps = [flights.get(f, {}).get("dep") for f in flight_nos]
    arrs = [flights.get(f, {}).get("arr") for f in flight_nos]
    if len(flight_nos) == 1:
        return deps[0] or "-", arrs[0] or "-", deps
    dep = ", ".join(f"{f} ({d or '-'})" for f, d in zip(flight_nos, deps))
    arr = ", ".join(f"{f} ({a or '-'})" for f, a in zip(flight_nos, arrs))
    return dep, arr, deps


def _flights_list(flight_nos: list, flights: dict) -> str:
    out = []
    for f in flight_nos:
        dep = flights.get(f, {}).get("dep")
        out.append(f"{f} ({dep})" if dep else f)
    return ", ".join(out)


def enrich(data: dict) -> dict:
    """Month file -> {ctx, rawSectors, rtItineraries, outboundOptions, inboundOptions, ...}."""
    ctx = month_context(data)
    if "enriched" in data:
        return {"ctx": ctx, **data["enriched"], "region_hint": data.get("region_hint", ""),
                "fetched_at": data.get("fetched_at"),
                "climate_note": data["climate_note"], "source_note": data["source_note"],
                "gaps": {}}

    cities = _read("cities.json", {})
    flights = _read("flights.json", {})
    climate = _read("climate.json", {})
    last, mon = ctx["last_day"], ctx["mon"]
    gaps = {"unknown_cities": set(), "unknown_flights": set(), "missing_climate": set()}

    raw = []
    for s in data["sectors"]:
        origin, dest = clean(s["origin"]), clean(s["destination"])
        s = {**s, "blackout": clean(s.get("blackout", "")),
             "cabin": clean(s["cabin"]), "miles": int(s["miles"]),
             "flight_nos": [f for f in s["flight_nos"] if re.fullmatch(r"SQ\d+", f)]}
        if origin == "Singapore":
            direction, city = "Outbound", dest
        elif dest == "Singapore":
            direction, city = "Inbound", origin
        else:
            direction, city = "Fifth Freedom", dest
        canon, entry = resolve_city(cities, city)
        if entry is None:
            gaps["unknown_cities"].add(city)
        region = "Fifth Freedom" if direction == "Fifth Freedom" else (entry or {}).get("region", "Other")

        fnos = s["flight_nos"]
        gaps["unknown_flights"].update(f for f in fnos if f not in flights)
        dep_time, arr_time, deps = _flight_cells(fnos, flights)
        durs = [flights[f]["dur_min"] for f in fnos if flights.get(f, {}).get("dur_min")]
        dur = min(durs) if durs else None

        clim = climate.get(canon, {}).get("months", {}).get(str(ctx["month"]))
        if clim:
            weather, weather_type = describe_climate(clim)
            t_low, t_high = round(clim["low"]), round(clim["high"])
        else:
            gaps["missing_climate"].add(canon)
            weather, weather_type, t_low, t_high = "No climate data yet", "Cloudy", "-", "-"

        bo_days = parse_blackout(s.get("blackout", ""), last)
        valid = [d for d in range(1, last + 1) if d not in bo_days]
        raw.append({
            "region": region,
            "route": f"{origin} to {dest}",
            "origin": origin,
            "destination": dest,
            "direction": direction,
            "cabin": s["cabin"],
            "miles": s["miles"],
            "flight_nos": ", ".join(fnos),
            "dep_time": dep_time,
            "arr_time": arr_time,
            "flight_dur_min": dur,
            "flight_dur_str": fmt_dur(dur),
            "blackout_str": s.get("blackout") if bo_days else "None",
            "blackout_days": bo_days,
            "temp_low": t_low,
            "temp_high": t_high,
            "weather": weather,
            "weather_type": weather_type,
            "pts_per_hr": round(s["miles"] / (dur / 60)) if dur else None,
            "valid_days_count": len(valid),
            "valid_days_str": day_ranges(valid, mon),
            "_city": canon,
            "_deps": deps,
        })

    raw.sort(key=lambda r: (_region_rank(r["region"]), r["_city"], r["direction"] != "Outbound",
                            CABINS.index(r["cabin"]) if r["cabin"] in CABINS else 9, r["miles"]))

    # Round trips: same cabin both ways, plus the October dashboard's
    # "Economy out + Business back" mix.
    legs = {}
    for r in raw:
        if r["direction"] in ("Outbound", "Inbound"):
            legs.setdefault((r["_city"], r["direction"], r["cabin"]), r)
    pairs = [(c, c, "Business Class" if c == "Business" else c, c) for c in CABINS]
    pairs.append(("Economy", "Business", "Mixed (Econ Out + Biz In)", "Mixed"))
    rt_types = CABINS + ["Mixed"]
    rts = []
    for (city, direction, cabin), o in legs.items():
        if direction != "Outbound":
            continue
        for out_cab, in_cab, label, ctype in pairs:
            if cabin != out_cab or (city, "Inbound", in_cab) not in legs:
                continue
            i = legs[(city, "Inbound", in_cab)]
            known = o["flight_dur_min"] and i["flight_dur_min"]
            dur = o["flight_dur_min"] + i["flight_dur_min"] if known else None
            miles = o["miles"] + i["miles"]
            rts.append({
                "destination": o["destination"],
                "region": o["region"],
                "cabin": label,
                "cabin_type": ctype,
                "miles": miles,
                "flight_dur_min": dur,
                "flight_dur_str": fmt_dur(dur),
                "pts_per_hr": round(miles / (dur / 60)) if dur else None,
                "temp_low": o["temp_low"],
                "temp_high": o["temp_high"],
                "weather": o["weather"],
                "weather_type": o["weather_type"],
                "out_schedule": schedule_band(o["_deps"]),
                "out_flights": _flights_list(o["flight_nos"].split(", "), flights),
                "in_schedule": schedule_band(i["_deps"]),
                "in_flights": _flights_list(i["flight_nos"].split(", "), flights),
                "out_bo_days": o["blackout_days"],
                "in_bo_days": i["blackout_days"],
                "notes": (f"Outbound open on {o['valid_days_count']} of {last} days; "
                          f"return open on {i['valid_days_count']} of {last}."),
            })
    rts.sort(key=lambda r: (_region_rank(r["region"]), r["destination"], rt_types.index(r["cabin_type"])))

    def option(r, end_key):
        return {"id": f"{r['route']} [{r['cabin']}]", "route": r["route"], end_key: r[end_key],
                "region": r["region"], "cabin": r["cabin"], "miles": r["miles"],
                "flight_nos": r["flight_nos"], "dep_time": r["dep_time"],
                "duration_min": r["flight_dur_min"], "duration_str": r["flight_dur_str"],
                "blackout_days": r["blackout_days"], "blackout_str": r["blackout_str"],
                "temp_low": r["temp_low"], "temp_high": r["temp_high"], "weather": r["weather"]}

    outbound = [option(r, "destination") for r in raw if r["direction"] == "Outbound"]
    inbound = [option(r, "origin") for r in raw if r["direction"] == "Inbound"]

    rt_regions = {r["region"] for r in rts}
    one_way = [g for g in dict.fromkeys(r["region"] for r in raw)
               if g not in rt_regions and g != "Fifth Freedom"]
    hint = ""
    if one_way:
        hint = (f"{' and '.join(one_way)} fares are one-way only this month, so they appear in the "
                "Full Promotional Flight Network Database and the open-jaw builder, not in the "
                "Two-Way Vacation Planner.")
    if any(r["region"] == "Fifth Freedom" for r in raw):
        hint += (" Fifth-freedom sectors (between two cities outside Singapore, e.g. "
                 "Frankfurt–New York) are listed in the Database only.")

    for r in raw:
        del r["_city"], r["_deps"]

    source_label = {"milelion": "The MileLion's published fare tables",
                    "sia-official": "Singapore Airlines' own promotional page",
                    "onemileatatime": "One Mile at a Time's published fare list"
                    }.get(data.get("source"), "the published fare list")
    return {
        "ctx": ctx,
        "fetched_at": data.get("fetched_at"),
        "rawSectors": raw,
        "rtItineraries": rts,
        "outboundOptions": outbound,
        "inboundOptions": inbound,
        "region_hint": hint.strip(),
        "climate_note": (f"Temperatures are the average daily low and high for {ctx['month_name']}, "
                         "and rain is the average monthly total, all from 2015–2024 daily records "
                         '(<a href="https://open-meteo.com/" rel="noopener" target="_blank">Open-Meteo</a>, '
                         "ERA5 reanalysis, CC BY 4.0). A typical-month guide, not a forecast."),
        "source_note": (f"Fare, mileage, flight-number and blackout data is taken from "
                        f'<a href="{data["source_url"]}" rel="noopener" target="_blank">{source_label}</a> '
                        f"(retrieved {data['fetched_at'][:10]}); flight times come from earlier months' "
                        "published schedules and show as \"-\" where not yet known"),
        "gaps": {k: sorted(v) for k, v in gaps.items()},
    }
