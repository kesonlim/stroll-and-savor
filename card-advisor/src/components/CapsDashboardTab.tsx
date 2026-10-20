import React from 'react';
import { UserCard, Transaction } from '../types';
import { SINGAPORE_CREDIT_CARDS } from '../data/singaporeCards';
import { calculateMonthlyCardSpend } from '../services/advisorEngine';
import { AlertCircle, CheckCircle2, TrendingUp, Calendar, Zap, CreditCard as CardIcon } from 'lucide-react';

interface CapsDashboardTabProps {
  userCards: UserCard[];
  transactions: Transaction[];
  onSelectCard: (cardId: string) => void;
}

export const CapsDashboardTab: React.FC<CapsDashboardTabProps> = ({
  userCards,
  transactions,
  onSelectCard,
}) => {
  const cardsMap = new Map(SINGAPORE_CREDIT_CARDS.map((c) => [c.id, c]));

  // Calculate days until 1st of next month
  const now = new Date();
  const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);
  const daysUntilReset = Math.ceil(
    (nextMonth.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
  );

  // Cards with caps
  const cappedCardsData = userCards
    .map((uc) => {
      const card = cardsMap.get(uc.cardId);
      if (!card) return null;
      const cap = uc.customBonusCap ?? card.monthlyBonusCap;
      const currentSpend = calculateMonthlyCardSpend(card.id, transactions, uc.billingCycleDay);
      const remaining = cap !== null ? Math.max(0, cap - currentSpend) : null;
      const percentage = cap !== null ? Math.min(100, Math.round((currentSpend / cap) * 100)) : null;

      return {
        card,
        userCard: uc,
        cap,
        currentSpend,
        remaining,
        percentage,
        isCapped: cap !== null,
        isExhausted: remaining !== null && remaining <= 0,
        isNearCap: remaining !== null && remaining > 0 && percentage! >= 75,
      };
    })
    .filter(Boolean) as Array<{
    card: (typeof SINGAPORE_CREDIT_CARDS)[0];
    userCard: UserCard;
    cap: number | null;
    currentSpend: number;
    remaining: number | null;
    percentage: number | null;
    isCapped: boolean;
    isExhausted: boolean;
    isNearCap: boolean;
  }>;

  // Separate capped vs uncapped cards
  const cappedList = cappedCardsData.filter((c) => c.isCapped);
  const uncappedList = cappedCardsData.filter((c) => !c.isCapped);

  // Total bonus potential tracking
  const totalCapPool = cappedList.reduce((acc, c) => acc + (c.cap || 0), 0);
  const totalSpentPool = cappedList.reduce((acc, c) => acc + c.currentSpend, 0);
  const totalRemainingPool = Math.max(0, totalCapPool - totalSpentPool);

  return (
    <div className="space-y-4 pb-20">
      {/* Overview Metric Banner */}
      <div className="bg-paper-card rounded-2xl p-4 border border-rule shadow-sm space-y-3">
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs uppercase font-bold text-ink-muted">
            MONTHLY 4.0 MPD BONUS CAPACITY
          </span>
          <div className="flex items-center space-x-1 text-xs font-mono text-ink-muted bg-paper px-2 py-0.5 rounded-full border border-rule">
            <Calendar size={13} />
            <span>Resets in {daysUntilReset} days</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-1">
          <div className="bg-paper p-3 rounded-xl border border-rule">
            <span className="text-[10px] font-mono uppercase text-ink-muted block">
              REMAINING BONUS CAPACITY
            </span>
            <span className="text-xl font-mono font-bold text-emerald-800">
              S${Math.round(totalRemainingPool).toLocaleString()}
            </span>
            <span className="text-[10px] font-mono text-ink-muted block mt-0.5">
              Available at 4.0 mpd
            </span>
          </div>

          <div className="bg-paper p-3 rounded-xl border border-rule">
            <span className="text-[10px] font-mono uppercase text-ink-muted block">
              TOTAL SPENT THIS MONTH
            </span>
            <span className="text-xl font-mono font-bold text-ink">
              S${Math.round(totalSpentPool).toLocaleString()}
            </span>
            <span className="text-[10px] font-mono text-ink-muted block mt-0.5">
              Across capped cards
            </span>
          </div>
        </div>
      </div>

      {/* Capped Cards List */}
      <div className="space-y-3">
        <h3 className="font-mono text-xs uppercase font-bold text-ink-muted px-1">
          Capped Reward Cards ({cappedList.length})
        </h3>

        {cappedList.map((item) => (
          <div
            key={item.card.id}
            className={`bg-paper-card rounded-2xl p-4 border transition-all ${
              item.isExhausted
                ? 'border-rose-300 bg-rose-50/20'
                : item.isNearCap
                ? 'border-amber-300'
                : 'border-rule'
            } shadow-sm space-y-3`}
          >
            {/* Top Card Title & Bank */}
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-ink/10 text-ink">
                    {item.card.bank}
                  </span>
                  <h4 className="font-display font-bold text-base text-ink">
                    {item.card.name}
                  </h4>
                </div>
                <p className="text-xs text-ink-muted mt-0.5 font-sans">
                  {item.card.bestFor}
                </p>
              </div>

              {/* Status Badge */}
              {item.isExhausted ? (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-rose-100 text-rose-800 border border-rose-200">
                  CAP REACHED
                </span>
              ) : item.isNearCap ? (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-100 text-amber-800 border border-amber-200">
                  {item.percentage}% USED
                </span>
              ) : (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                  HEALTHY
                </span>
              )}
            </div>

            {/* Progress Bar */}
            <div className="space-y-1">
              <div className="w-full h-3 rounded-full bg-rule/50 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    item.isExhausted
                      ? 'bg-rose-500'
                      : item.isNearCap
                      ? 'bg-amber-500'
                      : 'bg-emerald-600'
                  }`}
                  style={{ width: `${item.percentage}%` }}
                />
              </div>
              <div className="flex justify-between text-xs font-mono">
                <span className="text-ink font-semibold">
                  S${Math.round(item.currentSpend).toLocaleString()} spent
                </span>
                <span className="text-ink-muted">
                  Cap: S${item.cap?.toLocaleString()} / mo
                </span>
              </div>
            </div>

            {/* Remaining amount or warning */}
            <div className="pt-1 flex items-center justify-between text-xs border-t border-rule/60">
              {item.isExhausted ? (
                <span className="text-rose-700 font-sans font-medium flex items-center space-x-1">
                  <AlertCircle size={14} />
                  <span>Bonus cap exhausted. Further spend earns only 0.4 mpd!</span>
                </span>
              ) : (
                <span className="text-emerald-800 font-mono font-medium">
                  S${Math.round(item.remaining || 0).toLocaleString()} remaining at 4.0 mpd
                </span>
              )}

              <span className="text-[10px] font-mono text-ink-muted">
                Cycle: Day {item.userCard.billingCycleDay}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Uncapped Safety Net Cards */}
      {uncappedList.length > 0 && (
        <div className="space-y-2 pt-2">
          <h3 className="font-mono text-xs uppercase font-bold text-ink-muted px-1">
            Uncapped General Spend Cards ({uncappedList.length})
          </h3>
          <div className="grid grid-cols-1 gap-2">
            {uncappedList.map((item) => (
              <div
                key={item.card.id}
                className="bg-paper p-3 rounded-xl border border-rule flex items-center justify-between"
              >
                <div>
                  <span className="font-mono text-[10px] uppercase font-bold text-ink-muted">
                    {item.card.bank}
                  </span>
                  <h4 className="font-sans font-semibold text-sm text-ink">
                    {item.card.name}
                  </h4>
                  <p className="text-xs text-ink-muted">{item.card.bestFor}</p>
                </div>
                <div className="text-right">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-ink text-paper">
                    NO CAP
                  </span>
                  <span className="block text-xs font-mono text-ink-muted mt-1">
                    S${Math.round(item.currentSpend).toLocaleString()} spent
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
