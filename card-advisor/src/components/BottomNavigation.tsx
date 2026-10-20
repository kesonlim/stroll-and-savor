import React from 'react';
import { Compass, TrendingUp, CreditCard, Receipt } from 'lucide-react';

export type ActiveTab = 'advisor' | 'caps' | 'wallet' | 'ledger';

interface BottomNavigationProps {
  activeTab: ActiveTab;
  onChangeTab: (tab: ActiveTab) => void;
  capsWarningCount?: number;
}

export const BottomNavigation: React.FC<BottomNavigationProps> = ({
  activeTab,
  onChangeTab,
  capsWarningCount = 0,
}) => {
  const tabs = [
    { id: 'advisor' as ActiveTab, label: 'Advisor', icon: Compass },
    {
      id: 'caps' as ActiveTab,
      label: 'Caps',
      icon: TrendingUp,
      badge: capsWarningCount > 0 ? capsWarningCount : undefined,
    },
    { id: 'wallet' as ActiveTab, label: 'Wallet', icon: CreditCard },
    { id: 'ledger' as ActiveTab, label: 'Ledger', icon: Receipt },
  ];

  return (
    <nav className="sticky bottom-0 left-0 right-0 z-40 bg-paper/95 backdrop-blur-md border-t border-rule pb-safe mt-auto">
      <div className="max-w-md mx-auto grid grid-cols-4 px-2 py-1.5">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onChangeTab(tab.id)}
              className={`flex flex-col items-center justify-center py-1.5 px-1 rounded-xl transition-all relative ${
                isActive
                  ? 'text-ink font-bold'
                  : 'text-ink-muted hover:text-ink font-medium'
              }`}
            >
              <div className="relative">
                <Icon size={20} strokeWidth={isActive ? 2.4 : 1.8} />
                {tab.badge && (
                  <span className="absolute -top-1 -right-2 w-3.5 h-3.5 bg-rose-600 text-white rounded-full text-[9px] font-mono flex items-center justify-center font-bold">
                    !
                  </span>
                )}
              </div>
              <span className="text-[10px] font-mono tracking-tight mt-0.5">
                {tab.label}
              </span>
              {isActive && (
                <span className="w-1 h-1 rounded-full bg-ink absolute bottom-0.5" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};
