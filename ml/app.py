from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os
import random

app = Flask(__name__)
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
    
    # Standarisasi Kolom agar sesuai dengan kode / Frontend
    # Mapping untuk df_train
    if 'Judul' in df_train.columns and 'name' not in df_train.columns:
        df_train.rename(columns={'Judul': 'name', 'Genre': 'genres', 'Size_GB': 'size_gb', 'Rating_Global': 'rating'}, inplace=True)
        
    # Buat popularity_score mock jika tidak ada, menggunakan Rating * Jumlah_Rating atau Wishlist
    if 'popularity_score' not in df_train.columns:
        if 'Jumlah_Wishlist' in df_train.columns:
            # Min-Max scaler manual
            wishlist = df_train['Jumlah_Wishlist']
            df_train['popularity_score'] = (wishlist - wishlist.min()) / (wishlist.max() - wishlist.min() + 1e-5)
        else:
            df_train['popularity_score'] = np.random.uniform(0.1, 1.0, len(df_train))

    # Mapping untuk df_test
    if isinstance(df_test, pd.DataFrame):
        if 'Nama_Game' in df_test.columns and 'name' not in df_test.columns:
            df_test.rename(columns={'Nama_Game': 'name', 'Size_GB': 'size_gb', 'Genre': 'genres'}, inplace=True)

    print("Model berhasil dimuat dan kolom telah distandardisasi!")
except Exception as e:
    print(f"Error memuat model: {e}")
    df_train, df_test, sim_matrix = None, None, None


# ==========================================
# 2. FUNGSI BANTUAN
# ==========================================
def build_train_mask(ps_version='All', multiplayer_only=False, genre_filter='All', max_size_gb=1000.0, min_rating=0.0, singleplayer_only=False, quick_match=False):
    mask = pd.Series(True, index=df_train.index)
    
    # Filter PS Version (Cek kolom Bisa_PS4/5)
    if ps_version == 'PS4' and 'Bisa_PS4' in df_train.columns:
        mask = mask & (df_train['Bisa_PS4'] == 'Yes')
    elif ps_version == 'PS5' and 'Bisa_PS5' in df_train.columns:
        mask = mask & (df_train['Bisa_PS5'] == 'Yes')
        
    # Filter Multiplayer
    if multiplayer_only and 'Local_Multiplayer' in df_train.columns:
        mask = mask & (df_train['Local_Multiplayer'] == 'Yes')
        
    # Filter Singleplayer
    if singleplayer_only and 'Local_Multiplayer' in df_train.columns:
        mask = mask & (df_train['Local_Multiplayer'] != 'Yes')
        
    # Filter Quick Match (Fighting/Sports)
    if quick_match and 'genres' in df_train.columns:
        quick_genres = ['Sports', 'Fighting', 'Racing', 'Party']
        quick_mask = df_train['genres'].fillna('').apply(lambda x: any(g.lower() in str(x).lower() for g in quick_genres))
        mask = mask & quick_mask
        
    # Filter Genre
    if genre_filter != 'All' and 'genres' in df_train.columns:
        mask = mask & df_train['genres'].fillna('').str.contains(genre_filter, case=False, regex=False)
        
    # Filter Size
    if 'size_gb' in df_train.columns:
        # Convert ke float aman
        size_series = pd.to_numeric(df_train['size_gb'], errors='coerce').fillna(50.0)
        mask = mask & (size_series <= max_size_gb)
    
    # Filter Rating
    if 'rating' in df_train.columns:
        rating_series = pd.to_numeric(df_train['rating'], errors='coerce').fillna(0.0)
        mask = mask & (rating_series >= min_rating)
    
    return mask

def get_test_names():
    if isinstance(df_test, pd.DataFrame) and 'name' in df_test.columns:
        return df_test['name'].tolist()
    elif hasattr(df_test, 'tolist'):
        return df_test.tolist()
    return list(df_test)

def get_train_names():
    if isinstance(df_train, pd.DataFrame) and 'name' in df_train.columns:
        return df_train['name'].tolist()
    elif hasattr(df_train, 'tolist'):
        return df_train.tolist()
    return list(df_train)


# ==========================================
# 3. ROUTING / ENDPOINTS API
# ==========================================

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Rental PS Recommender API berjalan normal.", "status": "success"})

@app.route('/api/v1/games/stock', methods=['GET'])
def get_stock_games():
    if df_test is None:
        return jsonify({"status": "error", "message": "Data tidak tersedia"}), 500
    games = get_test_names()
    return jsonify({"status": "success", "data": games})

@app.route('/api/v1/game/detail/<path:game_name>', methods=['GET'])
def get_game_detail(game_name):
    if df_train is None:
        return jsonify({"status": "error", "message": "Data tidak tersedia"}), 500
    
    # Search in df_train first
    row = df_train[df_train['name'] == game_name]
    
    # Also search in df_test if it's a DataFrame
    in_stock = game_name in get_test_names()
    playtime = None
    if in_stock and isinstance(df_test, pd.DataFrame) and 'Total_Playtime' in df_test.columns:
        test_names = get_test_names()
        if game_name in test_names:
            idx = test_names.index(game_name)
            val = pd.to_numeric(df_test['Total_Playtime'].iloc[idx], errors='coerce')
            playtime = float(val) if not pd.isna(val) else 0.0
    
    if row.empty:
        return jsonify({"status": "error", "message": "Game tidak ditemukan"}), 404
    
    row = row.iloc[0]
    
    detail = {
        "name": str(row['name']) if 'name' in row.index else game_name,
        "genres": str(row['genres']) if 'genres' in row.index and row['genres'] is not None else None,
        "rating": float(row['rating']) if 'rating' in row.index and row['rating'] is not None else None,
        "size_gb": float(row['size_gb']) if 'size_gb' in row.index and row['size_gb'] is not None else None,
        "Bisa_PS4": str(row['Bisa_PS4']) if 'Bisa_PS4' in row.index else None,
        "Bisa_PS5": str(row['Bisa_PS5']) if 'Bisa_PS5' in row.index else None,
        "Local_Multiplayer": str(row['Local_Multiplayer']) if 'Local_Multiplayer' in row.index else None,
        "popularity_score": float(row['popularity_score']) if 'popularity_score' in row.index else None,
        "in_stock": in_stock,
        "total_playtime": playtime,
    }
    
    # Add any extra columns that exist
    for col in ['Developer', 'Publisher', 'Tahun_Rilis', 'Deskripsi', 'platforms', 'Jumlah_Wishlist']:
        if col in row.index and row[col] is not None:
            try:
                detail[col.lower()] = str(row[col])
            except:
                pass
    
    return jsonify({"status": "success", "data": detail})


@app.route('/api/v1/genres', methods=['GET'])
def get_genres():
    if df_train is None or 'genres' not in df_train.columns:
        return jsonify({"status": "error", "message": "Data/Kolom Genre tidak tersedia"}), 500
        
    all_genres = set()
    for genres_str in df_train['genres'].dropna():
        genres_list = [str(g).strip() for g in str(genres_str).split(',')]
        all_genres.update(genres_list)
        
    genre_list = sorted([g for g in all_genres if g])
    return jsonify({"status": "success", "data": genre_list})

@app.route('/api/v1/recommend/player', methods=['POST'])
def recommend_player():
    data = request.json
    game_names = data.get('game_names', [])
    top_n = data.get('top_k', 10)
    
    single_game = data.get('game_name')
    if single_game and single_game not in game_names:
        game_names.append(single_game)
    
    ps_version = data.get('ps_version', 'All')
    multiplayer_only = data.get('multiplayer_only', False)
    singleplayer_only = data.get('singleplayer_only', False)
    quick_match = data.get('quick_match', False)
    genre_filter = data.get('genre_filter', 'All')
    max_size_gb = float(data.get('max_size_gb', 1000.0))
    min_rating = float(data.get('min_rating', 0.0))
    
    test_names = get_test_names()
    valid_games = [g for g in game_names if g in test_names]
    
    if not valid_games:
        return jsonify({"status": "error", "message": "Game tidak ditemukan di stok rental."}), 404
        
    aggregated_sim_scores = np.zeros(sim_matrix.shape[1])
    for g in valid_games:
        idx = test_names.index(g) if g in test_names else 0
        aggregated_sim_scores += sim_matrix[idx]
        
    aggregated_sim_scores = aggregated_sim_scores / len(valid_games)
    
    scores_df = pd.DataFrame({
        'name': get_train_names(),
        'similarity': aggregated_sim_scores,
        'popularity_score': df_train['popularity_score']
    })
    
    scores_df['final_score'] = (scores_df['similarity'] * 0.7) + (scores_df['popularity_score'] * 0.3)
    
    mask = build_train_mask(ps_version, multiplayer_only, genre_filter, max_size_gb, min_rating, singleplayer_only, quick_match)
    filtered_scores = scores_df[mask]
    filtered_scores = filtered_scores[~filtered_scores['name'].isin(valid_games)]
    
    top_results = filtered_scores.sort_values('final_score', ascending=False).head(top_n)
    result_df = pd.merge(top_results, df_train, on='name', how='left').replace({np.nan: None})
    
    columns_to_return = ['name', 'genres', 'platforms', 'Bisa_PS4', 'Bisa_PS5', 'Local_Multiplayer', 'rating', 'size_gb', 'final_score', 'background_image']
    columns_to_return = [col for col in columns_to_return if col in result_df.columns]
    
    final_data = result_df[columns_to_return].to_dict(orient='records')
    return jsonify({"status": "success", "data": final_data})


@app.route('/api/v1/recommend/roi', methods=['POST'])
def recommend_roi():
    data = request.json or {}
    top_n = data.get('top_k', 15)
    ps_version = data.get('ps_version', 'All')
    multiplayer_only = data.get('multiplayer_only', False)
    singleplayer_only = data.get('singleplayer_only', False)
    quick_match = data.get('quick_match', False)
    genre_filter = data.get('genre_filter', 'All')
    max_size_gb = float(data.get('max_size_gb', 1000.0))
    min_rating = float(data.get('min_rating', 0.0))
    
    avg_sim = sim_matrix.mean(axis=0)
    scores_df = pd.DataFrame({
        'name': get_train_names(),
        'avg_similarity': avg_sim,
        'popularity_score': df_train['popularity_score'],
        'size_gb': pd.to_numeric(df_train['size_gb'], errors='coerce').fillna(50.0) if 'size_gb' in df_train.columns else 50.0
    })
    
    scores_df['potensi_laku'] = (scores_df['avg_similarity'] * 0.5) + (scores_df['popularity_score'] * 0.5)
    scores_df['roi_score'] = scores_df['potensi_laku'] / scores_df['size_gb'].replace(0, 0.1)
    
    mask = build_train_mask(ps_version, multiplayer_only, genre_filter, max_size_gb, min_rating, singleplayer_only, quick_match)
    scores_df = scores_df[mask]
    
    stock_games = set(get_test_names())
    scores_df = scores_df[~scores_df['name'].isin(stock_games)]
    
    max_roi = scores_df['roi_score'].max()
    scores_df['roi_score_normalized'] = (scores_df['roi_score'] / (max_roi + 1e-5)) * 100
    
    top_results = scores_df.sort_values('roi_score', ascending=False).head(top_n)
    
    merge_cols = ['name']
    if 'genres' in df_train.columns: merge_cols.append('genres')
    if 'rating' in df_train.columns: merge_cols.append('rating')
    if 'background_image' in df_train.columns: merge_cols.append('background_image')
        
    result_df = pd.merge(top_results, df_train[merge_cols], on='name', how='left').replace({np.nan: None})
    return jsonify({"status": "success", "data": result_df.to_dict(orient='records')})


@app.route('/api/v1/recommend/uninstall', methods=['GET'])
def recommend_uninstall():
    if df_test is None or df_train is None:
        return jsonify({"status": "error", "message": "Data tidak tersedia"}), 500
        
    uninstall_candidates = df_train[df_train['name'].isin(get_test_names())].copy() if 'name' in df_train.columns else df_train.iloc[0:0].copy()
    
    if uninstall_candidates.empty:
        return jsonify({"status": "success", "data": []})
        
    # Get total playtime from df_test mapping
    playtime_dict = {}
    if isinstance(df_test, pd.DataFrame) and 'Total_Playtime' in df_test.columns:
        test_names = get_test_names()
        for idx, name in enumerate(test_names):
            val = pd.to_numeric(df_test['Total_Playtime'].iloc[idx], errors='coerce')
            playtime_dict[name] = val if not pd.isna(val) else 0.0
            
    uninstall_candidates['total_playtime'] = uninstall_candidates['name'].apply(lambda x: playtime_dict.get(x, 0.0))
    
    size_series = pd.to_numeric(uninstall_candidates['size_gb'], errors='coerce').fillna(50.0) if 'size_gb' in uninstall_candidates.columns else 50.0
    
    # Calculate Uninstall Score: Large Size but Low Playtime
    max_playtime = uninstall_candidates['total_playtime'].max()
    if max_playtime == 0: max_playtime = 1
    
    # Invers of playtime (lower is higher score) multiplied by size
    uninstall_candidates['uninstall_score'] = size_series * (1.0 - (uninstall_candidates['total_playtime'] / max_playtime))
    
    top_uninstall = uninstall_candidates.sort_values('uninstall_score', ascending=False).head(5).replace({np.nan: None})
    
    cols = ['name', 'total_playtime']
    if 'size_gb' in top_uninstall.columns: cols.append('size_gb')
        
    return jsonify({"status": "success", "data": top_uninstall[cols].to_dict(orient='records')})


@app.route('/api/v1/analytics/stock_summary', methods=['GET'])
def analytics_stock_summary():
    if df_test is None or df_train is None:
        return jsonify({"status": "error", "message": "Data tidak tersedia"}), 500
        
    stock_games_df = df_train[df_train['name'].isin(get_test_names())].copy() if 'name' in df_train.columns else df_train.iloc[0:0].copy()
    
    # Total Games
    total_games = len(get_test_names())
    
    # Playtime map
    playtimes = []
    total_playtime = 0
    if isinstance(df_test, pd.DataFrame) and 'Total_Playtime' in df_test.columns:
        test_names = get_test_names()
        for idx, name in enumerate(test_names):
            val = pd.to_numeric(df_test['Total_Playtime'].iloc[idx], errors='coerce')
            pt = float(val) if not pd.isna(val) else 0.0
            total_playtime += pt
            
            # Find genre
            genre = ''
            match = stock_games_df[stock_games_df['name'] == name]
            if not match.empty and 'genres' in match.columns:
                genre = str(match.iloc[0]['genres']).split(',')[0]
                
            playtimes.append({
                "name": name,
                "playtime": pt,
                "genre": genre
            })
    else:
        # Dummy if missing
        test_names = get_test_names()
        for name in test_names:
            pt = float(np.random.randint(10, 500))
            total_playtime += pt
            playtimes.append({"name": name, "playtime": pt, "genre": ""})
            
    # Sort by playtime descending
    playtimes.sort(key=lambda x: x["playtime"], reverse=True)
    
    # PS5 and Multiplayer
    ps5_count = 0
    multiplayer_count = 0
    if not stock_games_df.empty:
        if 'Bisa_PS5' in stock_games_df.columns:
            ps5_count = len(stock_games_df[stock_games_df['Bisa_PS5'] == 'Yes'])
        if 'Local_Multiplayer' in stock_games_df.columns:
            multiplayer_count = len(stock_games_df[stock_games_df['Local_Multiplayer'] == 'Yes'])
            
    # Avg Similarity
    avg_similarity = 0.0
    if sim_matrix is not None and sim_matrix.size > 0:
        avg_similarity = float(sim_matrix.mean())
        
    return jsonify({
        "status": "success",
        "data": {
            "total_games": int(total_games),
            "total_playtime": float(total_playtime),
            "ps5_count": int(ps5_count),
            "multiplayer_count": int(multiplayer_count),
            "avg_similarity": float(round(avg_similarity, 3)),
            "ranking": playtimes
        }
    })

@app.route('/api/v1/analytics/genres', methods=['GET'])
def analytics_genres():
    if df_test is None or df_train is None:
        return jsonify({"status": "error", "message": "Data tidak tersedia"}), 500
        
    stock_games_df = df_train[df_train['name'].isin(get_test_names())] if 'name' in df_train.columns else df_train.iloc[0:0]
    inventory_genres = {}
    if 'genres' in stock_games_df.columns:
        for g_str in stock_games_df['genres'].dropna():
            for g in str(g_str).split(','):
                g = g.strip()
                if g: inventory_genres[g] = inventory_genres.get(g, 0) + 1
                
    demand_genres = {}
    if 'genres' in df_train.columns:
        for idx, row in df_train.iterrows():
            if pd.isna(row['genres']): continue
            pop = row['popularity_score'] if 'popularity_score' in row else 1.0
            for g in str(row['genres']).split(','):
                g = g.strip()
                if g: demand_genres[g] = demand_genres.get(g, 0) + pop
                
    top_genres = sorted(inventory_genres, key=inventory_genres.get, reverse=True)[:6]
    
    radar_data = []
    for g in top_genres:
        inv_val = (inventory_genres.get(g, 0) / (max(inventory_genres.values() or [1]))) * 100
        dem_val = (demand_genres.get(g, 0) / (max(demand_genres.values() or [1]))) * 100
        radar_data.append({
            "genre": g,
            "inventory": round(inv_val, 1),
            "demand": round(dem_val, 1)
        })
        
    return jsonify({"status": "success", "data": radar_data})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)