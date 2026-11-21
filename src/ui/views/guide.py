import os
import streamlit as st
from src.config import STEP1_IMG_PATH, STEP2_IMG_PATH, STEP3_IMG_PATH
from src.ui.primitives import render_micro_card, render_step_bar, render_amber_callout

def render_guide_view() -> None:
    """Renders the step-by-step user guide view using Sky/Slate Studio components."""
    render_micro_card(
        title="Guía Operativa de la Estación",
        subtitle="Instrucciones paso a paso para la extracción de audio, video y conversión de medios",
        badge_text="MANUAL TÉCNICO",
        badge_variant="amber",
        icon="menu_book"
    )

    # Visual Step Progress Bar
    render_step_bar(
        steps=["1. Copiar Enlace", "2. Configurar Formato", "3. Extraer y Descargar"],
        active_index=1
    )

    st.markdown("---")
    
    # Step 1
    st.markdown("### Paso 1: Copiar y pegar el enlace de YouTube")
    st.write(
        "Abrí YouTube en tu navegador web o aplicación, copiá la URL completa del video "
        "y pegala directamente en el campo principal de la pantalla de inicio."
    )
    if os.path.exists(STEP1_IMG_PATH):
        st.image(STEP1_IMG_PATH, width="stretch")
        
    st.html("<div style='margin: 1.5rem 0;'></div>")
    
    # Step 2
    st.markdown("### Paso 2: Confirmar detalles y seleccionar el método")
    st.write(
        "Al ingresar un enlace válido, el motor de inspección cargará automáticamente la "
        "miniatura, título, canal y duración. Seleccioná si deseás extraer la pista de **Audio puro** "
        "(MP3 hasta 320 kbps, WAV sin pérdida, o M4A) o el **Video completo** (MP4 hasta 1080p)."
    )
    if os.path.exists(STEP2_IMG_PATH):
        st.image(STEP2_IMG_PATH, width="stretch")

    st.html("<div style='margin: 1.5rem 0;'></div>")

    # Step 3
    st.markdown("### Paso 3: Extracción y Descarga Local")
    st.write(
        "Presioná el botón **Iniciar Extracción**. El indicador en tiempo real reportará la "
        "tasa de transferencia y el tiempo estimado de descarga. Una vez finalizado, el archivo "
        "se integrará en tu biblioteca local de descargas."
    )
    if os.path.exists(STEP3_IMG_PATH):
        st.image(STEP3_IMG_PATH, width="stretch")

    st.html("<div style='margin: 1.5rem 0;'></div>")

    # Amber Operational Callout
    render_amber_callout(
        title="Puntos Clave y Recomendaciones Operativas",
        items=[
            "Para música y sets en vivo, seleccioná el formato MP3 a 320 kbps para conservar la mayor fidelidad acústica.",
            "Si requerís editar la pista en DAWs como Ableton o FL Studio, el formato WAV conserva muestras sin compresión.",
            "Todos los archivos generados residen exclusivamente en tu equipo en la carpeta 'downloads/' o 'converted_images/'.",
            "Podés utilizar el botón 'Abrir Carpeta' para ubicar tus descargas directamente en el Explorador de Windows o tu gestor de archivos."
        ],
        icon="lightbulb"
    )
