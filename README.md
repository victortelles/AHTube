# AHTyler Media Extractor

Extractor profesional de alta velocidad de Audio (MP3/WAV/M4A) y Video (MP4) desde YouTube.

![Logo](src/assets/AHTyler_Logo_der_Alpha.png)

## 📌 Características
- **Interfaz Web Interactiva**: Desarrollada con **Streamlit** y estilo personalizado en tonos Azules (Blue Theme).
- **Vista Previa de Video**: Muestra título, autor, duración y miniatura en tiempo real antes de descargar.
- **Selección de Método y Calidad**:
  - 🎵 **Audio**: Formatos `.mp3`, `.wav`, `.m4a`. Selección de calidad bitrate (320, 192, 128 kbps).
  - 🎥 **Video**: Formato `.mp4`. Selección de resolución (Máxima calidad, 1080p, 720p, 480p).
- **Descarga Directa**: Botón para descargar el archivo directamente al navegador + copia local en la carpeta `downloads/`.
- **Modo Consola (CLI)**: Opción para ejecuciones rápidas sin interfaz gráfica.

---

## 🚀 Instalación

1. Clonar o estar dentro de la carpeta del proyecto.
2. Crear y activar el entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 💻 Modo de Uso

### 🌐 Interfaz Web (Streamlit) - Recomendado
Ejecutá el siguiente comando para abrir la aplicación web en tu navegador:
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
O simplemente:
```powershell
streamlit run app.py
```

### ⚡ Modo Consola (CLI)
- **Interactivo en consola**:
  ```powershell
  python main.py
  ```
- **Extracción rápida vía línea de comandos**:
  ```powershell
  python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --mode audio
  python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --mode video
  ```
