import React from 'react';
import { Gamepad2, LayoutDashboard, Settings, UserPlus, FileBox } from 'lucide-react';

const Sidebar = ({ activeMode, setActiveMode }) => {
  const menuItems = [
    { id: 'A', label: 'Player', icon: <Gamepad2 size={20} /> },
    { id: 'B', label: 'Owner', icon: <FileBox size={20} /> },
    { id: 'C', label: 'Analytics', icon: <LayoutDashboard size={20} /> },
  ];

  return (
    <aside className="w-64 bg-background border-r border-card flex flex-col h-screen fixed left-0 top-0">
      <div className="p-6">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
            <Gamepad2 size={18} className="text-background" />
          </div>
          DeepVision PS
        </h1>
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveMode(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
              activeMode === item.id 
                ? 'bg-card text-accent shadow-sm' 
                : 'text-textSecondary hover:text-textPrimary hover:bg-card/50'
            }`}
          >
            {item.icon}
            <span className="font-medium text-sm">{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="p-4 mt-auto">
        <div className="bg-card rounded-2xl p-5 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-24 h-24 bg-accent opacity-10 rounded-bl-full transform translate-x-4 -translate-y-4"></div>
          <p className="text-xs text-textSecondary mb-1">Status</p>
          <p className="text-sm font-semibold text-textPrimary">System Online</p>
          <div className="mt-4 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-accent animate-pulse"></div>
            <span className="text-xs text-textSecondary">Connected to ML</span>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
