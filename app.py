import pandas as pd
import streamlit as st
from datetime import date

# Caricamento dati da Excel
df = pd.read_excel("materiali.xlsx")
materiali = sorted(df["Name"].dropna().unique())

# Location disponibili (in ordine alfabetico)
locations = sorted([
    "Piazza Grande", "GranRex", "Palexpo (FEVI)", "La Sala", "L'altra Sala", "Teatro Kursaal",
    "Palavideo - Muralto", "Rialto 1", "Rialto 2", "Rialto 3", "PalaCinema 1", "PalaCinema 2",
    "PalaCinema 3", "Ex-Gas", "CapCom", "Monzeglio", "Galleria", "Sterrato Ex-Gas", "Rialto",
    "Rotonda - Magazzino", "Hotel Belvedere", "SES - Corte", "SES - Salone", "SES - Saletta blue",
    "Casa Rusca", "Sant'Eugenio", "Palazzo Casorella", "Palacinema", "Forum (@Spazio Cinema)",
    "Monte Verità", "Via V. Pedrotta", "Villa San Quirico", "Piazza Grande - Schermo", "Cassa - PG",
    "Cassa - Coop", "Cassa - Fevi", "Piazza Grande - Cabina Proiezione", "Lettering Locarno di UBS",
    "Rotonda by la Mobiliare", "PalaCinema - 3P", "Davide Campari Lounge", "PalaCinema - 4P",
    "Ufficio Remo Rossi", "Leopard Club Lounge", "La Posta PT", "Banfi (Vallemaggia)",
    "Palacinema - PGR", "Parcheggi Sunstore", "Swiss Life Lounge (@Spazio Cinema)",
    "Parcheggi scuola media Morettina", "Palacinema - LFF", "SUPSI - Magistrale", "Largo Zorzi",
    "Bagni - Marcacci", "Bagni - Fevi / Forum", "Castello Visconteo", "CPC - Uffici",
    "CPC - Spazi OD & Pro", "Hertz - Ritiro auto"
])

# Interfaccia Streamlit
st.title("📦 Modulo Ordine Materiale")

location = st.selectbox("📍 Seleziona la location di consegna", locations)
nome_richiedente = st.text_input("👤 Nome e cognome")
email_richiedente = st.text_input("📧 Indirizzo email")
materiale = st.selectbox("📦 Seleziona il materiale da ordinare", materiali)
quantita = st.number_input("🔢 Inserisci la quantità desiderata", min_value=1, step=1)
data_consegna = st.date_input("📅 Data di consegna", value=date.today())
data_ritiro = st.date_input("📅 Data di ritiro", value=date.today())

if st.button("✅ Invia ordine"):
    nuovo_ordine = pd.DataFrame([{
        "Nome Richiedente": nome_richiedente,
        "Email": email_richiedente,
        "Location": location,
        "Materiale": materiale,
        "Quantità": quantita,
        "Data Consegna": data_consegna,
        "Data Ritiro": data_ritiro
    }])

    try:
        ordini = pd.read_excel("ordini.xlsx")
        ordini = pd.concat([ordini, nuovo_ordine], ignore_index=True)
    except FileNotFoundError:
        ordini = nuovo_ordine

    ordini.to_excel("ordini.xlsx", index=False)
    st.success("✅ Ordine inviato con successo!")
