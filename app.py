import streamlit as st
import google.generativeai as genai
import requests
from streamlit_js_eval import get_geolocation
from geopy.distance import geodesic

# --- 1. KONFIGURASI GEMINI ---
genai.configure(api_key="Isikan_API_Key_Anda")
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- 2. FUNGSI AMBIL DATA CERDAS (OVERPASS API) ---
def cari_wisata_osm(lat, lon, categories):
    cat_query = ""
    for cat in categories:
        cat_query += f'node["tourism"="{cat}"](around:20000, {lat}, {lon});'
        cat_query += f'node["leisure"="{cat}"](around:20000, {lat}, {lon});'
        cat_query += f'way["tourism"="{cat}"](around:20000, {lat}, {lon});'

    query = f"""
    [out:json];
    ({cat_query});
    out body;
    """
    url = "https://overpass-api.de/api/interpreter"
    try:
        response = requests.get(url, params={'data': query}, timeout=15)
        data = response.json()
        
        results = []
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            nama = tags.get('name')
            if not nama: continue 
            
            t_lat = element.get('lat') if 'lat' in element else element.get('center', {}).get('lat')
            t_lon = element.get('lon') if 'lon' in element else element.get('center', {}).get('lon')
            
            if t_lat and t_lon:
                jarak = round(geodesic((lat, lon), (t_lat, t_lon)).km, 2)
                results.append({
                    "nama": nama,
                    "jarak": jarak,
                    "tipe": tags.get('tourism') or tags.get('leisure', 'Wisata')
                })
        
        # Urutkan berdasarkan jarak terdekat
        return sorted(results, key=lambda x: x['jarak'])[:7]
    except:
        return []

# --- 3. UI STREAMLIT ---
st.set_page_config(page_title="AI Travel Assistant Free", page_icon="🌳")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🌍 Smart AI Travel Assistant")
st.caption("Pencarian Real-Time Relevan dengan OpenStreetMap")

# Ambil Lokasi Otomatis
loc = get_geolocation()
if loc:
    user_lat = loc['coords']['latitude']
    user_lon = loc['coords']['longitude']
    st.success(f"Lokasi Terdeteksi: {user_lat}, {user_lon}")
else:
    st.info("Menunggu izin lokasi (klik 'Allow' pada browser)...")
    user_lat, user_lon = -6.2000, 106.8166 # Default Jakarta

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input User
if prompt := st.chat_input("Contoh: Cari tempat yang adem dan banyak pohon"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Menganalisa mood dan mencari tempat yang relevan..."):
        nlp_mapping = f"""
        User ingin: "{prompt}". 
        Pilih maksimal 3 kategori yang paling cocok dari daftar OpenStreetMap ini: 
        [theme_park, water_park, zoo, attraction, museum, park, garden, nature_reserve, viewpoint, beach].
        Aturan: Jika user minta 'adem/dingin/hijau', prioritaskan park, nature_reserve, atau garden. 
        HANYA balas dengan kata kunci yang dipisahkan koma.
        """
        raw_cats = model.generate_content(nlp_mapping).text.strip().lower()
        list_categories = [c.strip() for c in raw_cats.split(',')]

        daftar_wisata = cari_wisata_osm(user_lat, user_lon, list_categories)
        
        wisata_info = ""
        for w in daftar_wisata:
            wisata_info += f"- {w['nama']} (Jenis: {w['tipe']}, Jarak: {w['jarak']} km)\n"

        prompt_final = f"""
        Kamu adalah asisten travel profesional. 
        User ingin: {prompt}.
        Kategori yang ditemukan: {list_categories}.
        Daftar tempat terdekat:
        {wisata_info if wisata_info else "Tidak ditemukan tempat yang sangat spesifik."}
        
        Tugas: Berikan saran yang santai dan ajak user mengunjungi tempat yang paling RELEVAN dengan mood mereka.
        Urutkan dari yang terdekat.
        """
        
        response = model.generate_content(prompt_final)
        
    # Jawaban assistant
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
