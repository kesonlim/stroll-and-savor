"""One-off personal itinerary page for the Lim family's October 2026
KrisFlyer Spontaneous Escapes trip planning. Not part of the scraper-driven
monthly Spontaneous Escapes pipeline (site/templates/monthly_post.py) --
this is a bespoke interactive dashboard, restyled onto the Field Notes
brand system and wrapped in the shared site chrome for nav/footer/SEO
compliance (docs/seo-standards.md). Content (the `data` array in the
embedded script) is preserved verbatim from the source file the user
supplied -- do not edit flight numbers, miles, dates, or weather figures
without the user re-supplying updated source data.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chrome import page  # noqa: E402

ASSET_PREFIX = "../../../../"
URL_PATH = "singapore-airlines/spontaneous-escapes/2026-10/limfam-holidays/"

STYLE = """
  .hero { max-width: 1100px; margin: 0 auto; padding: 3rem 1.75rem 1.5rem; }
  .hero .eyebrow { font-family: var(--font-data); font-size: 0.76rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--rust-text); display: block; margin-bottom: 0.6rem; }
  .hero h1 { font-size: clamp(1.6rem, 2.6vw, 2.2rem); margin: 0 0 1rem; max-width: 24ch; }
  .hero p.lede { font-size: 1.02rem; max-width: 68ch; color: var(--ink-soft); }

  .kpi-grid {
    max-width: 1100px; margin: 0 auto 1.5rem; padding: 0 1.75rem;
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;
  }
  .kpi-card { background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px; padding: 1.1rem 1.3rem; }
  .kpi-label { font-family: var(--font-data); font-size: 0.68rem; font-weight: 400; text-transform: uppercase;
    letter-spacing: 0.08em; color: var(--ink-soft); margin-bottom: 0.3rem; }
  .kpi-val { font-family: var(--font-display); font-size: 1.4rem; font-weight: 700; color: var(--ink); }
  .kpi-sub { font-size: 0.76rem; color: var(--ink-soft); margin-top: 0.2rem; }

  .controls-card {
    max-width: 1100px; margin: 0 auto 1.25rem; padding: 1.25rem 1.5rem;
    background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px;
  }
  .controls-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; align-items: flex-end; }
  .control-group { display: flex; flex-direction: column; gap: 0.4rem; }
  .control-label { font-family: var(--font-data); font-size: 0.68rem; font-weight: 400; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--ink-soft); }
  .search-input, .select-control {
    padding: 0.55rem 0.7rem; border-radius: 8px; border: 1px solid var(--rule);
    font-family: var(--font-body); font-size: 0.85rem; background: var(--paper); color: var(--ink); outline: none;
  }
  .search-input:focus, .select-control:focus { border-color: var(--teal-text); }
  .toggle-group { display: flex; background: var(--paper); border: 1px solid var(--rule); border-radius: 8px; padding: 3px; gap: 3px; }
  .toggle-btn { flex: 1; padding: 0.45rem 0.75rem; border: none; background: transparent; border-radius: 6px;
    font-family: var(--font-body); font-size: 0.78rem; font-weight: 600; cursor: pointer; color: var(--ink-soft); }
  .toggle-btn.active { background: var(--paper-2); color: var(--ink); border: 1px solid var(--rule); }

  .table-container { max-width: 1100px; margin: 0 auto; background: var(--paper-2); border: 1px solid var(--rule);
    border-radius: 12px; overflow-x: auto; position: relative; }
  .table-container.has-overflow::after {
    content: ""; position: sticky; float: right; top: 0; right: 0; width: 28px; height: 100%;
    margin-left: -28px; margin-right: -1px; pointer-events: none;
    background: linear-gradient(to right, transparent, rgba(46,46,44,0.14));
  }
  .scroll-hint { max-width: 1100px; margin: 0.5rem auto 0; padding: 0 1.75rem;
    font-family: var(--font-data); font-size: 0.68rem; color: var(--ink-soft); display: none; }
  .scroll-hint.visible { display: block; }
  table { width: 100%; min-width: 920px; border-collapse: collapse; text-align: left; font-size: 0.8rem; }
  thead th { background: var(--ink); color: var(--paper); padding: 0.7rem 0.65rem; font-family: var(--font-data);
    font-weight: 400; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer;
    user-select: none; white-space: nowrap; }
  thead th .sort-icon { margin-left: 0.4rem; opacity: 0.55; font-size: 0.6rem; }
  thead th.sorted .sort-icon { opacity: 1; color: var(--rust-soft); }
  tbody tr { border-bottom: 1px solid var(--rule); }
  tbody tr:hover { background: var(--paper); }
  tbody tr:hover td:first-child { background: var(--paper); }
  tbody td { padding: 0.7rem 0.65rem; vertical-align: middle; }

  thead th:first-child, tbody td:first-child {
    position: sticky; left: 0; z-index: 1; background: var(--paper-2);
    box-shadow: 1px 0 0 var(--rule);
  }
  thead th:first-child { background: var(--ink); z-index: 2; }

  .dest-name { font-family: var(--font-display); font-weight: 700; color: var(--ink); font-size: 0.9rem; }
  .region-label { font-size: 0.66rem; color: var(--ink-soft); }

  .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 6px; font-family: var(--font-data);
    font-size: 0.66rem; font-weight: 400; white-space: nowrap; border: 1px solid var(--rule); }
  .badge-biz { background: rgba(180, 85, 47, 0.1); color: var(--rust-text); border-color: var(--rust-soft); }
  .badge-mix { background: var(--paper); color: var(--ink-soft); }
  .badge-econ { background: var(--paper); color: var(--ink-soft); }
  .badge-sunny { background: rgba(180, 85, 47, 0.1); color: var(--rust-text); border: none; }
  .badge-rainy { background: rgba(62, 124, 116, 0.12); color: var(--teal-text); border: none; }
  .badge-cloudy { background: var(--paper); color: var(--ink-soft); border: none; }

  .miles-cell { font-family: var(--font-data); font-size: 0.86rem; font-weight: 700; color: var(--teal-text); }
  .pph-cell { font-family: var(--font-data); font-weight: 700; color: var(--rust-text); font-size: 0.78rem; }
  .flight-time { font-family: var(--font-data); font-size: 0.72rem; color: var(--ink-soft); line-height: 1.4; }

  .card-view-grid { max-width: 1100px; margin: 0 auto; display: none;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; padding: 0 1.75rem; }
  .travel-card { background: var(--paper-2); border: 1px solid var(--rule); border-radius: 12px; padding: 1.25rem; }
  .card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }
  .card-dest { font-family: var(--font-display); font-size: 1.05rem; font-weight: 700; color: var(--ink); }
  .card-region { font-family: var(--font-data); font-size: 0.66rem; color: var(--ink-soft); text-transform: uppercase; }
  .card-stat-row { display: flex; justify-content: space-between; padding: 0.5rem 0; border-top: 1px solid var(--rule);
    font-size: 0.78rem; color: var(--ink); }
  .card-stat-row span:first-child { color: var(--ink-soft); }
  .card-note { font-family: var(--font-data); font-size: 0.7rem; color: var(--ink-soft); background: var(--paper);
    border-radius: 6px; padding: 0.5rem 0.65rem; margin-top: 0.75rem; }

  .page-footnote { max-width: 1100px; margin: 1.75rem auto 3rem; padding: 0 1.75rem;
    font-family: var(--font-data); font-size: 0.72rem; color: var(--ink-soft); line-height: 1.6; }

  .table-container, .kpi-grid, .controls-card, .page-footnote, .hero, .card-view-grid { padding-left: 1.75rem; padding-right: 1.75rem; }
"""


def render() -> str:
    body = """
    <div class="hero">
      <span class="eyebrow">Singapore Airlines Spontaneous Escapes</span>
      <h1>Lim family October 2026 KrisFlyer planner</h1>
      <p class="lede">
        Every Spontaneous Escapes option worth considering for a Singapore departure on
        9 or 10 October, matched against return dates of 16, 17, or 18 October 2026.
        Sort and filter by miles, cabin class, weather, and flight time to compare routes
        side by side.
      </p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Available itineraries</div>
        <div class="kpi-val" id="kpi-count">0</div>
        <div class="kpi-sub">Matching current filters</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Lowest mileage deal</div>
        <div class="kpi-val" id="kpi-lowest">11,200</div>
        <div class="kpi-sub">Penang or Brunei, economy</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Top burn efficiency</div>
        <div class="kpi-val">2,427 <span style="font-size:0.85rem;">pts/hr</span></div>
        <div class="kpi-sub">Manila economy, 7h 30m round trip</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Best autumn weather</div>
        <div class="kpi-val" style="color:var(--rust-text);">20&deg;C to 28&deg;C</div>
        <div class="kpi-sub">China open-jaw, sunny and clear</div>
      </div>
    </div>

    <div class="controls-card">
      <div class="controls-row">
        <div class="control-group" style="grid-column: span 2;">
          <label class="control-label">Quick search</label>
          <input type="text" id="searchInput" class="search-input" placeholder="Search destination, flight number, weather, notes...">
        </div>
        <div class="control-group">
          <label class="control-label">Region</label>
          <select id="regionFilter" class="select-control">
            <option value="ALL">All regions</option>
            <option value="South East Asia">South East Asia</option>
            <option value="South Asia">South Asia</option>
            <option value="East Asia">East Asia / China</option>
          </select>
        </div>
        <div class="control-group">
          <label class="control-label">Cabin class</label>
          <select id="cabinFilter" class="select-control">
            <option value="ALL">All cabin classes</option>
            <option value="Economy">Economy only</option>
            <option value="Mixed">Mixed cabins (economy + business)</option>
            <option value="Business">All-business class</option>
          </select>
        </div>
        <div class="control-group">
          <label class="control-label">Weather forecast</label>
          <select id="weatherFilter" class="select-control">
            <option value="ALL">All conditions</option>
            <option value="Sunny">Sunny / clear</option>
            <option value="Cloudy">Partly cloudy</option>
            <option value="Rainy">Showers / rainy</option>
          </select>
        </div>
        <div class="control-group">
          <label class="control-label">Max round-trip miles</label>
          <select id="milesFilter" class="select-control">
            <option value="999999">Any miles</option>
            <option value="20000">Under 20,000 miles</option>
            <option value="30000">Under 30,000 miles</option>
            <option value="40000">Under 40,000 miles</option>
          </select>
        </div>
        <div class="control-group">
          <label class="control-label">View mode</label>
          <div class="toggle-group">
            <button class="toggle-btn active" id="btnTableView" onclick="setViewMode('table')">Table</button>
            <button class="toggle-btn" id="btnCardView" onclick="setViewMode('cards')">Cards</button>
          </div>
        </div>
      </div>
    </div>

    <div class="table-container" id="tableView">
      <table>
        <thead>
          <tr>
            <th onclick="sortTable('destination')">Destination <span class="sort-icon" id="icon-destination">&#9650;&#9660;</span></th>
            <th onclick="sortTable('cabin')">Cabin class <span class="sort-icon" id="icon-cabin">&#9650;&#9660;</span></th>
            <th onclick="sortTable('miles')">RT miles <span class="sort-icon" id="icon-miles">&#9650;&#9660;</span></th>
            <th onclick="sortTable('temp_high')">Est. temp <span class="sort-icon" id="icon-temp_high">&#9650;&#9660;</span></th>
            <th onclick="sortTable('weather')">Weather <span class="sort-icon" id="icon-weather">&#9650;&#9660;</span></th>
            <th onclick="sortTable('flight_dur_min')">Flight time <span class="sort-icon" id="icon-flight_dur_min">&#9650;&#9660;</span></th>
            <th onclick="sortTable('pts_per_hr')">Pts / hour <span class="sort-icon" id="icon-pts_per_hr">&#9650;&#9660;</span></th>
            <th>Outbound flights (SIN departure time)</th>
            <th>Inbound flights (local departure time)</th>
            <th>Schedule caveats</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
    <p class="scroll-hint" id="scrollHint">Scroll the table sideways to see outbound/inbound flights and caveats, or switch to Cards above.</p>

    <div class="card-view-grid" id="cardView"></div>

    <p class="page-footnote">
      Data grounded strictly in Singapore Airlines KrisFlyer Spontaneous Escapes guidelines.<br>
      Departure window: 9 to 10 October 2026 &middot; Inbound window: 16 to 18 October 2026.
    </p>

    <script>
      const data = [{"region": "South East Asia", "destination": "Bangkok", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 18200, "temp_low": 25, "temp_high": 32, "weather": "Afternoon Showers", "weather_type": "Rainy", "flight_dur_min": 295, "flight_dur_str": "4h 55m", "pts_per_hr": 3702, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16 or 17 Oct", "out_flights": "SQ712 (15:45), SQ714 (17:30), SQ720 (18:30)", "in_flights": "SQ707 (12:15), SQ713 (20:15), SQ719 (21:15)", "notes": "18 Oct return is blacked out for Economy."}, {"region": "South East Asia", "destination": "Bangkok", "cabin": "Economy + Business", "cabin_type": "Mixed", "miles": 26600, "temp_low": 25, "temp_high": 32, "weather": "Afternoon Showers", "weather_type": "Rainy", "flight_dur_min": 295, "flight_dur_str": "4h 55m", "pts_per_hr": 5410, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ712 (15:45), SQ714 (17:30), SQ720 (18:30) [Econ]", "in_flights": "SQ713 (20:15), SQ719 (21:15) [Biz]", "notes": "Return in Business allows returning on 18 Oct."}, {"region": "South East Asia", "destination": "Bangkok", "cabin": "Business + Economy", "cabin_type": "Mixed", "miles": 26600, "temp_low": 25, "temp_high": 32, "weather": "Afternoon Showers", "weather_type": "Rainy", "flight_dur_min": 295, "flight_dur_str": "4h 55m", "pts_per_hr": 5410, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16 or 17 Oct", "out_flights": "SQ706 (06:40), SQ714 (17:30) [Biz]", "in_flights": "SQ707 (12:15), SQ713 (20:15), SQ719 (21:15) [Econ]", "notes": "Economy return blacked out on 18 Oct."}, {"region": "South East Asia", "destination": "Bangkok", "cabin": "Business + Business", "cabin_type": "Business", "miles": 35000, "temp_low": 25, "temp_high": 32, "weather": "Afternoon Showers", "weather_type": "Rainy", "flight_dur_min": 295, "flight_dur_str": "4h 55m", "pts_per_hr": 7119, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ706 (06:40), SQ714 (17:30)", "in_flights": "SQ713 (20:15), SQ719 (21:15)", "notes": "Daily Business availability across all dates."}, {"region": "South East Asia", "destination": "Ho Chi Minh City", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 18200, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Showers", "weather_type": "Cloudy", "flight_dur_min": 260, "flight_dur_str": "4h 20m", "pts_per_hr": 4200, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ186 (17:25), SQ188 (09:50)", "in_flights": "SQ177 (12:30), SQ187 (19:40)", "notes": "No blackout dates across promotional window."}, {"region": "South East Asia", "destination": "Ho Chi Minh City", "cabin": "Economy + Business", "cabin_type": "Mixed", "miles": 26600, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Showers", "weather_type": "Cloudy", "flight_dur_min": 260, "flight_dur_str": "4h 20m", "pts_per_hr": 6138, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ186 (17:25), SQ188 (09:50) [Econ]", "in_flights": "SQ177 (12:30), SQ183 (15:55), SQ185 (12:20) [Biz]", "notes": "Excellent timing choices for return."}, {"region": "South East Asia", "destination": "Ho Chi Minh City", "cabin": "Business + Economy", "cabin_type": "Mixed", "miles": 26600, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Showers", "weather_type": "Cloudy", "flight_dur_min": 260, "flight_dur_str": "4h 20m", "pts_per_hr": 6138, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ178 (09:45), SQ184 (13:55), SQ186 (17:25), SQ188 (09:50) [Biz]", "in_flights": "SQ177 (12:30), SQ187 (19:40) [Econ]", "notes": "4 morning/afternoon Business departures."}, {"region": "South East Asia", "destination": "Ho Chi Minh City", "cabin": "Business + Business", "cabin_type": "Business", "miles": 35000, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Showers", "weather_type": "Cloudy", "flight_dur_min": 260, "flight_dur_str": "4h 20m", "pts_per_hr": 8077, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ178 (09:45), SQ184 (13:55), SQ186 (17:25), SQ188 (09:50)", "in_flights": "SQ177 (12:30), SQ183 (15:55), SQ185 (12:20)", "notes": "Full Business flexibility with zero blackout days."}, {"region": "South East Asia", "destination": "Manila", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 18200, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Humid", "weather_type": "Cloudy", "flight_dur_min": 450, "flight_dur_str": "7h 30m", "pts_per_hr": 2427, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16 or 17 Oct", "out_flights": "SQ914 (09:15), SQ916 (14:05)", "in_flights": "SQ917 (14:15), SQ921 (19:00)", "notes": "18 Oct return blacked out for Economy."}, {"region": "South East Asia", "destination": "Manila", "cabin": "Economy + Business", "cabin_type": "Mixed", "miles": 26600, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Humid", "weather_type": "Cloudy", "flight_dur_min": 450, "flight_dur_str": "7h 30m", "pts_per_hr": 3547, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ914 (09:15), SQ916 (14:05) [Econ]", "in_flights": "SQ921 (19:00) [Biz]", "notes": "Business return valid across 16, 17, and 18 Oct."}, {"region": "South East Asia", "destination": "Manila", "cabin": "Business + Economy", "cabin_type": "Mixed", "miles": 26600, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Humid", "weather_type": "Cloudy", "flight_dur_min": 450, "flight_dur_str": "7h 30m", "pts_per_hr": 3547, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16 or 17 Oct", "out_flights": "SQ914 (09:15) [Biz]", "in_flights": "SQ917 (14:15), SQ921 (19:00) [Econ]", "notes": "18 Oct return blacked out for Economy."}, {"region": "South East Asia", "destination": "Manila", "cabin": "Business + Business", "cabin_type": "Business", "miles": 35000, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Humid", "weather_type": "Cloudy", "flight_dur_min": 450, "flight_dur_str": "7h 30m", "pts_per_hr": 4667, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ914 (09:15)", "in_flights": "SQ921 (19:00)", "notes": "Convenient morning departure and evening return."}, {"region": "South East Asia", "destination": "Phuket", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 18200, "temp_low": 24, "temp_high": 31, "weather": "Rainy / Tropical Showers", "weather_type": "Rainy", "flight_dur_min": 225, "flight_dur_str": "3h 45m", "pts_per_hr": 4853, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16 or 17 Oct", "out_flights": "SQ724 (07:35), SQ732 (09:30), SQ736 (14:10), SQ740 (18:30)", "in_flights": "SQ723 (09:30), SQ725 (11:30), SQ727 (16:30), SQ739 (20:10)", "notes": "18 Oct return blacked out for Economy."}, {"region": "South East Asia", "destination": "Phuket", "cabin": "Economy + Business", "cabin_type": "Mixed", "miles": 26600, "temp_low": 24, "temp_high": 31, "weather": "Rainy / Tropical Showers", "weather_type": "Rainy", "flight_dur_min": 225, "flight_dur_str": "3h 45m", "pts_per_hr": 7093, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ724 (07:35), SQ732 (09:30), SQ736 (14:10), SQ740 (18:30) [Econ]", "in_flights": "SQ723 (09:30), SQ725 (11:30) [Biz]", "notes": "Business return allows Sunday 18 Oct travel."}, {"region": "South East Asia", "destination": "Phuket", "cabin": "Business + Economy", "cabin_type": "Mixed", "miles": 26600, "temp_low": 24, "temp_high": 31, "weather": "Rainy / Tropical Showers", "weather_type": "Rainy", "flight_dur_min": 225, "flight_dur_str": "3h 45m", "pts_per_hr": 7093, "out_schedule": "Depart 9 Oct only", "in_schedule": "Return 16 or 17 Oct", "out_flights": "SQ724 (07:35), SQ740 (18:30) [Biz]", "in_flights": "SQ723 (09:30), SQ725 (11:30), SQ727 (16:30), SQ739 (20:10) [Econ]", "notes": "10 Oct outbound & 18 Oct inbound blacked out."}, {"region": "South East Asia", "destination": "Phuket", "cabin": "Business + Business", "cabin_type": "Business", "miles": 35000, "temp_low": 24, "temp_high": 31, "weather": "Rainy / Tropical Showers", "weather_type": "Rainy", "flight_dur_min": 225, "flight_dur_str": "3h 45m", "pts_per_hr": 9333, "out_schedule": "Depart 9 Oct only", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ724 (07:35), SQ740 (18:30)", "in_flights": "SQ723 (09:30), SQ725 (11:30)", "notes": "Highest points/hr density; 10 Oct outbound blacked out."}, {"region": "South East Asia", "destination": "Denpasar (Bali)", "cabin": "Economy + Business", "cabin_type": "Mixed", "miles": 21000, "temp_low": 24, "temp_high": 31, "weather": "Mostly Sunny / Dry Season", "weather_type": "Sunny", "flight_dur_min": 330, "flight_dur_str": "5h 30m", "pts_per_hr": 3818, "out_schedule": "Depart 10 Oct only", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ948 (18:05) [Econ]", "in_flights": "SQ935 (10:45), SQ947 (20:05), SQ949 (21:45) [Biz]", "notes": "Outbound 9 Oct blacked out; return Econ not on promo."}, {"region": "South East Asia", "destination": "Denpasar (Bali)", "cabin": "Business + Business", "cabin_type": "Business", "miles": 30800, "temp_low": 24, "temp_high": 31, "weather": "Mostly Sunny / Dry Season", "weather_type": "Sunny", "flight_dur_min": 330, "flight_dur_str": "5h 30m", "pts_per_hr": 5600, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ934 (08:20), SQ948 (18:05)", "in_flights": "SQ935 (10:45), SQ947 (20:05), SQ949 (21:45)", "notes": "Best weather destination; 3 return flight options."}, {"region": "South Asia", "destination": "Colombo", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 26600, "temp_low": 24, "temp_high": 30, "weather": "Monsoon Showers", "weather_type": "Rainy", "flight_dur_min": 470, "flight_dur_str": "7h 50m", "pts_per_hr": 3396, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ462 (10:00), SQ468 (22:20)", "in_flights": "SQ463 (11:30), SQ469 (00:50)", "notes": "Zero blackout dates in promo period."}, {"region": "South Asia", "destination": "Colombo", "cabin": "Economy + Business", "cabin_type": "Mixed", "miles": 44800, "temp_low": 24, "temp_high": 30, "weather": "Monsoon Showers", "weather_type": "Rainy", "flight_dur_min": 470, "flight_dur_str": "7h 50m", "pts_per_hr": 5719, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ462 (10:00), SQ468 (22:20) [Econ]", "in_flights": "SQ469 (00:50) [Biz]", "notes": "Overnight Business return on SQ469."}, {"region": "South Asia", "destination": "Colombo", "cabin": "Business + Economy", "cabin_type": "Mixed", "miles": 44800, "temp_low": 24, "temp_high": 30, "weather": "Monsoon Showers", "weather_type": "Rainy", "flight_dur_min": 470, "flight_dur_str": "7h 50m", "pts_per_hr": 5719, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ462 (10:00), SQ468 (22:20) [Biz]", "in_flights": "SQ463 (11:30), SQ469 (00:50) [Econ]", "notes": "Morning or redeye Business outbound."}, {"region": "South Asia", "destination": "Colombo", "cabin": "Business + Business", "cabin_type": "Business", "miles": 63000, "temp_low": 24, "temp_high": 30, "weather": "Monsoon Showers", "weather_type": "Rainy", "flight_dur_min": 470, "flight_dur_str": "7h 50m", "pts_per_hr": 8043, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ462 (10:00), SQ468 (22:20)", "in_flights": "SQ469 (00:50)", "notes": "Full Business comfort on widebody aircraft."}, {"region": "South Asia", "destination": "Dhaka", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 26600, "temp_low": 23, "temp_high": 32, "weather": "Mostly Sunny / Warm", "weather_type": "Sunny", "flight_dur_min": 505, "flight_dur_str": "8h 25m", "pts_per_hr": 3160, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ446 (20:35)", "in_flights": "SQ447 (23:55)", "notes": "Zero blackout dates in promo period."}, {"region": "South Asia", "destination": "Dhaka", "cabin": "Economy + Business", "cabin_type": "Mixed", "miles": 44800, "temp_low": 23, "temp_high": 32, "weather": "Mostly Sunny / Warm", "weather_type": "Sunny", "flight_dur_min": 505, "flight_dur_str": "8h 25m", "pts_per_hr": 5323, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ446 (20:35) [Econ]", "in_flights": "SQ447 (23:55) [Biz]", "notes": "Overnight Business return on SQ447."}, {"region": "South Asia", "destination": "Dhaka", "cabin": "Business + Economy", "cabin_type": "Mixed", "miles": 44800, "temp_low": 23, "temp_high": 32, "weather": "Mostly Sunny / Warm", "weather_type": "Sunny", "flight_dur_min": 505, "flight_dur_str": "8h 25m", "pts_per_hr": 5323, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ446 (20:35) [Biz]", "in_flights": "SQ447 (23:55) [Econ]", "notes": "Overnight Business outbound on SQ446."}, {"region": "South Asia", "destination": "Dhaka", "cabin": "Business + Business", "cabin_type": "Business", "miles": 63000, "temp_low": 23, "temp_high": 32, "weather": "Mostly Sunny / Warm", "weather_type": "Sunny", "flight_dur_min": 505, "flight_dur_str": "8h 25m", "pts_per_hr": 7485, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ446 (20:35)", "in_flights": "SQ447 (23:55)", "notes": "Both sectors operate on widebody A350."}, {"region": "South East Asia", "destination": "Jakarta", "cabin": "Business + Business", "cabin_type": "Business", "miles": 30800, "temp_low": 24, "temp_high": 33, "weather": "Mostly Sunny / Warm", "weather_type": "Sunny", "flight_dur_min": 220, "flight_dur_str": "3h 40m", "pts_per_hr": 8400, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ950 (06:20), SQ952 (07:40), SQ960 (15:15), SQ964 (17:20)", "in_flights": "SQ951 (05:25), SQ963 (18:05), SQ965 (19:00)", "notes": "Economy not offered on promo; 4 daily Business flights."}, {"region": "South Asia", "destination": "Chennai", "cabin": "Business + Business", "cabin_type": "Business", "miles": 63000, "temp_low": 25, "temp_high": 32, "weather": "Partly Cloudy / Coastal Showers", "weather_type": "Cloudy", "flight_dur_min": 495, "flight_dur_str": "8h 15m", "pts_per_hr": 7636, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16 or 18 Oct", "out_flights": "SQ528 (20:15)", "in_flights": "SQ529 (23:15)", "notes": "17 Oct return blacked out; 16 & 18 Oct valid."}, {"region": "East Asia", "destination": "China Open-Jaw (XMN + SZX)", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 21700, "temp_low": 20, "temp_high": 28, "weather": "Sunny & Clear (Autumn)", "weather_type": "Sunny", "flight_dur_min": 520, "flight_dur_str": "8h 40m", "pts_per_hr": 2504, "out_schedule": "Depart SIN -> XMN (10 Oct)", "in_schedule": "Return SZX -> SIN (16 or 17 Oct)", "out_flights": "SQ868 (07:50) to Xiamen", "in_flights": "SQ857 (02:05 AM) from Shenzhen", "notes": "Best value metric (2,504 pts/hr); 18 Oct return blacked out. XMN-SZX is ~3h HSR."}, {"region": "South East Asia", "destination": "Penang", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 11200, "temp_low": 24, "temp_high": 31, "weather": "Afternoon Showers", "weather_type": "Rainy", "flight_dur_min": 170, "flight_dur_str": "2h 50m", "pts_per_hr": 3953, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ136 (13:40), SQ138 (20:45)", "in_flights": "SQ133 (15:55), SQ135 (22:45)", "notes": "Lowest total mileage requirement (11,200 pts)."}, {"region": "South East Asia", "destination": "Brunei", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 11200, "temp_low": 24, "temp_high": 32, "weather": "Partly Cloudy / Showers", "weather_type": "Cloudy", "flight_dur_min": 260, "flight_dur_str": "4h 20m", "pts_per_hr": 2585, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ148 (08:40)", "in_flights": "SQ147 (11:55)", "notes": "Highly efficient points/hr burn rate."}, {"region": "South East Asia", "destination": "Phnom Penh", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 18200, "temp_low": 24, "temp_high": 31, "weather": "Scattered Showers", "weather_type": "Rainy", "flight_dur_min": 255, "flight_dur_str": "4h 15m", "pts_per_hr": 4282, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ154 (07:15), SQ156 (13:30), SQ158 (16:15)", "in_flights": "SQ153 (09:10), SQ155 (15:20), SQ157 (18:15)", "notes": "3 daily flight pairs with zero blackout days."}, {"region": "South East Asia", "destination": "Siem Reap", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 18200, "temp_low": 24, "temp_high": 31, "weather": "Partly Cloudy / Clearing", "weather_type": "Cloudy", "flight_dur_min": 275, "flight_dur_str": "4h 35m", "pts_per_hr": 3971, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 17 or 18 Oct", "out_flights": "SQ166 (08:45)", "in_flights": "SQ163 (10:40)", "notes": "16 Oct return blacked out; 17 & 18 Oct valid."}, {"region": "South East Asia", "destination": "Da Nang", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 18200, "temp_low": 23, "temp_high": 29, "weather": "Rainy / Monsoon Season", "weather_type": "Rainy", "flight_dur_min": 340, "flight_dur_str": "5h 40m", "pts_per_hr": 3212, "out_schedule": "Depart 9 Oct only", "in_schedule": "Return 16 or 17 Oct", "out_flights": "SQ172 (09:15), SQ174 (13:55), SQ176 (18:10)", "in_flights": "SQ171 (11:50), SQ173 (16:30), SQ175 (20:45)", "notes": "10 Oct outbound & 18 Oct inbound blacked out."}, {"region": "South Asia", "destination": "Male (Maldives)", "cabin": "Economy + Economy", "cabin_type": "Economy", "miles": 26600, "temp_low": 26, "temp_high": 30, "weather": "Partly Cloudy / Passing Rain", "weather_type": "Cloudy", "flight_dur_min": 580, "flight_dur_str": "9h 40m", "pts_per_hr": 2752, "out_schedule": "Depart 9 or 10 Oct", "in_schedule": "Return 16, 17, or 18 Oct", "out_flights": "SQ438 (20:35)", "in_flights": "SQ431 (23:25)", "notes": "Longest duration in economy; high points/hr value."}];
      let currentSortCol = 'miles';
      let sortAsc = true;

      function getBadgeClass(cabinType) {
        if (cabinType === 'Business') return 'badge-biz';
        if (cabinType === 'Mixed') return 'badge-mix';
        return 'badge-econ';
      }

      function getWeatherBadgeClass(wType) {
        if (wType === 'Sunny') return 'badge-sunny';
        if (wType === 'Rainy') return 'badge-rainy';
        return 'badge-cloudy';
      }

      function filterData() {
        const search = document.getElementById('searchInput').value.toLowerCase();
        const region = document.getElementById('regionFilter').value;
        const cabin = document.getElementById('cabinFilter').value;
        const weather = document.getElementById('weatherFilter').value;
        const maxMiles = parseInt(document.getElementById('milesFilter').value, 10);

        return data.filter(item => {
          if (region !== 'ALL' && item.region !== region) return false;
          if (cabin !== 'ALL' && item.cabin_type !== cabin) return false;
          if (weather !== 'ALL' && item.weather_type !== weather) return false;
          if (item.miles > maxMiles) return false;

          if (search) {
            const str = (item.destination + ' ' + item.cabin + ' ' + item.out_flights + ' ' + item.in_flights + ' ' + item.notes + ' ' + item.weather).toLowerCase();
            if (!str.includes(search)) return false;
          }
          return true;
        });
      }

      function sortData(arr) {
        return arr.sort((a, b) => {
          let vA = a[currentSortCol];
          let vB = b[currentSortCol];
          if (typeof vA === 'string') {
            vA = vA.toLowerCase();
            vB = vB.toLowerCase();
          }
          if (vA < vB) return sortAsc ? -1 : 1;
          if (vA > vB) return sortAsc ? 1 : -1;
          return 0;
        });
      }

      function render() {
        const filtered = filterData();
        const sorted = sortData(filtered);

        document.getElementById('kpi-count').innerText = sorted.length;
        if (sorted.length > 0) {
          const minMiles = Math.min(...sorted.map(s => s.miles));
          document.getElementById('kpi-lowest').innerText = minMiles.toLocaleString();
        } else {
          document.getElementById('kpi-lowest').innerText = '-';
        }

        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';

        sorted.forEach(row => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><span class="dest-name">${row.destination}</span><br><span class="region-label">${row.region}</span></td>
            <td><span class="badge ${getBadgeClass(row.cabin_type)}">${row.cabin}</span></td>
            <td class="miles-cell">${row.miles.toLocaleString()}</td>
            <td class="flight-time"><b>${row.temp_low}&deg;C&ndash;${row.temp_high}&deg;C</b></td>
            <td><span class="badge ${getWeatherBadgeClass(row.weather_type)}">${row.weather}</span></td>
            <td class="flight-time"><b>${row.flight_dur_str}</b> (RT)</td>
            <td class="pph-cell">${row.pts_per_hr.toLocaleString()} <span style="font-weight:400;">pts/hr</span></td>
            <td class="flight-time">
              <span style="font-weight:700; color:var(--ink);">${row.out_schedule}</span><br>
              ${row.out_flights}
            </td>
            <td class="flight-time">
              <span style="font-weight:700; color:var(--ink);">${row.in_schedule}</span><br>
              ${row.in_flights}
            </td>
            <td class="flight-time" style="max-width:240px;">${row.notes}</td>
          `;
          tbody.appendChild(tr);
        });

        const cardGrid = document.getElementById('cardView');
        cardGrid.innerHTML = '';
        sorted.forEach(row => {
          const card = document.createElement('div');
          card.className = 'travel-card';
          card.innerHTML = `
            <div>
              <div class="card-top">
                <div>
                  <div class="card-dest">${row.destination}</div>
                  <div class="card-region">${row.region}</div>
                </div>
                <span class="badge ${getBadgeClass(row.cabin_type)}">${row.cabin_type}</span>
              </div>
              <div style="margin: 0.6rem 0;">
                <span class="miles-cell" style="font-size:1.15rem;">${row.miles.toLocaleString()}</span> <span style="font-size:0.72rem; color:var(--ink-soft);">miles RT</span>
              </div>
              <div class="card-stat-row">
                <span>Weather</span>
                <span><b>${row.temp_low}&deg;C&ndash;${row.temp_high}&deg;C</b> (${row.weather})</span>
              </div>
              <div class="card-stat-row">
                <span>Flight time &amp; value</span>
                <span><b>${row.flight_dur_str}</b> &nbsp; <span class="pph-cell">${row.pts_per_hr.toLocaleString()} pts/hr</span></span>
              </div>
              <div class="card-stat-row">
                <span>Outbound flight</span>
                <span style="text-align:right;">${row.out_flights}</span>
              </div>
              <div class="card-stat-row">
                <span>Inbound flight</span>
                <span style="text-align:right;">${row.in_flights}</span>
              </div>
            </div>
            <div class="card-note">${row.notes}</div>
          `;
          cardGrid.appendChild(card);
        });
      }

      function sortTable(col) {
        if (currentSortCol === col) {
          sortAsc = !sortAsc;
        } else {
          currentSortCol = col;
          sortAsc = true;
        }

        document.querySelectorAll('.sort-icon').forEach(el => el.innerHTML = '&#9650;&#9660;');
        document.querySelectorAll('thead th').forEach(el => el.classList.remove('sorted'));
        const activeTh = document.querySelector(`th[onclick="sortTable('${col}')"]`);
        if (activeTh) {
          activeTh.classList.add('sorted');
          document.getElementById(`icon-${col}`).innerText = sortAsc ? '\\u25B2' : '\\u25BC';
        }

        render();
      }

      function setViewMode(mode) {
        if (mode === 'table') {
          document.getElementById('tableView').style.display = 'block';
          document.getElementById('cardView').style.display = 'none';
          document.getElementById('btnTableView').classList.add('active');
          document.getElementById('btnCardView').classList.remove('active');
          updateScrollHint();
        } else {
          document.getElementById('tableView').style.display = 'none';
          document.getElementById('cardView').style.display = 'grid';
          document.getElementById('btnTableView').classList.remove('active');
          document.getElementById('btnCardView').classList.add('active');
          document.getElementById('scrollHint').classList.remove('visible');
        }
      }

      function updateScrollHint() {
        const tc = document.getElementById('tableView');
        const overflowing = tc.scrollWidth > tc.clientWidth + 4;
        tc.classList.toggle('has-overflow', overflowing);
        document.getElementById('scrollHint').classList.toggle('visible', overflowing);
      }

      document.getElementById('searchInput').addEventListener('input', render);
      document.getElementById('regionFilter').addEventListener('change', render);
      document.getElementById('cabinFilter').addEventListener('change', render);
      document.getElementById('weatherFilter').addEventListener('change', render);
      document.getElementById('milesFilter').addEventListener('change', render);
      window.addEventListener('resize', updateScrollHint);

      render();
      updateScrollHint();
      if (window.innerWidth < 720) {
        setViewMode('cards');
      }
    </script>
    """
    return page(
        title="Lim family October 2026 KrisFlyer escapes planner | Stroll & Savor",
        description="Personalized KrisFlyer Spontaneous Escapes planner for the Lim family's October 2026 trip: compare destinations by miles, cabin class, weather, and flight time.",
        body=body,
        asset_prefix=ASSET_PREFIX,
        extra_style=STYLE,
        url_path=URL_PATH,
        og_type="website",
        breadcrumbs=[
            ("Home", ""),
            ("Singapore Airlines Spontaneous Escapes", "singapore-airlines/spontaneous-escapes/"),
            ("Lim family October 2026 planner", URL_PATH),
        ],
    )
