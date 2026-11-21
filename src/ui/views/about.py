import streamlit as st
from src.ui.primitives import render_micro_card, render_amber_callout

def render_about_view() -> None:
    """Renders the plain-language technical architecture explanation and legal disclaimer view."""
    render_micro_card(
        title="Arquitectura y Flujo del Motor",
        subtitle="Mapeo técnico de las etapas de inspección, separación de flujos DASH, decodificación FFmpeg y persistencia local",
        badge_text="DAW PIPELINE",
        badge_variant="audio",
        icon="memory"
    )

    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.html(
            """
            <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.15rem;margin-bottom:1rem;">
                <div style="font-size:1.02rem;font-weight:700;color:var(--primary);margin-bottom:0.5rem;display:flex;align-items:center;gap:0.4rem;">
                    <span class="material-symbols-rounded">search</span>
                    1. Inspección e Ingesta de Metadatos
                </div>
                <div style="font-size:0.88rem;color:var(--foreground);line-height:1.6;">
                    Al ingresar la URL del video, el backend invoca el motor <code>yt-dlp</code> para consultar
                    las tablas de flujos multimedia directamente desde la API interna sin transferir el archivo completo.
                    Esto reporta de inmediato el título, miniatura de alta resolución, duración y formatos disponibles.
                </div>
            </div>
            """
        )
        
        st.html(
            """
            <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.15rem;margin-bottom:1rem;">
                <div style="font-size:1.02rem;font-weight:700;color:var(--primary);margin-bottom:0.5rem;display:flex;align-items:center;gap:0.4rem;">
                    <span class="material-symbols-rounded">tune</span>
                    3. Decodificación y Recodificación FFmpeg
                </div>
                <div style="font-size:0.88rem;color:var(--foreground);line-height:1.6;">
                    El flujo binario es procesado a través de <code>FFmpeg</code>. El motor decodifica las muestras
                    de audio y las recodifica con parámetros de calidad seleccionados (como MP3 a 320 kbps o WAV PCM lineal a 44.1/48 kHz),
                    asegurando rango dinámico y preservación acústica para monitoreo o producción en DAW.
                </div>
            </div>
            """
        )

    with col_f2:
        st.html(
            """
            <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.15rem;margin-bottom:1rem;">
                <div style="font-size:1.02rem;font-weight:700;color:var(--accent);margin-bottom:0.5rem;display:flex;align-items:center;gap:0.4rem;">
                    <span class="material-symbols-rounded">call_split</span>
                    2. Aislamiento de Flujos DASH
                </div>
                <div style="font-size:0.88rem;color:var(--foreground);line-height:1.6;">
                    YouTube almacena las transmisiones mediante el estándar DASH, disociando video y audio.
                    Al solicitar una extracción sonora, AHTube descarga únicamente los paquetes de la pista de audio
                    (Opus o AAC), omitiendo el canal de video para reducir el consumo de ancho de banda y maximizar la velocidad.
                </div>
            </div>
            """
        )
        
        st.html(
            """
            <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.15rem;margin-bottom:1rem;">
                <div style="font-size:1.02rem;font-weight:700;color:var(--accent);margin-bottom:0.5rem;display:flex;align-items:center;gap:0.4rem;">
                    <span class="material-symbols-rounded">folder_zip</span>
                    4. Persistencia Local e Interfaz
                </div>
                <div style="font-size:0.88rem;color:var(--foreground);line-height:1.6;">
                    Los archivos resultantes se persisten de forma segura en las carpetas locales <code>downloads/</code>
                    o <code>converted_images/</code>. La interfaz de Streamlit indexa los metadatos y ofrece reproducción
                    inmediata, además de integración con el Explorador del sistema operativo.
                </div>
            </div>
            """
        )
        
    st.html("<div style='margin: 1rem 0;'></div>")
    
    # Amber Legal Notice
    render_amber_callout(
        title="Marco Legal y Aviso de Responsabilidad",
        items=[
            "Uso Estrictamente Personal y Educativo: AHTube ha sido desarrollado con propósitos educativos y de investigación sobre flujos multimedia.",
            "Exención de Responsabilidad: El autor no se responsabiliza por descargas indebidas de contenido protegido con copyright ni por el uso que terceros den a los archivos generados.",
            "Responsabilidad del Usuario: Es obligación del usuario respetar los Términos de Servicio de los proveedores de contenido y las leyes de propiedad intelectual correspondientes."
        ],
        icon="policy"
    )
