import urllib.request
import re
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = REPO_ROOT / "site" / "templates"

CITY_METADATA = {
    "Bangkok": {"region": "South East Asia", "dur_min": 145, "dur_str": "2h 25m", "low": 24, "high": 31, "w": "Mostly Sunny / Dry", "wt": "Sunny"},
    "Brunei": {"region": "South East Asia", "dur_min": 130, "dur_str": "2h 10m", "low": 24, "high": 32, "w": "Partly Cloudy / Showers", "wt": "Cloudy"},
    "Da Nang": {"region": "South East Asia", "dur_min": 165, "dur_str": "2h 45m", "low": 22, "high": 27, "w": "Tropical Showers", "wt": "Rainy"},
    "Denpasar": {"region": "South East Asia", "dur_min": 165, "dur_str": "2h 45m", "low": 24, "high": 31, "w": "Sunny / Warm", "wt": "Sunny"},
    "Denpasar (Bali)": {"region": "South East Asia", "dur_min": 165, "dur_str": "2h 45m", "low": 24, "high": 31, "w": "Sunny / Warm", "wt": "Sunny"},
    "Hanoi": {"region": "South East Asia", "dur_min": 200, "dur_str": "3h 20m", "low": 19, "high": 26, "w": "Pleasant / Mild", "wt": "Cloudy"},
    "Ho Chi Minh City": {"region": "South East Asia", "dur_min": 130, "dur_str": "2h 10m", "low": 23, "high": 31, "w": "Partly Cloudy / Warm", "wt": "Sunny"},
    "Jakarta": {"region": "South East Asia", "dur_min": 110, "dur_str": "1h 50m", "low": 24, "high": 33, "w": "Sunny / Warm", "wt": "Sunny"},
    "Kuala Lumpur": {"region": "South East Asia", "dur_min": 65, "dur_str": "1h 05m", "low": 24, "high": 32, "w": "Afternoon Showers", "wt": "Rainy"},
    "Manila": {"region": "South East Asia", "dur_min": 225, "dur_str": "3h 45m", "low": 24, "high": 30, "w": "Partly Cloudy", "wt": "Cloudy"},
    "Medan": {"region": "South East Asia", "dur_min": 90, "dur_str": "1h 30m", "low": 23, "high": 31, "w": "Tropical Showers", "wt": "Rainy"},
    "Penang": {"region": "South East Asia", "dur_min": 85, "dur_str": "1h 25m", "low": 24, "high": 31, "w": "Afternoon Showers", "wt": "Rainy"},
    "Phnom Penh": {"region": "South East Asia", "dur_min": 125, "dur_str": "2h 05m", "low": 23, "high": 30, "w": "Pleasant / Sunny", "wt": "Sunny"},
    "Phuket": {"region": "South East Asia", "dur_min": 110, "dur_str": "1h 50m", "low": 24, "high": 31, "w": "Tropical Showers", "wt": "Rainy"},
    "Siem Reap": {"region": "South East Asia", "dur_min": 135, "dur_str": "2h 15m", "low": 23, "high": 31, "w": "Dry / Sunny", "wt": "Sunny"},
    "Surabaya": {"region": "South East Asia", "dur_min": 145, "dur_str": "2h 25m", "low": 25, "high": 34, "w": "Sunny / Hot", "wt": "Sunny"},
    "Beijing": {"region": "North Asia", "dur_min": 375, "dur_str": "6h 15m", "low": 0, "high": 10, "w": "Crisp Late Autumn", "wt": "Sunny"},
    "Chengdu": {"region": "North Asia", "dur_min": 295, "dur_str": "4h 55m", "low": 9, "high": 16, "w": "Overcast Cool", "wt": "Cloudy"},
    "Chongqing": {"region": "North Asia", "dur_min": 305, "dur_str": "5h 05m", "low": 11, "high": 17, "w": "Mild Autumn", "wt": "Cloudy"},
    "Hangzhou": {"region": "North Asia", "dur_min": 310, "dur_str": "5h 10m", "low": 8, "high": 17, "w": "Autumn Foliage", "wt": "Sunny"},
    "Hong Kong": {"region": "North Asia", "dur_min": 240, "dur_str": "4h 00m", "low": 19, "high": 25, "w": "Pleasant / Sunny", "wt": "Sunny"},
    "Shanghai": {"region": "North Asia", "dur_min": 320, "dur_str": "5h 20m", "low": 9, "high": 17, "w": "Crisp / Sunny", "wt": "Sunny"},
    "Shenzhen": {"region": "North Asia", "dur_min": 245, "dur_str": "4h 05m", "low": 17, "high": 25, "w": "Pleasant / Clear", "wt": "Sunny"},
    "Xiamen": {"region": "North Asia", "dur_min": 275, "dur_str": "4h 35m", "low": 15, "high": 23, "w": "Mild Autumn", "wt": "Sunny"},
    "Taipei": {"region": "North Asia", "dur_min": 280, "dur_str": "4h 40m", "low": 18, "high": 24, "w": "Mild Showers", "wt": "Cloudy"},
    "Tokyo": {"region": "North Asia", "dur_min": 420, "dur_str": "7h 00m", "low": 9, "high": 17, "w": "Autumn Foliage", "wt": "Sunny"},
    "Ahmedabad": {"region": "West Asia & Africa", "dur_min": 340, "dur_str": "5h 40m", "low": 16, "high": 32, "w": "Warm Dry Season", "wt": "Sunny"},
    "Colombo": {"region": "West Asia & Africa", "dur_min": 230, "dur_str": "3h 50m", "low": 24, "high": 30, "w": "Intermonsoon Showers", "wt": "Rainy"},
    "Dhaka": {"region": "West Asia & Africa", "dur_min": 250, "dur_str": "4h 10m", "low": 18, "high": 29, "w": "Dry / Pleasant", "wt": "Sunny"},
    "Male": {"region": "West Asia & Africa", "dur_min": 285, "dur_str": "4h 45m", "low": 25, "high": 30, "w": "Tropical / Clear", "wt": "Sunny"},
    "Adelaide": {"region": "Southwest Pacific", "dur_min": 440, "dur_str": "7h 20m", "low": 14, "high": 25, "w": "Warm Late Spring", "wt": "Sunny"},
    "Brisbane": {"region": "Southwest Pacific", "dur_min": 490, "dur_str": "8h 10m", "low": 18, "high": 28, "w": "Warm Spring", "wt": "Sunny"},
    "Cairns": {"region": "Southwest Pacific", "dur_min": 400, "dur_str": "6h 40m", "low": 23, "high": 31, "w": "Warm Tropical Spring", "wt": "Sunny"},
    "Darwin": {"region": "Southwest Pacific", "dur_min": 285, "dur_str": "4h 45m", "low": 25, "high": 33, "w": "Build-up Season", "wt": "Sunny"},
    "Melbourne": {"region": "Southwest Pacific", "dur_min": 470, "dur_str": "7h 50m", "low": 12, "high": 22, "w": "Mild Spring", "wt": "Cloudy"},
    "Perth": {"region": "Southwest Pacific", "dur_min": 320, "dur_str": "5h 20m", "low": 14, "high": 26, "w": "Sunny Spring", "wt": "Sunny"},
    "Sydney": {"region": "Southwest Pacific", "dur_min": 460, "dur_str": "7h 40m", "low": 16, "high": 24, "w": "Pleasant Spring", "wt": "Sunny"},
    "Amsterdam": {"region": "Europe", "dur_min": 810, "dur_str": "13h 30m", "low": 4, "high": 10, "w": "Chilly / Overcast", "wt": "Cloudy"},
    "Brussels": {"region": "Europe", "dur_min": 815, "dur_str": "13h 35m", "low": 4, "high": 10, "w": "Chilly Autumn", "wt": "Cloudy"},
    "Copenhagen": {"region": "Europe", "dur_min": 785, "dur_str": "13h 05m", "low": 3, "high": 8, "w": "Cold Autumn", "wt": "Cloudy"},
    "Frankfurt": {"region": "Europe", "dur_min": 780, "dur_str": "13h 00m", "low": 3, "high": 9, "w": "Chilly / Foggy", "wt": "Cloudy"},
    "Istanbul": {"region": "Europe", "dur_min": 675, "dur_str": "11h 15m", "low": 9, "high": 16, "w": "Cool / Crisp", "wt": "Cloudy"},
    "London (LGW)": {"region": "Europe", "dur_min": 840, "dur_str": "14h 00m", "low": 5, "high": 11, "w": "Chilly / Mist", "wt": "Rainy"},
    "London Gatwick": {"region": "Europe", "dur_min": 840, "dur_str": "14h 00m", "low": 5, "high": 11, "w": "Chilly / Mist", "wt": "Rainy"},
    "London (LHR)": {"region": "Europe", "dur_min": 835, "dur_str": "13h 55m", "low": 5, "high": 11, "w": "Chilly / Mist", "wt": "Rainy"},
    "Milan": {"region": "Europe", "dur_min": 780, "dur_str": "13h 00m", "low": 5, "high": 12, "w": "Cool / Foggy", "wt": "Cloudy"},
    "Munich": {"region": "Europe", "dur_min": 775, "dur_str": "12h 55m", "low": 1, "high": 8, "w": "Chilly Alpine", "wt": "Cloudy"},
    "Paris": {"region": "Europe", "dur_min": 820, "dur_str": "13h 40m", "low": 5, "high": 11, "w": "Chilly Autumn", "wt": "Cloudy"},
    "Rome": {"region": "Europe", "dur_min": 790, "dur_str": "13h 10m", "low": 8, "high": 17, "w": "Mild Autumn", "wt": "Cloudy"},
    "Zurich": {"region": "Europe", "dur_min": 790, "dur_str": "13h 10m", "low": 2, "high": 8, "w": "Crisp / Chilly", "wt": "Cloudy"},
    "Los Angeles": {"region": "USA", "dur_min": 910, "dur_str": "15h 10m", "low": 13, "high": 23, "w": "Mild Autumn", "wt": "Sunny"},
    "New York": {"region": "USA", "dur_min": 525, "dur_str": "8h 45m", "low": 5, "high": 12, "w": "Brisk / Sunny", "wt": "Sunny"},
    "San Francisco": {"region": "USA", "dur_min": 890, "dur_str": "14h 50m", "low": 10, "high": 17, "w": "Mild Autumn", "wt": "Sunny"},
    "Seattle": {"region": "USA", "dur_min": 865, "dur_str": "14h 25m", "low": 5, "high": 11, "w": "Cool Showers", "wt": "Rainy"},
}

def parse_blackout(blackout_str, month_days=30):
    if not blackout_str or 'none' in blackout_str.lower():
        return [], month_days, f'1–{month_days} Nov'
    s = re.sub(r'(?i)\b(november|nov|2026)\b', '', blackout_str).strip().rstrip('.')
    days = set()
    parts = [p.strip() for p in s.split(',') if p.strip()]
    for p in parts:
        m = re.match(r'^(\d+)\s*[\-\–\—]\s*(\d+)$', p)
        if m:
            start, end = int(m.group(1)), int(m.group(2))
            for d in range(start, end + 1):
                if 1 <= d <= month_days:
                    days.add(d)
        else:
            m2 = re.match(r'^(\d+)$', p)
            if m2:
                d = int(m2.group(1))
                if 1 <= d <= month_days:
                    days.add(d)
    b_days = sorted(days)
    v_days = [d for d in range(1, month_days + 1) if d not in days]
    ranges = []
    if v_days:
        r_start = v_days[0]
        r_prev = v_days[0]
        for d in v_days[1:]:
            if d == r_prev + 1:
                r_prev = d
            else:
                ranges.append((r_start, r_prev))
                r_start = d
                r_prev = d
        ranges.append((r_start, r_prev))
    range_strs = [f'{s}–{e} Nov' if s != e else f'{s} Nov' for s, e in ranges]
    v_str = ', '.join(range_strs) if range_strs else 'None'
    return b_days, len(v_days), v_str

def main():
    headers = {'User-Agent': 'Mozilla/5.0'}
    raw_list = []
    tables = [('Business', '30470106'), ('Premium Economy', '30470108'), ('Economy', '30565085')]
    for cabin, vid in tables:
        url = f'https://flo.uri.sh/visualisation/{vid}/embed?auto=1'
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        m = re.search(r'_Flourish_data\s*=\s*(\{.*?\})\s*,\s*\n\s*_Flourish_visualisation_id', html, re.DOTALL)
        if m:
            for r in json.loads(m.group(1)).get('rows', []):
                cols = r.get('columns', [])
                if len(cols) >= 3 and cols[1]:
                    route = cols[0].strip()
                    if ' to ' not in route:
                        continue
                    orig, dest = route.split(' to ', 1)
                    orig = orig.strip()
                    dest = dest.strip()
                    direction = "Outbound" if orig == "Singapore" else "Inbound"
                    city = dest if direction == "Outbound" else orig
                    raw_list.append({
                        "route": route,
                        "origin": orig,
                        "destination": dest,
                        "city": city,
                        "direction": direction,
                        "cabin": cabin,
                        "miles": int(cols[1]),
                        "flight_nos": str(cols[2]).strip() if len(cols) > 2 and cols[2] else "",
                        "blackout": str(cols[3]).strip() if len(cols) > 3 and cols[3] else ""
                    })

    raw_sectors = []
    for s in raw_list:
        city = s["city"]
        meta = CITY_METADATA.get(city, {
            "region": "Other", "dur_min": 180, "dur_str": "3h 00m", "low": 20, "high": 28, "w": "Pleasant", "wt": "Sunny"
        })
        b_days, v_count, v_str = parse_blackout(s["blackout"], month_days=30)
        dur_min = meta["dur_min"]
        pts_per_hr = round(s["miles"] / (dur_min / 60))
        fnos = s["flight_nos"]

        raw_sectors.append({
            "region": meta["region"],
            "route": s["route"],
            "origin": s["origin"],
            "destination": s["destination"],
            "direction": s["direction"],
            "cabin": s["cabin"],
            "miles": s["miles"],
            "flight_nos": fnos,
            "dep_time": fnos if fnos else "Scheduled SQ",
            "arr_time": "Direct",
            "flight_dur_min": dur_min,
            "flight_dur_str": meta["dur_str"],
            "blackout_str": s["blackout"] if s["blackout"] else "No Blackout Dates",
            "blackout_days": b_days,
            "temp_low": meta["low"],
            "temp_high": meta["high"],
            "weather": meta["w"],
            "weather_type": meta["wt"],
            "pts_per_hr": pts_per_hr,
            "valid_days_count": v_count,
            "valid_days_str": v_str
        })

    raw_sectors.sort(key=lambda x: (x["region"], x["destination"], x["direction"] != "Outbound", x["miles"]))

    by_city_cabin = {}
    for s in raw_sectors:
        k = (s["destination"] if s["direction"] == "Outbound" else s["origin"], s["cabin"])
        by_city_cabin.setdefault(k, {"out": [], "in": []})
        if s["direction"] == "Outbound":
            by_city_cabin[k]["out"].append(s)
        else:
            by_city_cabin[k]["in"].append(s)

    rt_itineraries = []
    for (city, cabin), pair in sorted(by_city_cabin.items()):
        if pair["out"] and pair["in"]:
            o = pair["out"][0]
            i = pair["in"][0]
            tot_miles = o["miles"] + i["miles"]
            tot_min = o["flight_dur_min"] + i["flight_dur_min"]
            hrs = tot_min // 60
            mins = tot_min % 60
            dur_str = f"{hrs}h {mins}m" if mins else f"{hrs}h"
            pts_hr = round(tot_miles / (tot_min / 60))

            rt_itineraries.append({
                "destination": city,
                "region": o["region"],
                "cabin": cabin,
                "cabin_type": cabin,
                "miles": tot_miles,
                "flight_dur_min": tot_min,
                "flight_dur_str": dur_str,
                "pts_per_hr": pts_hr,
                "temp_low": o["temp_low"],
                "temp_high": o["temp_high"],
                "weather": o["weather"],
                "weather_type": o["weather_type"],
                "out_schedule": o["dep_time"],
                "out_flights": o["flight_nos"],
                "in_schedule": i["dep_time"],
                "in_flights": i["flight_nos"],
                "notes": f"Out: {o['blackout_str']}. In: {i['blackout_str']}.",
                "blackout_days_out": o["blackout_days"],
                "blackout_days_in": i["blackout_days"]
            })

    outbound_options = []
    for s in raw_sectors:
        if s["direction"] == "Outbound":
            outbound_options.append({
                "id": f"{s['route']} [{s['cabin']}]",
                "route": s["route"],
                "destination": s["destination"],
                "region": s["region"],
                "cabin": s["cabin"],
                "miles": s["miles"],
                "flight_nos": s["flight_nos"],
                "dep_time": s["dep_time"],
                "duration_min": s["flight_dur_min"],
                "duration_str": s["flight_dur_str"],
                "blackout_days": s["blackout_days"],
                "blackout_str": s["blackout_str"],
                "temp_low": s["temp_low"],
                "temp_high": s["temp_high"],
                "weather": s["weather"]
            })

    inbound_options = []
    for s in raw_sectors:
        if s["direction"] == "Inbound":
            inbound_options.append({
                "id": f"{s['route']} [{s['cabin']}]",
                "route": s["route"],
                "origin": s["origin"],
                "region": s["region"],
                "cabin": s["cabin"],
                "miles": s["miles"],
                "flight_nos": s["flight_nos"],
                "dep_time": s["dep_time"],
                "duration_min": s["flight_dur_min"],
                "duration_str": s["flight_dur_str"],
                "blackout_days": s["blackout_days"],
                "blackout_str": s["blackout_str"],
                "temp_low": s["temp_low"],
                "temp_high": s["temp_high"],
                "weather": s["weather"]
            })

    template_file = TEMPLATES_DIR / "krisflyer_kfescapes_landing.py"
    t = template_file.read_text(encoding="utf-8")

    t = t.replace("October 2026", "November 2026")
    t = t.replace("1 – 31 Oct 2026", "1 – 30 Nov 2026")
    t = t.replace("Book by 30 Sep 2026", "Book by 31 Oct 2026")
    t = t.replace("1 to 31 October 2026", "1 to 30 November 2026")
    t = t.replace("1 to 31 October", "1 to 30 November")
    t = t.replace("Step 1: Select Your Travel Dates (October 2026)", "Step 1: Select Your Travel Dates (November 2026)")
    t = re.sub(r'All \d+ Flight Sectors', f'All {len(raw_sectors)} Flight Sectors', t)
    t = re.sub(r'\d+ Destinations &bull; \d+ Itineraries', f'{len(set(r[\"destination\"] for r in rt_itineraries))} Destinations &bull; {len(rt_itineraries)} Itineraries', t)
    t = t.replace("for (let d = 1; d <= 31; d++)", "for (let d = 1; d <= 30; d++)")
    t = t.replace("Oct Blacked Out", "Nov Blacked Out")
    t = t.replace("' Oct'", "' Nov'")
    t = t.replace("' Oct '", "' Nov '")
    t = t.replace(" Oct ", " Nov ")

    t = re.sub(r'const rawSectors = \[.*?\];\s*const rtItineraries =', f'const rawSectors = {json.dumps(raw_sectors)};\n    const rtItineraries =', t, flags=re.DOTALL)
    t = re.sub(r'const rtItineraries = \[.*?\];\s*const outboundOptions =', f'const rtItineraries = {json.dumps(rt_itineraries)};\n    const outboundOptions =', t, flags=re.DOTALL)
    t = re.sub(r'const outboundOptions = \[.*?\];\s*const inboundOptions =', f'const outboundOptions = {json.dumps(outbound_options)};\n    const inboundOptions =', t, flags=re.DOTALL)
    t = re.sub(r'const inboundOptions = \[.*?\];\s*const colsModeRT =', f'const inboundOptions = {json.dumps(inbound_options)};\n    const colsModeRT =', t, flags=re.DOTALL)

    template_file.write_text(t, encoding="utf-8")
    print(f"SUCCESS: Updated {template_file} with {len(raw_sectors)} November 2026 sectors!")

if __name__ == "__main__":
    main()
