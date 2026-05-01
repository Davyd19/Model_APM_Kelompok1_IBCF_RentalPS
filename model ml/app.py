import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ── Konfigurasi Halaman ──
st.set_page_config(page_title="Sistem Rekomendasi Rental PS", layout="wide")

# ── 1. Load Model ──
@st.cache_resource # Cache agar model tidak di-load ulang setiap kali ada interaksi
def load_model():
    with open('rental_ps_recommender_v1.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()
df_train = model['df_train']
df_test = model['df_test']
sim_matrix = model['sim_matrix']

# Helper Fungsi Filter
def build_train_mask(ps_version, multiplayer_only):
    mask = np.ones(len(df_train), dtype=bool)
    if ps_version == "PS4":
        mask &= df_train["Bisa_PS4"].values == 1
    elif ps_version == "PS5":
        mask &= df_train["Bisa_PS5"].values == 1
    if multiplayer_only:
        mask &= df_train["Local_Multiplayer"].values == 1
    return mask

# ── 2. UI Sidebar (Navigasi & Filter) ──
st.sidebar.title("🎮 Navigasi")
menu = st.sidebar.radio("Pilih Mode:", ["Rekomendasi Pemain", "Rekomendasi Pemilik (Stok Baru)"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Filter Rekomendasi")
ps_filter = st.sidebar.selectbox("Platform", ["Semua", "PS4", "PS5"])
multi_filter = st.sidebar.checkbox("Hanya Game Multiplayer")

# Mapping untuk filter
ps_map = {"Semua": "Both", "PS4": "PS4", "PS5": "PS5"}

# ── 3. Mode: Rekomendasi Pemain ──
if menu == "Rekomendasi Pemain":
    st.title("🎯 Cari Game Mirip untuk Pemain")
    st.markdown("Pilih game yang disukai pelanggan dari stok kita, lalu sistem akan mencarikan game alternatif yang mirip dari katalog global.")
    
    # Input dari user
    game_list = sorted(df_test["Nama_Game"].tolist())
    selected_game = st.selectbox("Pilih Game dari Stok Rental:", game_list)
    
    if st.button("Cari Rekomendasi"):
        test_idx = df_test[df_test["Nama_Game"] == selected_game].index[0]
        sim_scores = sim_matrix[test_idx].copy()
        
        train_mask = build_train_mask(ps_map[ps_filter], multi_filter)
        
        # Hitung skor (70% Similarity + 30% Popularity)
        pop_norm = df_train["Popularity_Score"] / df_train["Popularity_Score"].max()
        combined = sim_scores * 0.70 + pop_norm.values * 0.30
        combined[~train_mask] = -1 # Abaikan yang tidak lolos filter
        
        top_indices = np.argsort(combined)[::-1][:10]
        
        # Format Hasil
        results = []
        for rank, idx in enumerate(top_indices):
            if combined[idx] > 0:
                row = df_train.iloc[idx]
                results.append({
                    "Rank": rank + 1,
                    "Judul Game": row["Judul"],
                    "Genre": row["Genre"],
                    "Platform": "PS4/PS5" if row["Bisa_PS4"] and row["Bisa_PS5"] else ("PS5" if row["Bisa_PS5"] else "PS4"),
                    "Skor Relevansi": f"{combined[idx]:.2f}"
                })
                
        if results:
            st.table(pd.DataFrame(results).set_index("Rank"))
        else:
            st.warning("Tidak ada game yang sesuai dengan kriteria filter.")

# ── 4. Mode: Rekomendasi Pemilik ──
elif menu == "Rekomendasi Pemilik (Stok Baru)":
    st.title("📦 Rekomendasi Tambah Stok Game")
    st.markdown("Sistem menganalisis seluruh inventaris saat ini dan menyarankan game populer baru yang paling cocok dengan profil rental.")
    
    if st.button("Analisis Katalog"):
        avg_sim = sim_matrix.mean(axis=0)
        train_mask = build_train_mask(ps_map[ps_filter], multi_filter)
        
        # Kecualikan game yang sudah ada di stok
        existing = set(df_test["Nama_Game"].str.lower().str.strip())
        in_stock = df_train["Judul"].str.lower().str.strip().isin(existing).values
        train_mask &= ~in_stock
        
        # Hitung skor (50% Avg Similarity + 50% Popularity)
        pop_norm = df_train["Popularity_Score"] / df_train["Popularity_Score"].max()
        combined = avg_sim * 0.50 + pop_norm.values * 0.50
        combined[~train_mask] = -1
        
        top_indices = np.argsort(combined)[::-1][:10]
        
        results = []
        for rank, idx in enumerate(top_indices):
            if combined[idx] > 0:
                row = df_train.iloc[idx]
                results.append({
                    "Rank": rank + 1,
                    "Judul Game Baru": row["Judul"],
                    "Genre": row["Genre"],
                    "Potensi Sukses": f"{combined[idx]:.2f}",
                    "Global Rating": row["Rating_Global"]
                })
                
        if results:
            st.dataframe(pd.DataFrame(results).set_index("Rank"), use_container_width=True)
        else:
            st.warning("Tidak ada game yang sesuai dengan kriteria filter.")