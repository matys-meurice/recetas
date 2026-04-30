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
        ["vegano","vegetariano","omnivoro"]
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
                imagen.getvalue()
            )
            
            url_imagen = supabase.storage.from_("imagenes").get_public_url(nombre_archivo)

        supabase.table('todos').insert({
            'nombre': nombre,
            'tipo': tipo,
            'estacion': estacion,
            'imagen': url_imagen
        }).execute()



if opcion == "ver recetas":
    st.title("Recetas")

    filtro_estacion = st.radio(
        "Filtrar por estación",
        ["todas", "invierno", "verano"]
    )

    filtro_tipo = st.radio(
        "Filtrar por tipo",
        ["todos", "vegano", "vegetariano", "omnivoro"]
    )
    data = supabase.table('todos').select("*").execute()
    recetas = data.data

    # FILTRO ESTACIÓN
    if filtro_estacion != "todas":
        recetas = [r for r in recetas if r["estacion"] == filtro_estacion]

    # FILTRO TIPO
    if filtro_tipo != "todos":
        recetas = [r for r in recetas if r["tipo"] == filtro_tipo]
    
    cols = st.columns(3)

    for i, receta in enumerate(recetas):
        col = cols[i % 3]

        with col:
            st.subheader(receta["nombre"])
            st.write(f"{receta['tipo']}")
            st.write(f"{receta['estacion']}")

            if receta["imagen"]:
                st.image(receta["imagen"], use_container_width=True)