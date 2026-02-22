Berikut versi **README.md** yang lebih rapi, konsisten, dan siap dipakai di GitHub (menggunakan Markdown standar):

---

# 🌍 Smart AI Travel Assistant (Free Version)

**Smart AI Travel Assistant** adalah aplikasi chatbot cerdas yang memberikan rekomendasi tempat wisata **secara real-time** berdasarkan **lokasi pengguna** dan **mood (suasana hati)**.
Aplikasi ini memanfaatkan teknologi **NLP dari Google Gemini** dan data peta dari **OpenStreetMap**.

---

## ✨ Fitur Utama

* **🧠 Mood-Based Recommendation**
  Menggunakan NLP untuk memahami keinginan pengguna
  *(contoh: “mau yang adem”, “cari yang seru”, “tempat tenang”)*

* **📍 Real-Time Geolocation**
  Mendeteksi lokasi pengguna secara otomatis melalui browser

* **🗺️ Live Map Data**
  Mengambil data tempat wisata nyata di sekitar pengguna menggunakan **Overpass API**

* **🎯 Smart Filtering**
  Mengurutkan tempat wisata dari yang **terdekat** hingga **paling relevan**

* **💳 No Credit Card Required**
  Menggunakan API gratis tanpa verifikasi kartu kredit

---

## 🛠️ Langkah-Langkah Instalasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda.

### 1️⃣ Install Python

Pastikan Anda telah menginstal **Python** versi **3.9 atau lebih baru**.

> ⚠️ **Penting:**
> Saat instalasi, **centang opsi “Add Python to PATH”**

---

### 2️⃣ Persiapkan Folder Proyek

Buka **Terminal / Command Prompt**, lalu jalankan:

```bash
mkdir smart-ai-travel-assistant
cd smart-ai-travel-assistant
```

---

### 3️⃣ Install Library yang Dibutuhkan

Install seluruh dependensi yang diperlukan:

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Dapatkan Google Gemini API Key

Aplikasi ini membutuhkan API Key dari Google Gemini.

Langkah-langkah:

1. Buka Google AI Studio
2. Login dengan akun Google
3. Klik **Get API Key**
4. Salin (copy) API Key Anda

---

### 5️⃣ Setup File Aplikasi

1. Buat file bernama `app.py` di folder proyek
2. Tempelkan kode Python aplikasi
3. Cari baris berikut:

   ```python
   genai.configure(api_key="Isi_API_Key_Anda")
   ```
4. Ganti dengan API Key Anda

---

## 🚀 Cara Menjalankan Aplikasi

1. Buka Terminal / VS Code di folder proyek
2. Jalankan perintah:

   ```bash
   streamlit run app.py
   ```
3. Browser akan terbuka otomatis di:

   ```
   http://localhost:8501
   ```
4. Klik **Allow** saat browser meminta izin akses lokasi
5. Mulai chatting dengan bot 🎉

   > Contoh: *“Cari tempat yang adem dan hijau di dekat sini”*

---

## 📁 Struktur File

```
📦 smart-ai-travel-assistant
 ┣ 📜 app.py              # Kode utama aplikasi (Streamlit)
 ┣ 📜 requirements.txt    # Daftar library untuk instalasi/deployment
 ┗ 📜 README.md           # Dokumentasi proyek
```
