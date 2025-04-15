import streamlit as st
import pandas as pd

def vista_participaciones(sheet):
    st.subheader("Añadir nuevas participaciones disponibles")
    opciones_tipos = sheet.worksheet("Opciones_Tipos").col_values(1)[1:]
    opciones_genero = sheet.worksheet("Opciones_Genero").col_values(1)[1:]

    with st.form("form_nuevas_participaciones"):
        numero = st.number_input("Número de asignación (0-9)", min_value=0, max_value=9, step=1)
        fecha = st.date_input("Fecha")
        tipo = st.selectbox("Tipo", opciones_tipos)
        sala = st.selectbox("Sala", ["A", "B"])
        genero_req = st.selectbox("Género requerido", ["Elige"] + opciones_genero)
        duplicar = st.checkbox("Añadir también para la otra sala", value=False)
        submitted = st.form_submit_button("Añadir participación")

        if submitted:
            filas = [{"Fecha": str(fecha), "Número": numero, "Tipo": tipo, "Sala": sala, "Género": genero_req}]
            if duplicar:
                otra_sala = "B" if sala == "A" else "A"
                filas.append({"Fecha": str(fecha), "Número": numero, "Tipo": tipo, "Sala": otra_sala, "Género": genero_req})
            nueva = pd.DataFrame(filas)

            try:
                worksheet = sheet.worksheet("Participaciones_Disponibles")
                datos_existentes = worksheet.get_all_records()
                df_existente = pd.DataFrame(datos_existentes)
                df_actualizado = pd.concat([df_existente, nueva], ignore_index=True)
            except:
                worksheet = sheet.add_worksheet(title="Participaciones_Disponibles", rows="100", cols="20")
                df_actualizado = nueva

            df_actualizado = df_actualizado.fillna("")
            worksheet.clear()
            worksheet.update([df_actualizado.columns.values.tolist()] + df_actualizado.values.tolist())
            st.success("Participación añadida correctamente.")

    st.markdown("---")
    try:
        worksheet = sheet.worksheet("Participaciones_Disponibles")
        datos_existentes = worksheet.get_all_records()
        df_part = pd.DataFrame(datos_existentes)
        st.subheader("Editar o eliminar participación")
        if not df_part.empty:
            seleccion = st.selectbox("Selecciona una participación", df_part.apply(lambda row: f"{row['Fecha']} - Tipo {row['Tipo']} ({row['Sala']}) Nº{row['Número']}", axis=1))
            idx = df_part.index[df_part.apply(lambda row: f"{row['Fecha']} - Tipo {row['Tipo']} ({row['Sala']}) Nº{row['Número']}" == seleccion, axis=1)][0]

            fecha_edit = st.date_input("Fecha", pd.to_datetime(df_part.at[idx, "Fecha"], errors="coerce"))
            numero_edit = st.number_input("Número de asignación (0-9)", min_value=0, max_value=9, step=1, value=int(df_part.at[idx, "Número"]))
            tipo_edit = st.selectbox("Tipo", opciones_tipos, index=opciones_tipos.index(df_part.at[idx, "Tipo"]) if df_part.at[idx, "Tipo"] in opciones_tipos else 0)
            sala_edit = st.selectbox("Sala", ["A", "B"], index=["A", "B"].index(df_part.at[idx, "Sala"]))
            genero_edit = st.selectbox("Género requerido", ["Elige"] + opciones_genero, index=(opciones_genero.index(df_part.at[idx, "Género"]) + 1) if df_part.at[idx, "Género"] in opciones_genero else 0)

            if st.button("Guardar cambios en participación"):
                df_part.at[idx, "Fecha"] = str(fecha_edit)
                df_part.at[idx, "Número"] = numero_edit
                df_part.at[idx, "Tipo"] = tipo_edit
                df_part.at[idx, "Sala"] = sala_edit
                df_part.at[idx, "Género"] = genero_edit
                df_part = df_part.fillna("")
                worksheet.clear()
                worksheet.update([df_part.columns.values.tolist()] + df_part.values.tolist())
                st.success("Participación actualizada.")
                st.rerun()

            if st.button("Eliminar participación"):
                df_part = df_part.drop(index=idx).reset_index(drop=True)
                worksheet.clear()
                if not df_part.empty:
                    worksheet.update([df_part.columns.values.tolist()] + df_part.values.tolist())
                st.success("Participación eliminada.")
                st.rerun()
        else:
            st.info("No hay participaciones para editar o eliminar.")
    except:
        st.info("Aún no hay participaciones disponibles registradas.")
