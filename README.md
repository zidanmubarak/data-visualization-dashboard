# Analisis Dataset Berbagi Sepeda

## Gambaran Proyek
Proyek ini menganalisis Dataset Berbagi Sepeda untuk memahami pola dan faktor-faktor yang mempengaruhi penyewaan sepeda. Analisis ini mencakup:
- Mengeksplorasi dampak musim dan cuaca pada permintaan penyewaan sepeda
- Menyelidiki pola penggunaan per jam dan harian
- Analisis pengelompokan untuk mengidentifikasi pola penggunaan yang berbeda
- Dashboard interaktif untuk memvisualisasikan temuan utama

## Dataset
Analisis ini menggunakan Dataset Berbagi Sepeda yang berisi:
- **day.csv**: Data penyewaan sepeda harian dengan informasi cuaca dan musim
- **hour.csv**: Data penyewaan sepeda per jam dengan informasi cuaca dan musim

## Struktur Proyek
```
submission/
├───dashboard/
│   ├───combined.csv
│   └───dashboard.py
├───data/
│   ├───day.csv
│   ├───hour.csv
│   └───combined.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Petunjuk Pengaturan

### Prasyarat
- Python 3.9 atau lebih tinggi
- Library yang diperlukan dalam requirements.txt

### Instalasi
1. Clone repositori ini atau ekstrak file ZIP yang disubmit
2. Instal paket yang diperlukan:
   ```
   pip install -r requirements.txt
   ```

### Menjalankan Dashboard
1. Pastikan untuk menjalankan notebook terlebih dahulu untuk menghasilkan file combined.csv
2. Salin file combined.csv ke direktori dashboard
3. Navigasi ke direktori dashboard:
   ```
   cd submission/dashboard
   ```
4. Jalankan aplikasi Streamlit:
   ```
   streamlit run dashboard.py
   ```
5. Dashboard akan terbuka di browser web default Anda di `http://localhost:8501`

## Sorotan Analisis

### Pertanyaan Bisnis yang Dijawab
1. **Bagaimana kondisi musim dan cuaca mempengaruhi permintaan penyewaan sepeda?**
   - Analisis pola penyewaan di berbagai musim
   - Dampak kondisi cuaca pada penyewaan harian
   - Efek suhu dan kelembaban

2. **Bagaimana pola penggunaan puncak sepanjang hari dan minggu?**
   - Pola penyewaan per jam pada hari kerja vs akhir pekan
   - Analisis hari dalam seminggu
   - Identifikasi jam-jam puncak

### Fitur Dashboard
- Penyaringan interaktif berdasarkan rentang tanggal, musim, dan kondisi cuaca
- Visualisasi pola musiman
- Analisis penggunaan harian dan per jam
- Analisis dampak cuaca
- Pengelompokan penggunaan berdasarkan volume penyewaan

## Penulis
Zidan Mubarak

## Ucapan Terima Kasih
- Sumber data: [Dataset Berbagi Sepeda](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset)
- Dicoding Indonesia - Kursus Belajar Analisis Data dengan Python