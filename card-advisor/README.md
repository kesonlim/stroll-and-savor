# Stroll & Savor • Credit Card Advisor & Cap Tracker

A mobile-first web app that advises you on the best credit card to use for any transaction scenario in Singapore, monitors your monthly 4.0 mpd bonus spending caps, and logs your rewards.

Part of the **Stroll & Savor** ecosystem (`stroll-and-savor/card-advisor`), styled using the Field Notes brand system (warm paper, ink, rust, teal, and Space Mono typography).

---

## Key Features

1. **Instant Card Advisor ("Which Card?")**:
   - Enter any merchant or situation (e.g. *Shopee order $85*, *Haidilao dinner $180*, *Grab ride to Changi Airport $35*, *Singapore Airlines flight $1,250*, *FairPrice groceries $95*).
   - Instant calculation of the **#1 Best Card**, exact reward rate (e.g. `4.0 mpd` or `10% cashback`), estimated miles earned, and remaining monthly cap.
   - Recommends a **Backup Card** if the #1 card's cap is exhausted.
   - Highlights critical Singapore banking exclusion rules (e.g. Citi Rewards excluding Grab rides/flights, offline supermarket contactless removal, utility exclusions).

2. **Monthly Bonus Cap Monitor ("Caps")**:
   - Live visual meters tracking each card's monthly bonus cap (e.g. DBS WWC S$1,500/mo, Citi Rewards S$1,000/mo, UOB Lady's S$1,000/mo, HSBC Revolution S$1,000/mo).
   - Color-coded alerts: Green (Healthy), Amber (>75% used), Red (Cap Reached — switch to backup card).
   - Shows days remaining until the monthly cycle resets (e.g. on the 1st of each calendar month).

3. **Card Wallet Management ("Wallet")**:
   - Manage all cards in your wallet with 1-tap toggles.
   - Browse the preloaded Singapore cards catalog (DBS, UOB, OCBC, Citi, HSBC, StanChart, Amex).
   - For UOB Lady's / Lady's Solitaire: select your chosen 4.0 mpd category (Dining, Travel, Fashion, Family, Transport, Entertainment).

4. **Spending & Rewards Ledger ("Ledger")**:
   - 1-click logging directly from the recommendation card.
   - Tracks cumulative spend, total KrisFlyer miles earned, and cashback credits.
   - Filter by card or delete entries.

5. **Optimization Strategies & Priorities**:
   - ✈️ **Maximize Air Miles**: Focuses on 4.0 mpd for KrisFlyer / Asia Miles.
   - 💰 **Maximize Cash Rebates**: Prioritizes statement cashback credits (up to 15%).
   - ⚖️ **Balanced Economic Value**: Evaluates real monetary value (customizable valuation e.g. 1.6¢ per KrisFlyer mile).

---

## Local Development & Access

```bash
cd card-advisor
npm install
npm run dev
```

App is accessible at `http://localhost:3000/`.
On desktop, it displays in an interactive smartphone frame with a toggle to expand to full browser view.
