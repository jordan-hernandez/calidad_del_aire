import streamlit as st
import pandas as pd

def main():
    # Coordenadas de ejemplo
    latitude = 6.19987
    longitude = -75.560951

    # Título HTML personalizado con CSS para centrarlo
    title_html = f"""
    <div style="position:relative; text-align:center;">
        <h1 style="position:relative; color:#2a7fff;">Ubicación de ejemplo</h1>
    </div>
    """

    # Añadir el título HTML al diseño
    st.markdown(title_html, unsafe_allow_html=True)

    # Crear un DataFrame con las coordenadas
    data = pd.DataFrame({"LATITUDE": [latitude], "LONGITUDE": [longitude]})

    # Añadir el mapa al diseño
    st.map(data)

if __name__ == "__main__":
    main()

