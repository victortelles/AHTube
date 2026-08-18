import os
import sys
import time
import ctypes
import subprocess

def open_folder_in_foreground(directory: str) -> None:
    """Opens the target directory in File Explorer and brings it to the foreground."""
    abs_path = os.path.abspath(directory)
    os.makedirs(abs_path, exist_ok=True)
    
    if sys.platform == "win32":
        subprocess.Popen(['explorer', os.path.normpath(abs_path)])
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
