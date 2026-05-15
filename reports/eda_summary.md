# EDA Summary: Smart Inventory Forecasting

## Pendahuluan
Dokumen ini merangkum hasil Exploratory Data Analysis (EDA) yang dilakukan pada dataset historis transaksi inventory (`inventory_timeseries.csv` dan `inventory_clean.csv`). Analisis ini berfokus pada pemahaman pergerakan produk, tren penjualan, dan pemantauan stok untuk mendukung keputusan *restock* pada dashboard UMKM.

## Pertanyaan Bisnis & Insight

### 1. Produk apa saja yang paling banyak terjual dan menghasilkan pendapatan terbesar (Top-selling products)?
Berdasarkan agregasi nilai penjualan (IDR), 10 produk penyumbang pendapatan terbesar (Top-selling) adalah:
1. **Paper Towels**
2. **Iron**
3. **Peanut Butter**
4. **Ketchup**
5. **Water**
6. **BBQ Sauce**
7. **Chicken**
8. **Pickles**
9. **Hand Sanitizer**
10. **Laundry Detergent**

> **Insight Bisnis:** Produk-produk ini merupakan penggerak utama cash-flow UMKM. UMKM harus memastikan produk ini tidak pernah mengalami *stock out* (kehabisan stok) karena akan berdampak signifikan pada pendapatan harian.

### 2. Produk apa saja yang memiliki tingkat penjualan terendah (Slow-moving products)?
Berdasarkan total unit yang terjual (`quantity_sold`), produk-produk yang tergolong lambat terjual (*slow-moving*) di antaranya adalah:
- Water, Trash Bags, Butter, Chicken, Canned Soup, Dustpan, Tissues, Spinach, Apple, dan Broom.

> **Insight Bisnis:** UMKM berisiko mengalami *overstock* untuk produk-produk ini jika dibeli dalam jumlah besar. Pengurangan frekuensi restock atau promo diskon disarankan untuk mempercepat perputaran barang.

### 3. Bagaimana tren penjualan secara keseluruhan dari waktu ke waktu?
Grafik tren penjualan bulanan menunjukkan fluktuasi. 
> **Insight Bisnis:** Pola naik-turun ini mengindikasikan adanya permintaan musiman atau pengaruh kejadian tertentu pada perilaku konsumen. Data ini sangat valid untuk dijadikan dasar pelatihan model *Time-Series Forecasting* untuk menangkap tren masa depan.

### 4. Produk mana yang sering mengalami kondisi stock out atau mendekati reorder point?
Berdasarkan selisih antara stok harian dan titik pemesanan kembali (*reorder point*), kita mengidentifikasi ada beberapa produk yang stok aslinya sangat sering mendekati atau menyentuh garis batas *reorder point*.

### 5. Bagaimana perbandingan stok saat ini dengan rekomendasi restock?
Hasil analisis pergerakan stok (Stock Movement) menyoroti top 10 produk yang akumulasi kebutuhan *restock*-nya paling tinggi. 
> **Insight Bisnis:** Model restock yang kita implementasikan berhasil menyarankan volume restock proporsional: cukup besar untuk produk yang mendekati limit *reorder*, dan merekomendasikan `0` (nol) untuk barang yang masih berstatus aman.

## Kesimpulan & Penyesuaian dengan PRD
Analisis ini **sepenuhnya selaras dengan PRD** MVP, yakni:
- Berfokus pada pergerakan produk terlaris dan paling sepi.
- Menghasilkan tren waktu yang dibutuhkan oleh model AI Forecasting.
- Visualisasi mudah dicerna oleh UMKM (Non-teknis).

*Catatan: Seluruh grafik penunjang dapat dilihat di dalam folder `visualizations/` dan dapat dijalankan interaktif melalui `notebooks/eda_inventory_analysis.ipynb`.*
