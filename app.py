import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import random
from participantes import vista_participantes
from participaciones import vista_participaciones
from calendario import vista_calendario
from asignador import vista_asignador
from opciones import vista_configuracion

@st.cache_resource
def conectar_google_sheets():
    import json
    from google.oauth2.service_account import Credentials

    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    sheet = client.open("asignador_dbs")
    return sheet

def cargar_participantes(sheet):
    worksheet = sheet.worksheet("Participantes")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def cargar_opciones(sheet, hoja):
    worksheet = sheet.worksheet(hoja)
    data = worksheet.col_values(1)
    return [op for op in data if op.strip() and op.lower() != hoja.lower()]

def guardar_participantes(sheet, df):
    df = df.fillna("")
    worksheet = sheet.worksheet("Participantes")
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def guardar_opciones(sheet, hoja, lista):
    worksheet = sheet.worksheet(hoja)
    worksheet.clear()
    valores = [[valor] for valor in lista if valor.strip()]
    worksheet.update([[hoja]] + valores)

def main():
    st.set_page_config(page_title="Gestor de Participaciones", layout="wide")
    st.title("Gestor de Participaciones")

    menu = st.sidebar.radio("Menú", [
        "Asignador Automático",
        "Calendario",
        "Gestión de Participantes",
        "Gestión de Participaciones",
        "Historial de Participaciones",
        "Configuración del Asignador"
    ])

    sheet = conectar_google_sheets()

    if menu == "Gestión de Participantes":
        vista_participantes(sheet)
    elif menu == "Gestión de Participaciones":
        vista_participaciones(sheet)
    elif menu == "Calendario":
        vista_calendario(sheet)
    elif menu == "Asignador Automático":
        vista_asignador(sheet)
    elif menu == "Configuración del Asignador":
        vista_configuracion(sheet)
    elif menu == "Historial de Participaciones":
        st.info("Esta sección estará disponible próximamente.")

if __name__ == "__main__":
    main()
