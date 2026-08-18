# AHTube 🎵🎥

> **¿Cansado de encontrar convertidores de YT a MP3 o MP4 que te limitan su uso o te llenan de redirecciones a sitios desconocidos?**  
> ¡Aquí tenés la solución! Ejecutá **AHTube** localmente en tu dispositivo y mantené el control total sin publicidad, sin límites y con máxima privacidad.

![AHTube Banner](src/assets/AHTyler_Logo_der_Alpha.png)

---

## 📌 Descripción del Proyecto

**AHTube** es una solución profesional desarrollada en Python que combina una **Interfaz Web (Streamlit)** moderna y una **Consola interactiva (CLI)** de alta velocidad. Permite analizar enlaces de YouTube, mostrar una vista previa en tiempo real con metadatos del video (título, autor, duración y miniatura) y extraer el contenido en formatos de **Audio (MP3, WAV, M4A)** o **Video (MP4)** con calidad configurable.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: [Python 3.10+](https://www.python.org/)
- **Interfaz Web**: [Streamlit](https://streamlit.io/)
- **Motor de Extracción**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Procesamiento de Audio y Video**: [FFmpeg](https://ffmpeg.org/) / `static-ffmpeg`
- **Gestión de Entorno**: Python `venv`

---

## ⚙️ Requisitos Mínimos para Desarrolladores

Antes de comenzar, asegurate de contar con:

1. **Python 3.10 o superior** instalado en el sistema.
2. **Pip** (gestor de paquetes de Python) actualizado.
3. **Acceso a Internet** para la conexión con la infraestructura de YouTube.
4. **Sistema Operativo**: Windows 10/11, macOS o Linux.

---

## 🚀 Instalación y Configuración

1. **Clonar o descargar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/AHTube.git
   cd AHTube
   ```

2. **Crear y activar el entorno virtual**:
   - En **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - En **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Modo de Uso

### 🌐 1. Interfaz Web (Streamlit) — Recomendado
Ejecutá el siguiente comando para iniciar la aplicación web interactiva en tu navegador:
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### ⚡ 2. Modo Consola (CLI)
Para ejecuciones ultrarrápidas sin interfaz gráfica:
- **Modo interactivo en consola**:
  ```powershell
  python main.py
  ```
- **Extracción directa por argumentos**:
  ```powershell
  python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --mode audio
  python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --mode video
  ```

---

## 📖 Guía Visual de Uso

### Paso 1: Copiar y pegar la URL de YouTube
Pegá el enlace en el campo principal. La aplicación analizará automáticamente el enlace y cargará una vista previa con los detalles del video.

![Paso 1: Pegar URL](src/assets/step_paste_link.jpg)

### Paso 2: Seleccionar formato y calidad
Elegí entre extraer solo **Audio** (MP3 hasta 320 kbps, WAV o M4A) o el **Video completo** (MP4 en resolución hasta 1080p / Máxima calidad).

![Paso 2: Elegir Formato](src/assets/step_select_format.jpg)

### Paso 3: Extraer y disfrutar
Hacé clic en **🚀 Iniciar Extracción**. Podrás ver el progreso en tiempo real y escuchar o reproducir el archivo directamente en la aplicación, o abrir la carpeta `downloads/` en primer plano.

![Paso 3: Descarga](src/assets/step_download.jpg)

---

## 📋 Alcances y Limitaciones

### ✅ Lo que SÍ se puede hacer
- **Uso Ilimitado y Local**: Sin límites de descargas diarias, sin acortadores y sin publicidad molesta.
- **Calidad de Audio Configurable**: Extracción en MP3 a **320 kbps** (Alta fidelidad), **192 kbps** (Estándar) o **128 kbps** (Ligera), además de formatos sin pérdida como WAV.
- **Resolución de Video Adaptable**: Conversión a MP4 manteniendo la resolución original del video.
- **Reproducción Integrada**: Escuchar el audio o mirar el video directamente dentro de la interfaz web.
- **Integración con el Sistema**: Botón para abrir la carpeta `downloads/` directamente en **primer plano** en el Explorador de archivos de Windows.

### ❌ Lo que NO se puede hacer (Limitaciones)
- **Contenido con Protección DRM**: No es posible descargar películas pagas, transmisiones en vivo protegidas o contenido privado de YouTube Primetime.
- **Bypass de Restricciones Geográficas Extremas**: Si un video está bloqueado en tu región por YouTube, la aplicación requerirá el uso de una VPN local en tu equipo.
- **Redistribución Comercial**: Este software está diseñado exclusivamente para uso personal, educativo y de respaldo. No fomenta la infracción de derechos de autor.
