import React, { useState, useEffect } from 'react';
import { UserProfile, UserCard, Transaction } from './types';
import {
  loadUserProfile,
  saveUserProfile,
  loadTransactions,
  saveTransactions,
  logNewSpend,
  deleteTransaction,
} from './services/storage';
import { SINGAPORE_CREDIT_CARDS } from './data/singaporeCards';
import { calculateMonthlyCardSpend } from './services/advisorEngine';

import { Header } from './components/Header';
import { BottomNavigation, ActiveTab } from './components/BottomNavigation';
import { AdvisorTab } from './components/AdvisorTab';
import { CapsDashboardTab } from './components/CapsDashboardTab';
import { WalletTab } from './components/WalletTab';
import { TransactionsTab } from './components/TransactionsTab';
import { SettingsModal } from './components/SettingsModal';

export const App: React.FC = () => {
  const [profile, setProfile] = useState<UserProfile>(loadUserProfile);
  const [transactions, setTransactions] = useState<Transaction[]>(loadTransactions);
  const [activeTab, setActiveTab] = useState<ActiveTab>('advisor');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isSimulatorMode, setIsSimulatorMode] = useState(true);

  // Sync profile changes
  const handleSaveProfile = (updatedProfile: UserProfile) => {
    setProfile(updatedProfile);
    saveUserProfile(updatedProfile);
  };

  const handleUpdateUserCards = (updatedCards: UserCard[]) => {
    const updatedProfile = { ...profile, selectedCards: updatedCards };
    setProfile(updatedProfile);
    saveUserProfile(updatedProfile);
  };

  // Spend logging
  const handleLogSpend = (txData: any) => {
    const newTx = logNewSpend(txData);
    setTransactions([newTx, ...transactions]);
  };

  const handleDeleteTransaction = (id: string) => {
    deleteTransaction(id);
    setTransactions(transactions.filter((t) => t.id !== id));
  };

  const handleResetData = () => {
    localStorage.clear();
    setProfile(loadUserProfile());
    setTransactions(loadTransactions());
  };

  // Count cards with urgent cap status
  const cardsMap = new Map(SINGAPORE_CREDIT_CARDS.map((c) => [c.id, c]));
  const capsWarningCount = profile.selectedCards.filter((uc) => {
    if (!uc.isActive) return false;
    const card = cardsMap.get(uc.cardId);
    if (!card || card.monthlyBonusCap === null) return false;
    const spend = calculateMonthlyCardSpend(card.id, transactions, uc.billingCycleDay);
    const cap = uc.customBonusCap ?? card.monthlyBonusCap;
    return spend >= cap * 0.8;
  }).length;

  const content = (
    <div className="min-h-full flex-1 bg-paper flex flex-col justify-between">
      <div className="flex-1">
        <Header
          priority={profile.priority}
          onOpenSettings={() => setIsSettingsOpen(true)}
          isSimulatorMode={isSimulatorMode}
          onToggleSimulator={() => setIsSimulatorMode(!isSimulatorMode)}
        />

        <main className="max-w-md mx-auto px-4 pt-4">
          {activeTab === 'advisor' && (
            <AdvisorTab
              priority={profile.priority}
              userCards={profile.selectedCards}
              transactions={transactions}
              onLogSpend={handleLogSpend}
            />
          )}

          {activeTab === 'caps' && (
            <CapsDashboardTab
              userCards={profile.selectedCards}
              transactions={transactions}
              onSelectCard={(id) => {
                setActiveTab('wallet');
              }}
            />
          )}

          {activeTab === 'wallet' && (
            <WalletTab
              userCards={profile.selectedCards}
              onUpdateUserCards={handleUpdateUserCards}
            />
          )}

          {activeTab === 'ledger' && (
            <TransactionsTab
              transactions={transactions}
              onDeleteTransaction={handleDeleteTransaction}
              onAddTransaction={(tx) => handleLogSpend(tx)}
            />
          )}
        </main>
      </div>

      <BottomNavigation
        activeTab={activeTab}
        onChangeTab={setActiveTab}
        capsWarningCount={capsWarningCount}
      />

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        profile={profile}
        onSaveProfile={handleSaveProfile}
        onResetData={handleResetData}
      />
    </div>
  );

  // If in desktop simulator mode, wrap in a sleek smartphone frame
  return (
    <div className="min-h-screen bg-paper-dark/70 md:py-6 flex items-center justify-center font-sans">
      {isSimulatorMode ? (
        <div className="w-full max-w-[430px] h-[92vh] max-h-[920px] bg-paper rounded-[42px] shadow-2xl border-[10px] border-ink overflow-hidden flex flex-col relative">
          {/* Phone Speaker & Dynamic Island */}
          <div className="h-6 bg-ink flex items-center justify-center relative shrink-0">
            <div className="w-24 h-4 bg-ink-light rounded-full mt-1 flex items-center justify-end px-2">
              <div className="w-2.5 h-2.5 rounded-full bg-slate-900 border border-slate-700" />
            </div>
          </div>

          {/* Screen Content */}
          <div className="flex-1 overflow-y-auto relative no-scrollbar">
            {content}
          </div>

          {/* Home indicator bar */}
          <div className="h-4 bg-paper flex items-center justify-center shrink-0">
            <div className="w-32 h-1 bg-ink/20 rounded-full" />
          </div>
        </div>
      ) : (
        <div className="w-full">{content}</div>
      )}
    </div>
  );
};
export default App;
