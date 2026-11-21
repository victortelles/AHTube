import os
import streamlit as st
from src.config import OUTPUT_DIR
from src.services.extractor import fetch_video_metadata, extract_media, list_downloaded_files
from src.services.explorer import open_folder_in_foreground
from src.ui.components import render_preview_card
from src.ui.primitives import render_micro_card, get_badge_html

def render_home_view() -> None:
    """Renders the main Home view: Audio/Video Studio Extractor & Downloads Gallery."""
    render_micro_card(
        title="Estación de Extracción de Medios",
        subtitle="Conversión y descarga de audio de alta fidelidad y video nativo desde YouTube",
        badge_text="DAW CORE",
        badge_variant="audio",
        icon="graphic_eq"
    )

    url_input = st.text_input(
        "URL del video de YouTube:",
        placeholder="https://www.youtube.com/watch?v=..."
    ).strip()

    if url_input:
        if "youtube.com/" in url_input or "youtu.be/" in url_input:
            with st.spinner("Sondeando flujos de audio y video..."):
                meta = fetch_video_metadata(url_input)
            
            if meta:
                render_preview_card(meta)

            st.markdown("### Parámetros de Procesamiento")
            
            mode_choice = st.radio(
                "Seleccioná el modo de salida:",
                ["Pista de Audio (Separada)", "Video Completo"],
                horizontal=True
            )

            col_opt1, col_opt2 = st.columns(2)

            if mode_choice == "Pista de Audio (Separada)":
                mode = "audio"
                with col_opt1:
                    audio_format = st.selectbox(
                        "Formato de Audio:",
                        ["mp3", "wav", "m4a"],
                        format_func=lambda x: f".{x.upper()} (Audio)"
                    )
                with col_opt2:
                    if audio_format == "mp3":
                        audio_quality = st.selectbox(
                            "Calidad de Bitrate (CBR):",
                            ["320", "192", "128"],
                            index=1,
                            format_func=lambda x: f"{x} kbps ({'Máxima Fidelidad' if x=='320' else 'Estándar Studio' if x=='192' else 'Compacto'})"
                        )
                    else:
                        audio_quality = "192"
                        st.info(f"Formato {audio_format.upper()} sin pérdida o nativo seleccionado.")
                video_res = "best"
            else:
                mode = "video"
                audio_format = "mp3"
                audio_quality = "192"
                with col_opt1:
                    video_res = st.selectbox(
                        "Resolución máxima de video:",
                        ["best", "1080", "720", "480"],
                        format_func=lambda x: "Máxima Calidad (Original)" if x == "best" else f"{x}p HD"
                    )
                with col_opt2:
                    st.info("Contenedor de salida: MP4 (H.264 / AAC)")

            st.markdown("<div style='margin: 0.75rem 0;'></div>", unsafe_allow_html=True)

            if st.button("Iniciar Extracción", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                def update_progress(percent, speed, eta):
                    progress_bar.progress(min(max(percent, 0.0), 1.0))
                    status_text.markdown(
                        f"<div class='tabular-nums' style='color:var(--muted-foreground);font-size:0.85rem;'>"
                        f"Descargando flujos... <strong>{int(percent * 100)}%</strong> | Velocidad: {speed} | ETA: {eta}</div>",
                        unsafe_allow_html=True
                    )

                status_text.text("Conectando con el servidor de YouTube...")
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
                    status_text.text("¡Procesamiento finalizado!")
                    st.balloons()
                    st.success(f"Archivo guardado exitosamente en: `{result_path}`")
                else:
                    st.error(f"Error durante el procesamiento: {result_path}")
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
        st.markdown("### Biblioteca Local de Descargas")
        st.markdown(
            f'<div class="file-counter">Archivos en almacén: <strong style="color:var(--primary);">{file_count}</strong></div>',
            unsafe_allow_html=True
        )
    
    with col_hdr_btn:
        if st.button("Abrir Carpeta", key="open_downloads_folder_btn", help="Abrir ubicación en el Explorador de archivos"):
            open_folder_in_foreground(OUTPUT_DIR)
            st.toast("Abriendo carpeta downloads/ en primer plano...")

    if not downloaded_files:
        st.caption("No hay archivos en la biblioteca actualmente.")
    else:
        for idx, item in enumerate(downloaded_files):
            badge_variant = "audio" if item['type'] == "audio" else "video"
            badge_label = f"{item['type'].upper()} · {item['ext'].upper()[1:]}"
            badge_html = get_badge_html(badge_label, variant=badge_variant)
            
            with st.container():
                st.markdown(
                    f"""
                    <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;margin:0.75rem 0;">
                        <div style="margin-bottom:0.4rem;">{badge_html}</div>
                        <div class="file-title">{item["name"]}</div>
                        <div class="file-meta">Tamaño: {item["size_mb"]} MB</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if item['type'] == "audio":
                    st.audio(item['path'], format=f"audio/{item['ext'][1:]}")
                else:
                    st.video(item['path'], format=f"video/{item['ext'][1:]}")
