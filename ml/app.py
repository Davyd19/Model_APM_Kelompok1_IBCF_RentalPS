from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
# Mengizinkan Frontend (React/Vue/HTML biasa) untuk memanggil API ini
CORS(app) 

# ==========================================
# 1. LOAD MODEL & DATA PADA SAAT SERVER JALAN
# ==========================================
MODEL_PATH = 'rental_ps_recommender_v1.pkl'

try:
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    
    df_train = model_data['df_train']
    df_test = model_data['df_test']
    sim_matrix = model_data['sim_matrix']
    print("Model berhasil dimuat!")
except Exception as e:
    print(f"Error memuat model: {e}")
    df_train, df_test, sim_matrix = None, None, None

# ==========================================
# 2. FUNGSI LOGIKA (Dipindah dari Streamlit)
# ==========================================
def build_train_mask(ps_version='All', multiplayer_only=False, genre_filter='All', max_size_gb=1000.0, min_rating=0.0):
    mask = pd.Series(True, index=df_train.index)
    
    # Filter PS Version
    if ps_version == 'PS4':
        mask = mask & df_train['is_ps4']
    elif ps_version == 'PS5':
        mask = mask & df_train['is_ps5']
        
    # Filter Multiplayer
    if multiplayer_only:
        mask = mask & df_train['is_multiplayer']
        
    # Filter Genre
    if genre_filter != 'All':
        mask = mask & df_train['genres'].fillna('').str.contains(genre_filter, case=False, regex=False)
        
    # Filter Size
    mask = mask & (df_train['size_gb'] <= max_size_gb)
    
    # Filter Rating
    mask = mask & (df_train['rating'] >= min_rating)
    
    return mask

# ==========================================
# 3. ROUTING / ENDPOINTS API
# ==========================================

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Rental PS Recommender API berjalan normal.", "status": "success"})

@app.route('/api/v1/games/stock', methods=['GET'])
def get_stock_games():
    """Mengambil daftar game yang ada di rental untuk dropdown UI Pemain"""
    if df_test is None:
        return jsonify({"status": "error", "message": "Data tidak tersedia"}), 500
        
    games = df_test['name'].tolist()
    return jsonify({"status": "success", "data": games})

@app.route('/api/v1/genres', methods=['GET'])
def get_genres():
    """Mengambil daftar genre unik untuk filter UI"""
    if df_train is None:
        return jsonify({"status": "error", "message": "Data tidak tersedia"}), 500
        
    all_genres = set()
    for genres_str in df_train['genres'].dropna():
        genres_list = [g.strip() for g in genres_str.split(',')]
        all_genres.update(genres_list)
        
    genre_list = sorted(list(all_genres))
    # Filter out empty strings if any
    genre_list = [g for g in genre_list if g]
    
    return jsonify({"status": "success", "data": genre_list})

@app.route('/api/v1/recommend/player', methods=['POST'])
def recommend_player():
    """Endpoint untuk tab 'Pemain' - Cari game mirip"""
    data = request.json
    
    game_name = data.get('game_name')
    top_n = data.get('top_k', 10)
    
    # Ambil filter
    ps_version = data.get('ps_version', 'All')
    multiplayer_only = data.get('multiplayer_only', False)
    genre_filter = data.get('genre_filter', 'All')
    max_size_gb = float(data.get('max_size_gb', 1000.0))
    min_rating = float(data.get('min_rating', 0.0))
    
    if not game_name or game_name not in df_test['name'].values:
        return jsonify({"status": "error", "message": "Game tidak ditemukan di stok rental."}), 404
        
    # Logika ML
    idx = df_test[df_test['name'] == game_name].index[0]
    sim_scores = sim_matrix[idx]
    
    scores_df = pd.DataFrame({
        'name': df_train['name'],
        'similarity': sim_scores,
        'popularity_score': df_train['popularity_score']
    })
    
    # Kombinasi bobot (Sama seperti Streamlit kamu)
    scores_df['final_score'] = (scores_df['similarity'] * 0.7) + (scores_df['popularity_score'] * 0.3)
    
    # Terapkan mask filter
    mask = build_train_mask(ps_version, multiplayer_only, genre_filter, max_size_gb, min_rating)
    filtered_scores = scores_df[mask]
    
    # Hilangkan game yang diinputkan (jika ada di data train)
    filtered_scores = filtered_scores[filtered_scores['name'] != game_name]
    
    # Ambil top N
    top_results = filtered_scores.sort_values('final_score', ascending=False).head(top_n)
    
    # Gabungkan dengan detail game dari df_train
    result_df = pd.merge(top_results, df_train, on='name', how='left')
    
    # Ubah NaN menjadi None agar aman jadi JSON
    result_df = result_df.replace({np.nan: None})
    
    # Pilih kolom yang mau dikirim ke frontend
    columns_to_return = ['name', 'genres', 'platforms', 'released', 'rating', 'size_gb', 'final_score', 'background_image']
    # Cek jika kolom background_image ada di dataset asli kamu
    columns_to_return = [col for col in columns_to_return if col in result_df.columns]
    
    final_data = result_df[columns_to_return].to_dict(orient='records')
    
    return jsonify({"status": "success", "data": final_data})

@app.route('/api/v1/recommend/owner', methods=['POST'])
def recommend_owner():
    """Endpoint untuk tab 'Pemilik' - Saran game baru untuk direntalkan"""
    data = request.json
    top_n = data.get('top_k', 10)
    
    # Ambil filter
    ps_version = data.get('ps_version', 'All')
    multiplayer_only = data.get('multiplayer_only', False)
    genre_filter = data.get('genre_filter', 'All')
    max_size_gb = float(data.get('max_size_gb', 1000.0))
    min_rating = float(data.get('min_rating', 0.0))
    
    # Logika ML (Rata-rata similarity terhadap stok saat ini)
    avg_sim = sim_matrix.mean(axis=0)
    
    scores_df = pd.DataFrame({
        'name': df_train['name'],
        'avg_similarity': avg_sim,
        'popularity_score': df_train['popularity_score']
    })
    
    scores_df['final_score'] = (scores_df['avg_similarity'] * 0.5) + (scores_df['popularity_score'] * 0.5)
    
    # Filter game yang sudah ada di stok rental
    stock_games = set(df_test['name'])
    scores_df = scores_df[~scores_df['name'].isin(stock_games)]
    
    # Terapkan mask filter
    mask = build_train_mask(ps_version, multiplayer_only, genre_filter, max_size_gb, min_rating)
    filtered_scores = scores_df[mask]
    
    top_results = filtered_scores.sort_values('final_score', ascending=False).head(top_n)
    
    result_df = pd.merge(top_results, df_train, on='name', how='left')
    result_df = result_df.replace({np.nan: None})
    
    columns_to_return = ['name', 'genres', 'platforms', 'released', 'rating', 'size_gb', 'final_score', 'background_image']
    columns_to_return = [col for col in columns_to_return if col in result_df.columns]
    
    final_data = result_df[columns_to_return].to_dict(orient='records')
    
    return jsonify({"status": "success", "data": final_data})

if __name__ == '__main__':
    # Gunakan port 5000 sebagai standar Flask
    app.run(debug=True, host='0.0.0.0', port=5000)