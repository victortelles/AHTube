import os
import streamlit as st
from streamlit_option_menu import option_menu
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
    """Renders sidebar navigation using streamlit-option-menu with Bootstrap icons."""
    with st.sidebar:
        if os.path.exists(LOGO_ALPHA_PATH):
            st.image(LOGO_ALPHA_PATH, width="stretch")
        st.title(APP_NAME)
        st.markdown("---")
        
        selected_option = option_menu(
            menu_title="Navegación",
            options=["Inicio", "Cómo usarlo", "Normas y Términos", "¿Cómo funciona por detrás?"],
            icons=["house", "book-half", "shield-check", "gear"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#60A5FA", "font-size": "1rem"},
                "nav-link": {
                    "font-size": "0.95rem",
                    "text-align": "left",
                    "margin": "4px 0",
                    "color": "#94A3B8",
                    "border-radius": "8px"
                },
                "nav-link-selected": {
                    "background-color": "#1E293B",
                    "color": "#60A5FA",
                    "font-weight": "600",
                    "border-left": "4px solid #3B82F6"
                },
            }
        )
        
        st.markdown("---")
        st.caption("AHTube © 2026 | Extractor Local")
        
        return selected_option

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
            st.write(f"**Canal:** {meta.get('uploader')}")
            dur_min = meta.get('duration', 0) // 60
            dur_sec = meta.get('duration', 0) % 60
            st.write(f"**Duración:** {dur_min}m {dur_sec}s")
        st.markdown('</div>', unsafe_allow_html=True)
