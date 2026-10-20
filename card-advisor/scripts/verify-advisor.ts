import { recommendBestCard, evaluateCardForSpend } from '../src/services/advisorEngine';
import { SINGAPORE_CREDIT_CARDS } from '../src/data/singaporeCards';
import { UserCard, Transaction } from '../src/types';

const defaultCards: UserCard[] = [
  { cardId: 'dbs-wwc', billingCycleDay: 1, isActive: true },
  { cardId: 'uob-ladys', billingCycleDay: 1, selectedCategories: ['dining'], isActive: true },
  { cardId: 'citi-rewards', billingCycleDay: 1, isActive: true },
  { cardId: 'hsbc-revolution', billingCycleDay: 1, isActive: true },
  { cardId: 'uob-prvi-miles', billingCycleDay: 1, isActive: true },
  { cardId: 'uob-one', billingCycleDay: 1, isActive: true },
];

console.log('=== RUNNING SINGAPORE CARD ADVISOR VERIFICATION SUITE ===\n');

// Test 1: Grab ride (Test Citi Rewards Exclusion)
const recGrab = recommendBestCard(
  'Grab ride to Marina Bay',
  undefined,
  35,
  true,
  false,
  'online',
  'miles',
  defaultCards,
  []
);
console.log('Test 1 [Grab Ride]:');
console.log('  Winner:', recGrab.bestCard.card.name, 'with', recGrab.bestCard.effectiveMpd, 'mpd');
console.log('  Rule applied:', recGrab.bestCard.ruleApplied);
const citiEval = recGrab.allEvaluations.find((e) => e.card.id === 'citi-rewards');
console.log('  Citi Rewards rate:', citiEval?.effectiveMpd, 'mpd (Exclusion correctly enforced:', citiEval?.effectiveMpd === 0.4, ')');
if (recGrab.bestCard.effectiveMpd !== 4.0 || citiEval?.effectiveMpd !== 0.4) {
  throw new Error('Test 1 Failed: Citi Rewards should be 0.4 mpd on Grab and DBS WWC should win with 4.0 mpd');
}

// Test 2: Dining at Haidilao
const recDining = recommendBestCard(
  'Haidilao Hotpot',
  undefined,
  180,
  false,
  false,
  'contactless',
  'miles',
  defaultCards,
  []
);
console.log('\nTest 2 [Dining - Haidilao]:');
console.log('  Winner:', recDining.bestCard.card.name, 'with', recDining.bestCard.effectiveMpd, 'mpd');
console.log('  Rule applied:', recDining.bestCard.ruleApplied);
if (recDining.bestCard.effectiveMpd !== 4.0) {
  throw new Error('Test 2 Failed: Expected 4.0 mpd on Dining');
}

// Test 3: Utilities SP Group (Miles cards excluded, UOB One should win)
const recBills = recommendBestCard(
  'SP Group electricity bill',
  undefined,
  150,
  true,
  false,
  'online',
  'balanced',
  defaultCards,
  []
);
console.log('\nTest 3 [Utilities - SP Group]:');
console.log('  Winner:', recBills.bestCard.card.name);
console.log('  Reward:', recBills.bestCard.effectiveCashback, '% cashback');
if (recBills.bestCard.card.id !== 'uob-one' || recBills.bestCard.effectiveCashback < 5.0) {
  throw new Error('Test 3 Failed: UOB One should win for utilities with cashback');
}

// Test 4: Cap Exhaustion Switch
const cappedTxs: Transaction[] = [
  {
    id: 'tx-old-1',
    date: new Date().toISOString(),
    cardId: 'dbs-wwc',
    merchant: 'Big Online Purchase',
    category: 'online_shopping',
    amount: 1500, // Exhausts DBS WWC S$1,500 cap
    isOnline: true,
    isForeignCurrency: false,
    channel: 'online',
    rewardEarned: { type: 'miles', value: 6000, unit: 'miles', details: 'Cap reached' },
  },
];

const recOnlineCapped = recommendBestCard(
  'Shopee Electronics purchase',
  undefined,
  200,
  true,
  false,
  'online',
  'miles',
  defaultCards,
  cappedTxs
);
console.log('\nTest 4 [Cap Exhaustion Fallback]:');
console.log('  DBS WWC Cap Exhausted! New Winner:', recOnlineCapped.bestCard.card.name, 'with', recOnlineCapped.bestCard.effectiveMpd, 'mpd');
console.log('  Summary Alert:', recOnlineCapped.summaryTip);
if (recOnlineCapped.bestCard.card.id === 'dbs-wwc') {
  throw new Error('Test 4 Failed: DBS WWC cap was exhausted, should have promoted backup card');
}

console.log('\nALL 4 TESTS PASSED PERFECTLY!');
