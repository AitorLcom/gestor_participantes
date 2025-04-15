import streamlit as st
import pandas as pd

def vista_configuracion(sheet):
    st.subheader("Configuración del Asignador")
    opciones_tipos = sheet.worksheet("Opciones_Tipos").col_values(1)[1:]
    opciones_genero = sheet.worksheet("Opciones_Genero").col_values(1)[1:]

    st.markdown("**Opciones para el campo 'Tipos'**")
    tipos_editables = st.data_editor(pd.DataFrame(opciones_tipos, columns=["Tipos"], dtype=str), num_rows="dynamic")
    if st.button("Guardar opciones de 'Tipos'"):
        valores = [[v] for v in tipos_editables["Tipos"].tolist() if v.strip()]
        sheet.worksheet("Opciones_Tipos").clear()
        sheet.worksheet("Opciones_Tipos").update([["Opciones_Tipos"]] + valores)
        st.success("Opciones actualizadas correctamente.")

    st.markdown("**Opciones para el campo 'Género'**")
    genero_editables = st.data_editor(pd.DataFrame(opciones_genero, columns=["Género"], dtype=str), num_rows="dynamic")
    if st.button("Guardar opciones de 'Género'"):
        valores = [[v] for v in genero_editables["Género"].tolist() if v.strip()]
        sheet.worksheet("Opciones_Genero").clear()
        sheet.worksheet("Opciones_Genero").update([["Opciones_Genero"]] + valores)
        st.success("Opciones actualizadas correctamente.")