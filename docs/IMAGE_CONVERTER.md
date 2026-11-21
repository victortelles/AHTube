# 🖼️ Módulo de Conversión de Imágenes (Image Converter)

> **Módulo independiente de alto rendimiento para la conversión y optimización de imágenes en lote, 100% local y privado.**

---

## 📌 Visión General

El **Conversor de Imágenes** de **AHTube** es un subsistema completamente desacoplado del motor de extracción de YouTube. Permite procesar archivos de imagen individuales o escanear directorios locales completos, identificar automáticamente los formatos de origen, y transformar los archivos a múltiples formatos de destino (.png, .jpg, .webp, .ico, .bmp, .tiff, .pdf) con compresión y ajuste de canal alfa configurables.

---

## 🏗️ Arquitectura y Desacoplamiento

El módulo sigue una arquitectura modular limpia (Clean / Hexagonal Architecture):

```
ExtractAudio/
├── src/
│   ├── config.py                       # Constantes y formatos compatibles
│   ├── services/
│   │   ├── image_converter.py          # Lógica de dominio pura (Pillow, ZIP, Escaneo)
│   │   └── explorer.py                 # Apertura de carpetas en Windows Explorer
│   └── ui/
│       └── views/
│           └── image_converter.py      # Interfaz visual interactiva en Streamlit
└── docs/
    └── IMAGE_CONVERTER.md              # Esta documentación técnica
```

### Principios de Diseño:
- **Cero Acoplamiento**: No depende de `yt-dlp` ni de `FFmpeg`. Funciona como un servicio puro basado en **Pillow**.
- **Eficiencia de Memoria**: Lectura de metadatos mediante streams e inspección de encabezados antes de cargar mapas de bits completos.
- **Procesamiento en Lote (Batch)**: Ejecución secuencial controlada con callbacks de progreso en tiempo real.

---

## 🔄 Formatos Compatibles

### Formatos de Entrada Detectados:
| Extensión | Formato | Transparencia (Alpha) |
|---|---|:---:|
| `.png` | Portable Network Graphics | ✅ Sí |
| `.jpg` / `.jpeg` | JPEG Image | ❌ No |
| `.webp` | WebP Image | ✅ Sí |
| `.bmp` | Bitmap Image File | ❌ No |
| `.tiff` / `.tif` | Tagged Image File Format | ✅ Sí |
| `.ico` | Windows Icon | ✅ Sí |
| `.gif` | Graphics Interchange Format | ✅ Sí |

### Formatos de Salida Disponibles:
- **`.PNG`**: Ideal para gráficos web, ilustraciones y contenido con transparencias sin pérdida.
- **`.JPEG` / `.JPG`**: Ideal para fotografías y optimización de peso web. Control de calidad configurable (10%–100%). Los canales transparentes se componen automáticamente sobre fondo blanco para evitar artefactos negros.
- **`.WEBP`**: Formato moderno de alta compresión para la web con soporte de transparencias y calidad ajustable.
- **`.ICO`**: Generación de iconos para aplicaciones y favicons, con reescalado automático inteligente a 256x256 e inclusión de múltiples capas de resolución (16x16, 32x32, 48x48, 64x64, 128x128, 256x256).
- **`.BMP`**: Formato de mapa de bits sin compresión.
- **`.TIFF`**: Formato industrial de alta fidelidad para impresión y archivado.
- **`.PDF`**: Empaquetado directo de imágenes en documentos PDF individuales.

---

## 💻 Modos de Uso

### 1. 📁 Modo "Subir Archivos Directamente"
1. En la barra lateral de navegación, seleccioná **Conversor de Imágenes**.
2. Elegí el modo **📁 Subir Archivos Directamente**.
3. Arrastrá o seleccioná uno o varios archivos de imagen desde tu explorador.
4. La herramienta identificará automáticamente las dimensiones, modo de color y peso de cada archivo.
5. Seleccioná el **Formato de Destino** y ajustá la calidad si elegiste JPG o WEBP.
6. Hacé clic en **🚀 Iniciar Conversión de Imágenes**.
7. Podés descargar el resultado en un archivo `.ZIP` o acceder directamente a la carpeta local `converted_images/`.

### 2. 📂 Modo "Escanear Carpeta Local"
1. Seleccioná el modo **📂 Escanear Carpeta Local**.
2. Ingresá la ruta absoluta de la carpeta en tu equipo (ejemplo: `C:\Users\TuUsuario\Pictures\MisFotos`).
3. Hacé clic en **🔍 Escanear**.
4. El programa recorrerá recursivamente el directorio detectando todos los archivos con formatos compatibles.
5. Elegí el formato deseado y presioná **🚀 Iniciar Conversión de Imágenes**.

---

## 🛠️ Uso Programático (Servicio en Python)

Podés importar y utilizar el servicio de conversión directamente en otros scripts o tests:

```python
from src.services.image_converter import (
    convert_single_image,
    batch_convert,
    scan_image_directory,
    create_zip_archive
)

# 1. Conversión de imagen individual
success, output_path = convert_single_image(
    input_source="ruta/a/imagen.webp",
    target_format="PNG",
    output_path="converted_images/imagen.png"
)

# 2. Conversión por lotes
items = scan_image_directory("C:/MisImagenes")
summary = batch_convert(
    items=items,
    target_format="JPEG",
    output_dir="converted_images",
    quality=85
)
print(f"Convertidas: {summary['successful_count']} / {summary['total']}")
```

---

## 🧪 Pruebas Automatizadas

El módulo incluye una suite completa de pruebas unitarias en `tests/test_image_converter.py`. Para ejecutarlas:

```powershell
python -m unittest tests/test_image_converter.py
```
