import streamlit as st
from src.ui.primitives import render_micro_card, render_amber_callout

def render_terms_view() -> None:
    """Renders the Terms of Use, Scope, and Legal Disclaimer view."""
    render_micro_card(
        title="Normas, Alcances y Términos de Uso",
        subtitle="Reglas operativas, capacidades del motor local y marco de responsabilidad legal",
        badge_text="COMPLIANCE",
        badge_variant="amber",
        icon="gavel"
    )

    col1, col2 = st.columns(2)
    
    with col1:
        st.html(
            """
            <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.15rem;height:100%;">
                <div style="font-size:1.05rem;font-weight:700;color:#10b981;margin-bottom:0.75rem;display:flex;align-items:center;gap:0.4rem;">
                    <span class="material-symbols-rounded">check_circle</span>
                    Acciones y Usos Permitidos
                </div>
                <ul style="color:var(--foreground);font-size:0.88rem;line-height:1.6;padding-left:1.2rem;margin:0;">
                    <li><strong>Procesamiento 100% Local:</strong> Ejecución ilimitada en tu máquina, sin telemetría ni publicidad invasiva.</li>
                    <li><strong>Respaldo y Archivo Personal:</strong> Descarga de pistas sonoras o videos para fines educativos, investigación y material bajo dominio público o Creative Commons.</li>
                    <li><strong>Fidelidad y Formatos:</strong> Extracción en MP3 hasta 320 kbps, WAV sin pérdidas, M4A y video MP4 hasta resolución nativa disponible.</li>
                    <li><strong>Conversión de Imágenes:</strong> Transformación ilimitada por lotes entre formatos modernos (.heic, .webp, .png, .jpg, .ico, .pdf).</li>
                </ul>
            </div>
            """
        )

    with col2:
        st.html(
            """
            <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.15rem;height:100%;">
                <div style="font-size:1.05rem;font-weight:700;color:#ef4444;margin-bottom:0.75rem;display:flex;align-items:center;gap:0.4rem;">
                    <span class="material-symbols-rounded">cancel</span>
                    Restricciones Técnicas y Legales
                </div>
                <ul style="color:var(--foreground);font-size:0.88rem;line-height:1.6;padding-left:1.2rem;margin:0;">
                    <li><strong>Protección DRM Estricta:</strong> La herramienta no vulnera ni descarga contenidos con cifrado DRM comercial (películas de pago o YouTube Primetime).</li>
                    <li><strong>Bypass de Restricciones Geográficas:</strong> No evade bloqueos regionales estrictos impuestos a nivel de red sin un proxy o VPN local.</li>
                    <li><strong>Redistribución Comercial:</strong> Queda prohibido lucrar o comercializar de forma ilegítima material sujeto a derechos de autor descargado mediante este software.</li>
                </ul>
            </div>
            """
        )

    st.html("<div style='margin: 1.5rem 0;'></div>")
    
    # Legal Disclaimer Card with Amber Styling
    render_amber_callout(
        title="Descargo de Responsabilidad Legal y Notificación al Usuario",
        items=[
            "Uso Estrictamente Personal y Educativo: AHTube Studio ha sido desarrollado como una herramienta técnica de investigación y gestión multimedia local.",
            "Exención Total de Responsabilidad del Creador: El autor y desarrollador de este proyecto NO asume responsabilidad alguna por el mal uso, infracciones de propiedad intelectual o descargas no autorizadas realizadas por terceros.",
            "Cumplimiento Normativo Obligatorio: Es obligación y responsabilidad exclusiva del usuario final certificar que sus actividades se apegan a los Términos de Servicio de YouTube y a la legislación de propiedad intelectual aplicable en su jurisdicción."
        ],
        icon="shield"
    )
