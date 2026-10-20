import React from 'react';
import { UserProfile, UserPriority } from '../types';
import { Sliders, RefreshCw, X, Check, Award, Plane, DollarSign, Scale } from 'lucide-react';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  profile: UserProfile;
  onSaveProfile: (profile: UserProfile) => void;
  onResetData: () => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  profile,
  onSaveProfile,
  onResetData,
}) => {
  if (!isOpen) return null;

  const priorities: {
    id: UserPriority;
    title: string;
    description: string;
    icon: string;
  }[] = [
    {
      id: 'miles',
      title: 'Maximize Air Miles (4.0 mpd)',
      description: 'Prioritizes KrisFlyer / Asia Miles. Ideal for business class redemptions.',
      icon: '✈️',
    },
    {
      id: 'cashback',
      title: 'Maximize Cash Rebates',
      description: 'Prioritizes direct cash rebates and monthly statement credits (3% - 15%).',
      icon: '💰',
    },
    {
      id: 'balanced',
      title: 'Balanced Economic Value',
      description: 'Calculates the real SGD monetary value of miles (~1.6¢/mile) vs cashback.',
      icon: '⚖️',
    },
  ];

  return (
    <div className="fixed inset-0 z-50 bg-ink/60 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4">
      <div className="bg-paper-card w-full max-w-md rounded-t-3xl sm:rounded-2xl border border-rule shadow-2xl p-5 space-y-5 animate-in slide-in-from-bottom-5">
        <div className="flex items-center justify-between border-b border-rule pb-3">
          <div className="flex items-center space-x-2">
            <Sliders size={18} className="text-ink" />
            <h3 className="font-display font-bold text-base text-ink">
              Advisor Strategy & Preferences
            </h3>
          </div>
          <button
            onClick={onClose}
            className="w-7 h-7 rounded-full bg-paper flex items-center justify-center text-ink-muted hover:text-ink text-sm font-mono"
          >
            ✕
          </button>
        </div>

        {/* Priority Selection */}
        <div className="space-y-2">
          <label className="block text-xs font-mono font-bold uppercase tracking-wider text-ink-muted">
            Optimization Priority
          </label>
          <div className="space-y-2">
            {priorities.map((p) => {
              const isSelected = profile.priority === p.id;
              return (
                <button
                  key={p.id}
                  onClick={() => onSaveProfile({ ...profile, priority: p.id })}
                  className={`w-full text-left p-3 rounded-xl border transition-all flex items-start justify-between ${
                    isSelected
                      ? 'bg-paper border-ink ring-1 ring-ink shadow-sm'
                      : 'bg-paper-card border-rule hover:border-ink/40'
                  }`}
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center space-x-2">
                      <span className="text-base">{p.icon}</span>
                      <span className="font-display font-bold text-sm text-ink">
                        {p.title}
                      </span>
                    </div>
                    <p className="text-xs text-ink-muted font-sans pl-6">
                      {p.description}
                    </p>
                  </div>
                  {isSelected && (
                    <div className="w-5 h-5 rounded-full bg-ink text-paper flex items-center justify-center text-xs mt-0.5">
                      ✓
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Mile Valuation Setting */}
        <div className="bg-paper p-3.5 rounded-xl border border-rule space-y-2">
          <div className="flex justify-between items-center text-xs font-mono">
            <span className="text-ink-muted uppercase">MILE VALUATION</span>
            <span className="font-bold text-ink">
              S${profile.valuationPerMileSGD.toFixed(3)} / mile
            </span>
          </div>
          <input
            type="range"
            min="0.010"
            max="0.025"
            step="0.001"
            value={profile.valuationPerMileSGD}
            onChange={(e) =>
              onSaveProfile({
                ...profile,
                valuationPerMileSGD: parseFloat(e.target.value),
              })
            }
            className="w-full accent-ink cursor-pointer"
          />
          <p className="text-[11px] text-ink-muted font-sans">
            Standard community benchmark for Singapore Airlines KrisFlyer is 1.5¢ - 1.8¢ per mile.
          </p>
        </div>

        {/* Data Reset Button */}
        <div className="pt-2 border-t border-rule flex items-center justify-between">
          <button
            onClick={() => {
              if (window.confirm('Reset all transactions and cards to default demo state?')) {
                onResetData();
                onClose();
              }
            }}
            className="flex items-center space-x-1.5 text-xs font-mono text-ink-muted hover:text-rose-700 transition-colors"
          >
            <RefreshCw size={14} />
            <span>Reset Demo Data</span>
          </button>

          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-ink text-paper text-xs font-mono font-bold hover:bg-ink-light transition-all"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
