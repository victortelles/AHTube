import sys
import argparse
from src.extractor import extract_media

OUTPUT_DIRECTORY = "downloads"

def print_banner():
    print("========================================")
    print("   YT Audio & Video Extractor (CLI)   ")
    print("========================================")

def interactive_loop():
    print_banner()
    print("Pegá la URL del video de YouTube y presioná Enter.")
    print("Escribí 'q' o 'salir' para finalizar.\n")
    
    while True:
        try:
            url = input("YouTube URL > ").strip()
            if not url:
                continue
            if url.lower() in ('q', 'salir', 'exit', 'quit'):
                print("¡Hasta luego!")
                break
            
            print(f"\nIniciando extracción a MP3...")
            success = extract_media(url, output_dir=OUTPUT_DIRECTORY, mode="audio")
            if success:
                print(f" ✔ Completado. Guardado en la carpeta '{OUTPUT_DIRECTORY}'\n")
            else:
                print(" ✖ Ocurrió un error al procesar el video.\n")
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario. ¡Hasta luego!")
            break

def main():
    parser = argparse.ArgumentParser(description="YouTube Audio/Video CLI Extractor")
    parser.add_argument("url", nargs="?", help="URL del video de YouTube")
    parser.add_argument("--mode", choices=["audio", "video"], default="audio", help="Modo de descarga: audio (mp3) o video (mp4)")
    parser.add_argument("--output", default=OUTPUT_DIRECTORY, help="Carpeta de destino")
    
    args = parser.parse_args()
    
    if args.url:
        print(f"Modo: {args.mode.upper()} | Destino: {args.output}")
        success = extract_media(args.url, output_dir=args.output, mode=args.mode)
        sys.exit(0 if success else 1)
    else:
        interactive_loop()

if __name__ == "__main__":
    main()
