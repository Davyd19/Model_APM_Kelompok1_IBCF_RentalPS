import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import TopBar from '../components/TopBar';
import ModeA from '../pages/ModeA';
import ModeB from '../pages/ModeB';
import ModeC from '../pages/ModeC';

const DashboardLayout = () => {
  const [activeMode, setActiveMode] = useState('C');

  const renderContent = () => {
    switch (activeMode) {
      case 'A': return <ModeA />;
      case 'B': return <ModeB />;
      case 'C': return <ModeC />;
      default: return <ModeA />;
    }
  };

  return (
    <div className="min-h-screen bg-background flex">
      <Sidebar activeMode={activeMode} setActiveMode={setActiveMode} />
      <div className="flex-1 ml-64 flex flex-col min-h-screen">
        <TopBar activeMode={activeMode} />
        <main className="flex-1 p-8 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
