import {
  Category,
  CreditCard,
  UserCard,
  UserPriority,
  SpendChannel,
  CardEvaluation,
  RecommendationResult,
  Transaction,
} from '../types';
import { SINGAPORE_CREDIT_CARDS } from '../data/singaporeCards';
import { matchMerchantQuery } from '../data/merchants';

export function calculateMonthlyCardSpend(
  cardId: string,
  transactions: Transaction[],
  billingCycleDay: number = 1
): number {
  const now = new Date();
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth();

  // Simple calendar month spend for standard cards
  // (or cycle day based)
  let cycleStart = new Date(currentYear, currentMonth, billingCycleDay);
  if (now.getDate() < billingCycleDay) {
    cycleStart = new Date(currentYear, currentMonth - 1, billingCycleDay);
  }

  const spend = transactions
    .filter((tx) => {
      if (tx.cardId !== cardId) return false;
      const txDate = new Date(tx.date);
      return txDate >= cycleStart && txDate <= now;
    })
    .reduce((sum, tx) => sum + tx.amount, 0);

  return spend;
}

export function evaluateCardForSpend(
  card: CreditCard,
  userCard: UserCard,
  category: Category,
  amount: number,
  isOnline: boolean,
  isForeignCurrency: boolean,
  channel: SpendChannel,
  priority: UserPriority,
  currentSpendInCycle: number,
  valuationPerMile: number = 0.016
): CardEvaluation {
  let effectiveMpd = card.baseMilesPerDollar;
  let effectiveCashback = card.baseCashbackPercent;
  let ruleApplied = 'Base earn rate';
  let isExcluded = false;
  let exclusionReason: string | undefined;

  // 1. General exclusion checks
  if (category === 'government_taxes') {
    isExcluded = true;
    exclusionReason = 'Government & taxes are excluded from credit card rewards.';
    effectiveMpd = 0;
    effectiveCashback = 0;
  } else if (category === 'insurance' && card.id !== 'sc-simply-cash') {
    isExcluded = true;
    exclusionReason = 'Insurance premiums excluded from rewards by this bank.';
    effectiveMpd = 0;
    effectiveCashback = 0;
  } else if (category === 'utilities_bills' && card.id !== 'uob-one' && card.id !== 'ocbc-365') {
    // Miles cards mostly exclude utilities
    effectiveMpd = 0;
    effectiveCashback = 0;
    ruleApplied = 'Excluded from miles rewards (Utilities/Bills)';
  } else {
    // 2. Specific card logic & quirks

    // A. DBS Woman's World Card
    if (card.id === 'dbs-wwc') {
      if (isOnline) {
        effectiveMpd = 4.0;
        ruleApplied = 'Online Retail & Travel (4.0 mpd / 10X DBS Points)';
      } else {
        effectiveMpd = 0.4;
        ruleApplied = 'Offline swipe gets only base rate (0.4 mpd). Use online or Apple Pay on a different card!';
      }
    }

    // B. Citi Rewards Card
    else if (card.id === 'citi-rewards') {
      if (
        category === 'travel_airlines' ||
        category === 'travel_hotels_ota' ||
        category === 'transport'
      ) {
        // Excluded MCCs for Citi Rewards 10X
        effectiveMpd = 0.4;
        ruleApplied = 'In-app travel & transport (Grab/Airlines/Agoda) strictly excluded from 10X (0.4 mpd only)';
      } else if (category === 'online_shopping' || (category === 'offline_shopping' && !isOnline)) {
        effectiveMpd = 4.0;
        ruleApplied = 'Retail Shopping & Department Stores (4.0 mpd / 10X ThankYou Points)';
      } else if (isOnline && (category === 'dining' || category === 'entertainment')) {
        // Food delivery & general e-commerce
        effectiveMpd = 4.0;
        ruleApplied = 'Online transaction (4.0 mpd)';
      } else {
        effectiveMpd = 0.4;
        ruleApplied = 'Non-retail / general spend earns base 0.4 mpd';
      }
    }

    // C. HSBC Revolution Card
    else if (card.id === 'hsbc-revolution') {
      if (category === 'supermarket' && !isOnline) {
        effectiveMpd = 0.4;
        ruleApplied = 'Offline supermarket contactless removed from 10X since 2024 (0.4 mpd)';
      } else if (
        isOnline &&
        (category === 'dining' ||
          category === 'online_shopping' ||
          category === 'travel_airlines' ||
          category === 'travel_hotels_ota' ||
          category === 'entertainment')
      ) {
        effectiveMpd = 4.0;
        ruleApplied = 'Online Dining, Travel & Shopping (4.0 mpd / 10X Points)';
      } else if (
        channel === 'contactless' &&
        (category === 'dining' || category === 'offline_shopping' || category === 'entertainment')
      ) {
        effectiveMpd = 4.0;
        ruleApplied = 'Contactless in-store Dining & Retail (4.0 mpd)';
      } else {
        effectiveMpd = 0.4;
        ruleApplied = 'Base earn rate (0.4 mpd)';
      }
    }

    // D. UOB Lady's / Lady's Solitaire
    else if (card.id === 'uob-ladys') {
      const selectedCats = userCard.selectedCategories || ['dining'];
      if (selectedCats.includes(category)) {
        effectiveMpd = 4.0;
        ruleApplied = `Preferred Category: ${category.replace('_', ' ').toUpperCase()} (4.0 mpd / 10X UNI$)`;
      } else {
        effectiveMpd = 0.4;
        ruleApplied = `Outside selected category (${selectedCats.join(', ')}). Base 0.4 mpd only.`;
      }
    }

    // E. KrisFlyer UOB
    else if (card.id === 'krisflyer-uob') {
      if (category === 'travel_airlines') {
        effectiveMpd = 3.0;
        ruleApplied = 'SIA Group & Scoot bookings (3.0 mpd uncapped)';
      } else if (
        category === 'dining' ||
        category === 'online_shopping' ||
        category === 'transport'
      ) {
        effectiveMpd = 3.0;
        ruleApplied = 'Accelerated everyday spend (3.0 mpd with min S$800 SIA annual spend)';
      } else {
        effectiveMpd = 1.2;
        ruleApplied = 'Base local spend (1.2 mpd uncapped)';
      }
    }

    // F. UOB PRVI Miles
    else if (card.id === 'uob-prvi-miles') {
      if (isForeignCurrency || category === 'overseas_fx') {
        effectiveMpd = 2.4;
        ruleApplied = 'Overseas foreign currency spend (2.4 mpd uncapped)';
      } else if (category === 'travel_hotels_ota') {
        effectiveMpd = 6.0;
        ruleApplied = 'Partner travel portals Agoda / Expedia (up to 6.0 mpd)';
      } else {
        effectiveMpd = 1.4;
        ruleApplied = 'Local general spend (1.4 mpd uncapped)';
      }
    }

    // G. DBS Altitude
    else if (card.id === 'dbs-altitude') {
      if (isForeignCurrency || category === 'overseas_fx') {
        effectiveMpd = 2.2;
        ruleApplied = 'Overseas FX spend (2.2 mpd uncapped)';
      } else if (category === 'travel_airlines' || category === 'travel_hotels_ota') {
        effectiveMpd = 3.0;
        ruleApplied = 'Expedia / Kaligo travel bookings (3.0 - 10.0 mpd)';
      } else {
        effectiveMpd = 1.3;
        ruleApplied = 'Local general spend (1.3 mpd uncapped)';
      }
    }

    // H. OCBC Rewards
    else if (card.id === 'ocbc-rewards') {
      if (category === 'online_shopping' || category === 'offline_shopping') {
        effectiveMpd = 4.0;
        ruleApplied = 'Eligible Retail & Electronics Shopping (4.0 mpd / 10X OCBC$)';
      } else {
        effectiveMpd = 0.4;
        ruleApplied = 'Base earn rate (0.4 mpd)';
      }
    }

    // I. UOB One Card
    else if (card.id === 'uob-one') {
      if (
        category === 'transport' ||
        category === 'online_shopping' ||
        category === 'supermarket' ||
        category === 'utilities_bills'
      ) {
        effectiveCashback = 10.0;
        ruleApplied = 'Grab, Shopee, DFI, SP Group (up to 10% - 15% cashback tier)';
      } else {
        effectiveCashback = 3.33;
        ruleApplied = 'General spend quarterly tier cashback (3.33%)';
      }
    }

    // J. OCBC 365
    else if (card.id === 'ocbc-365') {
      if (category === 'dining') {
        effectiveCashback = 5.0;
        ruleApplied = 'Dining & Food Delivery (5% cashback)';
      } else if (category === 'petrol') {
        effectiveCashback = 5.0;
        ruleApplied = 'Petrol & Fuel stations (5% cashback)';
      } else if (
        category === 'supermarket' ||
        category === 'transport' ||
        category === 'utilities_bills'
      ) {
        effectiveCashback = 3.0;
        ruleApplied = 'Groceries, Land Transport & Utilities (3% cashback)';
      } else {
        effectiveCashback = 0.3;
        ruleApplied = 'Base cashback (0.3%)';
      }
    }

    // K. SC Simply Cash / Citi Cash Back+
    else if (card.id === 'sc-simply-cash') {
      effectiveCashback = 1.5;
      ruleApplied = 'Uncapped 1.5% cashback on all eligible spends';
    } else if (card.id === 'citi-cashback-plus') {
      effectiveCashback = 1.6;
      ruleApplied = 'Uncapped 1.6% cashback on all eligible spends';
    }

    // L. Amex KrisFlyer Ascend
    else if (card.id === 'amex-krisflyer-ascend') {
      if (category === 'travel_airlines') {
        effectiveMpd = 3.2;
        ruleApplied = 'Singapore Airlines & KrisShop (3.2 mpd uncapped)';
      } else if (isForeignCurrency) {
        effectiveMpd = 2.0;
        ruleApplied = 'Overseas spend (2.0 mpd)';
      } else {
        effectiveMpd = 1.2;
        ruleApplied = 'Base local spend (1.2 mpd uncapped)';
      }
    }
  }

  // 3. Cap calculations
  const monthlyCap = userCard.customBonusCap ?? card.monthlyBonusCap;
  let capRemaining: number | null = null;
  let isCapExhausted = false;
  let warning: string | undefined;

  if (monthlyCap !== null) {
    capRemaining = Math.max(0, monthlyCap - currentSpendInCycle);
    if (capRemaining <= 0) {
      isCapExhausted = true;
      warning = `Monthly bonus cap of S$${monthlyCap.toLocaleString()} reached! Reverts to base rate.`;
      // Revert to base rate if cap exhausted
      effectiveMpd = card.baseMilesPerDollar;
      effectiveCashback = card.baseCashbackPercent;
    } else if (amount > capRemaining) {
      warning = `Only S$${Math.round(capRemaining).toLocaleString()} remaining in 4.0 mpd bonus cap for this month.`;
    }
  }

  // 4. Calculate total economic value score in SGD for this purchase
  // 1 mile is worth ~ valuationPerMile (e.g. 1.6 cents)
  const milesValue = amount * effectiveMpd * valuationPerMile;
  const cashbackValue = amount * (effectiveCashback / 100);

  let rewardValueScore = 0;
  if (priority === 'miles') {
    // Heavily weight miles
    rewardValueScore = effectiveMpd * 100 + effectiveCashback;
  } else if (priority === 'cashback') {
    // Heavily weight cashback
    rewardValueScore = effectiveCashback * 100 + effectiveMpd;
  } else {
    // Balanced: Economic value in SGD
    rewardValueScore = (milesValue + cashbackValue) * 10;
  }

  return {
    card,
    userCard,
    effectiveMpd,
    effectiveCashback,
    rewardValueScore,
    isExcluded,
    exclusionReason,
    ruleApplied,
    currentCycleSpend: currentSpendInCycle,
    monthlyCap,
    capRemaining,
    isCapExhausted,
    warning,
  };
}

export function recommendBestCard(
  query: string,
  explicitCategory: Category | undefined,
  amount: number,
  isOnlineExplicit: boolean | undefined,
  isForeignExplicit: boolean | undefined,
  channelExplicit: SpendChannel | undefined,
  priority: UserPriority,
  userCards: UserCard[],
  transactions: Transaction[],
  valuationPerMile: number = 0.016
): RecommendationResult {
  // 1. Identify category & parameters
  const merchantMatch = matchMerchantQuery(query);

  const category: Category =
    explicitCategory || merchantMatch?.category || 'general_spend';
  const isOnline: boolean =
    isOnlineExplicit !== undefined
      ? isOnlineExplicit
      : merchantMatch?.isOnline !== undefined
      ? merchantMatch.isOnline
      : true;
  const isForeign: boolean =
    isForeignExplicit !== undefined
      ? isForeignExplicit
      : merchantMatch?.isForeign !== undefined
      ? merchantMatch.isForeign
      : false;
  const channel: SpendChannel =
    channelExplicit ||
    (isOnline ? 'online' : 'contactless');

  // 2. Fetch all cards in user's wallet
  const allCardsMap = new Map(SINGAPORE_CREDIT_CARDS.map((c) => [c.id, c]));

  // If user has no cards configured, fallback to standard cards
  const cardsToEvaluate: { card: CreditCard; userCard: UserCard }[] = [];

  if (userCards.length > 0) {
    for (const uc of userCards) {
      if (!uc.isActive) continue;
      const meta = allCardsMap.get(uc.cardId);
      if (meta) {
        cardsToEvaluate.push({ card: meta, userCard: uc });
      }
    }
  } else {
    // Pre-populate with top default cards
    for (const defaultCard of SINGAPORE_CREDIT_CARDS.slice(0, 5)) {
      cardsToEvaluate.push({
        card: defaultCard,
        userCard: {
          cardId: defaultCard.id,
          selectedCategories: ['dining'],
          billingCycleDay: 1,
          isActive: true,
        },
      });
    }
  }

  // 3. Evaluate each card
  const evaluations: CardEvaluation[] = cardsToEvaluate.map(({ card, userCard }) => {
    const currentSpend = calculateMonthlyCardSpend(card.id, transactions, userCard.billingCycleDay);
    return evaluateCardForSpend(
      card,
      userCard,
      category,
      amount,
      isOnline,
      isForeign,
      channel,
      priority,
      currentSpend,
      valuationPerMile
    );
  });

  // 4. Sort evaluations: Highest rewardValueScore first
  evaluations.sort((a, b) => {
    // Non-excluded first
    if (a.isExcluded && !b.isExcluded) return 1;
    if (!a.isExcluded && b.isExcluded) return -1;

    // Non-exhausted caps first
    if (a.isCapExhausted && !b.isCapExhausted) return 1;
    if (!a.isCapExhausted && b.isCapExhausted) return -1;

    // Primary score
    return b.rewardValueScore - a.rewardValueScore;
  });

  const bestCard = evaluations[0];
  const backupCard = evaluations.length > 1 ? evaluations[1] : undefined;

  // 5. Generate human-readable summary tip
  let summaryTip = '';
  if (merchantMatch?.specialWarning) {
    summaryTip = merchantMatch.specialWarning;
  } else if (bestCard.isCapExhausted) {
    summaryTip = `⚠️ You have maxed out the monthly bonus cap on ${bestCard.card.name}. Switched recommendation to your backup card ${backupCard?.card.name || ''}.`;
  } else if (bestCard.effectiveMpd >= 4.0) {
    summaryTip = `🎉 Top-tier rewards! You will earn 4.0 miles per dollar (${Math.round(amount * 4.0).toLocaleString()} KrisFlyer miles) using ${bestCard.card.name}.`;
  } else if (bestCard.effectiveCashback >= 5.0) {
    summaryTip = `💰 High rebate! You will earn ${bestCard.effectiveCashback}% cashback (approx S$${((amount * bestCard.effectiveCashback) / 100).toFixed(2)}) using ${bestCard.card.name}.`;
  } else {
    summaryTip = `Best available card in your wallet is ${bestCard.card.name} (${bestCard.ruleApplied}).`;
  }

  return {
    merchantQuery: query || merchantMatch?.name || category.replace('_', ' '),
    category,
    isOnline,
    isForeign,
    amount,
    bestCard,
    backupCard,
    allEvaluations: evaluations,
    summaryTip,
  };
}
