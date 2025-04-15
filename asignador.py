import streamlit as st
import pandas as pd
import random

def vista_asignador(sheet):
    st.subheader("Asignador Automático")
    try:
        participantes = pd.DataFrame(sheet.worksheet("Participantes").get_all_records())
        df_part = pd.DataFrame(sheet.worksheet("Participaciones_Disponibles").get_all_records())

        df_part["Fecha"] = pd.to_datetime(df_part["Fecha"], errors="coerce")
        fechas_disponibles = df_part["Fecha"].dropna().sort_values().unique()

        if len(fechas_disponibles) == 0:
            st.warning("No hay fechas disponibles.")
            return

        fecha_inicio = st.date_input("Desde", value=min(fechas_disponibles))
        fecha_fin = st.date_input("Hasta", value=max(fechas_disponibles))

        if st.button("Asignar automáticamente"):
            periodo = df_part[(df_part["Fecha"] >= pd.to_datetime(fecha_inicio)) & (df_part["Fecha"] <= pd.to_datetime(fecha_fin))].copy()
            participantes = participantes.copy()
            participantes["Tipos"] = participantes["Tipos"].fillna("")
            participantes["Género"] = participantes["Género"].fillna("")

            asignaciones = []
            for _, row in periodo.iterrows():
                posibles = participantes[participantes["Tipos"].str.contains(row["Tipo"], na=False)]
                if row.get("Género") and row["Género"] != "Elige":
                    posibles = posibles[posibles["Género"] == row["Género"]]
                if not posibles.empty:
                    asignado = random.choice(posibles["Nombre"].tolist())
                else:
                    asignado = ""
                asignaciones.append(asignado)

            periodo["Asignado"] = asignaciones
            st.dataframe(periodo, use_container_width=True)

    except:
        st.warning("No se pudo cargar la hoja de participaciones o participantes.")
