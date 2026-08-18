import os
import streamlit as st
from src.config import OUTPUT_DIR
from src.services.extractor import fetch_video_metadata, extract_media, list_downloaded_files
from src.services.explorer import open_folder_in_foreground
from src.ui.components import render_preview_card

def render_home_view() -> None:
    """Renders the main Home view: Extractor & Downloads Gallery."""
    url_input = st.text_input(
        "URL del video de YouTube:",
        placeholder="https://www.youtube.com/watch?v=..."
    ).strip()

    if url_input:
        if "youtube.com/" in url_input or "youtu.be/" in url_input:
            with st.spinner("Cargando detalles del video..."):
                meta = fetch_video_metadata(url_input)
            
            if meta:
                render_preview_card(meta)

            st.markdown("### Opciones de Extracción")
            
            mode_choice = st.radio(
                "Seleccioná el método de extracción:",
                ["Extraer Audio", "Extraer Video"],
                horizontal=True
            )

            col_opt1, col_opt2 = st.columns(2)

            if mode_choice == "Extraer Audio":
                mode = "audio"
                with col_opt1:
                    audio_format = st.selectbox(
                        "Formato de Audio:",
                        ["mp3", "wav", "m4a"],
                        format_func=lambda x: f".{x.upper()}"
                    )
                with col_opt2:
                    if audio_format == "mp3":
                        audio_quality = st.selectbox(
                            "Calidad de Bitrate:",
                            ["320", "192", "128"],
                            index=1,
                            format_func=lambda x: f"{x} kbps ({'Alta' if x=='320' else 'Estándar' if x=='192' else 'Ligera'})"
                        )
                    else:
                        audio_quality = "192"
                        st.info(f"Formato {audio_format.upper()} seleccionado.")
                video_res = "best"
            else:
                mode = "video"
                audio_format = "mp3"
                audio_quality = "192"
                with col_opt1:
                    video_res = st.selectbox(
                        "Resolución máxima de video:",
                        ["best", "1080", "720", "480"],
                        format_func=lambda x: "Máxima Calidad (Original)" if x == "best" else f"{x}p"
                    )
                with col_opt2:
                    st.info("Formato de salida: MP4")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Iniciar Extracción"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                def update_progress(percent, speed, eta):
                    progress_bar.progress(min(max(percent, 0.0), 1.0))
                    status_text.text(f"Descargando... {int(percent * 100)}% | Velocidad: {speed} | ETA: {eta}")

                status_text.text("Iniciando conexión con YouTube...")
                success, result_path = extract_media(
                    url=url_input,
                    output_dir=OUTPUT_DIR,
                    mode=mode,
                    audio_format=audio_format,
                    audio_quality=audio_quality,
                    video_res=video_res,
                    progress_callback=update_progress
                )

                if success and os.path.exists(result_path):
                    progress_bar.progress(100)
                    status_text.text("¡Completado exitosamente!")
                    st.balloons()
                    st.success(f"Extracción finalizada. Guardado localmente en: `{result_path}`")
                else:
                    st.error(f"Error durante la descarga: {result_path}")
        else:
            st.warning("Por favor ingresá un enlace válido de YouTube.")
    else:
        st.info("Pegá el enlace de un video de YouTube para comenzar.")

    # ----------------------------------------------------
    # DOWNLOADS GALLERY SECTION
    # ----------------------------------------------------
    st.markdown("---")
    
    downloaded_files = list_downloaded_files(OUTPUT_DIR)
    file_count = len(downloaded_files)
    
    col_hdr_text, col_hdr_btn = st.columns([3, 1])
    
    with col_hdr_text:
        st.markdown("### Carpeta de Descargas (`downloads/`)")
        st.markdown(f'<div class="file-counter">Total de archivos: <strong>{file_count}</strong></div>', unsafe_allow_html=True)
    
    with col_hdr_btn:
        if st.button("Abrir Carpeta", key="open_downloads_folder_btn", help="Abrir ubicación en primer plano"):
            open_folder_in_foreground(OUTPUT_DIR)
            st.toast("Abriendo carpeta en primer plano...")

    if not downloaded_files:
        st.caption("No hay archivos descargados en la carpeta actualmente.")
    else:
        for idx, item in enumerate(downloaded_files):
            badge_class = "badge-audio" if item['type'] == "audio" else "badge-video"
            badge_label = f"AUDIO ({item['ext'].upper()[1:]})" if item['type'] == "audio" else f"VIDEO ({item['ext'].upper()[1:]})"
            
            with st.container():
                st.markdown(f'<span class="{badge_class}">{badge_label}</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="file-title">{item["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="file-meta">Tamaño: {item["size_mb"]} MB</div>', unsafe_allow_html=True)
                
                if item['type'] == "audio":
                    st.audio(item['path'], format=f"audio/{item['ext'][1:]}")
                else:
                    st.video(item['path'], format=f"video/{item['ext'][1:]}")
                
                st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 12px 0 16px 0;'>", unsafe_allow_html=True)
