import os
import streamlit as st

from src.config import (
    IMAGE_OUTPUT_DIR,
    SUPPORTED_IMAGE_INPUT_EXTS,
    SUPPORTED_IMAGE_OUTPUT_FORMATS,
)
from src.services.image_converter import (
    scan_image_directory,
    batch_convert,
    create_zip_archive,
    list_converted_images,
    get_image_info,
)
from src.services.explorer import open_folder_in_foreground
from src.ui.primitives import render_micro_card, get_badge_html

def render_image_converter_view() -> None:
    """Renders the independent Image Converter view with Sky/Slate Studio theme."""
    render_micro_card(
        title="Procesador y Conversor de Imágenes",
        subtitle="Conversión local de alta fidelidad entre formatos (.heic, .jfif, .png, .jpg, .webp, .ico, .pdf)",
        badge_text="IMAGE LAB",
        badge_variant="image",
        icon="photo_library"
    )

    # Mode Selector
    input_mode = st.radio(
        "Modo de selección de imágenes:",
        ["Subir Archivos Directamente", "Escanear Carpeta Local"],
        horizontal=True
    )

    items_to_convert: list[dict] = []

    if input_mode == "Subir Archivos Directamente":
        uploaded_files = st.file_uploader(
            "Seleccioná una o varias imágenes:",
            type=[ext.replace(".", "") for ext in SUPPORTED_IMAGE_INPUT_EXTS],
            accept_multiple_files=True,
            help="Arrastrá o seleccioná archivos HEIC, JFIF, PNG, JPG, WEBP, ICO, BMP, TIFF, GIF, etc."
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
            st.button("Escanear", type="secondary")

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
        st.html("<div style='margin: 1rem 0;'></div>")
        st.markdown("### Imágenes en Cola de Procesamiento")

        col_m1, col_m2, col_m3 = st.columns(3)
        total_kb = sum(item["size_kb"] for item in items_to_convert)
        formats_found = sorted(set(item["format"] for item in items_to_convert))
        
        with col_m1:
            st.metric("Total de Archivos", f"{len(items_to_convert)}")
        with col_m2:
            st.metric("Peso Estimado", f"{round(total_kb / 1024, 2)} MB" if total_kb > 1024 else f"{round(total_kb, 1)} KB")
        with col_m3:
            st.metric("Formatos", ", ".join(formats_found))

        # Format badges row
        badges_html = " ".join([get_badge_html(fmt, variant="image") for fmt in formats_found])
        st.html(f"<div style='margin: 0.5rem 0;'>{badges_html}</div>")

        with st.expander("Ver lista detallada de archivos detectados", expanded=False):
            preview_data = [
                {
                    "Archivo": item["name"],
                    "Formato": item["format"],
                    "Dimensiones": item["dimensions"],
                    "Color": item["mode"],
                    "Tamaño": f"{item['size_kb']} KB"
                }
                for item in items_to_convert
            ]
            st.dataframe(preview_data)

        st.markdown("---")
        st.markdown("### Configuración de Destino")

        col_opt1, col_opt2 = st.columns(2)

        with col_opt1:
            target_format = st.selectbox(
                "Formato de Destino:",
                SUPPORTED_IMAGE_OUTPUT_FORMATS,
                index=0,
                format_func=lambda x: f".{x.upper()} ({'Transparencia PNG/WEBP' if x in ('PNG', 'WEBP') else 'Fotografía estándar' if x == 'JPEG' else 'Documento multipágina' if x == 'PDF' else 'Icono de aplicación' if x == 'ICO' else 'Formato estándar'})"
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
                st.info(f"Formato **{target_format}** seleccionado (compresión sin pérdidas).")

        out_dir = IMAGE_OUTPUT_DIR
        st.caption(f"Los archivos convertidos se guardarán en: `{out_dir}/`")

        st.html("<div style='margin: 0.75rem 0;'></div>")

        if st.button("Iniciar Conversión de Imágenes", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(percent: float, message: str):
                progress_bar.progress(min(max(percent, 0.0), 1.0))
                status_text.html(
                    f"<div class='tabular-nums' style='color:var(--muted-foreground);font-size:0.85rem;'>"
                    f"Procesando lote... {message}</div>"
                )

            result = batch_convert(
                items=items_to_convert,
                target_format=target_format,
                output_dir=out_dir,
                quality=quality,
                progress_callback=update_progress
            )

            progress_bar.progress(1.0)
            status_text.text("¡Conversión de lote completada con éxito!")
            st.balloons()

            st.success(f"**{result['successful_count']}** de **{result['total']}** imágenes convertidas exitosamente a **.{target_format.lower()}**.")

            if result["failed_files"]:
                st.warning(f"Ocurrieron errores en {len(result['failed_files'])} archivos:")
                for fail in result["failed_files"]:
                    st.write(f"- `{fail['name']}`: {fail['error']}")

            if result["successful_files"]:
                zip_bytes = create_zip_archive(result["successful_files"])
                st.download_button(
                    label="Descargar lote convertido en archivo .ZIP",
                    data=zip_bytes,
                    file_name=f"imagenes_convertidas_{target_format.lower()}.zip",
                    mime="application/zip"
                )

    # ----------------------------------------------------
    # CONVERTED IMAGES GALLERY / FOLDER EXPLORER
    # ----------------------------------------------------
    st.markdown("---")
    converted_files = list_converted_images(IMAGE_OUTPUT_DIR)
    file_count = len(converted_files)

    col_hdr_text, col_hdr_btn = st.columns([3, 1])

    with col_hdr_text:
        st.markdown("### Biblioteca de Imágenes Convertidas")
        st.html(
            f'<div class="file-counter">Imágenes en almacén: <strong style="color:var(--primary);">{file_count}</strong></div>'
        )

    with col_hdr_btn:
        if st.button("Abrir Carpeta", key="open_images_folder_btn", help="Abrir ubicación en el Explorador de archivos"):
            open_folder_in_foreground(IMAGE_OUTPUT_DIR)
            st.toast("Abriendo carpeta converted_images/ en primer plano...")

    if not converted_files:
        st.caption("No hay imágenes en la carpeta de destino actualmente.")
    else:
        cols = st.columns(4)
        for idx, item in enumerate(converted_files[:12]):
            with cols[idx % 4]:
                badge_html = get_badge_html(item["ext"].upper()[1:], variant="image")
                with st.container():
                    st.html(
                        f"""
                        <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:0.75rem;margin-bottom:0.75rem;">
                            <div style="margin-bottom:0.4rem;">{badge_html}</div>
                        </div>
                        """
                    )
                    if item["ext"] in (".png", ".jpg", ".jpeg", ".jfif", ".webp", ".bmp", ".ico"):
                        try:
                            st.image(item["path"], width="stretch")
                        except Exception:
                            st.write(f"{item['name']}")
                    else:
                        st.write(f"{item['name']}")
                    st.html(
                        f'<div class="file-title">{item["name"]}</div>'
                        f'<div class="file-meta">{item["size_kb"]} KB</div>'
                    )
