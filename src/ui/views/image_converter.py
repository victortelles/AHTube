import os
import streamlit as st
from PIL import Image
import io

from src.config import (
    IMAGE_OUTPUT_DIR,
    SUPPORTED_IMAGE_INPUT_EXTS,
    SUPPORTED_IMAGE_OUTPUT_FORMATS,
)
from src.services.image_converter import (
    scan_image_directory,
    convert_single_image,
    batch_convert,
    create_zip_archive,
    list_converted_images,
    get_image_info,
)
from src.services.explorer import open_folder_in_foreground

def render_image_converter_view() -> None:
    """Renders the independent Image Converter view."""
    st.header("🖼️ Conversor Profesional de Imágenes")
    st.write("Convertí imágenes individuales o carpetas completas entre múltiples formatos (.webp, .png, .jpg, .ico, .pdf y más) sin límites y de forma 100% local.")

    st.markdown("---")

    # Mode Selector
    input_mode = st.radio(
        "Modo de selección de imágenes:",
        ["📁 Subir Archivos Directamente", "📂 Escanear Carpeta Local"],
        horizontal=True
    )

    items_to_convert: list[dict] = []

    if input_mode == "📁 Subir Archivos Directamente":
        uploaded_files = st.file_uploader(
            "Seleccioná una o varias imágenes:",
            type=[ext.replace(".", "") for ext in SUPPORTED_IMAGE_INPUT_EXTS],
            accept_multiple_files=True,
            help="Podés arrastrar o seleccionar archivos PNG, JPG, WEBP, ICO, BMP, TIFF, GIF, etc."
        )

        if uploaded_files:
            for file in uploaded_files:
                file_bytes = file.getvalue()
                info = get_image_info(file_bytes) or {}
                items_to_convert.append({
                    "name": file.name,
                    "source": file_bytes,
                    "format": info.get("format", os.path.splitext(file.name)[1].upper().replace(".", "")),
                    "size_kb": info.get("size_kb", round(len(file_bytes) / 1024, 2)),
                    "dimensions": f"{info.get('width', '?')}x{info.get('height', '?')}",
                    "mode": info.get("mode", "-"),
                })

    else:  # Escanear Carpeta Local
        col_path, col_scan = st.columns([4, 1])
        with col_path:
            folder_path = st.text_input(
                "Ruta absoluta de la carpeta a escanear:",
                placeholder="C:\\Ruta\\A\\Tu\\Carpeta_De_Imagenes"
            ).strip()
        with col_scan:
            st.write("")
            st.write("")
            scan_clicked = st.button("🔍 Escanear", use_container_width=True)

        if folder_path:
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                scanned_images = scan_image_directory(folder_path)
                if scanned_images:
                    st.success(f"Se encontraron **{len(scanned_images)}** imágenes compatibles en `{folder_path}`.")
                    for item in scanned_images:
                        items_to_convert.append({
                            "name": item["name"],
                            "path": item["path"],
                            "format": item["format"],
                            "size_kb": item["size_kb"],
                            "dimensions": f"{item['width']}x{item['height']}",
                            "mode": item["mode"],
                        })
                else:
                    st.warning("No se encontraron imágenes compatibles en la carpeta especificada.")
            else:
                st.error("La ruta indicada no existe o no es un directorio válido.")

    # ----------------------------------------------------
    # PREVIEW & CONVERSION SETTINGS
    # ----------------------------------------------------
    if items_to_convert:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Imágenes Seleccionadas para Conversión")

        # Summary Metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        total_kb = sum(item["size_kb"] for item in items_to_convert)
        formats_found = set(item["format"] for item in items_to_convert)
        
        with col_m1:
            st.metric("Total de Archivos", len(items_to_convert))
        with col_m2:
            st.metric("Peso Total Estimado", f"{round(total_kb / 1024, 2)} MB" if total_kb > 1024 else f"{round(total_kb, 1)} KB")
        with col_m3:
            st.metric("Formatos Detectados", ", ".join(formats_found))

        # Collapsible detailed table
        with st.expander("👁️ Ver lista detallada de archivos detectados", expanded=False):
            preview_data = [
                {
                    "Archivo": item["name"],
                    "Formato Original": item["format"],
                    "Dimensiones": item["dimensions"],
                    "Modo Color": item["mode"],
                    "Tamaño": f"{item['size_kb']} KB"
                }
                for item in items_to_convert
            ]
            st.dataframe(preview_data, use_container_width=True)

        st.markdown("---")
        st.markdown("### ⚙️ Parámetros de Salida")

        col_opt1, col_opt2 = st.columns(2)

        with col_opt1:
            target_format = st.selectbox(
                "Formato de Destino deseado:",
                SUPPORTED_IMAGE_OUTPUT_FORMATS,
                index=0,
                format_func=lambda x: f".{x.upper()} ({'Imágenes con o sin transparencia' if x in ('PNG', 'WEBP') else 'Fotografía estándar' if x == 'JPEG' else 'Documento' if x == 'PDF' else 'Icono de aplicación' if x == 'ICO' else 'Formato estándar'})"
            )

        with col_opt2:
            if target_format in ("JPEG", "WEBP"):
                quality = st.slider(
                    "Calidad de compresión:",
                    min_value=10,
                    max_value=100,
                    value=90,
                    step=5,
                    format="%d%%"
                )
            else:
                quality = 90
                st.info(f"Formato **{target_format}** seleccionado (calidad estándar sin pérdidas aplicable).")

        out_dir = IMAGE_OUTPUT_DIR
        st.caption(f"Los archivos convertidos se guardarán en la carpeta local: `{out_dir}/`")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Iniciar Conversión de Imágenes", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(percent: float, message: str):
                progress_bar.progress(min(max(percent, 0.0), 1.0))
                status_text.text(message)

            result = batch_convert(
                items=items_to_convert,
                target_format=target_format,
                output_dir=out_dir,
                quality=quality,
                progress_callback=update_progress
            )

            progress_bar.progress(1.0)
            status_text.text("¡Conversión completada con éxito!")
            st.balloons()

            st.success(f"✔ **{result['successful_count']}** de **{result['total']}** imágenes convertidas exitosamente a **.{target_format.lower()}**.")

            if result["failed_files"]:
                st.warning(f"Ocurrieron errores en {len(result['failed_files'])} archivos:")
                for fail in result["failed_files"]:
                    st.write(f"- `{fail['name']}`: {fail['error']}")

            # Direct ZIP download button for browser convenience
            if result["successful_files"]:
                zip_bytes = create_zip_archive(result["successful_files"])
                st.download_button(
                    label="📥 Descargar lote convertido en archivo .ZIP",
                    data=zip_bytes,
                    file_name=f"imagenes_convertidas_{target_format.lower()}.zip",
                    mime="application/zip",
                    use_container_width=True
                )

    # ----------------------------------------------------
    # CONVERTED IMAGES GALLERY / FOLDER EXPLORER
    # ----------------------------------------------------
    st.markdown("---")
    converted_files = list_converted_images(IMAGE_OUTPUT_DIR)
    file_count = len(converted_files)

    col_hdr_text, col_hdr_btn = st.columns([3, 1])

    with col_hdr_text:
        st.markdown("### Carpeta de Imágenes Convertidas (`converted_images/`)")
        st.markdown(f'<div class="file-counter">Total de archivos: <strong>{file_count}</strong></div>', unsafe_allow_html=True)

    with col_hdr_btn:
        if st.button("Abrir Carpeta", key="open_images_folder_btn", help="Abrir ubicación en primer plano"):
            open_folder_in_foreground(IMAGE_OUTPUT_DIR)
            st.toast("Abriendo carpeta de imágenes en primer plano...")

    if not converted_files:
        st.caption("No hay imágenes en la carpeta de destino actualmente.")
    else:
        # Gallery Grid View (up to 4 columns)
        cols = st.columns(4)
        for idx, item in enumerate(converted_files[:12]):
            with cols[idx % 4]:
                with st.container():
                    st.markdown('<span class="badge-image">IMAGEN</span>', unsafe_allow_html=True)
                    if item["ext"] in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".ico"):
                        try:
                            st.image(item["path"], use_container_width=True)
                        except Exception:
                            st.write(f"📄 {item['name']}")
                    else:
                        st.write(f"📄 {item['name']}")
                    st.markdown(f'<div class="file-title">{item["name"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="file-meta">{item["size_kb"]} KB | {item["ext"].upper()}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
