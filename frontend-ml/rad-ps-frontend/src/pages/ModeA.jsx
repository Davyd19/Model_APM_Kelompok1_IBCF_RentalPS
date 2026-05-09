import React, { useState, useEffect } from 'react';
import { Search, Plus, Trash2, Zap, Users, MonitorPlay, Activity, Gamepad2 } from 'lucide-react';

const ModeA = () => {
  const [stockGames, setStockGames] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [cart, setCart] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  // Filters
  const [coop, setCoop] = useState(false);
  const [story, setStory] = useState(false);
  const [quickMatch, setQuickMatch] = useState(false);

  useEffect(() => {
    fetch('http://localhost:5000/api/v1/games/stock')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') setStockGames(data.data);
      })
      .catch(err => console.error(err));
  }, []);

  const handleAddCart = (game) => {
    if (cart.length < 3 && !cart.includes(game)) {
      setCart([...cart, game]);
      setSearchQuery('');
    }
  };

  const handleRemoveCart = (game) => {
    setCart(cart.filter(g => g !== game));
  };

  const handleRecommend = () => {
    if (cart.length === 0) return;
    setLoading(true);

    const payload = {
      game_names: cart,
      top_k: 10,
      multiplayer_only: coop,
      singleplayer_only: story,
      quick_match: quickMatch
    };

    fetch('http://localhost:5000/api/v1/recommend/player', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      setLoading(false);
      if (data.status === 'success') {
        setRecommendations(data.data);
      }
    })
    .catch(err => {
      setLoading(false);
      console.error(err);
    });
  };

  return (
    <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
      {/* Left Panel: Inputs */}
      <div className="xl:col-span-1 flex flex-col gap-6">
        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-textPrimary">Keranjang Suka (Multi-Seed)</h3>
          
          <div className="relative mb-4">
            <Search className="absolute left-3 top-3 text-textSecondary" size={18} />
            <input 
              type="text" 
              placeholder="Cari game..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-background border border-white/10 rounded-xl py-2 pl-10 pr-4 text-textPrimary focus:outline-none focus:border-accent"
            />
          </div>

          <div className="space-y-2 max-h-60 overflow-y-auto pr-2 mb-4">
            {stockGames.filter(g => g.toLowerCase().includes(searchQuery.toLowerCase())).map((g, i) => {
              const isChecked = cart.includes(g);
              const isDisabled = !isChecked && cart.length >= 3;
              return (
                <label key={i} className={`flex items-center gap-3 p-3 rounded-xl border transition-all cursor-pointer ${isChecked ? 'bg-accent/10 border-accent/50' : 'bg-background border-white/5 hover:border-white/20'} ${isDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}>
                  <input 
                    type="checkbox" 
                    checked={isChecked}
                    disabled={isDisabled}
                    onChange={() => {
                      if (isChecked) {
                        handleRemoveCart(g);
                      } else if (!isDisabled) {
                        handleAddCart(g);
                      }
                    }}
                    className="accent-accent w-4 h-4 rounded"
                  />
                  <span className="text-sm font-medium">{g}</span>
                </label>
              );
            })}
            {stockGames.length > 0 && stockGames.filter(g => g.toLowerCase().includes(searchQuery.toLowerCase())).length === 0 && (
              <div className="text-center text-textSecondary text-sm py-4">Game tidak ditemukan.</div>
            )}
          </div>
          
          <div className="text-xs text-textSecondary mb-2">
            Terpilih: {cart.length} / 3
          </div>
        </div>

        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-textPrimary">Context Filters</h3>
          <div className="space-y-4">
            <label className="flex items-center justify-between cursor-pointer group">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${coop ? 'bg-accent/20 text-accent' : 'bg-background text-textSecondary'}`}>
                  <Users size={18} />
                </div>
                <span className="text-sm font-medium">Local Co-op / Split-screen</span>
              </div>
              <input type="checkbox" checked={coop} onChange={(e) => setCoop(e.target.checked)} className="accent-accent w-4 h-4 rounded" />
            </label>

            <label className="flex items-center justify-between cursor-pointer group">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${story ? 'bg-accent/20 text-accent' : 'bg-background text-textSecondary'}`}>
                  <MonitorPlay size={18} />
                </div>
                <span className="text-sm font-medium">Single-player Story</span>
              </div>
              <input type="checkbox" checked={story} onChange={(e) => setStory(e.target.checked)} className="accent-accent w-4 h-4 rounded" />
            </label>

            <label className="flex items-center justify-between cursor-pointer group">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${quickMatch ? 'bg-accent/20 text-accent' : 'bg-background text-textSecondary'}`}>
                  <Zap size={18} />
                </div>
                <span className="text-sm font-medium">Quick Match (Sesi Cepat)</span>
              </div>
              <input type="checkbox" checked={quickMatch} onChange={(e) => setQuickMatch(e.target.checked)} className="accent-accent w-4 h-4 rounded" />
            </label>
          </div>
        </div>

        <button 
          onClick={handleRecommend}
          disabled={cart.length === 0 || loading}
          className="w-full bg-accent text-background font-bold py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-accentHover disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {loading ? <Activity size={20} className="animate-spin" /> : <Zap size={20} />}
          Generate Recommendation
        </button>
      </div>

      {/* Right Panel: Results */}
      <div className="xl:col-span-2">
        <div className="bg-card p-6 rounded-2xl border border-white/5 shadow-lg min-h-[600px]">
          <div className="flex justify-between items-end mb-6 border-b border-white/5 pb-4">
            <div>
              <h3 className="text-xl font-bold text-textPrimary">Top Recommendations</h3>
              <p className="text-sm text-textSecondary">Berdasarkan AI Intersection Score</p>
            </div>
            {recommendations.length > 0 && <span className="text-xs font-semibold bg-accent/20 text-accent px-3 py-1 rounded-full">{recommendations.length} Matches</span>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec, i) => (
              <div key={i} className="bg-background rounded-xl p-5 border border-white/5 hover:border-accent/40 transition-all hover:shadow-[0_0_20px_rgba(74,222,128,0.1)] group flex flex-col relative overflow-hidden">
                <div className="absolute top-0 left-0 w-1 h-full bg-accent/20 group-hover:bg-accent transition-colors"></div>
                <div className="flex justify-between items-start mb-3 pl-2">
                  <h4 className="font-bold text-lg leading-tight text-textPrimary group-hover:text-accent transition-colors">{rec.name}</h4>
                  <div className="flex items-center gap-1 bg-accent/10 text-accent font-bold text-xs px-2 py-1 rounded">
                    <Activity size={12} />
                    {(rec.final_score * 100).toFixed(1)}% Match
                  </div>
                </div>
                
                <p className="text-sm text-textSecondary line-clamp-1 mb-4 pl-2 font-medium">{rec.genres}</p>
                
                <div className="mt-auto flex justify-between items-center pl-2">
                  <div className="text-xs font-semibold bg-card border border-white/5 px-3 py-1.5 rounded-md text-textSecondary flex items-center gap-2">
                    <FileBox size={14} className="text-white/30" />
                    {rec.size_gb} GB
                  </div>
                  {rec.Local_Multiplayer === 'Yes' && (
                    <div className="text-xs text-textSecondary flex items-center gap-1">
                      <Users size={14} className="text-white/30" />
                      Co-op
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {recommendations.length === 0 && !loading && (
              <div className="col-span-full flex flex-col items-center justify-center py-20 text-textSecondary opacity-50">
                <Gamepad2 size={64} className="mb-4" />
                <p>Pilih game dan klik Generate untuk melihat hasil.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModeA;
