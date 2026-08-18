import streamlit as st
from src.config import APP_NAME, CUSTOM_CSS
from src.ui.components import render_header, render_sidebar
from src.ui.views.home import render_home_view
from src.ui.views.guide import render_guide_view
from src.ui.views.terms import render_terms_view
from src.ui.views.about import render_about_view

# Streamlit Page Setup
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Apply Custom Theme CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def main():
    nav_option = render_sidebar()
    render_header()
    
    if nav_option == "🏠 Inicio":
        render_home_view()
    elif nav_option == "📖 Cómo usarlo":
        render_guide_view()
    elif nav_option == "⚖️ Normas y Términos":
        render_terms_view()
    elif nav_option == "⚙️ ¿Cómo funciona por detrás?":
        render_about_view()

if __name__ == "__main__":
    main()
