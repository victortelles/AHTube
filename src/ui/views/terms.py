import streamlit as st

def render_terms_view() -> None:
    """Renders the Terms of Use, Rules, and Legal Disclaimer view."""
    st.header("⚖️ Normas, Alcances y Términos de Uso")
    st.write("Consulta las reglas de uso, alcances permitidos y limitaciones legales de AHTube.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Lo que SÍ se puede hacer")
        st.markdown("""
        • **Uso Ilimitado y Local**: Ejecutar la herramienta en tu equipo sin publicidad, acortadores ni límites de uso.
        • **Respaldo Personal**: Descargar audios y videos para uso personal, educativo o de dominio público.
        • **Formatos y Calidad**: Extraer en MP3 (hasta 320 kbps), WAV, M4A y video MP4 en máxima resolución nativa.
        • **Reproducción y Gestión**: Escuchar/mirar el contenido dentro de la app y abrir la carpeta `downloads/` en primer plano.
        """)

    with col2:
        st.markdown("### ❌ Lo que NO se puede hacer")
        st.markdown("""
        • **Contenido Protegido por DRM**: No es posible descargar películas pagas, directos protegidos o YouTube Primetime.
        • **Bypass Geográfico Extremas**: No evade bloqueos regionales estrictos impuestos por la plataforma sin una VPN local.
        • **Redistribución Comercial**: No se permite utilizar esta herramienta para la redistribución comercial no autorizada de material con derechos de autor.
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Legal Disclaimer Card
    st.markdown('<div class="preview-card">', unsafe_allow_html=True)
    st.markdown("### 🛡️ Descargo de Responsabilidad Legal")
    st.warning("""
    **Aviso Importante para el Usuario**:
    1. **Uso Estrictamente Personal**: AHTube ha sido desarrollado como una herramienta técnica de investigación y uso personal.
    2. **Exención Total de Responsabilidad del Creador**: El desarrollador/autor de este proyecto **NO se hace responsable** del uso indebido, descargas no autorizadas ni violaciones a derechos de autor realizadas por otros usuarios.
    3. **Cumplimiento Legal**: Es responsabilidad única y exclusiva del usuario final asegurarse de que el uso de este software cumpla con los Términos de Servicio de YouTube y la legislación sobre propiedad intelectual de su país.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
