
import streamlit as st
import pandas as pd
from io import BytesIO
import base64

st.set_page_config(page_title="Ordine Materiali", layout="centered")

# ----------------- FORM ------------------
st.title("📦 Ordine Materiali")

with st.form("ordine_form"):
    nome = st.text_input("👤 Nome")
    email = st.text_input("📧 Email")
    materiale = st.text_input("📄 Materiale")
    quantita = st.number_input("🔢 Quantità", min_value=1)
    location = st.text_input("📍 Location")
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

    # Salva in memoria come Excel
    buffer = BytesIO()
    ordine.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    # Codifica il file per invio via JS (Base64)
    b64_excel = base64.b64encode(buffer.read()).decode()

    # Script JS per invio con EmailJS
    js = f"""
    <script type="text/javascript">
        function sendEmail() {{
            emailjs.init("{st.secrets['PUBLIC_KEY']}");

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
                console.error(error);
            }});
        }}

        sendEmail();
    </script>
    """

    st.components.v1.html(js, height=0)
