import supabase as sb
from supabase import create_client, client
import streamlit as st
import uuid

url = st.secrets["URL"]
key = st.secrets["KEY"]

supabase: client = create_client(url, key)

opcion = st.radio(
    "Que quieres: ",
    ["añadir recetas","ver recetas"]
)

if opcion == "añadir recetas":
    
    nombre = st.text_input("Nombre de la receta")
    
    tipo = st.radio(
        "Como es:",
        ["vegano","vegetariano","carne","pescado"]
    )
    
    estacion = st.radio(
        "De que estacion es:",
        ["invierno","verano"]
    )

    imagen = st.file_uploader("Sube una imagen (opcional)", type=["png","jpg","jpeg"])

    if st.button("Añadir receta"):
        
        url_imagen = None

        if imagen is not None:
            nombre_archivo = f"{uuid.uuid4()}.png"

            supabase.storage.from_("imagenes").upload(
                nombre_archivo,
                imagen.read()
            )

            url_imagen = supabase.storage.from_("imagenes").get_public_url(nombre_archivo)

        datos = {
            "nombre": nombre,
            "tipo": tipo,
            "estacion": estacion
        }

        if url_imagen:
            datos["imagen"] = url_imagen
        #st.write("DATOS:", datos)

        try:
            res = supabase.table("recetas").insert(datos).execute()
            st.success("Receta añadida")
            #st.write(res)
        except Exception as e:
            st.error("ERROR:")
            st.write(e)


if opcion == "ver recetas":
    
    col_filtros, col_recetas = st.columns([1, 4])

    # FILTROS
    with col_filtros:
        st.markdown("### Filtros")

        filtro_estacion = st.radio(
            "Estación",
            ["todas", "invierno", "verano"]
        )

        filtro_tipo = st.radio(
            "Tipo",
            ["todos", "vegano", "vegetariano","carne","pescado"]
        )

    # RECETAS
    with col_recetas:
        st.title("Recetas")

        data = supabase.table('recetas').select("*").execute()
        recetas = data.data

        # FILTROS
        if filtro_estacion != "todas":
            recetas = [r for r in recetas if r["estacion"] == filtro_estacion]

        if filtro_tipo != "todos":
            recetas = [r for r in recetas if r["tipo"] == filtro_tipo]

        cols = st.columns(2)

        for i, receta in enumerate(recetas):
            col = cols[i % 2]

            with col:
                # CAJA (card)
                with st.container(border=True):
                    st.subheader(receta["nombre"])
                    st.write(f"{receta['tipo']}")
                    st.write(f"{receta['estacion']}")

                    if receta["imagen"]:
                        st.image(receta["imagen"], use_container_width=True)
                    else:
                        st.write("Sin imagen")