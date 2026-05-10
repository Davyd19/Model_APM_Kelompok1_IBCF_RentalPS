import React, { useState, useEffect } from 'react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip } from 'recharts';
import { Activity, Gamepad2, Clock, MonitorPlay, Users, Trophy } from 'lucide-react';
import GameDetailModal from '../components/GameDetailModal';

const ModeC = () => {
  const [stockSummary, setStockSummary] = useState(null);
  const [radarData, setRadarData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedGame, setSelectedGame] = useState(null);

  useEffect(() => {
    // Fetch Stock Summary
    fetch('http://localhost:5000/api/v1/analytics/stock_summary')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') setStockSummary(data.data);
    })
    .catch(err => console.error(err));

    // Fetch Radar Data
    fetch('http://localhost:5000/api/v1/analytics/genres')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') setRadarData(data.data);
      setLoading(false);
    })
    .catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <>
    <div className="flex flex-col gap-8">
      {/* Analytics Intro */}
      <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg">
        <h3 className="text-xl font-bold text-textPrimary flex items-center gap-2 mb-2">
          <Activity size={22} className="text-blue-400" />
          Analisis Stok Rental
        </h3>
        <p className="text-sm text-textSecondary">Ringkasan performa stok saat ini berdasarkan playtime, platform, genre, dan kemiripan katalog.</p>
        
        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-6">
          <div className="bg-background border border-white/5 rounded-xl p-4 flex flex-col items-center justify-center text-center">
            <Gamepad2 size={24} className="text-blue-500 mb-2 opacity-80" />
            <h4 className="text-2xl font-bold text-textPrimary">{stockSummary ? stockSummary.total_games : '-'}</h4>
            <span className="text-[10px] uppercase tracking-wider text-textSecondary font-bold mt-1">Total Game Stok</span>
          </div>
          <div className="bg-background border border-white/5 rounded-xl p-4 flex flex-col items-center justify-center text-center">
            <Clock size={24} className="text-accent mb-2 opacity-80" />
            <h4 className="text-2xl font-bold text-textPrimary">{stockSummary ? Math.floor(stockSummary.total_playtime) : '-'}</h4>
            <span className="text-[10px] uppercase tracking-wider text-textSecondary font-bold mt-1">Total Playtime (Jam)</span>
          </div>
          <div className="bg-background border border-white/5 rounded-xl p-4 flex flex-col items-center justify-center text-center">
            <MonitorPlay size={24} className="text-purple-500 mb-2 opacity-80" />
            <h4 className="text-2xl font-bold text-textPrimary">{stockSummary ? stockSummary.ps5_count : '-'}</h4>
            <span className="text-[10px] uppercase tracking-wider text-textSecondary font-bold mt-1">Tersedia PS5</span>
          </div>
          <div className="bg-background border border-white/5 rounded-xl p-4 flex flex-col items-center justify-center text-center">
            <Users size={24} className="text-orange-500 mb-2 opacity-80" />
            <h4 className="text-2xl font-bold text-textPrimary">{stockSummary ? stockSummary.multiplayer_count : '-'}</h4>
            <span className="text-[10px] uppercase tracking-wider text-textSecondary font-bold mt-1">Multiplayer Lokal</span>
          </div>
          <div className="bg-background border border-white/5 rounded-xl p-4 flex flex-col items-center justify-center text-center">
            <Activity size={24} className="text-pink-500 mb-2 opacity-80" />
            <h4 className="text-2xl font-bold text-textPrimary">{stockSummary ? stockSummary.avg_similarity : '-'}</h4>
            <span className="text-[10px] uppercase tracking-wider text-textSecondary font-bold mt-1">Avg Similarity ke RAWG</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
        {/* Playtime Ranking */}
        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg flex flex-col h-[600px]">
          <div className="mb-6 border-b border-white/5 pb-4">
            <h3 className="text-xl font-bold text-textPrimary flex items-center gap-2">
              <Trophy size={22} className="text-accent" />
              Ranking Game berdasarkan Playtime
            </h3>
          </div>

          <div className="space-y-4 overflow-y-auto pr-2 flex-1">
            {loading || !stockSummary ? <p className="text-center text-textSecondary">Memuat ranking...</p> : (
              stockSummary.ranking.map((game, i) => {
                const maxPlaytime = stockSummary.ranking[0]?.playtime || 1;
                const percentage = Math.max(5, (game.playtime / maxPlaytime) * 100);
                
                return (
                  <div 
                    key={i} 
                    className="bg-background rounded-xl p-4 border border-white/5 cursor-pointer hover:border-accent/30 transition-colors group"
                    onClick={() => setSelectedGame(game.name)}
                  >
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex items-center gap-3">
                        <span className="text-textSecondary font-bold text-sm w-5">#{i + 1}</span>
                        <h4 className="font-bold text-sm text-textPrimary">{game.name}</h4>
                        {game.genre && (
                          <span className="text-[10px] bg-white/5 border border-white/10 px-2 py-0.5 rounded text-textSecondary">
                            {game.genre}
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-textSecondary">{Math.floor(game.playtime)} jam</span>
                        <span className="text-[10px] text-accent/60 group-hover:text-accent transition-colors hidden group-hover:inline">• Detail</span>
                      </div>
                    </div>
                    <div className="w-full bg-card rounded-full h-1.5 mt-2">
                      <div 
                        className="h-1.5 rounded-full bg-gradient-to-r from-blue-600 to-purple-500" 
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })
            )}
            
            {!loading && stockSummary?.ranking?.length === 0 && (
               <p className="text-center text-textSecondary">Data kosong.</p>
            )}
          </div>
        </div>

        {/* Genre Distribution Radar Chart */}
        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg flex flex-col h-[600px]">
          <div className="mb-2 border-b border-white/5 pb-4">
            <h3 className="text-xl font-bold text-textPrimary flex items-center gap-2">
              <Activity size={22} className="text-blue-400" />
              Kesehatan Distribusi Genre
            </h3>
            <p className="text-sm text-textSecondary mt-1">Supply (Inventaris) vs Demand (Minat Pemain)</p>
          </div>

          <div className="flex-1 flex flex-col items-center justify-center relative">
            {loading ? (
              <p className="text-textSecondary">Loading chart data...</p>
            ) : radarData.length > 0 ? (
              <>
                <ResponsiveContainer width="100%" height="80%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                    <PolarGrid stroke="#374151" />
                    <PolarAngleAxis dataKey="genre" tick={{ fill: '#9ca3af', fontSize: 12 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#6b7280' }} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e1e20', border: '1px solid #374151', borderRadius: '8px' }}
                      itemStyle={{ color: '#f3f4f6' }}
                    />
                    <Radar name="Supply (HDD)" dataKey="inventory" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
                    <Radar name="Demand (Pemain)" dataKey="demand" stroke="#4ade80" fill="#4ade80" fillOpacity={0.4} />
                  </RadarChart>
                </ResponsiveContainer>
                
                <div className="absolute bottom-4 flex gap-6 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                    <span className="text-textSecondary">Supply (Inventaris di HDD)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-accent"></div>
                    <span className="text-textSecondary">Demand (Minat Pemain)</span>
                  </div>
                </div>
              </>
            ) : (
              <p className="text-textSecondary">Data tidak cukup untuk menampilkan chart.</p>
            )}
          </div>
          
          {!loading && radarData.length > 0 && (
            <div className="mt-4 bg-background p-4 rounded-xl border border-white/5 text-sm text-textSecondary">
              <span className="font-semibold text-textPrimary">Insight Generator: </span>
              Berdasarkan grafik di atas, pastikan area Supply yang melebihi Demand dipertimbangkan untuk di-uninstall (Mode B), dan area Demand yang melebihi Supply segera dipenuhi dengan game baru.
            </div>
          )}
        </div>
      </div>
    </div>
    {selectedGame && <GameDetailModal gameName={selectedGame} onClose={() => setSelectedGame(null)} />}
    </>
  );
};

export default ModeC;
