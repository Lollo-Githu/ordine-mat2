import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Connessione a Google Sheets tramite secrets
@st.cache_resource
def connect_to_gsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(st.secrets["gspread"], scopes=scopes)
    client = gspread.authorize(creds)
    return client

# Carica materiali dal foglio "Magazzino"
@st.cache_data
def get_materiali():
    sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Magazzino")
    df = pd.DataFrame(sheet.get_all_records())
    return sorted(df["Nome"].dropna().unique())

# Carica location dal foglio "Magazzino"
@st.cache_data
def get_location():
    sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Magazzino")
    df = pd.DataFrame(sheet.get_all_records())
    return sorted(df["Location"].dropna().unique())

# Interfaccia Streamlit
st.title("📦 Modulo Ordine Materiale")

with st.form("order_form"):
    user_name = st.text_input("👤 Nome e Cognome")
    user_email = st.text_input("📧 Email")
    materiale = st.selectbox("📦 Materiale", get_materiali())
    quantita = st.number_input("🔢 Quantità", min_value=1, step=1)
    location = st.selectbox("📍 Location", get_location())
    consegna = st.date_input("📅 Data di Consegna")
    ritiro = st.date_input("📅 Data di Ritiro")
    
    submitted = st.form_submit_button("✅ Invia Ordine")

if submitted:
    try:
        sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Ordini")
        nuovo_ordine = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_name,
            user_email,
            materiale,
            quantita,
            location,
            consegna.strftime("%Y-%m-%d"),
            ritiro.strftime("%Y-%m-%d")
        ]
        sheet.append_row(nuovo_ordine)
        st.success("✅ Ordine inviato correttamente!")
    except Exception as e:
        st.error(f"❌ Errore durante l'invio dell'ordine: {e}")
