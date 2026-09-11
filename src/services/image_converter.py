import io
import os
import zipfile
from typing import Any, BinaryIO, Callable
from PIL import Image, ImageOps

from src.config import SUPPORTED_IMAGE_INPUT_EXTS

# Pillow target format mapping
FORMAT_MAPPING = {
    "PNG": "PNG",
    "JPEG": "JPEG",
    "JPG": "JPEG",
    "JFIF": "JPEG",
    "WEBP": "WEBP",
    "BMP": "BMP",
    "TIFF": "TIFF",
    "ICO": "ICO",
    "PDF": "PDF",
}

def get_image_info(source: str | bytes | BinaryIO) -> dict | None:
    """Reads basic image metadata without reading the entire pixel data into memory."""
    try:
        if isinstance(source, bytes):
            stream = io.BytesIO(source)
            with Image.open(stream) as img:
                return {
                    "format": img.format or "UNKNOWN",
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "size_kb": round(len(source) / 1024, 2),
                }
        elif isinstance(source, str):
            stat = os.stat(source)
            with Image.open(source) as img:
                return {
                    "format": img.format or os.path.splitext(source)[1].replace(".", "").upper(),
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "size_kb": round(stat.st_size / 1024, 2),
                }
        else:
            # File-like object
            pos = source.tell() if hasattr(source, "tell") else 0
            with Image.open(source) as img:
                info = {
                    "format": img.format or "UNKNOWN",
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "size_kb": round(len(source.getvalue()) / 1024, 2) if hasattr(source, "getvalue") else 0,
                }
            if hasattr(source, "seek"):
                source.seek(pos)
            return info
    except Exception:
        return None

def scan_image_directory(directory_path: str) -> list[dict]:
    """
    Scans a local directory for all supported image files.
    Returns a list of dictionaries with file metadata.
    """
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return []

    found_images: list[dict] = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_IMAGE_INPUT_EXTS:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, directory_path)
                try:
                    stat = os.stat(full_path)
                    with Image.open(full_path) as img:
                        fmt = img.format or ext.replace(".", "").upper()
                        width, height = img.size
                        mode = img.mode

                    found_images.append({
                        "name": file,
                        "relative_path": rel_path,
                        "path": full_path,
                        "ext": ext,
                        "format": fmt,
                        "width": width,
                        "height": height,
                        "mode": mode,
                        "size_kb": round(stat.st_size / 1024, 2),
                        "mtime": stat.st_mtime,
                    })
                except Exception:
                    # Skip corrupt or unreadable image files
                    continue

    found_images.sort(key=lambda x: x["name"].lower())
    return found_images

def prepare_image_for_format(
    img: Image.Image,
    target_format: str,
    background_color: tuple[int, int, int] = (255, 255, 255)
) -> Image.Image:
    """
    Handles color mode conversions and transparency flattening when needed
    for format compatibility (e.g. RGBA -> RGB for JPEG/BMP/PDF).
    """
    fmt = target_format.upper()

    # Correct image orientation based on EXIF tag if present
    img = ImageOps.exif_transpose(img)

    # Formats that do not support transparency
    no_alpha_formats = {"JPEG", "JPG", "BMP", "PDF"}

    if fmt in no_alpha_formats:
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            # Create a solid background and composite the image over it
            rgba_img = img.convert("RGBA")
            bg = Image.new("RGBA", rgba_img.size, background_color + (255,))
            combined = Image.alpha_composite(bg, rgba_img)
            return combined.convert("RGB")
        elif img.mode != "RGB":
            return img.convert("RGB")

    elif fmt == "ICO":
        # ICO handles RGBA or RGB up to 256x256
        if img.mode not in ("RGBA", "RGB"):
            img = img.convert("RGBA")
        if img.width > 256 or img.height > 256:
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
        return img

    elif fmt in ("PNG", "WEBP", "TIFF"):
        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")

    return img

def convert_single_image(
    input_source: str | bytes | BinaryIO,
    target_format: str,
    output_path: str | None = None,
    quality: int = 90,
    background_color: tuple[int, int, int] = (255, 255, 255)
) -> tuple[bool, str | bytes]:
    """
    Converts a single image to the requested format.
    
    :param input_source: File path, bytes, or file-like object.
    :param target_format: Desired format (e.g. 'PNG', 'JPEG', 'WEBP', 'ICO', 'PDF', 'BMP').
    :param output_path: Destination path on disk. If None, returns in-memory bytes.
    :param quality: Compression quality (1-100) for JPEG and WEBP.
    :param background_color: Background color for alpha channel compositing (default: white).
    :return: (Success_bool, Result_path_or_bytes_or_error_str)
    """
    target_format_clean = target_format.upper().strip()
    pil_format = FORMAT_MAPPING.get(target_format_clean, target_format_clean)

    try:
        if isinstance(input_source, (str, os.PathLike)):
            img = Image.open(input_source)
        elif isinstance(input_source, bytes):
            img = Image.open(io.BytesIO(input_source))
        else:
            if hasattr(input_source, "seek"):
                input_source.seek(0)
            img = Image.open(input_source)

        with img:
            prepared_img = prepare_image_for_format(img, pil_format, background_color)

            save_kwargs: dict[str, Any] = {}
            if pil_format in ("JPEG", "WEBP"):
                save_kwargs["quality"] = max(1, min(quality, 100))
                save_kwargs["optimize"] = True
            elif pil_format == "PNG":
                save_kwargs["optimize"] = True
            elif pil_format == "ICO":
                save_kwargs["sizes"] = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

            if output_path:
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                prepared_img.save(output_path, format=pil_format, **save_kwargs)
                return True, output_path
            else:
                out_buffer = io.BytesIO()
                prepared_img.save(out_buffer, format=pil_format, **save_kwargs)
                return True, out_buffer.getvalue()

    except Exception as e:
        return False, str(e)

def batch_convert(
    items: list[dict],
    target_format: str,
    output_dir: str,
    quality: int = 90,
    progress_callback: Callable[[float, str], None] | None = None
) -> dict:
    """
    Batch converts a list of image items to the specified format and saves them to output_dir.
    
    :param items: List of dicts with 'source' (path or bytes/UploadedFile) and 'name'.
    :param target_format: Target format string (e.g. 'PNG', 'JPEG', 'WEBP').
    :param output_dir: Local destination folder.
    :param quality: Compression quality.
    :param progress_callback: Optional function (percent: float, message: str) -> None.
    :return: Summary dict with counts and output file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    ext_suffix = target_format.lower()
    if ext_suffix == "jpeg":
        ext_suffix = "jpg"

    successful_files: list[str] = []
    failed_files: list[dict] = []
    total = len(items)

    for idx, item in enumerate(items):
        source = item.get("source") or item.get("path")
        orig_name = item.get("name", f"image_{idx}")
        base_name = os.path.splitext(orig_name)[0]
        out_filename = f"{base_name}.{ext_suffix}"
        out_filepath = os.path.join(output_dir, out_filename)

        # Avoid collision if file exists
        counter = 1
        while os.path.exists(out_filepath):
            out_filepath = os.path.join(output_dir, f"{base_name}_{counter}.{ext_suffix}")
            counter += 1

        if progress_callback:
            percent = idx / max(total, 1)
            progress_callback(percent, f"Convirtiendo {orig_name}...")

        success, result = convert_single_image(
            input_source=source,
            target_format=target_format,
            output_path=out_filepath,
            quality=quality
        )

        if success:
            successful_files.append(out_filepath)
        else:
            failed_files.append({"name": orig_name, "error": str(result)})

    if progress_callback:
        progress_callback(1.0, "¡Conversión por lotes finalizada!")

    return {
        "total": total,
        "successful_count": len(successful_files),
        "failed_count": len(failed_files),
        "successful_files": successful_files,
        "failed_files": failed_files,
        "output_dir": output_dir,
    }

def create_zip_archive(file_paths: list[str]) -> bytes:
    """Packs given file paths into an in-memory ZIP archive buffer."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            if os.path.exists(file_path):
                arcname = os.path.basename(file_path)
                zip_file.write(file_path, arcname=arcname)
    return zip_buffer.getvalue()

def list_converted_images(directory: str) -> list[dict]:
    """Lists existing converted image files in the target directory sorted by mtime."""
    if not os.path.exists(directory):
        return []

    files_info = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_IMAGE_INPUT_EXTS:
                stat = os.stat(filepath)
                files_info.append({
                    "name": filename,
                    "path": filepath,
                    "ext": ext,
                    "size_kb": round(stat.st_size / 1024, 2),
                    "mtime": stat.st_mtime,
                })

    files_info.sort(key=lambda x: x["mtime"], reverse=True)
    return files_info
