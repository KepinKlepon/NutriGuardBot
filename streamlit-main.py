# streamlit-main.py (Modifikasi untuk LangGraph)
import streamlit as st
from google import genai 
from agent import create_nutriguard_agent, run_agent # Import Agent logic

st.set_page_config(
    page_title="Nutri-Guard Bot",
    layout="wide", # Menggunakan lebar penuh layar
    initial_sidebar_state="expanded"
)

# --- 1. Page Configuration and Title ---
st.title("🍎 Nutri-Guard Bot | Asisten Kesehatan AI")
st.caption("💪 Informasi Gizi, Pencegahan Penyakit, dan Tips Hidup Sehat")

# --- 2. Sidebar for Settings ---
# --- 2. Sidebar for Settings ---

# Buatlah subheader yang lebih menarik
with st.sidebar:
    st.subheader("⚙️ Pengaturan Aplikasi")
    
    # [... Kode untuk google_api_key dan reset_button ...]
    
    # ----------------------------------------------------
    # Bagian Baru: Informasi dan Estetika
    # ----------------------------------------------------
    
    # Tambahkan garis horizontal untuk pemisah visual
    st.markdown("---") 
    
    st.subheader("Tentang Nutri-Guard Bot")
    st.markdown(
        "Bot ini dirancang sebagai asisten gizi dan kesehatan. "
        "Kami menggunakan model **Gemini 2.5 Flash** dan "
        "framework **LangGraph** untuk memastikan respons "
        "yang informatif dan terstruktur. "
        "\n\n**⚠️ Selalu konsultasikan masalah medis profesional.**"
    )

with st.sidebar:
    st.subheader("Settings")
    google_api_key = st.text_input("Google AI API Key", type="password")
    reset_button = st.button("Reset Conversation", help="Clear all messages and start fresh")

# --- 3. API Key and Agent Initialization Check ---
if not google_api_key:
    st.info("Masukkan Google AI API key Anda di sidebar untuk memulai.", icon="🗝️")
    st.stop()

# Inisialisasi LangGraph Agent
if ("agent_app" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        # Gunakan fungsi dari agent.py
        st.session_state.agent_app = create_nutriguard_agent(google_api_key)
        st.session_state._last_key = google_api_key
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error(f"Invalid API Key or Error initializing Agent: {e}")
        st.stop()

# --- 4. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_button:
    st.session_state.pop("messages", None)
    st.rerun()

# --- 5. Display Past Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. Handle User Input and Agent Communication ---
prompt = st.chat_input("Tanyakan tentang gizi, makanan sehat, atau gejala umum...")

if prompt:
    # 1. Tampilkan pesan pengguna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Dapatkan respons dari LangGraph Agent
    try:
        # Panggil fungsi run_agent dari agen.py
        answer = run_agent(st.session_state.agent_app, prompt) 
        
    except Exception as e:
        # Menampilkan error yang ramah pengguna
        answer = f"⚠️ Maaf, terjadi kesalahan saat memproses permintaan Anda: {e}"

    # 3. Tampilkan dan simpan respons asisten
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})