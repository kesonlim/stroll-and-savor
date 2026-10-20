import { Category, SpendChannel } from '../types';

export interface KnownMerchant {
  keywords: string[];
  name: string;
  category: Category;
  defaultChannel: SpendChannel;
  isOnline: boolean;
  isForeign: boolean;
  mccDescription?: string;
  specialWarning?: string;
  tip?: string;
}

export const KNOWN_MERCHANTS: KnownMerchant[] = [
  // Transport & Ride Hailing
  {
    keywords: ['grab', 'grab ride', 'grabcar', 'grabpay'],
    name: 'Grab Transport / GrabFood',
    category: 'transport',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 4121 (Taxicabs & Limousines)',
    specialWarning: '⚠️ Citi Rewards explicitly EXCLUDES Grab rides (earns only 0.4 mpd). Use DBS WWC, UOB Lady\'s (if Transport selected), or KrisFlyer UOB (3.0 mpd).',
    tip: 'Direct credit card payments on Grab earn 4.0 mpd on DBS WWC or 10% on UOB One. Avoid GrabPay wallet top-ups as top-ups are excluded from rewards by all banks.',
  },
  {
    keywords: ['gojek', 'tada', 'comfortdelgro', 'zig'],
    name: 'Gojek / ComfortDelGro / TADA',
    category: 'transport',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 4121 (Taxicabs & Limousines)',
    specialWarning: 'Citi Rewards excludes ride-hailing services. Use DBS WWC or UOB Lady\'s.',
  },
  {
    keywords: ['simplygo', 'mrt', 'bus', 'transitlink', 'smrt'],
    name: 'SimplyGo (Bus & MRT)',
    category: 'transport',
    defaultChannel: 'contactless',
    isOnline: false,
    isForeign: false,
    tip: 'Use UOB Lady\'s (if Transport category selected - 4.0 mpd) or KrisFlyer UOB (3.0 mpd). UOB One yields up to 10% cashback.',
  },

  // Airlines & Flight Travel
  {
    keywords: ['singapore airlines', 'sia', 'sq', 'krisflyer', 'krisshop'],
    name: 'Singapore Airlines / Scoot',
    category: 'travel_airlines',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 3075 (Singapore Airlines)',
    specialWarning: 'Citi Rewards excludes airlines. DBS WWC (4.0 mpd up to S$1,500), KrisFlyer UOB (3.0 mpd uncapped), or Amex KrisFlyer Ascend (3.2 mpd) are best.',
    tip: 'For tickets above S$1,500, split across cards or use KrisFlyer UOB / UOB PRVI Miles for uncapped miles.',
  },
  {
    keywords: ['scoot', 'cathay', 'emirates', 'qantas', 'ana', 'jal', 'flight', 'air ticket'],
    name: 'Airlines & Flights',
    category: 'travel_airlines',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    specialWarning: 'Citi Rewards excludes airline tickets. Use DBS WWC or UOB Lady\'s (Travel category).',
  },

  // Online Shopping & E-Commerce
  {
    keywords: ['shopee', 'lazada', 'amazon', 'taobao', 'qoo10', 'ezbuy', 'tiktok shop'],
    name: 'E-Commerce (Shopee / Lazada / Amazon)',
    category: 'online_shopping',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 5311 / 5399 / 5999',
    tip: 'Prime territory for 4.0 mpd: Citi Rewards, DBS WWC, or HSBC Revolution all qualify! UOB One also gives up to 10% cashback on Shopee.',
  },
  {
    keywords: ['apple', 'apple store', 'challenger', 'best denki', 'courts', 'harvey norman'],
    name: 'Electronics (Apple / Courts / Best Denki)',
    category: 'online_shopping',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    tip: 'If buying online: DBS WWC or Citi Rewards give 4.0 mpd (watch the S$1,000 / S$1,500 cap!). If buying in-store: OCBC Rewards or HSBC Revolution (contactless) give 4.0 mpd.',
  },

  // Food & Dining
  {
    keywords: ['haidilao', 'hdl', 'restaurant', 'cafe', 'starbucks', 'mcdonald', 'kfc', 'din tai fung', 'sushiro', 'chicha', 'koi', 'liho'],
    name: 'Restaurants & Dining Out',
    category: 'dining',
    defaultChannel: 'contactless',
    isOnline: false,
    isForeign: false,
    mccDescription: 'MCC 5812 / 5814 (Eating Places & Restaurants)',
    tip: 'Top miles picks: UOB Lady\'s (if Dining selected - 4.0 mpd) or HSBC Revolution (4.0 mpd via Apple Pay/Google Pay). Top cashback: OCBC 365 (5% cashback).',
  },
  {
    keywords: ['deliveroo', 'foodpanda', 'chope', 'oddle'],
    name: 'Food Delivery (Deliveroo / Foodpanda)',
    category: 'dining',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    tip: 'DBS WWC, HSBC Revolution, or UOB Lady\'s (Dining) all earn 4.0 mpd for online food delivery.',
  },

  // Supermarkets & Groceries
  {
    keywords: ['fairprice', 'ntuc', 'cold storage', 'cs fresh', 'giant', 'sheng siong', 'donki', 'don don donki', 'meidi-ya', 'redmart'],
    name: 'Supermarket & Groceries',
    category: 'supermarket',
    defaultChannel: 'contactless',
    isOnline: false,
    isForeign: false,
    mccDescription: 'MCC 5411 (Grocery Stores & Supermarkets)',
    specialWarning: '⚠️ HSBC Revolution NO LONGER earns 4.0 mpd on offline supermarkets (since Jan 2024).',
    tip: 'If shopping online on RedMart or FairPrice Online: DBS WWC earns 4.0 mpd! For physical stores: UOB One gives up to 10% on Cold Storage/Giant/Guardian, or use UOB PRVI (1.4 mpd).',
  },

  // Travel Agencies, Hotels & OTAs
  {
    keywords: ['agoda', 'booking.com', 'trip.com', 'expedia', 'klook', 'marriott', 'hilton', 'hyatt', 'hotel'],
    name: 'Hotels & Travel Booking (Agoda / Klook / Trip.com)',
    category: 'travel_hotels_ota',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 4722 / 7011',
    specialWarning: 'Citi Rewards strictly excludes hotels & travel agencies. Use DBS WWC (4.0 mpd), HSBC Revolution (4.0 mpd), or UOB Lady\'s (Travel category - 4.0 mpd).',
    tip: 'Check dedicated partner booking links on DBS Altitude (up to 10 mpd on Kaligo) or UOB PRVI Miles (up to 6.0 mpd on Expedia/Agoda).',
  },

  // Utilities & Bills
  {
    keywords: ['sp group', 'sp services', 'tuas power', 'geneco', 'senoko', 'keppel electric', 'singtel', 'starhub', 'm1', 'electricity', 'water bill'],
    name: 'Utilities & Telco (SP Group / Geneco)',
    category: 'utilities_bills',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 4900 (Utilities)',
    specialWarning: '⚠️ Almost ALL miles cards (DBS WWC, Citi Rewards, HSBC Revolution, UOB PRVI) put utilities on their general EXCLUSION list (0 miles)!',
    tip: 'Best option: UOB One Card (earns up to 10% cashback on SP Group bill recurring payments) or OCBC 365 (3% cashback with min spend).',
  },

  // Overseas & Foreign Currency
  {
    keywords: ['japan', 'tokyo', 'yen', 'usd', 'eur', 'bangkok', 'thb', 'korea', 'krw', 'overseas', 'foreign currency', 'london', 'fx'],
    name: 'Overseas Spend / Foreign Currency (Non-SGD)',
    category: 'overseas_fx',
    defaultChannel: 'any',
    isOnline: false,
    isForeign: true,
    tip: 'Top uncapped miles: UOB PRVI Miles (2.4 mpd) or DBS Altitude (2.2 mpd). Watch out for bank foreign transaction fee (~3.25%). If dining/shopping overseas, UOB Lady\'s still earns 4.0 mpd!',
  },

  // Medical & Health
  {
    keywords: ['hospital', 'nuh', 'sgh', 'ttsh', 'kkh', 'clinic', 'doctor', 'raffles medical', 'parkway', 'polyclinic'],
    name: 'Hospitals & Medical Care',
    category: 'medical_health',
    defaultChannel: 'contactless',
    isOnline: false,
    isForeign: false,
    mccDescription: 'MCC 8062 (Hospitals) / 8011 (Doctors)',
    specialWarning: 'Public hospitals and government polyclinics are often excluded by most rewards cards.',
    tip: 'Private clinics and Parkway/Raffles hospitals earn 4.0 mpd on UOB Lady\'s Solitaire (Family category) or standard general spend on UOB PRVI (1.4 mpd).',
  },

  // Government & Taxes (General Exclusion)
  {
    keywords: ['iras', 'income tax', 'property tax', 'lta', 'road tax', 'stamp duty', 'court', 'fine'],
    name: 'Government & Tax Payments (IRAS / LTA)',
    category: 'government_taxes',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 9399 / 9311 (Government Services)',
    specialWarning: '⚠️ 100% EXCLUDED from direct credit card points across all Singapore banks!',
    tip: 'To earn miles on taxes: Use CardUp or ipaymy with Citi PremierMiles or UOB PRVI Miles (admin fee ~1.75% to 2.25% buys miles at ~1.2¢ - 1.5¢ each).',
  },

  // Insurance
  {
    keywords: ['great eastern', 'prudential', 'aia', 'aviva', 'singlife', 'manulife', 'fwd', 'insurance premium'],
    name: 'Insurance Premiums',
    category: 'insurance',
    defaultChannel: 'online',
    isOnline: true,
    isForeign: false,
    mccDescription: 'MCC 6300 (Insurance)',
    specialWarning: '⚠️ Excluded by almost all credit cards for bonus rewards.',
    tip: 'CardUp or SCB Simply Cash (check current T&Cs) or specialized insurance payment promotions.',
  },

  // Petrol
  {
    keywords: ['shell', 'esso', 'spc', 'caltex', 'sinopec', 'petrol', 'fuel'],
    name: 'Petrol & Fuel',
    category: 'petrol',
    defaultChannel: 'contactless',
    isOnline: false,
    isForeign: false,
    mccDescription: 'MCC 5541 / 5542 (Service Stations)',
    tip: 'OCBC 365 gives up to 5% cashback (+ partner discounts up to 16% at Caltex/Sinopec). DBS Altitude gives site discounts at Esso.',
  }
];

export function matchMerchantQuery(query: string): KnownMerchant | null {
  if (!query || !query.trim()) return null;
  const clean = query.toLowerCase().trim();

  // Try exact keyword match
  for (const item of KNOWN_MERCHANTS) {
    if (item.keywords.some((k) => clean.includes(k) || k.includes(clean))) {
      return item;
    }
  }

  return null;
}
