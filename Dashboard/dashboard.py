# Menyiapkan semua library yang dibutuhkan
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium 
import json
sns.set(style='dark')


def load_data():
    data = pd.read_csv('Dashboard/data_gabungan.csv')
    return data

# OVERVIEW
def overview_page(data):
    st.title('Overview')
    st.write(" Hi semua, ini merupakan dashboard analysis Air Quality di 12 Station.")

    # Filter station
    station = st.selectbox('Pilih Station', data['station'].unique())
    filtered_data = data[data['station'] == station]

    st.write('Data for Station', station)
    st.dataframe(filtered_data)


# ANALYSIS

def analysis_page(data):
    st.title('Analysis')
    
    st.write('Pada section ini akan disajikan beberapa analysis dari data Air Quality')

    st.write("### Bagaimana tren kualitas udara di tiap station dalam tahun 2016?")
    
    # Filter data untuk tahun 2016 saja
    data_tahun_2016 = data[data['year'] == 2016]

    # Pilih station yang ingin dianalisis
    station_selected = st.multiselect('Pilih Station untuk Analisis', data_tahun_2016['station'].unique())

    
    # Plot dengan matplotlib
    fig, ax = plt.subplots()

    # Loop melalui setiap station yang dipilih
    for station in station_selected:
        # Filter data berdasarkan station yang dipilih
        filtered_data = data_tahun_2016[data_tahun_2016['station'] == station]

        # Grouping data berdasarkan bulan dan hitung rata-rata PM2.5
        monthly_avg_pm25 = filtered_data.groupby('month')['PM2.5'].mean().reset_index()

        # Plot tiap station sebagai garis yang berbeda
        ax.plot(monthly_avg_pm25['month'], monthly_avg_pm25['PM2.5'], marker='o', linestyle='-', linewidth=2, label=station)

    # Tambahkan label dan judul
    ax.set_title("Perbandingan Rata-rata PM2.5 di Berbagai Station Tahun 2016")
    ax.set_xlabel('Bulan')
    ax.set_ylabel('PM2.5')

    # Tampilkan legend untuk membedakan tiap station
    ax.legend(title="Station")

    # Tampilkan plot di Streamlit
    st.pyplot(fig)


    st.write("### Apakah terdapat jam-jam tertentu dimana kualitas udara cenderung buruk ?")
   # Grouping data berdasarkan jam dan hitung rata-rata PM2.5
    hourly_avg_pm25 = data.groupby('hour')['PM2.5'].mean().reset_index()

    # Plotting dengan Matplotlib dan Seaborn
    plt.figure(figsize=(12, 7))
    sns.lineplot(x='hour', y='PM2.5', data=hourly_avg_pm25, marker='o')
    plt.title('Rata-rata PM2.5 setiap jam')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(range(0, 24))  
    plt.ylim(bottom=0)
    plt.grid(True)

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)

    # Menurut BMKG ambang batas PM2.5 adalah 65
    with st.expander('Penjelasan'):
        bad_air_quality = hourly_avg_pm25[hourly_avg_pm25['PM2.5'] > 65]['hour'].tolist()
        st.write(f"Jam-jam dengan kualitas udara cenderung buruk (PM2.5 > 65): {bad_air_quality}")

    # Menampilkan tabel data hasil rata-rata per jam
        st.dataframe(hourly_avg_pm25)

    st.write("### Apakah ada hari dalam seminggu yang memiliki kualitas udara lebih buruk dibandingkan hari lainnya ")

    def day_of_week_analysis(data):
        st.title('Analysis: Kualitas Udara Berdasarkan Hari')

    # Pemetaan nama hari
    day_names = {
        1: 'Mon',
        2: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat',
        7: 'Sun'
    }

    # Tambahkan kolom nama hari berdasarkan angka hari
    data['day_of_week'] = data['day'].map(day_names)

    # Hitung rata-rata PM2.5 per hari dalam seminggu
    day_of_week_avg_pm25 = (
        data.groupby('day_of_week', as_index=False)['PM2.5']
        .mean()
    )

    # Visualisasikan dengan bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='day_of_week', y='PM2.5', data=day_of_week_avg_pm25, order=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.title('Rata-rata PM2.5 Setiap Hari dalam Seminggu')
    plt.xlabel('Hari')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(rotation=45, ha='right')  # Rotasi label x untuk visibilitas lebih baik
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Tambahkan grid horizontal untuk keterbacaan
    plt.tight_layout()

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)
    with st.expander('Penjelasan'):
    # Menampilkan tabel data hasil rata-rata per hari
        st.dataframe(day_of_week_avg_pm25)

    st.write("### Apakah ada hubungan antara suhu dan kualitas udara  ? ")
    

    # Pilih kolom/parameter yang ingin dianalisis korelasinya
    parameters = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN']  

    # Mengambil data untuk parameter-parameter yang dipilih
    data_corr = data[parameters]

    # Menghitung matriks korelasi
    correlation_matrix = data_corr.corr()

    # Visualisasi dengan heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Korelasi Antar Parameter')

    # Menampilkan heatmap di Streamlit
    st.pyplot(plt)
    with st.expander('Penjelasan'):
        st.write(
            """
            1.  Dari hasil visualisasi diatas menunjukkan bahwa jika PM10 meningkat maka PM2.5 juga cenderung menignkat
            2. TEMP, PRES, DEWP, RAIN memiliki korasi rendah, yang brarti parameter ini tidak terlalu memengaruhi konsentrasi udara (PM2.5) 
            """
        )
        
    st.write("### Distribusi Parameter di Setiap Station")

    parameters = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN']

    # Filter
    selected_parameter = st.selectbox('Pilih Parameter: ', parameters)

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(14, 6))  
    sns.boxplot(data=data, x='station', y=selected_parameter, palette='Set3', ax=ax)
    ax.set_title(f'Distribusi {selected_parameter}', fontsize=14)
    ax.set_xlabel('Station', fontsize=12)
    ax.set_ylabel(selected_parameter, fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)

    # Display the plot in Streamlit
    st.pyplot(fig)

  


def conclusion_page():
    st.title('Conclusion')
    st.write('Kesimpulan dari analisis data kualitas udara: ')
    st.markdown(
        """
1. Dara visualisasi data yang didapatkan, data PM2.5 tiap bulannya di 2016 berfluktuatif dengan peningkatan yang signifikan di antara bulan 10 hingga 12. 
2. Rata-rata PM2.5 di tiap jamnya cenderung buruk 
3. Dari hasil visualisasi diatas menunjukkan bahwa jika PM10 meningkat maka PM2.5 juga cenderung menignkat
4. TEMP, PRES, DEWP, RAIN memiliki korasi rendah, yang brarti parameter ini tidak terlalu memengaruhi konsentrasi udara (PM2.5) 
5. PM2.5 dan PM10 menunjukkan distribusi yang relatif seragam, dengan beberapa station yang memiliki pencilan seperti  Changping dan Dingling
6.  Distribusi SO2 cenderung rendah hampir di semua station, dengan beberapa nilai outlier di beberapa station seperti Gucheng
7.  Distrubsi CO2 memiliki konsentrasi tinggi di beberapa station seperti Aotizhongxin
8.  TEMP memiliki distribusi yang cukup beragam di seluruh station dengan variablitas tinggi, mencerminkan perubahan suhu musiman
9. PRES / Tekanan atmosfer menunjukkakn perubahan kecil antar-stasiun
10. RAIN memiliki nilai yang dominan rendah di semua station.
        """)
    
# Main app


# Komponen

with st.sidebar:

    # Logo
    st.image("Dashboard/logo.png")
def main():
    data = load_data()

    # Sidebar
    page = st.sidebar.selectbox('Select Page', ['Overview', 'Analysis', 'Conclusion'])

    if page == 'Overview':
        overview_page(data)
    elif page == 'Analysis':
        analysis_page(data)
    elif page == 'Conclusion':
        conclusion_page()

if __name__ == '__main__':
    main()


    




