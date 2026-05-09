import React from 'react';
import { Search, Bell, Settings } from 'lucide-react';

const TopBar = ({ activeMode }) => {
  const getTitle = () => {
    switch (activeMode) {
      case 'A': return 'Player Recommendations';
      case 'B': return 'Inventory & Yield Optimization';
      case 'C': return 'Dashboard Analytics';
      default: return 'Dashboard';
    }
  };

  return (
    <header className="h-20 border-b border-card bg-background/80 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-10">
      <div>
        <h2 className="text-2xl font-bold text-textPrimary">{getTitle()}</h2>
      </div>
    </header>
  );
};

export default TopBar;
