import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

# Connessione a Google Sheets tramite secrets
@st.cache_resource
def connect_to_gsheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["gspread"], scopes=scopes)
    client = gspread.authorize(creds)
    return client

# Carica materiali dal foglio "Magazzino"
@st.cache_data
def get_materiali():
    sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Magazzino")
    df = pd.DataFrame(sheet.get_all_records())
    return sorted(df["Nome"].dropna().unique())

# UI
st.title("Modulo Ordine Materiali")

materiali = get_materiali()
materiale = st.selectbox("Scegli il materiale", materiali)
quantita = st.number_input("Quantità", min_value=1, step=1)
location = st.text_input("Location")
data_consegna = st.date_input("Data consegna")
ritiro = st.text_input("Modalità di ritiro")
nome = st.text_input("Il tuo nome")
email = st.text_input("Email")

if st.button("Invia Ordine"):
    if not all([materiale, quantita, location, nome, email]):
        st.error("Compila tutti i campi obbligatori.")
    else:
        try:
            sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Ordini")
            nuovo_ordine = [nome, email, materiale, quantita, location, str(data_consegna), ritiro]
            sheet.append_row(nuovo_ordine)
            st.success("Ordine inviato con successo!")
        except Exception as e:
            st.error(f"Errore durante l'invio dell'ordine: {e}")
