import os
import sys
import shutil
import yt_dlp

# Automatically make ffmpeg and ffprobe available in PATH
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass

def resolve_ffmpeg_path() -> str | None:
    """Check if ffmpeg directory can be resolved."""
    ffmpeg_system = shutil.which("ffmpeg")
    if ffmpeg_system:
        return os.path.dirname(ffmpeg_system)
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(ffmpeg_exe):
            return os.path.dirname(ffmpeg_exe)
    except Exception:
        pass
    return None

def fetch_video_metadata(url: str) -> dict | None:
    """Fetch video title, thumbnail, duration, and author without downloading."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'mweb']
            }
        },
    }
    ffmpeg_loc = resolve_ffmpeg_path()
    if ffmpeg_loc:
        ydl_opts['ffmpeg_location'] = ffmpeg_loc

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return None
            return {
                'title': info.get('title', 'Sin título'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Desconocido'),
                'view_count': info.get('view_count', 0),
            }
    except Exception as e:
        sys.stderr.write(f"Metadata error: {e}\n")
        return None

def extract_media(
    url: str,
    output_dir: str = "downloads",
    mode: str = "audio",
    audio_format: str = "mp3",
    audio_quality: str = "192",
    video_res: str = "best",
    progress_callback = None
) -> tuple[bool, str]:
    """Downloads media from YouTube url with customizable options."""
    os.makedirs(output_dir, exist_ok=True)
    ffmpeg_location = resolve_ffmpeg_path()

    def internal_hook(d: dict):
        if progress_callback and d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
            downloaded = d.get('downloaded_bytes', 0)
            percentage = downloaded / total
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            progress_callback(percentage, speed, eta)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [internal_hook] if progress_callback else [],
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'mweb']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location

    if mode == "audio":
        postprocessors = []
        if audio_format in ("mp3", "m4a", "wav"):
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_quality if audio_format == "mp3" else '5',
            })
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': postprocessors,
        })
    elif mode == "video":
        if video_res != "best" and video_res.isdigit():
            format_spec = f"bestvideo[height<={video_res}][ext=mp4]+bestaudio[ext=m4a]/best[height<={video_res}][ext=mp4]/best"
        else:
            format_spec = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        ydl_opts.update({
            'format': format_spec,
        })
    else:
        return False, f"Modo no soportado: {mode}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if mode == "audio" and audio_format in ("mp3", "m4a", "wav"):
                base, _ = os.path.splitext(filename)
                filename = f"{base}.{audio_format}"
            return True, filename
    except Exception as e:
        return False, str(e)

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
