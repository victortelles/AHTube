import os
import html
import streamlit as st
from streamlit_option_menu import option_menu
from src.config import APP_NAME, APP_SUBTITLE, LOGO_ALPHA_PATH
from src.ui.primitives import get_badge_html

def render_header() -> None:
    """Renders the top branding header banner with Sky / Slate Studio aesthetic."""
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        if os.path.exists(LOGO_ALPHA_PATH):
            st.image(LOGO_ALPHA_PATH, width=90)
    with col_title:
        title_html = f"""
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.2rem;">
            <span style="font-size:2rem;font-weight:800;color:var(--foreground);letter-spacing:-0.03em;">{APP_NAME}</span>
            <span class="dad-badge dad-badge-audio" style="font-size:0.7rem;">STUDIO EDITION</span>
        </div>
        <div style="color:var(--muted-foreground);font-size:0.92rem;font-weight:400;">{APP_SUBTITLE}</div>
        """
        st.html(title_html)

    st.html("<div style='margin-bottom: 1.25rem;'></div>")

def render_sidebar() -> str:
    """Renders sidebar navigation using streamlit-option-menu with Sky/Slate Studio theme."""
    with st.sidebar:
        if os.path.exists(LOGO_ALPHA_PATH):
            st.image(LOGO_ALPHA_PATH, width="stretch")
        
        st.html(
            f'<div style="font-size:1.4rem;font-weight:700;color:var(--foreground);margin-top:0.5rem;">{APP_NAME}</div>'
            '<div style="font-size:0.8rem;color:var(--muted-foreground);margin-bottom:0.75rem;">Digital Audio & Video Station</div>'
        )
        st.markdown("---")
        
        selected_option = option_menu(
            menu_title="Navegación",
            options=[
                "Inicio",
                "Conversor de Imágenes",
                "Cómo usarlo",
                "Normas y Términos",
                "¿Cómo funciona por detrás?"
            ],
            icons=["house", "images", "book-half", "shield-check", "gear"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#38bdf8", "font-size": "1rem"},
                "nav-link": {
                    "font-size": "0.9rem",
                    "text-align": "left",
                    "margin": "4px 0",
                    "color": "#94a3b8",
                    "border-radius": "8px",
                    "padding": "7px 12px",
                },
                "nav-link-selected": {
                    "background-color": "#1e293b",
                    "color": "#38bdf8",
                    "font-weight": "600",
                    "border-left": "4px solid #38bdf8",
                },
            }
        )
        
        st.markdown("---")
        
        # System status badge in sidebar footer
        st.html(
            """
            <div style="background:var(--secondary);border:1px solid var(--border);border-radius:var(--radius);padding:0.65rem 0.85rem;margin-bottom:0.75rem;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.25rem;">
                    <span style="font-size:0.75rem;color:var(--muted-foreground);font-weight:600;">ESTADO MOTOR</span>
                    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;box-shadow:0 0 6px #10b981;"></span>
                </div>
                <div style="font-size:0.8rem;color:var(--foreground);font-family:var(--font-mono);font-variant-numeric:tabular-nums;">
                    FFmpeg & yt-dlp OK
                </div>
            </div>
            """
        )
        st.caption("AHTube Studio © 2026 | Procesamiento Local")
        
        return selected_option

def render_preview_card(meta: dict) -> None:
    """Renders video metadata preview card with DAW audio-workstation aesthetic."""
    title = meta.get('title', 'Sin título')
    uploader = meta.get('uploader', 'Desconocido')
    duration = meta.get('duration', 0)
    view_count = meta.get('view_count', 0)
    thumbnail = meta.get('thumbnail', '')
    
    dur_min = duration // 60
    dur_sec = duration % 60
    duration_str = f"{dur_min:02d}:{dur_sec:02d}"
    
    views_str = f"{view_count:,}".replace(",", ".") if view_count else "N/A"
    
    badge_dur = get_badge_html(f"⏱ {duration_str}", variant="default")
    badge_views = get_badge_html(f"👁 {views_str} vistas", variant="default")
    
    card_html = f"""
    <div class="preview-card">
      <div style="display:flex;gap:1.25rem;flex-wrap:wrap;align-items:center;">
        <div style="flex:1;min-width:240px;max-width:320px;">
          <img src="{thumbnail}" style="width:100%;border-radius:calc(var(--radius) - 0.2rem);border:1px solid var(--border);object-fit:cover;" />
        </div>
        <div style="flex:2;min-width:260px;">
          <div style="margin-bottom:0.5rem;display:flex;gap:0.4rem;flex-wrap:wrap;">
            {badge_dur}
            {badge_views}
          </div>
          <div style="font-size:1.15rem;font-weight:700;color:var(--foreground);margin-bottom:0.35rem;line-height:1.35;">
            {html.escape(title)}
          </div>
          <div style="font-size:0.88rem;color:var(--muted-foreground);display:flex;align-items:center;gap:0.35rem;">
            <span class="material-symbols-rounded" style="font-size:1rem;color:var(--primary);">account_circle</span>
            <span>{html.escape(uploader)}</span>
          </div>
        </div>
      </div>
    </div>
    """
    st.html(card_html)
