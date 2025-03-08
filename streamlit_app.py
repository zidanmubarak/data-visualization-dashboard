import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Set konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Berbagi Sepeda",
    page_icon="🚲",
    layout="wide"
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    # Memuat dataset gabungan dari file CSV
    combined_df = pd.read_csv('dashboard/combined.csv')
    
    # Mengonversi kolom tanggal ke datetime
    combined_df['dteday'] = pd.to_datetime(combined_df['dteday'])
    
    # Memetakan kolom kategorikal
    season_map = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    weathersit_map = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan/Salju Ringan', 4: 'Hujan/Salju Lebat'}
    weekday_map = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    
    combined_df['season_name'] = combined_df['season'].map(season_map)
    combined_df['weathersit_name'] = combined_df['weathersit'].map(weathersit_map)
    combined_df['weekday_name'] = combined_df['weekday'].map(weekday_map)
    
    # Menambahkan kolom weekend/weekday seperti di notebook
    combined_df['is_weekend'] = combined_df['weekday'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')
    
    # Membuat agregasi per hari untuk analisis tingkat hari
    day_df = combined_df.groupby('dteday').agg({
        'season': 'first',
        'yr': 'first',
        'mnth': 'first',
        'holiday': 'first',
        'weekday': 'first',
        'workingday': 'first',
        'weathersit': 'first',
        'temp': 'mean',
        'atemp': 'mean',
        'hum': 'mean',
        'windspeed': 'mean',
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum',
        'season_name': 'first',
        'weathersit_name': 'first',
        'weekday_name': 'first',
        'is_weekend': 'first'
    }).reset_index()
    
    return combined_df, day_df

# Memuat data
combined_df, day_df = load_data()

# Judul dan deskripsi
st.title("🚲 Dashboard Analisis Berbagi Sepeda")
st.markdown("""
Dashboard ini menyajikan analisis data berbagi sepeda untuk memahami pola penggunaan dan faktor-faktor yang mempengaruhi penyewaan sepeda.
""")

# Sidebar untuk filter
st.sidebar.header("Filter")

# Filter rentang tanggal
min_date = combined_df['dteday'].min().date()
max_date = combined_df['dteday'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Pilih rentang tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Mengonversi ke datetime untuk filter
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Filter dataframe berdasarkan tanggal
filtered_combined_df = combined_df[(combined_df['dteday'] >= start_date) & (combined_df['dteday'] <= end_date)]
filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]

# Filter musim
selected_seasons = st.sidebar.multiselect(
    "Pilih musim",
    options=day_df['season_name'].unique(),
    default=day_df['season_name'].unique()
)

# Filter cuaca
selected_weather = st.sidebar.multiselect(
    "Pilih kondisi cuaca",
    options=day_df['weathersit_name'].unique(),
    default=day_df['weathersit_name'].unique()
)

# Menerapkan filter
if selected_seasons:
    filtered_combined_df = filtered_combined_df[filtered_combined_df['season_name'].isin(selected_seasons)]
    filtered_day_df = filtered_day_df[filtered_day_df['season_name'].isin(selected_seasons)]

if selected_weather:
    filtered_combined_df = filtered_combined_df[filtered_combined_df['weathersit_name'].isin(selected_weather)]
    filtered_day_df = filtered_day_df[filtered_day_df['weathersit_name'].isin(selected_weather)]

# Menampilkan metrik utama
st.header("Metrik Utama")
col1, col2, col3, col4 = st.columns(4)

total_rentals = filtered_day_df['cnt'].sum()
avg_daily_rentals = filtered_day_df['cnt'].mean()
max_daily_rentals = filtered_day_df['cnt'].max()
total_days = filtered_day_df.shape[0]

col1.metric("Total Penyewaan", f"{total_rentals:,}")
col2.metric("Rata-rata Penyewaan Harian", f"{avg_daily_rentals:.2f}")
col3.metric("Penyewaan Harian Maksimum", f"{max_daily_rentals:,}")
col4.metric("Jumlah Hari Dianalisis", f"{total_days}")

# Membuat tab untuk analisis sesuai pertanyaan bisnis
tab1, tab2, tab3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Analisis Lanjutan"])

with tab1:
    # st.header("1. Bagaimana kondisi musim dan cuaca mempengaruhi permintaan penyewaan sepeda?")
    
    # Kolom untuk dua visualisasi
    col1, col2 = st.columns(2)
    
    with col1:
        # Analysis of seasonal impact - persis seperti di notebook
        seasonal_rentals = filtered_day_df.groupby('season_name')['cnt'].agg(['mean', 'sum']).reset_index()
        seasonal_rentals = seasonal_rentals.sort_values('sum', ascending=False)
        
        fig = px.bar(
            seasonal_rentals, 
            x='season_name', 
            y='mean',
            color='season_name',
            labels={'mean': 'Rata-rata Penyewaan', 'season_name': 'Musim'},
            title='Rata-rata Penyewaan Sepeda Harian berdasarkan Musim',
            category_orders={"season_name": seasonal_rentals['season_name'].tolist()}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Analysis of weather impact - persis seperti di notebook
        weather_rentals = filtered_day_df.groupby('weathersit_name')['cnt'].agg(['mean', 'sum', 'count']).reset_index()
        weather_rentals = weather_rentals.sort_values('mean', ascending=False)
        
        fig = px.bar(
            weather_rentals, 
            x='weathersit_name', 
            y='mean',
            color='weathersit_name',
            labels={'mean': 'Rata-rata Penyewaan', 'weathersit_name': 'Kondisi Cuaca'},
            title='Rata-rata Penyewaan Sepeda Harian berdasarkan Kondisi Cuaca',
            category_orders={"weathersit_name": weather_rentals['weathersit_name'].tolist()}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Advanced analysis: Impact of temperature and humidity - persis seperti di notebook
    st.subheader("Hubungan Penyewaan Sepeda dengan Suhu dan Kelembaban")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            filtered_day_df, 
            x='temp', 
            y='cnt',
            color='season_name',
            labels={'cnt': 'Jumlah Penyewaan', 'temp': 'Suhu (Ternormalisasi)', 'season_name': 'Musim'},
            title='Hubungan Penyewaan Sepeda dengan Suhu (berdasarkan Musim)',
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            filtered_day_df, 
            x='hum', 
            y='cnt',
            color='season_name',
            labels={'cnt': 'Jumlah Penyewaan', 'hum': 'Kelembaban (Ternormalisasi)', 'season_name': 'Musim'},
            title='Hubungan Penyewaan Sepeda dengan Kelembaban (berdasarkan Musim)',
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # st.header("2. Bagaimana pola penggunaan sepeda sepanjang hari dan minggu?")
    
    # Hourly usage patterns - persis seperti di notebook
    hourly_rentals = filtered_combined_df.groupby('hr')['cnt'].mean().reset_index()
    
    fig = px.line(
        hourly_rentals, 
        x='hr', 
        y='cnt',
        markers=True,
        labels={'cnt': 'Rata-rata Jumlah Penyewaan', 'hr': 'Jam'},
        title='Rata-rata Penyewaan Sepeda berdasarkan Jam'
    )
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig, use_container_width=True)
    
    # Hourly patterns by day type (weekday vs weekend) - persis seperti di notebook
    hourly_by_daytype = filtered_combined_df.groupby(['hr', 'is_weekend'])['cnt'].mean().reset_index()
    
    fig = px.line(
        hourly_by_daytype, 
        x='hr', 
        y='cnt', 
        color='is_weekend',
        markers=True,
        labels={'cnt': 'Rata-rata Jumlah Penyewaan', 'hr': 'Jam', 'is_weekend': 'Tipe Hari'},
        title='Rata-rata Penyewaan Sepeda berdasarkan Jam dan Tipe Hari'
    )
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis by hour and user type - persis seperti di notebook
    hour_df_agg = filtered_combined_df.groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()
    
    # Melting data untuk format yang sesuai dengan plotly
    hour_df_agg_melted = pd.melt(
        hour_df_agg,
        id_vars=['hr'],
        value_vars=['casual', 'registered', 'cnt'],
        var_name='user_type',
        value_name='avg_rentals'
    )
    
    # Memetakan jenis pengguna
    user_type_map = {
        'casual': 'Pengguna Biasa', 
        'registered': 'Pengguna Terdaftar', 
        'cnt': 'Total Penyewaan'
    }
    hour_df_agg_melted['user_type'] = hour_df_agg_melted['user_type'].map(user_type_map)
    
    fig = px.line(
        hour_df_agg_melted,
        x='hr',
        y='avg_rentals',
        color='user_type',
        markers=True,
        labels={
            'hr': 'Jam',
            'avg_rentals': 'Rata-rata Jumlah Penyewaan',
            'user_type': 'Tipe Pengguna'
        },
        title='Penyewaan Sepeda per Jam berdasarkan Tipe Pengguna'
    )
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # st.header("Analisis Lanjutan")
    
    st.subheader("1. Time-based Usage Clustering")
    
    # Create features for time-based clustering
    hour_features = filtered_combined_df.groupby('hr')['cnt'].mean().reset_index()
    hour_features.columns = ['hour', 'avg_rentals']
    
    # Manual clustering using pd.cut (binning) based on the hourly pattern
    hour_features['usage_cluster'] = pd.cut(
        hour_features['avg_rentals'],
        bins=[0, 50, 150, 250, 500],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Map English to Indonesian for display
    cluster_map = {
        'Low': 'Rendah',
        'Medium': 'Sedang',
        'High': 'Tinggi',
        'Very High': 'Sangat Tinggi'
    }
    hour_features['cluster_name'] = hour_features['usage_cluster'].map(cluster_map)
    
    # Visualize the time-based clusters
    fig = px.bar(
        hour_features,
        x='hour',
        y='avg_rentals',
        color='cluster_name',
        labels={
            'hour': 'Jam',
            'avg_rentals': 'Rata-rata Jumlah Penyewaan',
            'cluster_name': 'Tingkat Penggunaan'
        },
        title='Penyewaan Sepeda per Jam dengan Pengelompokan berdasarkan Volume Penggunaan',
        color_discrete_map={
            'Rendah': 'lightblue',
            'Sedang': 'skyblue',
            'Tinggi': 'royalblue',
            'Sangat Tinggi': 'darkblue'
        }
    )
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig, use_container_width=True)
    
    # Create a summary of the time-based clusters
    time_cluster_summary = hour_features.groupby('cluster_name')['hour'].apply(list).reset_index()
    time_cluster_summary['count'] = time_cluster_summary['hour'].apply(len)
    time_cluster_summary['hours'] = time_cluster_summary['hour'].apply(lambda x: ', '.join([f"{h}:00" for h in sorted(x)]))
    
    # Urutkan berdasarkan tingkat penggunaan
    cluster_order = {
        'Rendah': 0,
        'Sedang': 1,
        'Tinggi': 2,
        'Sangat Tinggi': 3
    }
    time_cluster_summary['order'] = time_cluster_summary['cluster_name'].map(cluster_order)
    time_cluster_summary = time_cluster_summary.sort_values('order')
    
    # Tampilkan tabel ringkasan
    st.write("Ringkasan Klaster berdasarkan Waktu:")
    st.dataframe(time_cluster_summary[['cluster_name', 'count', 'hours']])
    
    st.subheader("2. Weather-Temperature Impact Clustering")
    
    # Create a dataset for weather analysis
    weather_temp_df = filtered_day_df[['temp', 'hum', 'windspeed', 'weathersit_name', 'cnt']].copy()
    
    # Bin temperature into categories
    weather_temp_df['temp_category'] = pd.cut(
        weather_temp_df['temp'],
        bins=[0, 0.25, 0.5, 0.75, 1.0],
        labels=['Dingin', 'Sejuk', 'Hangat', 'Panas']
    )
    
    # Bin humidity into categories
    weather_temp_df['humidity_category'] = pd.cut(
        weather_temp_df['hum'],
        bins=[0, 0.5, 0.7, 1.0],
        labels=['Rendah', 'Sedang', 'Tinggi']
    )
    
    # Create weather-temp groups (manual clustering based on domain knowledge)
    weather_temp_df['weather_temp_group'] = weather_temp_df.apply(
        lambda row: f"{row['weathersit_name']} - {row['temp_category']}",
        axis=1
    )
    
    # Analyze the impact of these weather-temp groups on rentals
    weather_temp_impact = weather_temp_df.groupby('weather_temp_group')['cnt'].agg(['mean', 'count']).reset_index()
    weather_temp_impact = weather_temp_impact.sort_values('mean', ascending=False)
    
    # Filter groups with sufficient data points (at least 10)
    weather_temp_impact = weather_temp_impact[weather_temp_impact['count'] >= 10]
    
    # Visualize weather-temp groups
    fig = px.bar(
        weather_temp_impact,
        x='weather_temp_group',
        y='mean',
        color='weather_temp_group',
        labels={
            'weather_temp_group': 'Kelompok Cuaca-Suhu',
            'mean': 'Rata-rata Jumlah Penyewaan'
        },
        title='Rata-rata Penyewaan Sepeda berdasarkan Kelompok Cuaca-Suhu'
    )
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("3. Seasonal User Type Clustering")
    
    # Create a seasonal user type dataset
    seasonal_user_df = filtered_day_df[['season_name', 'casual', 'registered', 'cnt']].copy()
    
    # Calculate the proportion of casual vs registered users
    seasonal_user_df['casual_ratio'] = seasonal_user_df['casual'] / seasonal_user_df['cnt']
    seasonal_user_df['registered_ratio'] = seasonal_user_df['registered'] / seasonal_user_df['cnt']
    
    # Bin days based on proportion of registered users (manual clustering)
    seasonal_user_df['user_composition'] = pd.cut(
        seasonal_user_df['registered_ratio'],
        bins=[0, 0.6, 0.75, 0.9, 1.0],
        labels=['Mayoritas Pengguna Biasa', 'Campuran', 'Mayoritas Pengguna Terdaftar', 'Hampir Semua Pengguna Terdaftar']
    )
    
    # Analyze user composition by season
    user_comp_by_season = pd.crosstab(
        seasonal_user_df['season_name'],
        seasonal_user_df['user_composition'],
        normalize='index'
    ) * 100
    
    # Melting untuk format yang sesuai dengan plotly
    user_comp_melted = user_comp_by_season.reset_index().melt(
        id_vars=['season_name'],
        var_name='user_composition',
        value_name='percentage'
    )
    
    # Visualize the seasonal user composition
    fig = px.bar(
        user_comp_melted,
        x='season_name',
        y='percentage',
        color='user_composition',
        barmode='stack',
        labels={
            'season_name': 'Musim',
            'percentage': 'Persentase Hari',
            'user_composition': 'Komposisi Pengguna'
        },
        title='Komposisi Pengguna berdasarkan Musim'
    )
    st.plotly_chart(fig, use_container_width=True)

# Kesimpulan
st.header("Kesimpulan")
st.write("""
Berdasarkan analisis data penyewaan sepeda, berikut adalah kesimpulan utama:

1. **Kondisi Musim dan Cuaca**:
   - Penyewaan sepeda tertinggi terjadi pada Musim Panas dan Musim Gugur, dengan penggunaan yang lebih rendah di Musim Dingin.
   - Kondisi cuaca cerah menghasilkan jumlah penyewaan tertinggi, sementara penyewaan menurun drastis saat cuaca hujan.
   - Suhu memiliki korelasi positif yang kuat dengan penyewaan sepeda, menunjukkan bahwa orang lebih cenderung menyewa sepeda saat cuaca hangat.
   - Kelembaban tinggi berdampak negatif pada penyewaan sepeda.

2. **Pola Penggunaan Sepanjang Hari dan Minggu**:
   - Terdapat dua puncak penggunaan sepeda yang jelas pada hari kerja: pukul 8 pagi dan pukul 17-18 sore, yang sesuai dengan waktu perjalanan komuter.
   - Pada akhir pekan, penyewaan sepeda cenderung meningkat secara bertahap sepanjang pagi hingga mencapai puncak di siang hari, menunjukkan pola rekreasi.
   - Pengguna terdaftar merupakan mayoritas penggunaan pada hari kerja, sementara proporsi pengguna kasual meningkat pada akhir pekan.
   - Jam 0-6 pagi secara konsisten menunjukkan tingkat penggunaan rendah di seluruh minggu.

3. **Segmentasi Pengguna**:
   - Pengguna terdaftar mencerminkan pola perjalanan komuter dengan puncak penggunaan yang jelas pada jam sibuk.
   - Pengguna kasual lebih dipengaruhi oleh kondisi cuaca dan akhir pekan, menunjukkan penggunaan yang lebih rekreasional.
   - Komposisi pengguna bervariasi berdasarkan musim, dengan peningkatan proporsi pengguna kasual selama Musim Panas.

4. **Rekomendasi Bisnis**:
   - Optimalkan ketersediaan sepeda selama jam puncak (8 pagi dan 17-18 sore) pada hari kerja untuk mengakomodasi pengguna terdaftar.
   - Tingkatkan promosi untuk pengguna kasual selama akhir pekan dan Musim Panas ketika penggunaan rekreasional meningkat.
   - Jadwalkan pemeliharaan sepeda pada jam penggunaan rendah (tengah malam hingga pagi hari) untuk meminimalkan gangguan layanan.
   - Pertimbangkan strategi harga dinamis yang menawarkan diskon selama kondisi cuaca kurang ideal atau pada jam-jam sepi untuk mengoptimalkan penggunaan.
""")

# Menambahkan footer dengan informasi pembuat
st.markdown("---")
st.markdown("Dibuat oleh Zidan Mubarak untuk Dicoding Indonesia - Belajar Analisis Data dengan Python")