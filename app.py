import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Connessione a Google Sheets tramite Streamlit secrets
@st.cache_resource
def connect_to_gsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(st.secrets["gspread"], scopes=scopes)
    client = gspread.authorize(creds)
    return client

# Carica materiali e location da Google Sheets
@st.cache_data
def get_materiali_e_location():
    sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Magazzino")
    df = pd.DataFrame(sheet.get_all_records())
    materiali = sorted(df["Nome"].dropna().unique())
    location = sorted(df["Location"].dropna().unique())
    return materiali, location

# UI
st.title("📦 Modulo Ordine Materiale")

materiali, locations = get_materiali_e_location()

with st.form("order_form"):
    nome = st.text_input("👤 Nome e Cognome")
    email = st.text_input("📧 Email")
    materiale = st.selectbox("📦 Materiale", materiali)
    quantita = st.number_input("🔢 Quantità", min_value=1, step=1)
    location = st.selectbox("📍 Location", locations)
    data_consegna = st.date_input("📅 Data di consegna")
    data_ritiro = st.date_input("📅 Data di ritiro")

    submitted = st.form_submit_button("✅ Invia Ordine")

if submitted:
    try:
        sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Ordini")
        nuovo_ordine = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            nome, email, materiale, quantita,
            location,
            data_consegna.strftime("%Y-%m-%d"),
            data_ritiro.strftime("%Y-%m-%d")
        ]
        sheet.append_row(nuovo_ordine)
        st.success("✅ Ordine inviato con successo!")
    except Exception as e:
        st.error(f"❌ Errore durante l'invio dell'ordine: {e}")
