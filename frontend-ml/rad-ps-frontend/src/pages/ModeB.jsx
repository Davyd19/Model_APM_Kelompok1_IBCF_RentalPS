import React, { useState, useEffect } from 'react';
import { HardDrive, AlertTriangle, Download, ArrowUpRight, ArrowDownRight } from 'lucide-react';

const ModeB = () => {
  const [roiGames, setRoiGames] = useState([]);
  const [uninstallGames, setUninstallGames] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch ROI Games
    fetch('http://localhost:5000/api/v1/recommend/roi', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ top_k: 8 })
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') setRoiGames(data.data);
    })
    .catch(err => console.error(err));

    // Fetch Uninstall Recommendations
    fetch('http://localhost:5000/api/v1/recommend/uninstall')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') setUninstallGames(data.data);
      setLoading(false);
    })
    .catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div className="flex flex-col gap-8">
      {/* Top Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg flex justify-between items-center">
          <div>
            <h3 className="text-sm font-medium text-textSecondary mb-1">Total Storage Capacity</h3>
            <p className="text-3xl font-bold text-textPrimary">2.0 TB</p>
            <div className="flex items-center gap-2 mt-2">
              <div className="w-full bg-background rounded-full h-2 max-w-[200px]">
                <div className="bg-accent h-2 rounded-full" style={{ width: '85%' }}></div>
              </div>
              <span className="text-xs text-textSecondary">85% Used</span>
            </div>
          </div>
          <div className="w-16 h-16 rounded-full bg-accent/10 flex items-center justify-center border border-accent/20">
            <HardDrive size={28} className="text-accent" />
          </div>
        </div>

        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg flex justify-between items-center">
          <div>
            <h3 className="text-sm font-medium text-textSecondary mb-1">Storage Efficiency Score</h3>
            <p className="text-3xl font-bold text-textPrimary">A-</p>
            <p className="text-xs text-accent flex items-center gap-1 mt-2">
              <ArrowUpRight size={14} /> +12% from last month
            </p>
          </div>
          <div className="w-16 h-16 rounded-full bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
            <Activity size={28} className="text-blue-500" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
        {/* Knapsack ROI Section */}
        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg">
          <div className="flex items-center justify-between mb-6 border-b border-white/5 pb-4">
            <div>
              <h3 className="text-lg font-bold text-textPrimary flex items-center gap-2">
                <Download size={18} className="text-accent" />
                Saran Install (ROI Tertinggi)
              </h3>
              <p className="text-xs text-textSecondary mt-1">Berdasarkan rasio Potensi Laku per GB</p>
            </div>
          </div>

          <div className="space-y-4">
            {loading ? <p className="text-center text-textSecondary">Loading...</p> : roiGames.map((game, i) => (
              <div key={i} className="flex items-center justify-between bg-background p-3 rounded-xl border border-white/5 hover:border-accent/30 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-accent/10 rounded-lg flex items-center justify-center flex-shrink-0 border border-accent/20">
                    <Download size={20} className="text-accent" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-textPrimary">{game.name}</h4>
                    <p className="text-xs text-textSecondary font-medium">{game.size_gb} GB</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-accent font-bold text-sm flex items-center gap-1 justify-end">
                    {game.roi_score_normalized.toFixed(0)} <span className="text-[10px] text-textSecondary">Score</span>
                  </div>
                  <div className="w-16 bg-card rounded-full h-1.5 mt-1 ml-auto">
                    <div className="bg-accent h-1.5 rounded-full" style={{ width: `${game.roi_score_normalized}%` }}></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Uninstall Section */}
        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg">
          <div className="flex items-center justify-between mb-6 border-b border-white/5 pb-4">
            <div>
              <h3 className="text-lg font-bold text-textPrimary flex items-center gap-2">
                <AlertTriangle size={18} className="text-danger" />
                Saran Uninstall
              </h3>
              <p className="text-xs text-textSecondary mt-1">Game berukuran besar dengan minat menurun</p>
            </div>
          </div>

          <div className="space-y-4">
            {loading ? <p className="text-center text-textSecondary">Loading...</p> : uninstallGames.map((game, i) => (
              <div key={i} className="flex items-center justify-between bg-background p-3 rounded-xl border border-danger/20 border-l-4 border-l-danger">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-danger/10 rounded-lg flex items-center justify-center flex-shrink-0 border border-danger/20">
                    <AlertTriangle size={20} className="text-danger" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-textPrimary">{game.name}</h4>
                    <p className="text-xs text-textSecondary font-medium">{game.size_gb} GB terpakai</p>
                  </div>
                </div>
                <div className="text-right flex flex-col items-end">
                  <div className="text-danger font-bold text-xs flex items-center gap-1 bg-danger/10 px-2 py-1 rounded">
                    <ArrowDownRight size={14} /> -{game.mock_playtime_drop.toFixed(0)}% tren
                  </div>
                </div>
              </div>
            ))}
            
            {uninstallGames.length === 0 && !loading && (
              <p className="text-center text-textSecondary text-sm py-4">Inventaris Anda dalam kondisi optimal.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Simple Activity Icon mock if missing from lucide
const Activity = ({ size, className }) => <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>;

export default ModeB;
