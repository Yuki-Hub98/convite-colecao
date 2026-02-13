import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheets
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "formatura-amor-1-6aa6a56574ce.json",
    scopes=scopes
)

client = gspread.authorize(creds)
SPREADSHEET_ID = "1DPmHq2y10ei_S0t4bAxWNKZeNhOTb9hEKBBskuVjZyM"
SHEET = client.open_by_key(SPREADSHEET_ID).worksheet("Página1")

st.set_page_config(page_title="Convite", layout="centered")

# Exibe HTML apenas como layout
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

st.components.v1.html(
    html,
    height=900,
    scrolling=False
)

st.markdown("""
<style>
.label {
    font-size: 18px;
    font-weight: bold;
    color: #ffd700;
    margin-bottom: 8px;
    display: block;
}

.big-input input {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: 2px solid #ffd700;
    font-size: 16px;
    color: #16213e;
    margin-bottom: 15px;
}

.big-button button {
    width: 100%;
    padding: 14px;
    background: #ffd700;
    border:none;
    border-radius: 12px;
    font-weight:bold;
    font-size:16px;
    cursor:pointer;
    color:#16213e;
    transition: all 0.3s ease;
}

.big-button button:hover {
    background: #ffed4e;
    transform: scale(1.05);
    color:#16213e;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Label + Input
# -------------------------------
st.markdown('<label class="label" for="nome_input">Digite seu nome para confirmar</label>', unsafe_allow_html=True)
nome = st.text_input("Nome", placeholder="Seu nome", key="nome_input", label_visibility="collapsed")

# -------------------------------
# Botão estilizado
# -------------------------------
if st.button("Enviar"):
    if nome.strip():
        # Descobre a próxima linha vazia, começando na linha 2
        all_values = SHEET.get_all_values()
        next_row = max(len(all_values) + 1, 2)  # sempre começa da linha 2
        SHEET.update(f"A{next_row}:B{next_row}", [[nome, datetime.now().strftime("%d/%m/%Y %H:%M:%S")]])
        st.success(f"🎉 Presença de **{nome}** confirmada!")
    else:
        st.warning("Digite um nome válido 🙂")
