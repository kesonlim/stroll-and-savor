import { UserProfile, UserCard, Transaction } from '../types';

const STORAGE_KEYS = {
  PROFILE: 'stroll_savor_card_advisor_profile',
  TRANSACTIONS: 'stroll_savor_card_advisor_transactions',
};

const DEFAULT_USER_CARDS: UserCard[] = [
  {
    cardId: 'dbs-wwc',
    billingCycleDay: 1,
    isActive: true,
  },
  {
    cardId: 'uob-ladys',
    billingCycleDay: 1,
    selectedCategories: ['dining'],
    isActive: true,
  },
  {
    cardId: 'citi-rewards',
    billingCycleDay: 1,
    isActive: true,
  },
  {
    cardId: 'hsbc-revolution',
    billingCycleDay: 1,
    isActive: true,
  },
  {
    cardId: 'uob-prvi-miles',
    billingCycleDay: 1,
    isActive: true,
  },
  {
    cardId: 'uob-one',
    billingCycleDay: 1,
    isActive: true,
  },
];

const DEFAULT_PROFILE: UserProfile = {
  id: 'user-default',
  name: 'Keson',
  email: 'keson@strollsavor.com',
  priority: 'miles',
  valuationPerMileSGD: 0.016, // 1.6 cents per KrisFlyer mile
  selectedCards: DEFAULT_USER_CARDS,
};

// Seed realistic sample transactions for current month to demonstrate cap tracking
function getSeedTransactions(): Transaction[] {
  const now = new Date();
  const currentMonthStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;

  return [
    {
      id: 'tx-1',
      date: `${currentMonthStr}-02T19:30:00.000Z`,
      cardId: 'uob-ladys',
      merchant: 'Haidilao Hotpot VivoCity',
      category: 'dining',
      amount: 218.5,
      isOnline: false,
      isForeignCurrency: false,
      channel: 'contactless',
      rewardEarned: {
        type: 'miles',
        value: 874,
        unit: 'miles',
        details: '4.0 mpd (10X UNI$) - Dining Category',
      },
    },
    {
      id: 'tx-2',
      date: `${currentMonthStr}-04T14:15:00.000Z`,
      cardId: 'dbs-wwc',
      merchant: 'Shopee Official Store',
      category: 'online_shopping',
      amount: 450.0,
      isOnline: true,
      isForeignCurrency: false,
      channel: 'online',
      rewardEarned: {
        type: 'miles',
        value: 1800,
        unit: 'miles',
        details: '4.0 mpd (10X DBS Points) - Online Retail',
      },
    },
    {
      id: 'tx-3',
      date: `${currentMonthStr}-06T08:45:00.000Z`,
      cardId: 'dbs-wwc',
      merchant: 'Grab Ride to Changi T3',
      category: 'transport',
      amount: 38.2,
      isOnline: true,
      isForeignCurrency: false,
      channel: 'online',
      rewardEarned: {
        type: 'miles',
        value: 152.8,
        unit: 'miles',
        details: '4.0 mpd (10X DBS Points) - Online Transport',
      },
    },
    {
      id: 'tx-4',
      date: `${currentMonthStr}-08T12:20:00.000Z`,
      cardId: 'citi-rewards',
      merchant: 'Amazon SG Prime Delivery',
      category: 'online_shopping',
      amount: 185.0,
      isOnline: true,
      isForeignCurrency: false,
      channel: 'online',
      rewardEarned: {
        type: 'miles',
        value: 740,
        unit: 'miles',
        details: '4.0 mpd (10X Citi Points) - Online Retail',
      },
    },
    {
      id: 'tx-5',
      date: `${currentMonthStr}-10T20:10:00.000Z`,
      cardId: 'uob-ladys',
      merchant: 'Jumbo Seafood East Coast',
      category: 'dining',
      amount: 360.0,
      isOnline: false,
      isForeignCurrency: false,
      channel: 'contactless',
      rewardEarned: {
        type: 'miles',
        value: 1440,
        unit: 'miles',
        details: '4.0 mpd (10X UNI$) - Dining Category',
      },
    },
  ];
}

export function loadUserProfile(): UserProfile {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.PROFILE);
    if (!raw) {
      saveUserProfile(DEFAULT_PROFILE);
      return DEFAULT_PROFILE;
    }
    return JSON.parse(raw);
  } catch (e) {
    console.error('Error loading user profile:', e);
    return DEFAULT_PROFILE;
  }
}

export function saveUserProfile(profile: UserProfile): void {
  try {
    localStorage.setItem(STORAGE_KEYS.PROFILE, JSON.stringify(profile));
  } catch (e) {
    console.error('Error saving user profile:', e);
  }
}

export function loadTransactions(): Transaction[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.TRANSACTIONS);
    if (!raw) {
      const seed = getSeedTransactions();
      saveTransactions(seed);
      return seed;
    }
    return JSON.parse(raw);
  } catch (e) {
    console.error('Error loading transactions:', e);
    return [];
  }
}

export function saveTransactions(transactions: Transaction[]): void {
  try {
    localStorage.setItem(STORAGE_KEYS.TRANSACTIONS, JSON.stringify(transactions));
  } catch (e) {
    console.error('Error saving transactions:', e);
  }
}

export function logNewSpend(tx: Omit<Transaction, 'id' | 'date'>): Transaction {
  const all = loadTransactions();
  const newTx: Transaction = {
    ...tx,
    id: `tx-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
    date: new Date().toISOString(),
  };
  all.unshift(newTx);
  saveTransactions(all);
  return newTx;
}

export function deleteTransaction(txId: string): void {
  const all = loadTransactions();
  const filtered = all.filter((t) => t.id !== txId);
  saveTransactions(filtered);
}
