import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# ══════════════════════════════════════════════════════════
#  KONFIGURASI HALAMAN
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RAD PS · Game Recommender",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
#  CUSTOM CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main { background: #0c0c14; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #13131f !important;
    border-right: 1px solid #2a2a3e;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* ── Header Banner ── */
.app-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    border: 1px solid #2d2d4e;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.app-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
}
.app-header p {
    color: #94a3b8;
    font-size: 1rem;
    margin: 0;
    font-weight: 300;
}
.app-header .badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #818cf8;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
}

/* ── Mode Cards ── */
.mode-card {
    background: #13131f;
    border: 1px solid #2a2a3e;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.mode-card:hover { border-color: #4f46e5; }
.mode-card.active {
    border-color: #6366f1;
    background: linear-gradient(135deg, #1e1b4b, #1a1a2e);
}
.mode-card h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.4rem 0;
}
.mode-card p {
    color: #64748b;
    font-size: 0.85rem;
    margin: 0;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.3rem 0;
}
.section-sub {
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 1.8rem;
}

/* ── Metric Cards ── */
.metrics-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    flex: 1;
    min-width: 130px;
    background: #13131f;
    border: 1px solid #2a2a3e;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-card .val {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #818cf8;
}
.metric-card .lbl {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 2px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Result Cards ── */
.result-card {
    background: #13131f;
    border: 1px solid #2a2a3e;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    transition: border-color 0.15s, background 0.15s;
}
.result-card:hover {
    border-color: #4f46e5;
    background: #16162a;
}
.result-card .rank-badge {
    min-width: 36px;
    height: 36px;
    background: #1e1b4b;
    border: 1px solid #3730a3;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 0.9rem;
    color: #818cf8;
}
.result-card .game-info { flex: 1; }
.result-card .game-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #f1f5f9;
    margin: 0 0 0.35rem 0;
}
.result-card .game-meta {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    align-items: center;
}
.tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 5px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.tag-genre { background: rgba(99,102,241,0.15); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.25); }
.tag-ps4   { background: rgba(59,130,246,0.15); color: #93c5fd; border: 1px solid rgba(59,130,246,0.25); }
.tag-ps5   { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.25); }
.tag-multi { background: rgba(245,158,11,0.15); color: #fcd34d; border: 1px solid rgba(245,158,11,0.25); }
.tag-size  { background: rgba(100,116,139,0.15); color: #94a3b8; border: 1px solid rgba(100,116,139,0.25); }

.result-card .score-section { text-align: right; min-width: 90px; }
.result-card .score-main {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #6366f1;
}
.result-card .score-label {
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.result-card .sim-bar-wrap {
    width: 80px;
    height: 4px;
    background: #1e293b;
    border-radius: 2px;
    margin-top: 4px;
    overflow: hidden;
}
.result-card .sim-bar {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
}
.score-extra {
    font-size: 0.72rem;
    color: #64748b;
    margin-top: 2px;
}

/* ── Stok Popularity Bar ── */
.stok-item {
    background: #13131f;
    border: 1px solid #2a2a3e;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
}
.stok-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.stok-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #e2e8f0;
}
.stok-pt { font-size: 0.8rem; color: #6366f1; font-weight: 600; }
.stok-bar-wrap {
    width: 100%;
    height: 5px;
    background: #1e293b;
    border-radius: 3px;
    overflow: hidden;
}
.stok-bar {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
}

/* ── Alert / Info Box ── */
.info-box {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #a5b4fc;
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
}
.warn-box {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #fcd34d;
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
}

/* ── Selected Game Preview ── */
.selected-game-card {
    background: linear-gradient(135deg, #1e1b4b, #1a1a2e);
    border: 1px solid #4338ca;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.8rem;
}
.selected-game-card .sg-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #c7d2fe;
}
.selected-game-card .sg-sub {
    font-size: 0.82rem;
    color: #6366f1;
    margin-top: 2px;
}

/* ── Divider ── */
.my-divider { border: none; border-top: 1px solid #1e293b; margin: 1.5rem 0; }

/* ── Sidebar Labels ── */
.sidebar-section {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
    margin: 1.5rem 0 0.8rem 0;
}

/* ── Streamlit overrides ── */
.stButton button {
    background: #4f46e5 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    padding: 0.5rem 1.5rem !important;
    transition: background 0.2s !important;
    width: 100%;
}
.stButton button:hover { background: #4338ca !important; }
.stSelectbox label, .stMultiSelect label, .stSlider label,
.stCheckbox label, .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    background: #1e1e2e !important;
    border-color: #2a2a3e !important;
    border-radius: 8px !important;
}
.stRadio [data-testid="stMarkdownContainer"] p { color: #94a3b8 !important; }
h1, h2, h3 { color: #f1f5f9; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  LOAD MODEL
# ══════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
# Cara kebal error: Cari tahu secara dinamis di mana lokasi app.py ini berada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Gabungkan lokasi app.py dengan nama file pickle-nya
    file_path = os.path.join(current_dir, 'rental_ps_recommender_v1.pkl')
    
    with open(file_path, 'rb') as f:
        return pickle.load(f)

try:
    model        = load_model()
    df_train     = model['df_train']
    df_test      = model['df_test']
    sim_matrix   = model['sim_matrix']
    SIMILARITY_THRESHOLD = model.get('similarity_threshold', 0.25)
    TOP_K        = model.get('top_k', 10)
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    st.error(f"⚠️ Gagal memuat model: {e}")
    st.stop()


# ══════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════
def build_train_mask(ps_version, multiplayer_only, genre_filter=None, max_size_gb=None):
    mask = np.ones(len(df_train), dtype=bool)
    if ps_version == "PS4":
        mask &= df_train["Bisa_PS4"].values == 1
    elif ps_version == "PS5":
        mask &= df_train["Bisa_PS5"].values == 1
    if multiplayer_only:
        mask &= df_train["Local_Multiplayer"].values == 1
    if genre_filter:
        gf_lower = [g.lower() for g in genre_filter]
        gmask = df_train["Genre"].str.lower().apply(
            lambda g: any(gf in str(g) for gf in gf_lower)
        ).values
        mask &= gmask
    if max_size_gb is not None:
        mask &= df_train["Size_GB"].values <= max_size_gb
    return mask


def get_platform_tag(ps4, ps5):
    if ps4 == 1 and ps5 == 1: return "PS4 & PS5"
    elif ps5 == 1: return "PS5"
    else: return "PS4"


def get_score_color(score):
    if score >= 0.7: return "#22c55e"
    elif score >= 0.5: return "#6366f1"
    elif score >= 0.35: return "#f59e0b"
    else: return "#ef4444"


def recommend_player_full(game_name, top_k=10, ps_version="Both",
                           multiplayer_only=False, genre_filter=None,
                           max_size_gb=None, min_rating=0.0, min_metacritic=0):
    names      = df_test["Nama_Game"].str.lower().str.strip()
    mask_exact = names == game_name.lower().strip()
    mask_sub   = names.str.contains(game_name.lower().strip(), na=False)
    test_idx   = (names[mask_exact].index[0] if mask_exact.any() else
                  names[mask_sub].index[0] if mask_sub.any() else None)
    if test_idx is None:
        return pd.DataFrame()

    sim_scores  = sim_matrix[test_idx].copy()
    train_mask  = build_train_mask(ps_version, multiplayer_only, genre_filter, max_size_gb)

    # Filter tambahan
    if min_rating > 0:
        train_mask &= df_train["Rating_Global"].values >= min_rating
    if min_metacritic > 0:
        meta_vals = df_train["Metacritic_Score"].fillna(0).values
        train_mask &= meta_vals >= min_metacritic

    pop_norm = df_train["Popularity_Score"] / df_train["Popularity_Score"].max()
    combined = sim_scores * 0.70 + pop_norm.values * 0.30
    combined[~train_mask] = -1

    top_indices = np.argsort(combined)[::-1]
    results = []
    for idx in top_indices:
        if combined[idx] < 0 or sim_scores[idx] < SIMILARITY_THRESHOLD:
            continue
        row  = df_train.iloc[idx]
        meta = row["Metacritic_Score"]
        results.append({
            "Rank"           : len(results) + 1,
            "Judul"          : row["Judul"],
            "Genre"          : row["Genre"],
            "Rating_Global"  : round(float(row["Rating_Global"]), 2),
            "Metacritic"     : int(meta) if not np.isnan(meta) else 0,
            "Waktu_Main_Jam" : int(row["Waktu_Main_Jam"]),
            "Bisa_PS4"       : int(row["Bisa_PS4"]),
            "Bisa_PS5"       : int(row["Bisa_PS5"]),
            "Multiplayer"    : int(row["Local_Multiplayer"]),
            "Size_GB"        : round(float(row["Size_GB"]), 1),
            "Similarity"     : round(float(sim_scores[idx]), 4),
            "Popularity_Norm": round(float(pop_norm.values[idx]), 4),
            "Skor_Akhir"     : round(float(combined[idx]), 4),
        })
        if len(results) >= top_k:
            break
    return pd.DataFrame(results)


def recommend_owner_full(top_k=10, ps_version="Both", multiplayer_only=False,
                          genre_filter=None, max_size_gb=None, min_rating=0.0):
    avg_sim    = sim_matrix.mean(axis=0)
    train_mask = build_train_mask(ps_version, multiplayer_only, genre_filter, max_size_gb)
    existing   = set(df_test["Nama_Game"].str.lower().str.strip())
    in_stock   = df_train["Judul"].str.lower().str.strip().isin(existing).values
    train_mask &= ~in_stock
    if min_rating > 0:
        train_mask &= df_train["Rating_Global"].values >= min_rating

    pop_norm = df_train["Popularity_Score"] / df_train["Popularity_Score"].max()
    combined = avg_sim * 0.50 + pop_norm.values * 0.50
    combined[~train_mask] = -1

    top_indices = np.argsort(combined)[::-1]
    results = []
    for idx in top_indices:
        if combined[idx] < 0:
            continue
        row  = df_train.iloc[idx]
        meta = row["Metacritic_Score"]
        results.append({
            "Rank"             : len(results) + 1,
            "Judul"            : row["Judul"],
            "Genre"            : row["Genre"],
            "Rating_Global"    : round(float(row["Rating_Global"]), 2),
            "Metacritic"       : int(meta) if not np.isnan(meta) else 0,
            "Waktu_Main_Jam"   : int(row["Waktu_Main_Jam"]),
            "Bisa_PS4"         : int(row["Bisa_PS4"]),
            "Bisa_PS5"         : int(row["Bisa_PS5"]),
            "Multiplayer"      : int(row["Local_Multiplayer"]),
            "Size_GB"          : round(float(row["Size_GB"]), 1),
            "Popularity_Score" : round(float(pop_norm.values[idx] * 100), 1),
            "Avg_Similarity"   : round(float(avg_sim[idx]), 4),
            "Skor_Akhir"       : round(float(combined[idx]), 4),
        })
        if len(results) >= top_k:
            break
    return pd.DataFrame(results)


def render_result_card_player(row):
    rank       = int(row["Rank"])
    title      = row["Judul"]
    genre      = row["Genre"]
    rating     = row["Rating_Global"]
    meta       = int(row["Metacritic"]) if row["Metacritic"] > 0 else "N/A"
    ps4        = int(row["Bisa_PS4"])
    ps5        = int(row["Bisa_PS5"])
    multi      = int(row["Multiplayer"])
    size       = row["Size_GB"]
    sim        = row["Similarity"]
    score      = row["Skor_Akhir"]
    waktu      = int(row["Waktu_Main_Jam"])
    sim_pct    = int(sim * 100)
    score_col  = get_score_color(score)

    plat_tag   = get_platform_tag(ps4, ps5)
    plat_class = "tag-ps5" if ps5 and not ps4 else "tag-ps4" if ps4 and not ps5 else "tag-ps5"
    genre_short = genre[:30] + "…" if len(genre) > 30 else genre

    multi_tag = '<span class="tag tag-multi">👥 Multiplayer</span>' if multi else ""
    size_tag  = f'<span class="tag tag-size">💾 {size} GB</span>'
    waktu_tag = f'<span class="tag tag-size">⏱ {waktu} jam</span>' if waktu > 0 else ""

    st.markdown(f"""
    <div class="result-card">
        <div class="rank-badge">#{rank}</div>
        <div class="game-info">
            <div class="game-title">{title}</div>
            <div class="game-meta">
                <span class="tag tag-genre">{genre_short}</span>
                <span class="tag {plat_class}">{plat_tag}</span>
                {multi_tag}
                {size_tag}
                {waktu_tag}
            </div>
        </div>
        <div class="score-section">
            <div class="score-main" style="color:{score_col};">{score:.3f}</div>
            <div class="score-label">Relevansi</div>
            <div class="sim-bar-wrap">
                <div class="sim-bar" style="width:{sim_pct}%; background: linear-gradient(90deg, {score_col}, #818cf8);"></div>
            </div>
            <div class="score-extra">⭐ {rating}/5 · MC: {meta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_result_card_owner(row):
    rank      = int(row["Rank"])
    title     = row["Judul"]
    genre     = row["Genre"]
    rating    = row["Rating_Global"]
    meta      = int(row["Metacritic"]) if row["Metacritic"] > 0 else "N/A"
    ps4       = int(row["Bisa_PS4"])
    ps5       = int(row["Bisa_PS5"])
    multi     = int(row["Multiplayer"])
    size      = row["Size_GB"]
    pop       = row["Popularity_Score"]
    avg_sim   = row["Avg_Similarity"]
    score     = row["Skor_Akhir"]
    waktu     = int(row["Waktu_Main_Jam"])
    score_col = get_score_color(score)
    sim_pct   = int(avg_sim * 100)

    plat_tag   = get_platform_tag(ps4, ps5)
    plat_class = "tag-ps5" if ps5 and not ps4 else "tag-ps4" if ps4 and not ps5 else "tag-ps5"
    genre_short = genre[:30] + "…" if len(genre) > 30 else genre

    multi_tag = '<span class="tag tag-multi">👥 Multiplayer</span>' if multi else ""
    pop_tag   = f'<span class="tag tag-size">🔥 Pop: {pop:.0f}</span>'

    st.markdown(f"""
    <div class="result-card">
        <div class="rank-badge">#{rank}</div>
        <div class="game-info">
            <div class="game-title">{title}</div>
            <div class="game-meta">
                <span class="tag tag-genre">{genre_short}</span>
                <span class="tag {plat_class}">{plat_tag}</span>
                {multi_tag}
                {pop_tag}
                <span class="tag tag-size">💾 {size} GB</span>
            </div>
        </div>
        <div class="score-section">
            <div class="score-main" style="color:{score_col};">{score:.3f}</div>
            <div class="score-label">Potensi</div>
            <div class="sim-bar-wrap">
                <div class="sim-bar" style="width:{sim_pct}%; background: linear-gradient(90deg, {score_col}, #818cf8);"></div>
            </div>
            <div class="score-extra">⭐ {rating}/5 · MC: {meta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
    <div class="badge">🎮 Item-Based CF · RAWG Dataset</div>
    <h1>RAD PlayStation · Game Recommender</h1>
    <p>Sistem rekomendasi berbasis kemiripan fitur game — bantu pemain temukan game baru &amp; bantu pemilik rencanakan stok optimal.</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800;
                color:#c7d2fe; margin-bottom:0.3rem;">⚙️ Panel Kontrol</div>
    <div style="font-size:0.8rem; color:#475569; margin-bottom:1.5rem;">
        Atur mode dan filter rekomendasi
    </div>
    """, unsafe_allow_html=True)

    # ── Mode
    st.markdown('<div class="sidebar-section">Mode</div>', unsafe_allow_html=True)
    menu = st.radio(
        "Pilih Mode:",
        ["🎯 Rekomendasi Pemain", "📦 Saran Stok Baru", "📊 Analisis Stok"],
        label_visibility="collapsed"
    )

    # ── Filter Platform
    st.markdown('<div class="sidebar-section">Platform</div>', unsafe_allow_html=True)
    ps_filter_raw = st.selectbox("Platform:", ["Semua", "PS4", "PS5"], label_visibility="collapsed")
    ps_map = {"Semua": "Both", "PS4": "PS4", "PS5": "PS5"}
    ps_version = ps_map[ps_filter_raw]

    # ── Filter Multiplayer
    multi_filter = st.checkbox("Hanya game multiplayer lokal", value=False)

    # ── Filter Genre
    st.markdown('<div class="sidebar-section">Filter Genre</div>', unsafe_allow_html=True)
    all_genres = sorted(set(
        g.strip()
        for genres in df_train["Genre"].dropna()
        for g in genres.split(",")
    ))
    genre_filter = st.multiselect("Genre:", all_genres, placeholder="Semua genre…",
                                   label_visibility="collapsed")

    # ── Filter Rating
    st.markdown('<div class="sidebar-section">Filter Kualitas</div>', unsafe_allow_html=True)
    min_rating = st.slider("Minimum Rating Global:", 0.0, 5.0, 0.0, 0.1,
                            format="%.1f ⭐", label_visibility="visible")

    min_meta = st.slider("Minimum Metacritic Score:", 0, 100, 0, 5,
                          label_visibility="visible")

    # ── Max Size
    max_size = st.slider("Max Ukuran Game (GB):", 5, 135,
                          int(df_train["Size_GB"].max()), 5,
                          label_visibility="visible")

    # ── Jumlah Rekomendasi
    st.markdown('<div class="sidebar-section">Jumlah Hasil</div>', unsafe_allow_html=True)
    n_results = st.slider("Tampilkan top:", 5, 20, 10, label_visibility="visible")

    # ── Stats kecil
    st.markdown("<hr style='border-color:#1e293b; margin:1.5rem 0 1rem'>", unsafe_allow_html=True)
    n_filtered = build_train_mask(ps_version, multi_filter,
                                   genre_filter if genre_filter else None,
                                   max_size).sum()
    st.markdown(f"""
    <div style="background:#0f0f1a; border:1px solid #1e293b; border-radius:8px;
                padding:0.8rem 1rem; font-size:0.8rem; color:#64748b;">
        📂 Katalog aktif setelah filter:<br>
        <span style="color:#818cf8; font-family:'Syne',sans-serif;
                     font-weight:700; font-size:1.1rem;">{n_filtered:,}</span>
        <span style="color:#475569;"> / {len(df_train):,} game</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  MODE 1: REKOMENDASI PEMAIN
# ══════════════════════════════════════════════════════════
if menu == "🎯 Rekomendasi Pemain":
    st.markdown('<div class="section-title">🎯 Cari Game Mirip untuk Pemain</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pilih game favorit dari stok rental — sistem akan merekomendasikan game serupa dari katalog global RAWG.</div>', unsafe_allow_html=True)

    game_list = sorted(df_test["Nama_Game"].tolist())
    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        selected_game = st.selectbox("Pilih game dari stok rental:", game_list,
                                      label_visibility="collapsed",
                                      placeholder="Ketik nama game…")
    with col_btn:
        cari = st.button("🔍 Cari Rekomendasi", use_container_width=True)

    # Preview game yang dipilih
    if selected_game:
        game_row = df_test[df_test["Nama_Game"] == selected_game].iloc[0]
        genre_sel = game_row["Genre"]
        ps4_sel   = game_row["Bisa_PS4"]
        ps5_sel   = game_row["Bisa_PS5"]
        plat_sel  = get_platform_tag(
            1 if str(ps4_sel).lower() in ["yes","1","true"] else 0,
            1 if str(ps5_sel).lower() in ["yes","1","true"] else 0
        )
        meja_sel  = game_row.get("Tersedia_Di_Meja", "-")
        pt_sel    = int(game_row.get("Total_Playtime", 0))

        st.markdown(f"""
        <div class="selected-game-card">
            <div>
                <div class="sg-title">🎮 {selected_game}</div>
                <div class="sg-sub">Genre: {genre_sel} &nbsp;·&nbsp; Platform: {plat_sel} &nbsp;·&nbsp; Meja: {meja_sel}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800; color:#818cf8;">{pt_sel:,} jam</div>
                <div style="font-size:0.75rem; color:#475569;">Total Playtime Rental</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if cari:
        with st.spinner("Menghitung rekomendasi..."):
            results = recommend_player_full(
                selected_game, top_k=n_results,
                ps_version=ps_version,
                multiplayer_only=multi_filter,
                genre_filter=genre_filter if genre_filter else None,
                max_size_gb=max_size if max_size < int(df_train["Size_GB"].max()) else None,
                min_rating=min_rating,
                min_metacritic=min_meta,
            )

        if results.empty:
            st.markdown('<div class="warn-box">⚠️ Tidak ada game yang sesuai dengan kriteria filter. Coba longgarkan filter di sidebar.</div>', unsafe_allow_html=True)
        else:
            # Summary metrics
            avg_sim  = results["Similarity"].mean()
            avg_rat  = results["Rating_Global"].mean()
            n_multi  = results["Multiplayer"].sum()
            top_score = results["Skor_Akhir"].max()

            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-card">
                    <div class="val">{len(results)}</div>
                    <div class="lbl">Rekomendasi</div>
                </div>
                <div class="metric-card">
                    <div class="val">{avg_sim:.2f}</div>
                    <div class="lbl">Avg Similarity</div>
                </div>
                <div class="metric-card">
                    <div class="val">{avg_rat:.1f}⭐</div>
                    <div class="lbl">Avg Rating</div>
                </div>
                <div class="metric-card">
                    <div class="val">{n_multi}</div>
                    <div class="lbl">Multiplayer</div>
                </div>
                <div class="metric-card">
                    <div class="val">{top_score:.3f}</div>
                    <div class="lbl">Top Score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="info-box">💡 <b>Skor Relevansi</b> = 70% Cosine Similarity + 30% Popularitas Global. Semakin tinggi skor, semakin cocok game tersebut dengan preferensi pemain.</div>', unsafe_allow_html=True)

            for _, row in results.iterrows():
                render_result_card_player(row)

            # Export
            st.markdown("<hr class='my-divider'>", unsafe_allow_html=True)
            csv = results.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download hasil sebagai CSV",
                csv,
                f"rekomendasi_{selected_game.replace(' ','_')}.csv",
                "text/csv",
                use_container_width=True,
            )


# ══════════════════════════════════════════════════════════
#  MODE 2: REKOMENDASI PEMILIK
# ══════════════════════════════════════════════════════════
elif menu == "📦 Saran Stok Baru":
    st.markdown('<div class="section-title">📦 Saran Penambahan Stok Game</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Analisis katalog global vs stok saat ini untuk menemukan game berpotensi tinggi yang belum dimiliki rental.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        sort_by = st.selectbox(
            "Urutkan berdasarkan:",
            ["Skor Akhir (Gabungan)", "Popularitas Global", "Rata-rata Similarity", "Rating Global"],
        )
    with col2:
        analisis = st.button("🔬 Analisis Sekarang", use_container_width=True)

    sort_map = {
        "Skor Akhir (Gabungan)" : "Skor_Akhir",
        "Popularitas Global"    : "Popularity_Score",
        "Rata-rata Similarity"  : "Avg_Similarity",
        "Rating Global"         : "Rating_Global",
    }

    if analisis:
        with st.spinner("Menganalisis katalog..."):
            results = recommend_owner_full(
                top_k=n_results,
                ps_version=ps_version,
                multiplayer_only=multi_filter,
                genre_filter=genre_filter if genre_filter else None,
                max_size_gb=max_size if max_size < int(df_train["Size_GB"].max()) else None,
                min_rating=min_rating,
            )

        if results.empty:
            st.markdown('<div class="warn-box">⚠️ Tidak ada game yang sesuai dengan kriteria filter.</div>', unsafe_allow_html=True)
        else:
            sort_col = sort_map.get(sort_by, "Skor_Akhir")
            if sort_col in results.columns:
                results = results.sort_values(sort_col, ascending=False).reset_index(drop=True)
                results["Rank"] = range(1, len(results) + 1)

            # Metrics
            avg_pop  = results["Popularity_Score"].mean()
            avg_sim  = results["Avg_Similarity"].mean()
            avg_rat  = results["Rating_Global"].mean()
            n_multi  = results["Multiplayer"].sum()

            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-card">
                    <div class="val">{len(results)}</div>
                    <div class="lbl">Kandidat</div>
                </div>
                <div class="metric-card">
                    <div class="val">{avg_pop:.0f}</div>
                    <div class="lbl">Avg Popularitas</div>
                </div>
                <div class="metric-card">
                    <div class="val">{avg_sim:.2f}</div>
                    <div class="lbl">Avg Similarity</div>
                </div>
                <div class="metric-card">
                    <div class="val">{avg_rat:.1f}⭐</div>
                    <div class="lbl">Avg Rating</div>
                </div>
                <div class="metric-card">
                    <div class="val">{n_multi}</div>
                    <div class="lbl">Multiplayer</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="info-box">💡 <b>Skor Potensi</b> = 50% Avg Similarity ke Stok + 50% Popularitas Global. Game yang sudah ada di stok otomatis dikecualikan.</div>', unsafe_allow_html=True)

            for _, row in results.iterrows():
                render_result_card_owner(row)

            st.markdown("<hr class='my-divider'>", unsafe_allow_html=True)
            csv = results.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download saran stok sebagai CSV",
                csv, "saran_stok_baru.csv", "text/csv",
                use_container_width=True,
            )


# ══════════════════════════════════════════════════════════
#  MODE 3: ANALISIS STOK
# ══════════════════════════════════════════════════════════
elif menu == "📊 Analisis Stok":
    st.markdown('<div class="section-title">📊 Analisis Stok Rental</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ringkasan performa stok saat ini berdasarkan playtime, platform, genre, dan kemiripan katalog.</div>', unsafe_allow_html=True)

    # ── Overview metrics
    total_pt   = int(df_test["Total_Playtime"].sum())
    n_ps5_only = int((df_test["Bisa_PS5"].apply(lambda x: str(x).lower()) == "yes").sum())
    n_multi    = int((df_test["Local_Multiplayer"].apply(lambda x: str(x).lower()) == "yes").sum())
    avg_sim_all = float(sim_matrix.mean())

    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card">
            <div class="val">{len(df_test)}</div>
            <div class="lbl">Total Game Stok</div>
        </div>
        <div class="metric-card">
            <div class="val">{total_pt:,}</div>
            <div class="lbl">Total Playtime</div>
        </div>
        <div class="metric-card">
            <div class="val">{n_ps5_only}</div>
            <div class="lbl">Tersedia PS5</div>
        </div>
        <div class="metric-card">
            <div class="val">{n_multi}</div>
            <div class="lbl">Multiplayer</div>
        </div>
        <div class="metric-card">
            <div class="val">{avg_sim_all:.3f}</div>
            <div class="lbl">Avg Similarity ke RAWG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Ranking stok by playtime
    st.markdown("#### 🏆 Ranking Game berdasarkan Playtime", unsafe_allow_html=False)
    df_stk = df_test.copy().sort_values("Total_Playtime", ascending=False).reset_index(drop=True)
    pt_max = int(df_stk["Total_Playtime"].max())

    for _, row in df_stk.iterrows():
        name  = row["Nama_Game"]
        pt    = int(row["Total_Playtime"])
        genre = row["Genre"]
        pct   = int(pt / pt_max * 100)
        rank  = _ + 1

        st.markdown(f"""
        <div class="stok-item">
            <div class="stok-header">
                <div>
                    <span style="color:#475569; font-size:0.75rem; font-weight:700;">#{rank}</span>
                    <span class="stok-name" style="margin-left:0.5rem;">{name}</span>
                    <span class="tag tag-genre" style="margin-left:0.5rem; font-size:0.7rem;">{genre}</span>
                </div>
                <div class="stok-pt">{pt:,} jam</div>
            </div>
            <div class="stok-bar-wrap">
                <div class="stok-bar" style="width:{pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Best match per game
    st.markdown("<hr class='my-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🔗 Pasangan Game Paling Mirip (per stok)", unsafe_allow_html=False)

    sim_rows = []
    for i, row in df_test.iterrows():
        sim_row  = sim_matrix[i]
        best_idx = np.argmax(sim_row)
        sim_rows.append({
            "Game Stok Rental"   : row["Nama_Game"],
            "Best Match di RAWG" : df_train.iloc[best_idx]["Judul"],
            "Similarity"         : round(float(sim_row[best_idx]), 4),
            "Avg Similarity"     : round(float(sim_row.mean()), 4),
        })

    df_sim_summary = pd.DataFrame(sim_rows).sort_values("Similarity", ascending=False).reset_index(drop=True)
    st.dataframe(
        df_sim_summary.style
            .background_gradient(subset=["Similarity","Avg Similarity"], cmap="Blues")
            .format({"Similarity": "{:.4f}", "Avg Similarity": "{:.4f}"}),
        use_container_width=True,
        height=420,
    )

    # ── Genre distribution
    st.markdown("<hr class='my-divider'>", unsafe_allow_html=True)
    st.markdown("#### 🎭 Distribusi Genre Stok Rental", unsafe_allow_html=False)

    from collections import Counter
    genre_cnt = Counter()
    for g in df_test["Genre"].dropna():
        for part in str(g).replace("-", " ").split(","):
            genre_cnt[part.strip()] += 1

    df_genre = pd.DataFrame(genre_cnt.most_common(), columns=["Genre", "Jumlah"])
    g_max = df_genre["Jumlah"].max()

    for _, grow in df_genre.iterrows():
        pct = int(grow["Jumlah"] / g_max * 100)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
            <div style="min-width:140px; font-size:0.85rem; color:#94a3b8; font-weight:500;">{grow['Genre']}</div>
            <div style="flex:1; height:8px; background:#1e293b; border-radius:4px; overflow:hidden;">
                <div style="width:{pct}%; height:100%; background:linear-gradient(90deg,#6366f1,#8b5cf6); border-radius:4px;"></div>
            </div>
            <div style="min-width:24px; text-align:right; font-family:'Syne',sans-serif;
                        font-weight:700; font-size:0.9rem; color:#818cf8;">{grow['Jumlah']}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════
st.markdown("""
<hr style='border-color:#1e293b; margin:3rem 0 1rem;'>
<div style="text-align:center; color:#334155; font-size:0.8rem;">
    RAD PlayStation · Game Recommender System &nbsp;|&nbsp;
    Item-Based Collaborative Filtering &nbsp;|&nbsp;
    RAWG Dataset · 2000 game
</div>
""", unsafe_allow_html=True)