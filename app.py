import os
import sys
import time
import ctypes
import subprocess
import streamlit as st
from src.extractor import fetch_video_metadata, extract_media

# Configure Streamlit page
st.set_page_config(
    page_title="AHTyler Media Extractor",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Blue Aesthetic & Minimalist UI
st.markdown("""
    <style>
    /* Global Background & Typography */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Card */
    .main-title {
        color: #60A5FA;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: border-color 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* Primary Action Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    }

    /* Cards */
    .preview-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .badge-audio {
        background-color: rgba(37, 99, 235, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 6px;
    }

    .badge-video {
        background-color: rgba(168, 85, 247, 0.15);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 6px;
    }

    .file-title {
        color: #F8FAFC;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .file-meta {
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 2px;
    }

    .file-counter {
        color: #94A3B8;
        font-size: 0.85rem;
        margin-top: -8px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Assets paths
LOGO_ALPHA_PATH = os.path.join("src", "assets", "AHTyler_Logo_der.PNG")
STEP1_IMG = os.path.join("src", "assets", "step_paste_link.jpg")
STEP2_IMG = os.path.join("src", "assets", "step_select_format.jpg")
STEP3_IMG = os.path.join("src", "assets", "step_download.jpg")
OUTPUT_DIR = "downloads"

def open_folder_in_foreground(directory: str):
    """Opens the downloads folder directly in Explorer and brings it to the foreground."""
    abs_path = os.path.abspath(directory)
    os.makedirs(abs_path, exist_ok=True)
    
    if sys.platform == "win32":
        # Launch explorer process
        subprocess.Popen(['explorer', os.path.normpath(abs_path)])
        
        # Bring window to foreground using Windows API
        try:
            time.sleep(0.3)
            user32 = ctypes.windll.user32
            target_name = os.path.basename(abs_path).lower()
            
            def enum_windows_callback(hwnd, extra):
                if user32.IsWindowVisible(hwnd):
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buff = ctypes.create_unicode_buffer(length + 1)
                        user32.GetWindowTextW(hwnd, buff, length + 1)
                        title = buff.value.lower()
                        if target_name in title:
                            user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                            user32.SetForegroundWindow(hwnd)
                return True

            WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
            user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
        except Exception:
            pass
    elif sys.platform == "darwin":
        subprocess.Popen(['open', abs_path])
    else:
        subprocess.Popen(['xdg-open', abs_path])

def list_downloaded_files(directory: str) -> list[dict]:
    """Scans the downloads directory and returns file information sorted by modification time."""
    if not os.path.exists(directory):
        return []
    
    valid_exts = ('.mp3', '.wav', '.m4a', '.mp4', '.webm', '.mkv')
    files_info = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.lower().endswith(valid_exts):
            stat = os.stat(filepath)
            ext = os.path.splitext(filename)[1].lower()
            media_type = "audio" if ext in ('.mp3', '.wav', '.m4a') else "video"
            files_info.append({
                'name': filename,
                'path': filepath,
                'ext': ext,
                'type': media_type,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'mtime': stat.st_mtime
            })
            
    files_info.sort(key=lambda x: x['mtime'], reverse=True)
    return files_info

# Sidebar Branding & Navigation
with st.sidebar:
    if os.path.exists(LOGO_ALPHA_PATH):
        st.image(LOGO_ALPHA_PATH, use_container_width=True)
    st.title("AHTyler Extractor")
    st.markdown("---")
    
    nav_option = st.radio(
        "Navegación / Secciones",
        ["🏠 Inicio", "📖 Cómo usarlo", "⚙️ ¿Cómo funciona por detrás?"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📌 Características")
    st.markdown("• Extracción ultra-rápida de audio")
    st.markdown("• Formatos: MP3, WAV, M4A y Video MP4")
    st.markdown("• Calidad bitrate hasta 320 kbps")
    st.markdown("• Galería integrada de descargas")
    st.markdown("---")
    st.caption("AHTyler Tools © 2026")

# Header Banner
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists(LOGO_ALPHA_PATH):
        st.image(LOGO_ALPHA_PATH, width=100)
with col_title:
    st.markdown('<div class="main-title">AHTyler Media Extractor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Extractor profesional de Audio (MP3) y Video (MP4) desde YouTube</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# SECTION 1: INICIO (Main Extractor + Minimalist Downloads Gallery)
if nav_option == "🏠 Inicio":
    url_input = st.text_input(
        "🔗 Pegá la URL del video de YouTube:",
        placeholder="https://www.youtube.com/watch?v=..."
    ).strip()

    if url_input:
        if "youtube.com/" in url_input or "youtu.be/" in url_input:
            with st.spinner("Cargando detalles del video..."):
                meta = fetch_video_metadata(url_input)
            
            if meta:
                with st.container():
                    st.markdown('<div class="preview-card">', unsafe_allow_html=True)
                    col_thumb, col_info = st.columns([1, 2])
                    with col_thumb:
                        if meta.get('thumbnail'):
                            st.image(meta['thumbnail'], use_container_width=True)
                    with col_info:
                        st.subheader(meta.get('title'))
                        st.write(f"👤 **Canal:** {meta.get('uploader')}")
                        dur_min = meta.get('duration', 0) // 60
                        dur_sec = meta.get('duration', 0) % 60
                        st.write(f"⏱️ **Duración:** {dur_min}m {dur_sec}s")
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### ⚙️ Opciones de Extracción")
            
            mode_choice = st.radio(
                "Seleccioná el método de extracción:",
                ["🎵 Extraer Audio", "🎥 Extraer Video"],
                horizontal=True
            )

            col_opt1, col_opt2 = st.columns(2)

            if mode_choice == "🎵 Extraer Audio":
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

            if st.button("🚀 Iniciar Extracción"):
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
                    st.success(f"✅ Extracción finalizada. Guardado localmente en: `{result_path}`")
                else:
                    st.error(f"❌ Error durante la descarga: {result_path}")
        else:
            st.warning("⚠️ Por favor ingresá un enlace válido de YouTube.")
    else:
        st.info("👋 Pegá el enlace de un video de YouTube para comenzar.")

    # ----------------------------------------------------
    # DOWNLOADS GALLERY SECTION (Foreground Window Trigger)
    # ----------------------------------------------------
    st.markdown("---")
    
    downloaded_files = list_downloaded_files(OUTPUT_DIR)
    file_count = len(downloaded_files)
    
    # Title Header aligned with Foreground Folder Action Button
    col_hdr_text, col_hdr_btn = st.columns([3, 1])
    
    with col_hdr_text:
        st.markdown("### 📂 Carpeta de Descargas (`downloads/`)")
        st.markdown(f'<div class="file-counter">Total de archivos: <strong>{file_count}</strong></div>', unsafe_allow_html=True)
    
    with col_hdr_btn:
        if st.button("📁 Abrir Carpeta", key="open_downloads_folder_btn", help="Abrir ubicación en primer plano"):
            open_folder_in_foreground(OUTPUT_DIR)
            st.toast("Abriendo carpeta en primer plano...", icon="📂")

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
                
                # Streamlit Media Player (Audio / Video)
                if item['type'] == "audio":
                    st.audio(item['path'], format=f"audio/{item['ext'][1:]}")
                else:
                    st.video(item['path'], format=f"video/{item['ext'][1:]}")
                
                st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 12px 0 16px 0;'>", unsafe_allow_html=True)

# SECTION 2: CÓMO USARLO
elif nav_option == "📖 Cómo usarlo":
    st.header("📖 Guía Paso a Paso: ¿Cómo usar la aplicación?")
    st.write("Sigue estas sencillas indicaciones para extraer cualquier audio o video de YouTube en segundos.")
    
    st.markdown("---")
    
    st.subheader("Paso 1: Copiar y pegar el enlace de YouTube")
    st.write("Abrí YouTube en tu navegador o aplicación, copiá el enlace completo del video que deseas descargar y pégalo en el campo principal de entrada.")
    if os.path.exists(STEP1_IMG):
        st.image(STEP1_IMG, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Paso 2: Confirmar detalles y seleccionar el método")
    st.write("Al pegar un enlace válido, la aplicación cargará una vista previa con el título y duración. Elegí si querés extraer únicamente el **Audio** (MP3/WAV/M4A) o el **Video completo** (MP4), ajustando la calidad según tus necesidades.")
    if os.path.exists(STEP2_IMG):
        st.image(STEP2_IMG, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Paso 3: Extracción y Descarga")
    st.write("Hacé clic en el botón **🚀 Iniciar Extracción**. Podrás visualizar la velocidad y porcentaje en tiempo real. Al finalizar, el archivo aparecerá automáticamente en tu carpeta de descargas.")
    if os.path.exists(STEP3_IMG):
        st.image(STEP3_IMG, use_container_width=True)

    st.markdown("---")
    st.success("💡 **Tip**: También podés acceder a la sección *¿Cómo funciona por detrás?* en el menú lateral para conocer los aspectos técnicos de la herramienta.")

# SECTION 3: CÓMO FUNCIONA POR DETRÁS
elif nav_option == "⚙️ ¿Cómo funciona por detrás?":
    st.header("⚙️ ¿Cómo funciona AHTyler Media Extractor por detrás?")
    st.write("Te explicamos de manera sencilla la arquitectura y el proceso técnico que ocurre en segundo plano cada vez que realizás una extracción.")
    
    st.markdown("---")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("""
        ### 1. Inspección e Información (API / Meta-Data)
        Cuando pegás la URL, el backend utiliza **`yt-dlp`** para conectarse con YouTube y consultar los metadatos del video sin descargar el archivo entero. 
        Esto nos permite obtener el título, duración, miniatura y los flujos (streams) de audio/video disponibles casi al instante.
        """)
        
        st.markdown("""
        ### 3. Procesamiento y Conversión con FFmpeg
        Una vez obtenido el flujo directo, entra en acción **FFmpeg** (un potente motor multimedia industrial).
        FFmpeg decodifica el flujo comprimido y lo recodifica en el formato solicitado (como MP3 a 320 kbps o 192 kbps), optimizando la compresión sin degradar la fidelidad sonora.
        """)

    with col_f2:
        st.markdown("""
        ### 2. Separación de Flujos de Audio y Video
        YouTube almacena por separado la pista de video y la pista de audio (tecnología *DASH*).
        Si solicitás **Audio**, nuestra herramienta descarga únicamente la pista sonora nativa (Opus o AAC), evitando descargar gigabytes de video innecesarios para máxima velocidad.
        """)
        
        st.markdown("""
        ### 4. Entrega y Almacenamiento Seguro
        El archivo generado se almacena en la carpeta local `downloads/` del servidor y simultáneamente se transfiere como un flujo de datos binario seguro al navegador para tu descarga directa.
        """)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🔒 **Seguridad y Privacidad**: Toda la conversión se procesa localmente en tu sistema sin almacenar copias en servidores de terceros ni enviar información personal.")
