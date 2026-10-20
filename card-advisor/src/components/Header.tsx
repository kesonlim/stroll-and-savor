import React from 'react';
import { UserPriority } from '../types';
import { Smartphone, Monitor, Sparkles, Award } from 'lucide-react';

interface HeaderProps {
  priority: UserPriority;
  onOpenSettings: () => void;
  isSimulatorMode: boolean;
  onToggleSimulator: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  priority,
  onOpenSettings,
  isSimulatorMode,
  onToggleSimulator,
}) => {
  const getPriorityLabel = () => {
    switch (priority) {
      case 'miles':
        return { label: 'MAX MILES', icon: '✈️', color: 'bg-rust-subtle text-rust-text border-rust/20' };
      case 'cashback':
        return { label: 'MAX CASHBACK', icon: '💰', color: 'bg-emerald-50 text-emerald-800 border-emerald-200' };
      case 'discounts':
        return { label: 'DISCOUNTS', icon: '🏷️', color: 'bg-blue-50 text-blue-800 border-blue-200' };
      case 'balanced':
        return { label: 'BALANCED', icon: '⚖️', color: 'bg-amber-50 text-amber-900 border-amber-200' };
    }
  };

  const badge = getPriorityLabel();

  return (
    <header className="sticky top-0 z-40 bg-paper/95 backdrop-blur-md border-b border-rule px-4 py-3">
      <div className="max-w-md mx-auto flex items-center justify-between">
        {/* Brand identity */}
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-ink text-paper flex items-center justify-center font-display font-bold text-lg shadow-sm">
            S
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-display font-bold text-ink tracking-tight text-base">
                Stroll & Savor
              </span>
              <span className="text-[10px] font-mono uppercase bg-ink/10 text-ink px-1.5 py-0.5 rounded font-semibold">
                SG
              </span>
            </div>
            <p className="text-[11px] font-mono text-ink-muted -mt-0.5">
              CARD ADVISOR & CAP TRACKER
            </p>
          </div>
        </div>

        {/* Right actions: Priority button & Device simulator toggle */}
        <div className="flex items-center space-x-2">
          {/* Priority chip */}
          <button
            onClick={onOpenSettings}
            className={`flex items-center space-x-1 px-2.5 py-1 rounded-full text-xs font-mono font-semibold border transition-transform active:scale-95 shadow-sm ${badge.color}`}
            title="Change optimization priority"
          >
            <span>{badge.icon}</span>
            <span>{badge.label}</span>
          </button>

          {/* Desktop simulator toggle */}
          <button
            onClick={onToggleSimulator}
            className="hidden md:flex items-center justify-center w-8 h-8 rounded-full border border-rule bg-paper-card text-ink-muted hover:text-ink transition-colors shadow-sm"
            title={isSimulatorMode ? 'Switch to responsive view' : 'Switch to phone frame'}
          >
            {isSimulatorMode ? <Monitor size={15} /> : <Smartphone size={15} />}
          </button>
        </div>
      </div>
    </header>
  );
};
