import streamlit as st
import pandas as pd

def vista_calendario(sheet):
    st.subheader("Calendario de Participaciones")
    try:
        df_cal = pd.DataFrame(sheet.worksheet("Participaciones_Disponibles").get_all_records())
        if not df_cal.empty:
            df_cal["Fecha"] = pd.to_datetime(df_cal["Fecha"], errors="coerce")
            eventos = df_cal.groupby("Fecha").apply(
                lambda x: "\n".join(
                    f"{row['Tipo']} ({row['Sala']}) Nº{row['Número']}" for _, row in x.iterrows()
                )
            ).reset_index()
            eventos.columns = ["Fecha", "Eventos"]
            st.dataframe(eventos, use_container_width=True)
        else:
            st.info("No hay participaciones registradas todavía.")
    except:
        st.info("No se pudo cargar el calendario. ¿Existe la hoja 'Participaciones_Disponibles'?")