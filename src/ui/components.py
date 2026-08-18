import os
import streamlit as st
from src.config import APP_NAME, APP_SUBTITLE, LOGO_ALPHA_PATH

def render_header() -> None:
    """Renders the top branding header banner."""
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if os.path.exists(LOGO_ALPHA_PATH):
            st.image(LOGO_ALPHA_PATH, width=100)
    with col_title:
        st.markdown(f'<div class="main-title">{APP_NAME}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-title">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

def render_sidebar() -> str:
    """Renders the simplified sidebar navigation and branding."""
    with st.sidebar:
        if os.path.exists(LOGO_ALPHA_PATH):
            st.image(LOGO_ALPHA_PATH, width="stretch")
        st.title(APP_NAME)
        st.markdown("---")
        
        nav_option = st.radio(
            "Navegación / Secciones",
            [
                "🏠 Inicio",
                "📖 Cómo usarlo",
                "⚖️ Normas y Términos",
                "⚙️ ¿Cómo funciona por detrás?"
            ],
            index=0
        )
        
        st.markdown("---")
        st.caption("AHTube © 2026 | Extractor Local")
        
        return nav_option

def render_preview_card(meta: dict) -> None:
    """Renders video metadata preview card."""
    with st.container():
        st.markdown('<div class="preview-card">', unsafe_allow_html=True)
        col_thumb, col_info = st.columns([1, 2])
        with col_thumb:
            if meta.get('thumbnail'):
                st.image(meta['thumbnail'], width="stretch")
        with col_info:
            st.subheader(meta.get('title'))
            st.write(f"👤 **Canal:** {meta.get('uploader')}")
            dur_min = meta.get('duration', 0) // 60
            dur_sec = meta.get('duration', 0) % 60
            st.write(f"⏱️ **Duración:** {dur_min}m {dur_sec}s")
        st.markdown('</div>', unsafe_allow_html=True)
