🎮 System Context & Design: PlayStation Rental Recommender System

Version: 2.0 (Enhancement Plan)
Core Engine: Item-Based Collaborative Filtering (rental_ps_recommender_v1.pkl)
Target Audience: Penjaga Rental (Mode A) & Pemilik Rental (Mode B & C)

📑 System Overview

Sistem ini adalah aplikasi pendukung operasional untuk rental PlayStation. Engine utamanya menggunakan model Machine Learning (Item-Based CF) untuk menganalisis relasi antar-game. Sistem dibagi menjadi tiga mode operasional utama untuk memaksimalkan Customer Experience sekaligus melakukan Inventory & Yield Optimization pada sisi bisnis.

🎯 Mode A: Rekomendasi Pemain (Player Experience)

Konsep AI: Context-Aware & Multi-Seed Recommendation
Fungsi: Menghasilkan rekomendasi alternatif game secara akurat berdasarkan preferensi pemain saat itu juga, disesuaikan dengan konteks penyewaan.

1. Fitur Multi-Game Input (Keranjang Suka)

Logika Sistem: Mengubah input tunggal (1 Game) menjadi input jamak (2-3 Game).

Mekanisme AI Agent: Model CF akan mengakumulasi dan menghitung nilai rata-rata (mean/weighted average) skor kemiripan dari seed games yang diinputkan (Misal: GTA V, RDR 2, Tekken).

Output: Menghasilkan rekomendasi irisan (intersection) yang memiliki skor probabilitas tertinggi dari gabungan preferensi tersebut (contoh: Sleeping Dogs, Yakuza).

2. Filter Konteks Rental (Context-Aware Filtering)

Logika Sistem: Post-processing filter yang diterapkan setelah model CF menghasilkan daftar rekomendasi. Sangat krusial karena menyesuaikan dengan skenario rental fisik.

Toggles:

🕹️ Local Co-op / Split-screen: Hanya menampilkan game yang bisa dimainkan berdua/berempat di satu konsol/TV.

👤 Single-player Story: Hanya menampilkan game berbasis narasi untuk pemain solo.

⏱️ Quick Match: Memfilter game dengan session pendek (seperti Mortal Kombat atau FIFA), ditujukan untuk pelanggan yang hanya menyewa dalam durasi singkat (misal: 1 jam), menyingkirkan RPG beralur panjang.

📦 Mode B: Saran Pemilik (Inventory & Yield Optimization)

Konsep AI: Knapsack Problem Logic & Storage Yield Optimization
Fungsi: Berperan sebagai penasihat Business Intelligence (BI) bagi pemilik rental dalam mengelola ruang penyimpanan HDD konsol yang terbatas dan mahal.

1. Kalkulator ROI Hard Disk (Return on Storage)

Logika Sistem: Menggunakan pendekatan Knapsack. Tidak sekadar menyarankan game yang "Paling Laku", tetapi game yang "Paling Efisien".

Mekanisme Metrik: Menghitung Skor Efisiensi Storage = (Potensi Laku / Ukuran Game dalam GB).

Contoh Eksekusi AI: * Game A: Potensi 90, Size 150GB.

Game B: Potensi 85, Size 40GB.

Decision: AI akan merekomendasikan Game B untuk di-install karena rasio profitabilitas per GB lebih tinggi dan hemat ruang HDD rental.

2. Rekomendasi "Game to Uninstall" (Saran Penghapusan)

Logika Sistem: Evaluasi inventaris dua arah. Memberikan saran game yang sebaiknya dihapus dari HDD konsol.

Mekanisme AI Agent: Menganalisis dua variabel:

Penurunan playtime historis (tren negatif).

Skor sentimen/kemiripan dari model yang rendah terhadap tren global (RAWG) saat ini.

Output: Daftar game yang membebani ruang penyimpanan dengan rasio return (dimainkan pelanggan) yang sangat rendah.

📊 Mode C: Dashboard Analytics (Prescriptive Analytics)

Konsep AI: Descriptive to Prescriptive Analytics Transformation
Fungsi: Mengubah data mentah (historis) menjadi instruksi atau resep tindakan (Actionable Insights) untuk menjaga kesehatan bisnis rental.

1. Trend Prediction (Deteksi Kebosanan)

Logika Sistem: Analisis time-series pada data playtime harian/mingguan.

Mekanisme AI Agent: Mendeteksi anomali negatif (penurunan) secara persentase.

Output (Prescriptive Text): Prompt langsung kepada pemilik. Misal: "Tingkat permainan Game X turun 30% minggu ini. Pertimbangkan untuk mengadakan turnamen kecil atau menjadikannya paket promo."

2. Kesehatan Distribusi Genre (Supply vs Demand Matching)

Logika Sistem: Pemetaan inventaris dibandingkan dengan selera aktual pelanggan rental.

Mekanisme Visual: Menggunakan Radar Chart (Grafik Laba-laba) dengan dua sumbu data:

Data A: Genre of Available Inventory (Genre game yang saat ini ter-install di HDD).

Data B: Genre of Played Games (Genre game yang paling sering dimainkan pelanggan).

Insight Generation: Jika Radar Chart menunjukkan ketimpangan (Misal: HDD penuh game RPG, tapi 80% playtime lari ke genre Sports/Fighting), sistem otomatis menyarankan pemilik untuk merotasi inventaris (kembali terhubung ke Mode B).