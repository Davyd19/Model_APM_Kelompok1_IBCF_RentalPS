import React, { useState, useEffect } from 'react';
import { X, Gamepad2, HardDrive, Star, Users, MonitorPlay, Clock, Package, TrendingUp, CheckCircle, XCircle } from 'lucide-react';

const GameDetailModal = ({ gameName, onClose }) => {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!gameName) return;
    setLoading(true);
    setError(null);
    fetch(`http://localhost:5000/api/v1/game/detail/${encodeURIComponent(gameName)}`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') setDetail(data.data);
        else setError('Data game tidak ditemukan.');
        setLoading(false);
      })
      .catch(() => {
        setError('Gagal terhubung ke server.');
        setLoading(false);
      });
  }, [gameName]);

  if (!gameName) return null;

  const BadgeYesNo = ({ value, label }) => {
    const yes = value === 'Yes' || value === true;
    return (
      <div className={`flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-lg border ${yes ? 'bg-accent/10 text-accent border-accent/30' : 'bg-white/5 text-textSecondary border-white/10'}`}>
        {yes ? <CheckCircle size={13} /> : <XCircle size={13} />}
        {label}
      </div>
    );
  };

  const InfoRow = ({ icon, label, value }) => {
    if (value === null || value === undefined || value === 'None') return null;
    return (
      <div className="flex items-start gap-3 py-3 border-b border-white/5 last:border-0">
        <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center flex-shrink-0 mt-0.5">
          {icon}
        </div>
        <div>
          <p className="text-[11px] text-textSecondary uppercase tracking-wider font-bold">{label}</p>
          <p className="text-sm text-textPrimary font-medium mt-0.5">{value}</p>
        </div>
      </div>
    );
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div 
        className="bg-card border border-white/10 rounded-2xl w-full max-w-lg shadow-2xl relative overflow-hidden"
        onClick={e => e.stopPropagation()}
      >
        {/* Decorative gradient top bar */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 via-purple-500 to-accent"></div>

        {/* Header */}
        <div className="p-6 pb-4 flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600/30 to-purple-500/30 border border-white/10 flex items-center justify-center flex-shrink-0">
              <Gamepad2 size={24} className="text-accent" />
            </div>
            <div>
              <h2 className="font-bold text-lg text-textPrimary leading-tight">
                {gameName}
              </h2>
              {detail?.genres && (
                <p className="text-xs text-textSecondary mt-0.5">{detail.genres}</p>
              )}
            </div>
          </div>
          <button 
            onClick={onClose}
            className="w-8 h-8 rounded-lg bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors flex-shrink-0"
          >
            <X size={16} className="text-textSecondary" />
          </button>
        </div>

        {/* Content */}
        <div className="px-6 pb-6">
          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin"></div>
            </div>
          )}
          
          {error && (
            <p className="text-center text-danger py-8 text-sm">{error}</p>
          )}
          
          {detail && !loading && (
            <div>
              {/* Status badges */}
              <div className="flex flex-wrap gap-2 mb-5">
                <BadgeYesNo value={detail.in_stock} label="Di Stok" />
                <BadgeYesNo value={detail.Bisa_PS4} label="PS4" />
                <BadgeYesNo value={detail.Bisa_PS5} label="PS5" />
                <BadgeYesNo value={detail.Local_Multiplayer} label="Multiplayer Lokal" />
              </div>

              {/* Stats grid */}
              <div className="grid grid-cols-3 gap-3 mb-5">
                {detail.rating !== null && (
                  <div className="bg-background rounded-xl p-3 text-center border border-white/5">
                    <Star size={16} className="text-yellow-400 mx-auto mb-1" />
                    <p className="text-lg font-bold text-textPrimary">{detail.rating?.toFixed(1)}</p>
                    <p className="text-[10px] text-textSecondary uppercase tracking-wide">Rating</p>
                  </div>
                )}
                {detail.size_gb !== null && (
                  <div className="bg-background rounded-xl p-3 text-center border border-white/5">
                    <HardDrive size={16} className="text-blue-400 mx-auto mb-1" />
                    <p className="text-lg font-bold text-textPrimary">{detail.size_gb?.toFixed(0)}</p>
                    <p className="text-[10px] text-textSecondary uppercase tracking-wide">GB</p>
                  </div>
                )}
                {detail.total_playtime !== null && (
                  <div className="bg-background rounded-xl p-3 text-center border border-white/5">
                    <Clock size={16} className="text-accent mx-auto mb-1" />
                    <p className="text-lg font-bold text-textPrimary">{Math.floor(detail.total_playtime)}</p>
                    <p className="text-[10px] text-textSecondary uppercase tracking-wide">Jam Main</p>
                  </div>
                )}
                {detail.popularity_score !== null && (
                  <div className="bg-background rounded-xl p-3 text-center border border-white/5">
                    <TrendingUp size={16} className="text-purple-400 mx-auto mb-1" />
                    <p className="text-lg font-bold text-textPrimary">{(detail.popularity_score * 100).toFixed(0)}</p>
                    <p className="text-[10px] text-textSecondary uppercase tracking-wide">Popularitas</p>
                  </div>
                )}
                {detail.jumlah_wishlist && (
                  <div className="bg-background rounded-xl p-3 text-center border border-white/5">
                    <Package size={16} className="text-pink-400 mx-auto mb-1" />
                    <p className="text-lg font-bold text-textPrimary">{detail.jumlah_wishlist}</p>
                    <p className="text-[10px] text-textSecondary uppercase tracking-wide">Wishlist</p>
                  </div>
                )}
              </div>

              {/* Extra Info */}
              <div className="bg-background rounded-xl border border-white/5 px-4 divide-y divide-white/5">
                <InfoRow icon={<Users size={15} className="text-textSecondary" />} label="Platform" value={detail.platforms} />
                <InfoRow icon={<MonitorPlay size={15} className="text-textSecondary" />} label="Developer" value={detail.developer} />
                <InfoRow icon={<MonitorPlay size={15} className="text-textSecondary" />} label="Publisher" value={detail.publisher} />
                <InfoRow icon={<MonitorPlay size={15} className="text-textSecondary" />} label="Tahun Rilis" value={detail.tahun_rilis} />
                <InfoRow icon={<Gamepad2 size={15} className="text-textSecondary" />} label="Deskripsi" value={detail.deskripsi} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GameDetailModal;
