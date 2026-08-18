import os
import streamlit as st
from src.config import STEP1_IMG_PATH, STEP2_IMG_PATH, STEP3_IMG_PATH

def render_guide_view() -> None:
    """Renders the step-by-step user guide view."""
    st.header("Guía Paso a Paso: ¿Cómo usar la aplicación?")
    st.write("Sigue estas sencillas indicaciones para extraer cualquier audio o video de YouTube en segundos.")
    
    st.markdown("---")
    
    st.subheader("Paso 1: Copiar y pegar el enlace de YouTube")
    st.write("Abrí YouTube en tu navegador o aplicación, copiá el enlace completo del video que deseas descargar y pégalo en el campo principal de entrada.")
    if os.path.exists(STEP1_IMG_PATH):
        st.image(STEP1_IMG_PATH, width="stretch")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Paso 2: Confirmar detalles y seleccionar el método")
    st.write("Al pegar un enlace válido, la aplicación cargará una vista previa con el título y duración. Elegí si querés extraer únicamente el **Audio** (MP3/WAV/M4A) o el **Video completo** (MP4), ajustando la calidad según tus necesidades.")
    if os.path.exists(STEP2_IMG_PATH):
        st.image(STEP2_IMG_PATH, width="stretch")

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Paso 3: Extracción y Descarga")
    st.write("Hacé clic en el botón **Iniciar Extracción**. Podrás visualizar la velocidad y porcentaje en tiempo real. Al finalizar, el archivo aparecerá automáticamente en tu carpeta de descargas.")
    if os.path.exists(STEP3_IMG_PATH):
        st.image(STEP3_IMG_PATH, width="stretch")

    st.markdown("---")
    st.info("Tip: También podés acceder a la sección '¿Cómo funciona por detrás?' en el menú lateral para conocer los aspectos técnicos de la herramienta.")
