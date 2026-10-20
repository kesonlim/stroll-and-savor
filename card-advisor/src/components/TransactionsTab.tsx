import React, { useState } from 'react';
import { Transaction, Category } from '../types';
import { SINGAPORE_CREDIT_CARDS } from '../data/singaporeCards';
import { Trash2, Plus, Calendar, ArrowUpRight, Filter, Receipt } from 'lucide-react';

interface TransactionsTabProps {
  transactions: Transaction[];
  onDeleteTransaction: (id: string) => void;
  onAddTransaction: (tx: Omit<Transaction, 'id' | 'date'>) => void;
}

export const TransactionsTab: React.FC<TransactionsTabProps> = ({
  transactions,
  onDeleteTransaction,
  onAddTransaction,
}) => {
  const [selectedCardFilter, setSelectedCardFilter] = useState<string>('ALL');

  const cardsMap = new Map(SINGAPORE_CREDIT_CARDS.map((c) => [c.id, c]));

  const filteredTransactions = transactions.filter((tx) => {
    if (selectedCardFilter !== 'ALL' && tx.cardId !== selectedCardFilter) return false;
    return true;
  });

  // Calculate totals
  const totalSpend = filteredTransactions.reduce((sum, tx) => sum + tx.amount, 0);
  const totalMiles = filteredTransactions
    .filter((tx) => tx.rewardEarned.type === 'miles')
    .reduce((sum, tx) => sum + tx.rewardEarned.value, 0);
  const totalCashback = filteredTransactions
    .filter((tx) => tx.rewardEarned.type === 'cashback')
    .reduce((sum, tx) => sum + tx.rewardEarned.value, 0);

  return (
    <div className="space-y-4 pb-20">
      {/* Summary Card */}
      <div className="bg-paper-card rounded-2xl p-4 border border-rule shadow-sm space-y-3">
        <div className="flex items-center justify-between">
          <span className="font-mono text-xs uppercase font-bold text-ink-muted">
            SPENDING & REWARDS LEDGER
          </span>
          <span className="text-xs font-mono text-ink-muted">
            {filteredTransactions.length} transactions
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-1">
          <div className="bg-paper p-3 rounded-xl border border-rule">
            <span className="text-[10px] font-mono uppercase text-ink-muted block">
              TOTAL SPEND LOGGED
            </span>
            <span className="text-xl font-mono font-bold text-ink">
              S${totalSpend.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
          </div>

          <div className="bg-paper p-3 rounded-xl border border-rule">
            <span className="text-[10px] font-mono uppercase text-ink-muted block">
              TOTAL MILES EARNED
            </span>
            <span className="text-xl font-mono font-bold text-rust-text">
              +{Math.round(totalMiles).toLocaleString()}
            </span>
            <span className="text-[10px] font-mono text-ink-muted block">
              KrisFlyer miles
            </span>
          </div>
        </div>
      </div>

      {/* Card Filter Chips */}
      <div className="flex space-x-1.5 overflow-x-auto pb-1 no-scrollbar">
        <button
          onClick={() => setSelectedCardFilter('ALL')}
          className={`px-3 py-1.5 rounded-xl border text-xs font-mono whitespace-nowrap transition-all ${
            selectedCardFilter === 'ALL'
              ? 'bg-ink text-paper border-ink font-semibold'
              : 'bg-paper hover:bg-paper-dark border-rule text-ink-muted'
          }`}
        >
          All Cards
        </button>
        {SINGAPORE_CREDIT_CARDS.map((card) => {
          const hasTx = transactions.some((t) => t.cardId === card.id);
          if (!hasTx) return null;
          return (
            <button
              key={card.id}
              onClick={() => setSelectedCardFilter(card.id)}
              className={`px-3 py-1.5 rounded-xl border text-xs font-mono whitespace-nowrap transition-all ${
                selectedCardFilter === card.id
                  ? 'bg-ink text-paper border-ink font-semibold'
                  : 'bg-paper hover:bg-paper-dark border-rule text-ink-muted'
              }`}
            >
              {card.name.split(' ')[0]} {card.name.includes('Lady') ? "Lady's" : ''}
            </button>
          );
        })}
      </div>

      {/* Transactions List */}
      <div className="space-y-2">
        {filteredTransactions.length === 0 ? (
          <div className="text-center py-12 bg-paper-card rounded-2xl border border-rule">
            <Receipt className="mx-auto text-ink-faint mb-2" size={32} />
            <p className="font-sans text-sm text-ink-muted">No transactions logged yet.</p>
            <p className="font-mono text-xs text-ink-faint mt-1">
              Log a spend from the Card Advisor to track your monthly caps!
            </p>
          </div>
        ) : (
          filteredTransactions.map((tx) => {
            const card = cardsMap.get(tx.cardId);
            const dateStr = new Date(tx.date).toLocaleDateString('en-SG', {
              month: 'short',
              day: 'numeric',
            });

            return (
              <div
                key={tx.id}
                className="bg-paper-card rounded-xl p-3 border border-rule flex items-center justify-between hover:border-ink/40 transition-colors shadow-sm"
              >
                <div className="space-y-0.5">
                  <div className="flex items-center space-x-2">
                    <span className="font-sans font-semibold text-sm text-ink">
                      {tx.merchant}
                    </span>
                    <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-paper border border-rule text-ink-muted">
                      {dateStr}
                    </span>
                  </div>
                  <div className="flex items-center space-x-1.5 text-xs text-ink-muted">
                    <span className="font-mono font-medium text-ink-light">
                      {card?.name || tx.cardId}
                    </span>
                    <span>•</span>
                    <span className="font-sans">{tx.category.replace('_', ' ')}</span>
                  </div>
                  <p className="text-[11px] font-mono text-rust-text">
                    +{tx.rewardEarned.value.toLocaleString()} {tx.rewardEarned.unit} ({tx.rewardEarned.details})
                  </p>
                </div>

                <div className="text-right flex items-center space-x-3">
                  <div>
                    <span className="font-mono font-bold text-sm text-ink block">
                      S${tx.amount.toFixed(2)}
                    </span>
                  </div>
                  <button
                    onClick={() => onDeleteTransaction(tx.id)}
                    className="p-1.5 text-ink-faint hover:text-rose-600 rounded transition-colors"
                    title="Delete transaction"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
