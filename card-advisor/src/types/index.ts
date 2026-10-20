export type RewardType = 'miles' | 'cashback' | 'points' | 'discount';

export type UserPriority = 'miles' | 'cashback' | 'discounts' | 'balanced';

export type SpendChannel = 'online' | 'contactless' | 'chip_pin' | 'any';

export type Category =
  | 'dining'
  | 'online_shopping'
  | 'offline_shopping'
  | 'supermarket'
  | 'travel_airlines'
  | 'travel_hotels_ota'
  | 'transport'
  | 'petrol'
  | 'utilities_bills'
  | 'overseas_fx'
  | 'entertainment'
  | 'medical_health'
  | 'government_taxes'
  | 'insurance'
  | 'education_fees'
  | 'general_spend';

export interface BonusRule {
  categories: Category[];
  channel?: SpendChannel;
  foreignOnly?: boolean;
  localOnly?: boolean;
  milesPerDollar: number;
  cashbackPercent: number;
  description: string;
  conditionNote?: string;
}

export interface CreditCard {
  id: string;
  name: string;
  bank: string;
  network: 'Visa' | 'Mastercard' | 'Amex';
  cardTier: 'entry' | 'mass_affluent' | 'prestige';
  annualFee: number;
  waivable: boolean;
  styling: {
    bgGradient: string;
    textColor: string;
    accentColor: string;
    badgeColor: string;
  };
  baseMilesPerDollar: number;
  baseCashbackPercent: number;
  monthlyBonusCap: number | null; // e.g. 1000 SGD, null if uncapped
  capResetType: 'calendar_month' | 'statement_cycle';
  bonusRules: BonusRule[];
  exclusions: string[];
  minMonthlySpend: number; // e.g. 0 or 800
  bestFor: string;
  notes: string;
  customizableCategories?: boolean; // e.g. UOB Lady's
  allowedCustomCategories?: Category[];
}

export interface UserCard {
  cardId: string;
  customNickname?: string;
  selectedCategories?: Category[]; // e.g., 'dining' for UOB Lady's
  billingCycleDay: number; // 1 to 31
  isActive: boolean;
  customBonusCap?: number;
}

export interface Transaction {
  id: string;
  date: string;
  cardId: string;
  merchant: string;
  category: Category;
  amount: number;
  isOnline: boolean;
  isForeignCurrency: boolean;
  channel: SpendChannel;
  rewardEarned: {
    type: RewardType;
    value: number;
    unit: string;
    details: string;
  };
  notes?: string;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  priority: UserPriority;
  valuationPerMileSGD: number; // default 0.016 (1.6 cents per mile)
  selectedCards: UserCard[];
}

export interface MerchantQueryMatch {
  merchantName: string;
  matchedCategory: Category;
  isOnline: boolean;
  isForeign: boolean;
  specialMCCNote?: string;
  warningNote?: string;
}

export interface CardEvaluation {
  card: CreditCard;
  userCard: UserCard;
  effectiveMpd: number;
  effectiveCashback: number;
  rewardValueScore: number; // calculated in SGD equivalent
  isExcluded: boolean;
  exclusionReason?: string;
  ruleApplied: string;
  currentCycleSpend: number;
  monthlyCap: number | null;
  capRemaining: number | null;
  isCapExhausted: boolean;
  warning?: string;
}

export interface RecommendationResult {
  merchantQuery: string;
  category: Category;
  isOnline: boolean;
  isForeign: boolean;
  amount: number;
  bestCard: CardEvaluation;
  backupCard?: CardEvaluation;
  allEvaluations: CardEvaluation[];
  summaryTip: string;
}
