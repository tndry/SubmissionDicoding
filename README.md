# **Air Quality Analysis**

## **Deskripsi**

Website ini dibangun dengan Streamlit yang berguna dalam melakukan analisis Air Quality pada 12 stasiun di China. Website ini memungkinkan pengguna untuk melihat tren Air Quality berdasarkan data yang ada.

---

## **Analisis ini meliputi**

- Dasar-dasar Analisis Data
- Penerapan Dasar-dasar Descriptive Statistics
- Pertimbangan dalam Pengolahan Data
- Data Wrangling
- Exploratory Data Analysis
- Data Visualization
- Pengembangan Dashboard

---

## **Teknologi yang Digunakan**

Website ini dibangun dengan menggunakan teknologi berikut:

- **Backend**: Python
- **Frontend**: Streamlit
- **Database**: CSV
- **Tools**: Streamlit

---

## **URL Website**

[Air Quality Dashboard](https://airqualityanalysiswebsite.streamlit.app/)

---

## **Cara Menjalankan Project**

### **Persyaratan**

Pastikan Anda telah menginstal software berikut di komputer Anda:

- Python (versi 3.8 atau lebih baru)
- pip (Package Installer for Python)

### **Langkah-langkah Setup Environment**

1. **Clone Repository**

   ```bash
   git clone https://github.com/username/air-quality-analysis.git
   cd air-quality-analysis
   ```

2. **Buat Virtual Environment (Opsional)**
   Sangat disarankan untuk membuat virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate    # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
   ```

3. **Install Dependencies**
   Instal semua package yang diperlukan:

   ```bash
   pip install -r requirements.txt
   ```

4. **Tambahkan File Data**
   Pastikan file data CSV telah tersedia di direktori `data/`.

### **Menjalankan Dashboard**

1. Jalankan perintah berikut untuk memulai aplikasi:

   ```bash
   streamlit run dashboard.py
   ```

2. Dashboard akan tersedia di browser Anda melalui URL default:
   ```
   http://localhost:
   ```

---

## **Keterangan Dataset**

Dataset digunakan dalam format CSV dengan struktur kolom sebagai berikut:

- **year**: Tahun pengukuran.
- **month**: Bulan pengukuran.
- **day**: Hari pengukuran.
- **hour**: Jam pengukuran.
- **PM2.5**: Kadar Particulate Matter 2.5.
- **PM10**: Kadar Particulate Matter 10.
- **SO2**: Konsentrasi sulfur dioksida.
- **NO2**: Konsentrasi nitrogen dioksida.
- **O3**: Konsentrasi ozon.
- **CO**: Konsentrasi karbon monoksida.
- **TEMP**: Suhu/Temperature.
- **PRES**: Tekanan Udara.
- **RAIN**: Curah Hujan.
- **station**: Stasiun Pengamatan.

Pastikan dataset disimpan dalam folder `data/`
