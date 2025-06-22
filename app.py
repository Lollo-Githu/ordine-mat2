
import streamlit as st
import pandas as pd
from io import BytesIO
import base64

st.set_page_config(page_title="Ordine Materiali", layout="centered")

# Carica materiali da Excel
@st.cache_data
def carica_materiali():
    df = pd.read_excel("materiali.xlsx", sheet_name="Magazzino")
    return sorted(df["Nome"].dropna().unique())

# Lista location
location_list = sorted([
    "Bagni - Fevi / Forum", "Bagni - Marcacci", "Banfi (Vallemaggia)", "CapCom",
    "Casa Rusca", "Castello Visconteo", "Cassa - Coop", "Cassa - Fevi",
    "Cassa - PG", "CPC - Spazi OD & Pro", "CPC - Uffici", "Davide Campari Lounge",
    "Ex-Gas", "Forum (@Spazio Cinema)", "Galleria", "GranRex", "Hotel Belvedere",
    "Hertz - Ritiro auto", "L'altra Sala", "La Posta PT", "La Sala",
    "Largo Zorzi", "Leopard Club Lounge", "Lettering Locarno di UBS", "Monzeglio",
    "Monte Verità", "Palacinema", "Palacinema - 4P", "Palacinema - LFF",
    "Palacinema - PGR", "PalaCinema 1", "PalaCinema 2", "PalaCinema 3",
    "PalaCinema - 3P", "Palexpo (FEVI)", "Palavideo - Muralto", "Piazza Grande",
    "Piazza Grande - Cabina Proiezione", "Piazza Grande - Schermo", "Rialto",
    "Rialto 1", "Rialto 2", "Rialto 3", "Rotonda - Magazzino", "Rotonda by la Mobiliare",
    "Sant'Eugenio", "Sant'Eugenio", "SES - Corte", "SES - Saletta blue", "SES - Salone",
    "Sterrato Ex-Gas", "SUPSI - Magistrale", "Swiss Life Lounge (@Spazio Cinema)",
    "Teatro Kursaal", "Ufficio Remo Rossi", "Via V. Pedrotta", "Villa San Quirico"
])

materiali = carica_materiali()

# ----------------- FORM ------------------
st.title("📦 Ordine Materiali")

with st.form("ordine_form"):
    nome = st.text_input("👤 Nome")
    email = st.text_input("📧 Email")
    materiale = st.selectbox("📄 Materiale", materiali)
    quantita = st.number_input("🔢 Quantità", min_value=1)
    location = st.selectbox("📍 Location", location_list)
    data_consegna = st.date_input("📅 Data Consegna")
    data_ritiro = st.date_input("📅 Data Ritiro")

    submitted = st.form_submit_button("✅ Invia Ordine")

if submitted:
    # Crea DataFrame ordine
    ordine = pd.DataFrame([{
        "Nome": nome,
        "Email": email,
        "Materiale": materiale,
        "Quantità": quantita,
        "Location": location,
        "Data Consegna": data_consegna,
        "Data Ritiro": data_ritiro
    }])

    # Salva come Excel in memoria
    buffer = BytesIO()
    ordine.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    b64_excel = base64.b64encode(buffer.read()).decode()

    js = f"""
    <script src="https://cdn.jsdelivr.net/npm/emailjs-com@2/dist/email.min.js"></script>
    <script type="text/javascript">
        (function() {{
            emailjs.init("{st.secrets['PUBLIC_KEY']}");
        }})();

        var templateParams = {{
            user_name: "{nome}",
            user_email: "{email}",
            materiale: "{materiale}",
            quantita: "{quantita}",
            location: "{location}",
            consegna: "{data_consegna}",
            ritiro: "{data_ritiro}",
            allegato: "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}"
        }};

        emailjs.send("{st.secrets['SERVICE_ID']}", "{st.secrets['TEMPLATE_ID']}", templateParams)
        .then(function(response) {{
            alert("✅ Ordine inviato con successo!");
        }}, function(error) {{
            alert("❌ Errore durante l'invio dell'ordine.");
            console.error("Errore EmailJS:", error);
        }});
    </script>
    """

    st.components.v1.html(js, height=0)
