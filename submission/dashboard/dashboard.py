import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Nonaktifkan peringatan PyplotGlobalUse
st.set_option('deprecation.showPyplotGlobalUse', False)

# Memuat data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Konversi kolom 'dteday' ke datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Tambahkan kolom 'month' ke dataframe dan konversi ke string
day_df['month'] = day_df['dteday'].dt.to_period('M').astype(str)

# Set tema Seaborn
sns.set_theme(style="whitegrid")

# Fungsi untuk membuat visualisasi
def plot_weather_vs_rentals():
    # Menghitung jumlah penyewaan sepeda berdasarkan musim
    season_counts = day_df.groupby('season')['cnt'].sum().reset_index()
    
    # Plot pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(season_counts['cnt'], labels=['Spring', 'Summer', 'Fall', 'Winter'], autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue', 'gold', 'lightgreen'], startangle=140)
    plt.title('Distribusi Penyewaan Sepeda Berdasarkan Musim', fontsize=16, fontweight='bold')
    st.pyplot()

def plot_daily_orders(selected_date):
    # Filter data berdasarkan tanggal yang dipilih
    selected_date = selected_date.strftime('%Y-%m-%d')
    selected_day_data = day_df[day_df['dteday'] == selected_date]
    
    # Menampilkan total order pada tanggal yang dipilih
    total_orders = selected_day_data['cnt'].sum()
    st.metric(label=f"Total Peminjaman Sepeda pada {selected_date}", value=total_orders)

    # Line chart untuk melihat tren jumlah order per hari
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=day_df, x='dteday', y='cnt', marker='o', color='royalblue', linestyle='-', linewidth=2)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='', alpha=0.6)
    
    st.pyplot()

# Main program
st.title('Dashboard Analisis Data Penyewaan Sepeda🚲')

# Sidebar untuk memilih tanggal
with st.sidebar:
    st.image("https://raw.githubusercontent.com/VikriAHaikal/test1/main/assets/bikesharing.png")
    selected_date = st.date_input("Pilih Tanggal", value=pd.to_datetime(day_df['dteday'].min()), min_value=pd.to_datetime(day_df['dteday'].min()), max_value=pd.to_datetime(day_df['dteday'].max()))

# Menampilkan visualisasi trend penyewaan sepeda
st.subheader('Daily Bike Sharing')
plot_daily_orders(selected_date)

# Menampilkan visualisasi distribusi penyewaan sepeda berdasarkan musim
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Musim')
plot_weather_vs_rentals()

def plot_temperature_vs_rentals():
    # Scatter plot untuk melihat hubungan antara temperatur dan jumlah penyewaan sepeda
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=day_df, x='temp', y='cnt', alpha=0.5, color='orange')
    plt.title('Hubungan Antara Temperatur dan Jumlah Penyewaan Sepeda', fontsize=16, fontweight='bold')
    plt.xlabel('Temperatur (Celsius)', fontsize=14)
    plt.ylabel('Jumlah Penyewaan', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    st.pyplot()

# Menampilkan visualisasi hubungan antara Temperatur dengan jumlah penyewaan sepeda
st.subheader('Hubungan Antara Temperatur dan Jumlah Penyewaan Sepeda')
plot_temperature_vs_rentals()
