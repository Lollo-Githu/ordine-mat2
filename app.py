
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

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
=======

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# === Autenticazione Google ===
def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credenziali.json", scopes=scope)
    client = gspread.authorize(creds)
    return client

# === Lettura materiali da foglio "Magazzino" ===
@st.cache_data
def get_materiali():
    sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Magazzino")
    data = sheet.col_values(1)  # Prima colonna
    return sorted(list(set([m.strip() for m in data if m.strip().lower() != "nome del materiale"])))

# === App Streamlit ===
st.title("Modulo ordine materiale")

# Dati utente
user_name = st.text_input("Il tuo nome")
user_email = st.text_input("La tua email")

# Dropdown dei materiali
materiali = get_materiali()
materiale_scelto = st.selectbox("Scegli un materiale", materiali)

# Altri campi
quantita = st.number_input("Quantità", min_value=1, step=1)
location = st.text_input("Location")
consegna = st.date_input("Data di consegna")
ritiro = st.date_input("Data di ritiro")

# Invia ordine
if st.button("Invia Ordine"):
    try:
        sheet = connect_to_gsheet().open("Gestione Ordini").worksheet("Ordini")
        sheet.append_row([user_name, user_email, materiale_scelto, quantita, location, str(consegna), str(ritiro)])
        st.success("Ordine inviato con successo!")
    except Exception as e:
        st.error(f"Errore durante l'invio: {e}")
>>>>>>> e14aa5adc5270ab4c4ec1538f5ea6274d51a506e
