import streamlit as st
import pandas as pd

def vista_participantes(sheet):
    st.subheader("Participantes")
    participantes = sheet.worksheet("Participantes").get_all_records()
    df = pd.DataFrame(participantes)
    opciones_tipos = sheet.worksheet("Opciones_Tipos").col_values(1)[1:]
    opciones_genero = sheet.worksheet("Opciones_Genero").col_values(1)[1:]

    st.dataframe(df, use_container_width=True)

    nombres = df["Nombre"].tolist()
    seleccionado = st.selectbox("Selecciona un participante para editar", ["Nuevo participante"] + nombres)

    if seleccionado == "Nuevo participante":
        nombre = st.text_input("Nombre")
        genero = st.selectbox("Género", ["Elige"] + opciones_genero)
        tipos = st.multiselect("Tipos", opciones_tipos, default=[])
        if st.button("Añadir participante"):
            nuevo = pd.DataFrame([{"Nombre": nombre, "Género": genero, "Tipos": ", ".join(tipos)}])
            df = pd.concat([df, nuevo], ignore_index=True)
            df = df.fillna("")
            sheet.worksheet("Participantes").clear()
            sheet.worksheet("Participantes").update([df.columns.values.tolist()] + df.values.tolist())
            st.success("Participante añadido correctamente.")
            st.rerun()
    else:
        fila = df[df["Nombre"] == seleccionado].iloc[0]
        nombre = st.text_input("Nombre", value=fila["Nombre"], disabled=True)
        genero = st.selectbox("Género", ["Elige"] + opciones_genero, index=(opciones_genero.index(fila.get("Género", "Elige")) + 1) if fila.get("Género") in opciones_genero else 0)
        tipos_raw = [t.strip() for t in fila.get("Tipos", "").split(",") if t.strip()]
        tipos_validos = [t for t in tipos_raw if t in opciones_tipos]
        tipos = st.multiselect("Tipos", opciones_tipos, default=tipos_validos)

        if st.button("Guardar cambios"):
            df.loc[df["Nombre"] == nombre, ["Género", "Tipos"]] = [[genero, ", ".join(tipos)]]
            df = df.fillna("")
            sheet.worksheet("Participantes").clear()
            sheet.worksheet("Participantes").update([df.columns.values.tolist()] + df.values.tolist())
            st.success("Cambios guardados correctamente.")
            st.rerun()

        if st.button("Eliminar participante"):
            df = df[df["Nombre"] != nombre].reset_index(drop=True)
            df = df.fillna("")
            sheet.worksheet("Participantes").clear()
            if not df.empty:
                sheet.worksheet("Participantes").update([df.columns.values.tolist()] + df.values.tolist())
            st.success("Participante eliminado correctamente.")
            st.rerun()
