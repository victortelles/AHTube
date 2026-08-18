import streamlit as st

def render_about_view() -> None:
    """Renders the plain-language technical architecture explanation view."""
    st.header("⚙️ ¿Cómo funciona AHTube por detrás?")
    st.write("Te explicamos de manera sencilla la arquitectura y el proceso técnico que ocurre en segundo plano cada vez que realizás una extracción.")
    
    st.markdown("---")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("""
        ### 1. Inspección e Información (API / Meta-Data)
        Cuando pegás la URL, el backend utiliza **`yt-dlp`** para conectarse con YouTube y consultar los metadatos del video sin descargar el archivo entero. 
        Esto nos permite obtener el título, duración, miniatura y los flujos (streams) de audio/video disponibles casi al instante.
        """)
        
        st.markdown("""
        ### 3. Procesamiento y Conversión con FFmpeg
        Una vez obtenido el flujo directo, entra en acción **FFmpeg** (un potente motor multimedia industrial).
        FFmpeg decodifica el flujo comprimido y lo recodifica en el formato solicitado (como MP3 a 320 kbps o 192 kbps), optimizando la compresión sin degradar la fidelidad sonora.
        """)

    with col_f2:
        st.markdown("""
        ### 2. Separación de Flujos de Audio y Video
        YouTube almacena por separado la pista de video y la pista de audio (tecnología *DASH*).
        Si solicitás **Audio**, nuestra herramienta descarga únicamente la pista sonora nativa (Opus o AAC), evitando descargar gigabytes de video innecesarios para máxima velocidad.
        """)
        
        st.markdown("""
        ### 4. Entrega y Almacenamiento Seguro
        El archivo generado se almacena en la carpeta local `downloads/` del servidor y simultáneamente se transfiere como un flujo de datos binario seguro al navegador para tu descarga directa.
        """)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🔒 **Seguridad y Privacidad**: Toda la conversión se procesa localmente en tu sistema sin almacenar copias en servidores de terceros ni enviar información personal.")
