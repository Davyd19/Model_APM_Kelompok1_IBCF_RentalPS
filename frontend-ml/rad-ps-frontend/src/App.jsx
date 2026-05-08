import React, { useState, useEffect } from 'react';
import { 
  Gamepad2, User, Store, Search, Info, List, 
  Monitor, HardDrive, Star, AlertCircle, Image as ImageIcon
} from 'lucide-react';

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

export default function App() {
  const [activeTab, setActiveTab] = useState('pemain');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Data dari API
  const [stockGames, setStockGames] = useState([]);
  const [availableGenres, setAvailableGenres] = useState([]);
  const [results, setResults] = useState([]);

  // State untuk Filter & Input
  const [filters, setFilters] = useState({
    platform: 'All',
    multiplayer: false,
    genre: 'All',
    storage: 1000,
    rating: 0
  });
  
  const [query, setQuery] = useState({
    gameName: '',
    topK: 10
  });

  // Fetch Initial Data (Stock & Genres)
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        // Coba fetch dari Flask API Lokal
        const [gamesRes, genresRes] = await Promise.all([
          fetch(`${API_BASE_URL}/games/stock`).catch(() => null),
          fetch(`${API_BASE_URL}/genres`).catch(() => null)
        ]);

        if (gamesRes && gamesRes.ok && genresRes && genresRes.ok) {
          const gamesData = await gamesRes.json();
          const genresData = await genresRes.json();
          setStockGames(gamesData.data || []);
          setAvailableGenres(genresData.data || []);
        } else {
          throw new Error("Local API not reachable");
        }
      } catch (err) {
        // Fallback Data Dummy (Agar UI tetap bisa di-preview di web ini)
        console.warn("Menggunakan data dummy karena API lokal (Flask) tidak terdeteksi.");
        setStockGames(["FIFA 23", "GTA V", "God of War Ragnarok", "Tekken 7", "Elden Ring"]);
        setAvailableGenres(["Action", "Adventure", "RPG", "Sports", "Fighting", "Shooter"]);
      }
    };

    fetchInitialData();
  }, []);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleSearch = async () => {
    if (activeTab === 'pemain' && !query.gameName) {
      setError("Mohon pilih game terakhir yang dimainkan terlebih dahulu!");
      return;
    }

    setIsLoading(true);
    setError('');
    setResults([]);

    const payload = {
      game_name: query.gameName,
      top_k: Number(query.topK),
      ps_version: filters.platform,
      multiplayer_only: filters.multiplayer,
      genre_filter: filters.genre,
      max_size_gb: Number(filters.storage),
      min_rating: Number(filters.rating)
    };

    const endpoint = activeTab === 'pemain' ? '/recommend/player' : '/recommend/owner';

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Gagal mengambil data dari server");
      const data = await response.json();
      
      if (data.status === 'error') throw new Error(data.message);
      setResults(data.data);

    } catch (err) {
      console.warn("API Error, using fallback mock data for preview.", err);
      // Generate Dummy Results based on tab
      setTimeout(() => {
        const dummyResults = Array.from({ length: query.topK || 4 }).map((_, i) => ({
          name: activeTab === 'pemain' ? `Rekomendasi ${query.gameName} Vol.${i+1}` : `Saran Game Baru ${i+1}`,
          genres: filters.genre !== 'All' ? `${filters.genre}, Action` : "Action, RPG",
          platforms: filters.platform !== 'All' ? filters.platform : "PS4, PS5",
          released: "2023-10-15",
          rating: (Math.random() * (5.0 - 4.0) + 4.0).toFixed(1),
          size_gb: Math.floor(Math.random() * filters.storage),
          final_score: (Math.random() * 0.5 + 0.5).toFixed(3),
          background_image: null
        }));
        setResults(dummyResults);
        setIsLoading(false);
      }, 1000); // simulate network delay
      return;
    }

    setIsLoading(false);
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 font-sans overflow-hidden">
      
      {/* SIDEBAR FILTER */}
      <aside className="w-72 bg-gray-800 border-r border-gray-700 flex flex-col h-full shadow-xl z-20">
        <div className="p-6 border-b border-gray-700 bg-gray-800/50">
          <h1 className="text-2xl font-bold text-blue-400 flex items-center gap-3">
            <Gamepad2 size={28} /> RAD PS
          </h1>
          <p className="text-sm text-gray-400 mt-1 ml-10">AI Recommender</p>
        </div>

        <div className="p-6 flex-1 overflow-y-auto space-y-6 custom-scrollbar">
          <h2 className="text-xs uppercase tracking-wider text-gray-500 font-bold mb-2">Filter Pencarian</h2>
          
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Platform</label>
            <select 
              className="w-full bg-gray-700 border border-gray-600 rounded-lg py-2 px-3 focus:ring-2 focus:ring-blue-500 outline-none transition"
              value={filters.platform}
              onChange={(e) => handleFilterChange('platform', e.target.value)}
            >
              <option value="All">Semua Konsol</option>
              <option value="PS4">PlayStation 4</option>
              <option value="PS5">PlayStation 5</option>
            </select>
          </div>

          <div className="flex items-center space-x-3 bg-gray-700/30 p-3 rounded-lg border border-gray-700">
            <input 
              type="checkbox" 
              id="multiplayer"
              className="w-5 h-5 rounded border-gray-600 text-blue-500 focus:ring-blue-500 bg-gray-700"
              checked={filters.multiplayer}
              onChange={(e) => handleFilterChange('multiplayer', e.target.checked)}
            />
            <label htmlFor="multiplayer" className="text-sm font-medium text-gray-300 cursor-pointer">
              Wajib Multiplayer
            </label>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Genre Utama</label>
            <select 
              className="w-full bg-gray-700 border border-gray-600 rounded-lg py-2 px-3 focus:ring-2 focus:ring-blue-500 outline-none transition"
              value={filters.genre}
              onChange={(e) => handleFilterChange('genre', e.target.value)}
            >
              <option value="All">Semua Genre</option>
              {availableGenres.map(g => (
                <option key={g} value={g}>{g}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <label className="text-sm font-medium text-gray-300">Sisa Storage</label>
              <span className="text-xs font-bold text-blue-400 bg-blue-400/10 px-2 py-1 rounded">
                {filters.storage} GB
              </span>
            </div>
            <input 
              type="range" 
              min="5" max="1000" step="5"
              className="w-full accent-blue-500"
              value={filters.storage}
              onChange={(e) => handleFilterChange('storage', e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Minimal Rating (0-5)</label>
            <input 
              type="number" min="0" max="5" step="0.1"
              className="w-full bg-gray-700 border border-gray-600 rounded-lg py-2 px-3 focus:ring-2 focus:ring-blue-500 outline-none transition"
              value={filters.rating}
              onChange={(e) => handleFilterChange('rating', e.target.value)}
            />
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 flex flex-col h-full relative bg-gray-900">
        
        {/* TABS HEADER */}
        <header className="bg-gray-800 border-b border-gray-700 p-4 z-10 shadow-md">
          <div className="flex space-x-2">
            <button 
              onClick={() => { setActiveTab('pemain'); setResults([]); setError(''); }}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                activeTab === 'pemain' 
                ? 'bg-blue-600 text-white shadow-lg' 
                : 'text-gray-400 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <User size={18} /> Mode Pemain
            </button>
            <button 
              onClick={() => { setActiveTab('pemilik'); setResults([]); setError(''); }}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                activeTab === 'pemilik' 
                ? 'bg-purple-600 text-white shadow-lg' 
                : 'text-gray-400 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <Store size={18} /> Mode Pemilik
            </button>
          </div>
        </header>

        {/* CONTENT AREA */}
        <div className="p-8 flex-1 overflow-y-auto">
          
          {/* SEARCH BOX */}
          <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-lg flex flex-wrap lg:flex-nowrap items-end gap-4 mb-8">
            
            {activeTab === 'pemain' ? (
              <div className="flex-1 min-w-[250px]">
                <label className="block text-sm font-medium text-gray-300 mb-2">Game Terakhir Dimainkan</label>
                <select 
                  className="w-full bg-gray-700 border border-gray-600 rounded-xl py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none transition"
                  value={query.gameName}
                  onChange={(e) => setQuery({...query, gameName: e.target.value})}
                >
                  <option value="">-- Pilih game dari stok rental --</option>
                  {stockGames.map(g => (
                    <option key={g} value={g}>{g}</option>
                  ))}
                </select>
              </div>
            ) : (
              <div className="flex-1 min-w-[250px]">
                <div className="bg-purple-900/30 border border-purple-800/50 rounded-xl p-4 flex gap-3 text-purple-200">
                  <Info className="shrink-0 text-purple-400" />
                  <p className="text-sm">
                    Mode ini otomatis menganalisis <strong>seluruh stok game rental Anda</strong> dan mencari game baru di pasar yang memiliki tingkat kecocokan (similarity) paling tinggi untuk dibeli.
                  </p>
                </div>
              </div>
            )}

            <div className="w-32">
              <label className="block text-sm font-medium text-gray-300 mb-2">Jumlah</label>
              <input 
                type="number" min="1" max="50"
                className="w-full bg-gray-700 border border-gray-600 rounded-xl py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none"
                value={query.topK}
                onChange={(e) => setQuery({...query, topK: e.target.value})}
              />
            </div>

            <button 
              onClick={handleSearch}
              disabled={isLoading}
              className={`py-3 px-8 rounded-xl font-bold flex items-center gap-2 transition-all duration-300 shadow-lg ${
                activeTab === 'pemain' 
                  ? 'bg-blue-600 hover:bg-blue-500 shadow-blue-900/50' 
                  : 'bg-purple-600 hover:bg-purple-500 shadow-purple-900/50'
              } disabled:opacity-50 disabled:cursor-not-allowed transform hover:-translate-y-1`}
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
              ) : (
                <Search size={20} />
              )}
              {isLoading ? 'Menganalisis...' : 'Cari Game'}
            </button>
          </div>

          {/* ERROR ALERT */}
          {error && (
            <div className="bg-red-900/40 border border-red-500/50 text-red-200 px-4 py-3 rounded-xl mb-6 flex items-center gap-3">
              <AlertCircle className="text-red-400" /> {error}
            </div>
          )}

          {/* RESULTS */}
          {!isLoading && results.length > 0 && (
            <div className="animate-fade-in-up">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-2 text-gray-100">
                <List className="text-blue-400" /> Hasil Rekomendasi
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {results.map((game, idx) => (
                  <div key={idx} className="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden hover:border-blue-500/50 transition-all duration-300 group shadow-lg hover:shadow-2xl hover:shadow-blue-900/20 flex flex-col h-full">
                    
                    {/* Image Area */}
                    <div className="h-40 bg-gray-700 relative overflow-hidden flex items-center justify-center">
                      {game.background_image ? (
                        <img 
                          src={game.background_image} 
                          alt={game.name} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="text-gray-500 flex flex-col items-center gap-2">
                          <ImageIcon size={32} />
                          <span className="text-xs">No Image Available</span>
                        </div>
                      )}
                      
                      {/* Match Badge */}
                      <div className="absolute top-3 right-3 bg-gray-900/80 backdrop-blur-sm px-3 py-1 rounded-full border border-gray-600 flex items-center gap-1">
                        <span className="text-xs font-bold text-green-400">
                          {Math.round(game.final_score * 100)}% Match
                        </span>
                      </div>
                    </div>

                    {/* Content Area */}
                    <div className="p-5 flex-1 flex flex-col">
                      <h4 className="text-lg font-bold text-white mb-2 line-clamp-1" title={game.name}>
                        {game.name}
                      </h4>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {(game.platforms || '').split(',').slice(0, 2).map((p, i) => (
                          <span key={i} className="text-[10px] font-semibold bg-gray-700 text-gray-300 px-2 py-1 rounded uppercase">
                            {p.trim()}
                          </span>
                        ))}
                      </div>

                      <div className="space-y-2 mt-auto">
                        <div className="flex items-center text-sm text-gray-400 gap-2">
                          <Gamepad2 size={14} className="text-blue-400 shrink-0" />
                          <span className="line-clamp-1">{game.genres || 'Unknown'}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-400 gap-2">
                          <HardDrive size={14} className="text-purple-400 shrink-0" />
                          <span>{game.size_gb ? `${game.size_gb} GB` : '? GB'}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-400 gap-2">
                          <Star size={14} className="text-yellow-400 shrink-0" />
                          <span>{game.rating || 'N/A'} / 5.0</span>
                        </div>
                      </div>

                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* EMPTY STATE */}
          {!isLoading && results.length === 0 && !error && (
            <div className="h-64 flex flex-col items-center justify-center text-gray-500">
              <Monitor size={48} className="mb-4 opacity-50" />
              <p>Sesuaikan filter dan klik cari untuk melihat rekomendasi AI.</p>
            </div>
          )}

        </div>
      </main>

      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #4b5563; border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #6b7280; }
        
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up {
          animation: fadeInUp 0.5s ease-out forwards;
        }
      `}} />
    </div>
  );
}