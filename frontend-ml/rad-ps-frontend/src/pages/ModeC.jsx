import React, { useState, useEffect } from 'react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip } from 'recharts';
import { TrendingDown, Activity, Lightbulb } from 'lucide-react';

const ModeC = () => {
  const [trends, setTrends] = useState([]);
  const [radarData, setRadarData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch Trends
    fetch('http://localhost:5000/api/v1/analytics/trends')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') setTrends(data.data);
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
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
      {/* Trend Predictions */}
      <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg flex flex-col h-[600px]">
        <div className="mb-6 border-b border-white/5 pb-4 flex justify-between items-center">
          <div>
            <h3 className="text-xl font-bold text-textPrimary flex items-center gap-2">
              <TrendingDown size={22} className="text-danger" />
              Trend Prediction (Deteksi Kebosanan)
            </h3>
            <p className="text-sm text-textSecondary mt-1">Saran tindakan untuk game dengan tren menurun</p>
          </div>
        </div>

        <div className="space-y-4 overflow-y-auto pr-2">
          {loading ? <p className="text-center text-textSecondary">Analyzing trends...</p> : trends.map((trend, i) => (
            <div key={i} className="bg-background rounded-xl p-5 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-danger opacity-5 rounded-bl-full transition-transform group-hover:scale-110"></div>
              
              <div className="flex flex-col relative z-10">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-bold text-lg text-textPrimary">{trend.game_name}</h4>
                  <span className="bg-danger/10 text-danger text-xs font-bold px-2 py-1 rounded border border-danger/20">
                    -{trend.drop_percentage}% Playtime
                  </span>
                </div>
                  
                  <div className="bg-accent/10 border border-accent/20 p-3 rounded-lg mt-3 flex gap-3 items-start">
                    <Lightbulb size={18} className="text-accent flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-textPrimary leading-relaxed">
                      {trend.prescriptive_action}
                    </p>
                  </div>
                </div>
              </div>
          ))}
        </div>
      </div>

      {/* Genre Distribution Radar Chart */}
      <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg flex flex-col h-[600px]">
        <div className="mb-2 border-b border-white/5 pb-4">
          <h3 className="text-xl font-bold text-textPrimary flex items-center gap-2">
            <Activity size={22} className="text-accent" />
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
  );
};

export default ModeC;
