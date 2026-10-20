import React, { useState } from 'react';
import { UserCard, Category } from '../types';
import { SINGAPORE_CREDIT_CARDS } from '../data/singaporeCards';
import { Plus, Check, Trash2, Settings2, ShieldCheck, Sparkles, CreditCard as CardIcon } from 'lucide-react';

interface WalletTabProps {
  userCards: UserCard[];
  onUpdateUserCards: (newCards: UserCard[]) => void;
}

const LADYS_CATEGORIES: { id: Category; label: string }[] = [
  { id: 'dining', label: 'Dining (Restaurants, food delivery)' },
  { id: 'travel_airlines', label: 'Travel (Airlines & OTAs)' },
  { id: 'online_shopping', label: 'Fashion / Online Shopping' },
  { id: 'transport', label: 'Transport (Grab, petrol, SimplyGo)' },
  { id: 'entertainment', label: 'Entertainment (Bars, cinemas, ticketing)' },
  { id: 'medical_health', label: 'Family / Healthcare (Clinics & hospitals)' },
];

export const WalletTab: React.FC<WalletTabProps> = ({
  userCards,
  onUpdateUserCards,
}) => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedBankFilter, setSelectedBankFilter] = useState<string>('ALL');

  const existingCardIds = new Set(userCards.map((c) => c.cardId));

  const availableCatalogCards = SINGAPORE_CREDIT_CARDS.filter((c) => {
    if (selectedBankFilter !== 'ALL' && c.bank !== selectedBankFilter) return false;
    return true;
  });

  const handleToggleCardActive = (cardId: string) => {
    const updated = userCards.map((c) =>
      c.cardId === cardId ? { ...c, isActive: !c.isActive } : c
    );
    onUpdateUserCards(updated);
  };

  const handleRemoveCard = (cardId: string) => {
    const updated = userCards.filter((c) => c.cardId !== cardId);
    onUpdateUserCards(updated);
  };

  const handleAddCard = (cardId: string) => {
    const updated: UserCard[] = [
      ...userCards,
      {
        cardId,
        billingCycleDay: 1,
        selectedCategories: ['dining' as Category],
        isActive: true,
      },
    ];
    onUpdateUserCards(updated);
  };

  const handleSelectLadysCategory = (cardId: string, cat: Category) => {
    const updated = userCards.map((c) =>
      c.cardId === cardId ? { ...c, selectedCategories: [cat] } : c
    );
    onUpdateUserCards(updated);
  };

  const banks = ['ALL', 'DBS', 'UOB', 'OCBC', 'Citi', 'HSBC', 'Standard Chartered', 'American Express'];

  return (
    <div className="space-y-4 pb-20">
      {/* Header banner with Add Card Button */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-display font-bold text-lg text-ink">My Card Wallet</h2>
          <p className="text-xs text-ink-muted">
            {userCards.filter((c) => c.isActive).length} active cards in your advisor rotation
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-ink text-paper text-xs font-mono font-bold hover:bg-ink-light transition-all shadow-sm"
        >
          <Plus size={15} />
          <span>Add Card</span>
        </button>
      </div>

      {/* Cards currently in wallet */}
      <div className="space-y-3">
        {userCards.map((uc) => {
          const card = SINGAPORE_CREDIT_CARDS.find((c) => c.id === uc.cardId);
          if (!card) return null;

          return (
            <div
              key={uc.cardId}
              className={`rounded-2xl border p-4 bg-paper-card transition-all ${
                uc.isActive ? 'border-rule shadow-sm' : 'border-rule/50 opacity-50 bg-paper'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  {/* Card Mini Color Badge */}
                  <div
                    className={`w-11 h-8 rounded-lg bg-gradient-to-br ${card.styling.bgGradient} flex items-center justify-center text-white text-[9px] font-mono font-bold shrink-0 shadow-sm`}
                  >
                    {card.bank}
                  </div>

                  <div>
                    <div className="flex items-center space-x-2">
                      <h4 className="font-display font-bold text-sm text-ink leading-snug">
                        {card.name}
                      </h4>
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-paper border border-rule text-ink-muted">
                        {card.network}
                      </span>
                    </div>

                    <p className="text-xs text-ink-muted mt-0.5 font-sans">
                      {card.bestFor}
                    </p>

                    <div className="flex items-center space-x-3 mt-2 text-xs font-mono">
                      <span className="text-rust-text font-semibold">
                        {card.monthlyBonusCap ? `Cap: S$${card.monthlyBonusCap}/mo` : 'Uncapped'}
                      </span>
                      <span className="text-ink-muted">•</span>
                      <span className="text-ink-muted">
                        Cycle Day {uc.billingCycleDay}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Right controls: Active switch & delete */}
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleToggleCardActive(uc.cardId)}
                    className={`px-2 py-1 rounded-md text-[11px] font-mono transition-colors ${
                      uc.isActive
                        ? 'bg-emerald-100 text-emerald-800 font-semibold'
                        : 'bg-paper text-ink-muted'
                    }`}
                  >
                    {uc.isActive ? 'ACTIVE' : 'MUTED'}
                  </button>
                  <button
                    onClick={() => handleRemoveCard(uc.cardId)}
                    className="p-1 text-ink-faint hover:text-rose-600 transition-colors"
                    title="Remove from wallet"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>

              {/* Special options for UOB Lady's (Choose Category) */}
              {card.id === 'uob-ladys' && uc.isActive && (
                <div className="mt-3 pt-3 border-t border-rule/70">
                  <label className="block text-[11px] font-mono text-ink-muted mb-1.5 uppercase">
                    Preferred 4.0 mpd Category:
                  </label>
                  <div className="grid grid-cols-2 gap-1.5">
                    {LADYS_CATEGORIES.map((cat) => {
                      const isSelected = uc.selectedCategories?.includes(cat.id);
                      return (
                        <button
                          key={cat.id}
                          onClick={() => handleSelectLadysCategory(uc.cardId, cat.id)}
                          className={`text-left px-2.5 py-1.5 rounded-lg text-xs font-sans transition-all border ${
                            isSelected
                              ? 'bg-ink text-paper font-semibold border-ink'
                              : 'bg-paper hover:bg-paper-dark border-rule text-ink-light'
                          }`}
                        >
                          {cat.label}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Add Card Catalog Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-ink/50 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4">
          <div className="bg-paper-card w-full max-w-md rounded-t-3xl sm:rounded-2xl border border-rule shadow-2xl max-h-[85vh] flex flex-col overflow-hidden animate-in slide-in-from-bottom-5">
            {/* Modal Header */}
            <div className="p-4 border-b border-rule flex items-center justify-between">
              <div>
                <h3 className="font-display font-bold text-base text-ink">
                  Add Singapore Card
                </h3>
                <p className="text-xs text-ink-muted">
                  Choose from popular miles & cashback cards
                </p>
              </div>
              <button
                onClick={() => setShowAddModal(false)}
                className="w-7 h-7 rounded-full bg-paper flex items-center justify-center text-ink-muted hover:text-ink font-mono text-sm"
              >
                ✕
              </button>
            </div>

            {/* Bank Filter Chips */}
            <div className="p-3 border-b border-rule bg-paper overflow-x-auto flex space-x-1.5 no-scrollbar">
              {banks.map((b) => (
                <button
                  key={b}
                  onClick={() => setSelectedBankFilter(b)}
                  className={`px-2.5 py-1 rounded-full text-xs font-mono whitespace-nowrap transition-colors ${
                    selectedBankFilter === b
                      ? 'bg-ink text-paper font-bold'
                      : 'bg-paper-card text-ink-muted hover:text-ink border border-rule'
                  }`}
                >
                  {b}
                </button>
              ))}
            </div>

            {/* Cards Catalog List */}
            <div className="p-4 overflow-y-auto space-y-2.5 flex-1">
              {availableCatalogCards.map((card) => {
                const isAlreadyInWallet = existingCardIds.has(card.id);

                return (
                  <div
                    key={card.id}
                    className="p-3 rounded-xl border border-rule bg-paper hover:bg-paper-light transition-all flex items-center justify-between"
                  >
                    <div>
                      <div className="flex items-center space-x-1.5">
                        <span className="text-[10px] font-mono px-1 rounded bg-ink/10 text-ink font-semibold">
                          {card.bank}
                        </span>
                        <h4 className="font-sans font-bold text-sm text-ink">
                          {card.name}
                        </h4>
                      </div>
                      <p className="text-xs text-ink-muted mt-0.5">{card.bestFor}</p>
                      <span className="text-[11px] font-mono text-rust-text block mt-1">
                        {card.monthlyBonusCap ? `Cap S$${card.monthlyBonusCap}/mo` : 'Uncapped'}
                      </span>
                    </div>

                    <div>
                      {isAlreadyInWallet ? (
                        <span className="flex items-center space-x-1 text-xs font-mono text-emerald-700 bg-emerald-100 px-2 py-1 rounded-lg">
                          <Check size={14} />
                          <span>Added</span>
                        </span>
                      ) : (
                        <button
                          onClick={() => {
                            handleAddCard(card.id);
                            setShowAddModal(false);
                          }}
                          className="px-3 py-1.5 rounded-lg bg-ink text-paper text-xs font-mono font-bold hover:bg-ink-light transition-all"
                        >
                          + Add
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
