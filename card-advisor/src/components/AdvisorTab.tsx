import React, { useState, useMemo } from 'react';
import {
  Category,
  SpendChannel,
  UserPriority,
  UserCard,
  Transaction,
  RecommendationResult,
} from '../types';
import { recommendBestCard } from '../services/advisorEngine';
import {
  Search,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  PlusCircle,
  Sparkles,
  CreditCard as CardIcon,
  Globe,
  Wifi,
  Smartphone,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

interface AdvisorTabProps {
  priority: UserPriority;
  userCards: UserCard[];
  transactions: Transaction[];
  onLogSpend: (txData: {
    cardId: string;
    merchant: string;
    category: Category;
    amount: number;
    isOnline: boolean;
    isForeignCurrency: boolean;
    channel: SpendChannel;
    rewardEarned: {
      type: 'miles' | 'cashback';
      value: number;
      unit: string;
      details: string;
    };
  }) => void;
}

const CATEGORY_CHIPS: { id: Category; label: string; icon: string }[] = [
  { id: 'dining', label: 'Dining / Food', icon: '🍽️' },
  { id: 'online_shopping', label: 'Online Retail', icon: '🛍️' },
  { id: 'travel_airlines', label: 'SIA & Flights', icon: '✈️' },
  { id: 'transport', label: 'Grab & Transport', icon: '🚕' },
  { id: 'supermarket', label: 'Supermarkets', icon: '🛒' },
  { id: 'travel_hotels_ota', label: 'Hotels & Agoda', icon: '🏨' },
  { id: 'overseas_fx', label: 'Overseas FX', icon: '🌏' },
  { id: 'utilities_bills', label: 'Utilities & Bills', icon: '⚡' },
  { id: 'general_spend', label: 'General Retail', icon: '💳' },
];

const SUGGESTED_SCENARIOS = [
  'Shopee order $85',
  'Haidilao hotpot dinner $180',
  'Grab ride to airport $35',
  'Singapore Airlines flight $1,250',
  'FairPrice groceries $95',
  'Apple Store MacBook $2,499',
  'SP Group utility bill $160',
  'Tokyo dinner ¥15,000 (FX)',
];

export const AdvisorTab: React.FC<AdvisorTabProps> = ({
  priority,
  userCards,
  transactions,
  onLogSpend,
}) => {
  const [query, setQuery] = useState('');
  const [amountStr, setAmountStr] = useState('100');
  const [selectedCategory, setSelectedCategory] = useState<Category | undefined>(undefined);
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [isForeign, setIsForeign] = useState<boolean>(false);
  const [channel, setChannel] = useState<SpendChannel>('online');
  const [showAllRankings, setShowAllRankings] = useState(false);
  const [loggedSuccess, setLoggedSuccess] = useState(false);

  const amount = parseFloat(amountStr) || 0;

  // Run the advisor engine
  const recommendation: RecommendationResult = useMemo(() => {
    return recommendBestCard(
      query,
      selectedCategory,
      amount,
      isOnline,
      isForeign,
      channel,
      priority,
      userCards,
      transactions
    );
  }, [
    query,
    selectedCategory,
    amount,
    isOnline,
    isForeign,
    channel,
    priority,
    userCards,
    transactions,
  ]);

  const best = recommendation.bestCard;
  const backup = recommendation.backupCard;

  const handleSelectScenario = (scenario: string) => {
    setQuery(scenario);
    // Auto extract amount if present
    const match = scenario.match(/\$(\d+[\d,]*)/);
    if (match) {
      setAmountStr(match[1].replace(',', ''));
    }
    // Auto toggle online/contactless
    if (scenario.toLowerCase().includes('haidilao') || scenario.toLowerCase().includes('fairprice')) {
      setIsOnline(false);
      setChannel('contactless');
    } else {
      setIsOnline(true);
      setChannel('online');
    }
  };

  const handleLogClick = () => {
    if (!best || amount <= 0) return;

    const isMilesPriority = priority === 'miles' || best.effectiveMpd > 0;
    const earnedValue = isMilesPriority
      ? Math.round(amount * best.effectiveMpd)
      : parseFloat(((amount * best.effectiveCashback) / 100).toFixed(2));

    onLogSpend({
      cardId: best.card.id,
      merchant: query.trim() || recommendation.category.replace('_', ' ').toUpperCase(),
      category: recommendation.category,
      amount,
      isOnline,
      isForeignCurrency: isForeign,
      channel,
      rewardEarned: {
        type: isMilesPriority ? 'miles' : 'cashback',
        value: earnedValue,
        unit: isMilesPriority ? 'miles' : 'SGD',
        details: best.ruleApplied,
      },
    });

    setLoggedSuccess(true);
    setTimeout(() => setLoggedSuccess(false), 2500);
  };

  return (
    <div className="space-y-4 pb-20">
      {/* 1. Situation Search & Amount Input */}
      <div className="bg-paper-card rounded-2xl p-4 border border-rule shadow-sm space-y-3">
        <label className="block text-xs font-mono font-bold uppercase tracking-wider text-ink-muted">
          Where are you spending?
        </label>

        {/* Input box */}
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              // reset explicit chip if typing freeform
              if (selectedCategory) setSelectedCategory(undefined);
            }}
            placeholder="e.g. Shopee, Haidilao, Grab, SIA tickets..."
            className="w-full bg-paper pl-10 pr-4 py-3 rounded-xl border border-rule text-ink placeholder:text-ink-faint font-sans text-sm focus:outline-none focus:ring-2 focus:ring-ink"
          />
          <Search
            size={18}
            className="absolute left-3.5 top-3.5 text-ink-muted"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="absolute right-3 top-3 text-xs font-mono text-ink-muted hover:text-ink px-1.5 py-0.5 rounded"
            >
              Clear
            </button>
          )}
        </div>

        {/* Quick scenarios suggestion bar */}
        {!query && (
          <div className="flex items-center space-x-1.5 overflow-x-auto py-1 no-scrollbar text-xs">
            <span className="text-[10px] font-mono text-ink-muted whitespace-nowrap">Try:</span>
            {SUGGESTED_SCENARIOS.slice(0, 4).map((sc) => (
              <button
                key={sc}
                onClick={() => handleSelectScenario(sc)}
                className="whitespace-nowrap px-2.5 py-1 bg-paper hover:bg-paper-dark rounded-full border border-rule text-ink-light text-xs transition-colors font-sans"
              >
                {sc}
              </button>
            ))}
          </div>
        )}

        {/* Spend Amount & Modifiers */}
        <div className="grid grid-cols-2 gap-2 pt-1">
          {/* Amount */}
          <div>
            <label className="block text-[11px] font-mono text-ink-muted mb-1">
              ESTIMATED SPEND (SGD)
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2.5 text-sm font-mono text-ink-muted">$</span>
              <input
                type="number"
                value={amountStr}
                onChange={(e) => setAmountStr(e.target.value)}
                placeholder="100"
                className="w-full bg-paper pl-7 pr-3 py-2 rounded-lg border border-rule text-ink font-mono text-sm focus:outline-none focus:ring-2 focus:ring-ink"
              />
            </div>
          </div>

          {/* Online vs In-Person Toggle */}
          <div>
            <label className="block text-[11px] font-mono text-ink-muted mb-1">
              PAYMENT METHOD
            </label>
            <div className="grid grid-cols-2 gap-1 bg-paper p-1 rounded-lg border border-rule">
              <button
                type="button"
                onClick={() => {
                  setIsOnline(true);
                  setChannel('online');
                }}
                className={`text-xs py-1.5 rounded-md font-mono text-center transition-all ${
                  isOnline
                    ? 'bg-paper-card font-bold text-ink shadow-sm'
                    : 'text-ink-muted hover:text-ink'
                }`}
              >
                🌐 Online
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsOnline(false);
                  setChannel('contactless');
                }}
                className={`text-xs py-1.5 rounded-md font-mono text-center transition-all ${
                  !isOnline
                    ? 'bg-paper-card font-bold text-ink shadow-sm'
                    : 'text-ink-muted hover:text-ink'
                }`}
              >
                📱 Tap / Pay
              </button>
            </div>
          </div>
        </div>

        {/* Foreign Currency FX Checkbox */}
        <div className="flex items-center justify-between pt-1 text-xs">
          <label className="flex items-center space-x-2 text-ink-muted cursor-pointer">
            <input
              type="checkbox"
              checked={isForeign}
              onChange={(e) => setIsForeign(e.target.checked)}
              className="rounded border-rule text-ink focus:ring-0 w-4 h-4"
            />
            <span className="font-sans">Foreign currency spend (Non-SGD / Overseas)</span>
          </label>
          <span className="font-mono text-[10px] text-ink-faint">
            {isForeign ? '🌏 Overseas Rates' : '🇸🇬 Local SGD'}
          </span>
        </div>

        {/* Category Quick Chips */}
        <div>
          <label className="block text-[11px] font-mono text-ink-muted mb-1.5">
            OR SELECT CATEGORY
          </label>
          <div className="flex space-x-1.5 overflow-x-auto pb-1 no-scrollbar">
            {CATEGORY_CHIPS.map((cat) => {
              const isSelected = selectedCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategory(isSelected ? undefined : cat.id)}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border text-xs whitespace-nowrap transition-all ${
                    isSelected
                      ? 'bg-ink text-paper border-ink font-semibold shadow-sm'
                      : 'bg-paper hover:bg-paper-dark border-rule text-ink-light'
                  }`}
                >
                  <span>{cat.icon}</span>
                  <span>{cat.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* 2. Recommendation Result Card (HERO) */}
      <div className="relative overflow-hidden rounded-2xl border-2 border-ink bg-paper-card shadow-field">
        {/* Header banner */}
        <div className="bg-ink text-paper px-4 py-2.5 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-mono font-bold text-xs uppercase tracking-wider">
              BEST CARD RECOMMENDATION
            </span>
          </div>
          <span className="font-mono text-[11px] text-paper-dark bg-white/10 px-2 py-0.5 rounded">
            {recommendation.category.replace('_', ' ').toUpperCase()}
          </span>
        </div>

        {/* Card Body */}
        <div className="p-4 space-y-4">
          {/* Card Presentation visual */}
          <div
            className={`rounded-xl p-4 bg-gradient-to-br ${best.card.styling.bgGradient} text-white shadow-md relative overflow-hidden`}
          >
            {/* Background design accents */}
            <div className="absolute right-0 top-0 translate-x-4 -translate-y-4 w-32 h-32 rounded-full bg-white/5 pointer-events-none" />
            <div className="absolute right-4 bottom-4 opacity-20 font-display font-bold text-3xl">
              {best.card.network}
            </div>

            <div className="flex justify-between items-start mb-4">
              <div>
                <span className="text-[10px] font-mono tracking-widest uppercase opacity-75">
                  {best.card.bank}
                </span>
                <h3 className="font-display font-bold text-lg leading-tight mt-0.5 text-white">
                  {best.card.name}
                </h3>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-white/20 backdrop-blur-sm">
                #{1} PICK
              </span>
            </div>

            {/* Big Reward Display */}
            <div className="flex items-baseline space-x-2 pt-2 border-t border-white/10">
              {best.effectiveMpd > 0 && (
                <div className="flex items-baseline space-x-1.5">
                  <span className="font-mono font-bold text-2xl text-amber-300">
                    {best.effectiveMpd.toFixed(1)}
                  </span>
                  <span className="text-xs font-mono uppercase text-amber-200">mpd</span>
                  <span className="text-[11px] opacity-75 ml-1">
                    (approx +{Math.round(amount * best.effectiveMpd).toLocaleString()} miles)
                  </span>
                </div>
              )}
              {best.effectiveCashback > 0 && (
                <div className="flex items-baseline space-x-1.5">
                  <span className="font-mono font-bold text-2xl text-emerald-300">
                    {best.effectiveCashback.toFixed(1)}%
                  </span>
                  <span className="text-xs font-mono uppercase text-emerald-200">rebate</span>
                  <span className="text-[11px] opacity-75 ml-1">
                    (approx S${((amount * best.effectiveCashback) / 100).toFixed(2)})
                  </span>
                </div>
              )}
            </div>

            <p className="text-xs opacity-85 mt-2 font-sans flex items-center space-x-1">
              <span>✓</span>
              <span>{best.ruleApplied}</span>
            </p>
          </div>

          {/* Monthly Cap Progress (if card has a monthly cap) */}
          {best.monthlyCap !== null && (
            <div className="bg-paper p-3 rounded-xl border border-rule space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="font-mono text-ink-muted">
                  MONTHLY BONUS CAP (S${best.monthlyCap.toLocaleString()})
                </span>
                <span className="font-mono font-bold text-ink">
                  {best.isCapExhausted
                    ? '⚠️ CAP EXHAUSTED'
                    : `S$${Math.round(best.capRemaining || 0).toLocaleString()} LEFT`}
                </span>
              </div>
              {/* Progress bar */}
              <div className="w-full h-2 rounded-full bg-rule/50 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    best.isCapExhausted
                      ? 'bg-rose-500'
                      : (best.capRemaining || 0) < 300
                      ? 'bg-amber-500'
                      : 'bg-emerald-600'
                  }`}
                  style={{
                    width: `${Math.min(
                      100,
                      (best.currentCycleSpend / best.monthlyCap) * 100
                    )}%`,
                  }}
                />
              </div>
              <div className="flex justify-between text-[11px] text-ink-muted">
                <span>Used: S${Math.round(best.currentCycleSpend).toLocaleString()}</span>
                <span>Resets 1st of month</span>
              </div>
            </div>
          )}

          {/* Special Advice / Warning Box */}
          {recommendation.summaryTip && (
            <div className="bg-amber-subtle border border-amber-border/50 p-3 rounded-xl flex items-start space-x-2 text-xs text-amber-950 font-sans">
              <AlertTriangle size={16} className="text-amber-700 shrink-0 mt-0.5" />
              <div>
                <p className="leading-relaxed">{recommendation.summaryTip}</p>
              </div>
            </div>
          )}

          {/* Backup Card Recommendation */}
          {backup && (
            <div className="bg-paper p-3 rounded-xl border border-rule flex items-center justify-between">
              <div>
                <span className="text-[10px] font-mono uppercase text-ink-muted block">
                  RUNNER-UP / BACKUP CARD
                </span>
                <span className="font-sans font-semibold text-sm text-ink">
                  {backup.card.name}
                </span>
                <span className="text-xs font-mono text-ink-muted ml-2">
                  {backup.effectiveMpd > 0 ? `${backup.effectiveMpd} mpd` : `${backup.effectiveCashback}%`}
                </span>
              </div>
              <span className="text-xs font-mono text-rust-text font-semibold">
                Use if cap maxed
              </span>
            </div>
          )}

          {/* Quick Action: Log Spend to Ledger */}
          <div className="pt-2">
            <button
              onClick={handleLogClick}
              disabled={loggedSuccess}
              className={`w-full py-3 px-4 rounded-xl font-mono text-xs font-bold uppercase tracking-wider flex items-center justify-center space-x-2 transition-all ${
                loggedSuccess
                  ? 'bg-emerald-700 text-white'
                  : 'bg-ink text-paper hover:bg-ink-light active:scale-[0.99] shadow-sm'
              }`}
            >
              {loggedSuccess ? (
                <>
                  <CheckCircle2 size={16} />
                  <span>Logged S${amount} to {best.card.name}!</span>
                </>
              ) : (
                <>
                  <PlusCircle size={16} />
                  <span>Log S${amount} spend on {best.card.bank}</span>
                </>
              )}
            </button>
          </div>

          {/* Drawer trigger to see all cards ranking */}
          <div className="text-center pt-1">
            <button
              onClick={() => setShowAllRankings(!showAllRankings)}
              className="text-xs font-mono text-ink-muted hover:text-ink inline-flex items-center space-x-1"
            >
              <span>{showAllRankings ? 'Hide other cards' : 'Compare all cards in wallet'}</span>
              {showAllRankings ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
          </div>
        </div>

        {/* Collapsible Wallet Comparison Drawer */}
        {showAllRankings && (
          <div className="border-t border-rule bg-paper p-4 space-y-2">
            <h4 className="font-mono text-xs uppercase font-bold text-ink-muted mb-2">
              Full Wallet Ranking for this spend:
            </h4>
            <div className="space-y-2">
              {recommendation.allEvaluations.map((evalItem, idx) => (
                <div
                  key={evalItem.card.id}
                  className={`p-3 rounded-xl border text-xs flex items-center justify-between ${
                    idx === 0
                      ? 'bg-emerald-50/60 border-emerald-300'
                      : evalItem.isExcluded
                      ? 'bg-paper-dark/50 border-rule opacity-60'
                      : 'bg-paper-card border-rule'
                  }`}
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center space-x-1.5">
                      <span className="font-mono font-bold text-ink-muted">#{idx + 1}</span>
                      <span className="font-sans font-semibold text-ink">
                        {evalItem.card.name}
                      </span>
                    </div>
                    <p className="text-[11px] text-ink-muted">{evalItem.ruleApplied}</p>
                    {evalItem.warning && (
                      <p className="text-[10px] text-rose-700 font-mono">{evalItem.warning}</p>
                    )}
                  </div>
                  <div className="text-right">
                    <span className="font-mono font-bold text-sm text-ink block">
                      {evalItem.effectiveMpd > 0
                        ? `${evalItem.effectiveMpd} mpd`
                        : `${evalItem.effectiveCashback}%`}
                    </span>
                    <span className="text-[10px] font-mono text-ink-muted">
                      {evalItem.effectiveMpd > 0
                        ? `+${Math.round(amount * evalItem.effectiveMpd)} mi`
                        : `S$${((amount * evalItem.effectiveCashback) / 100).toFixed(2)}`}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
