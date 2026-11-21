@echo off
setlocal enabledelayedexpansion

title AHTube Studio Launcher
echo ========================================================
echo        AHTube Studio - Multi-Platform Launcher
echo ========================================================
echo.

:: 1. Navigate to script root
cd /d "%~dp0"

:: 2. Check Git status if git is available
where git >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Verificando repositorio Git...
    for /f "delims=" %%i in ('git status --porcelain 2^>nul') do (
        set "GIT_DIRTY=1"
    )
    if defined GIT_DIRTY (
        echo [i] Nota: Se detectaron cambios locales no confirmados en Git.
    ) else (
        echo [OK] Repositorio sincronizado y limpio.
    )
    echo.
)

:: 3. Check Python installation and version (>= 3.10)
echo [*] Verificando interprete Python...
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH.
    echo Por favor instala Python 3.10 o superior desde https://www.python.org/
    pause
    exit /b 1
)

python -c "import sys; min_v = (3, 10); sys.exit(0 if sys.version_info >= min_v else 1)" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Se requiere Python 3.10 o superior.
    python --version
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo [OK] %%v detectado.
echo.

:: 4. Check or bootstrap .venv
if not exist ".venv\Scripts\python.exe" (
    echo [*] Creando entorno virtual .venv...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Fallo al crear el entorno virtual .venv.
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual .venv creado exitosamente.
    echo.
)

:: 5. Verify / install requirements
if not exist ".venv\Scripts\streamlit.exe" (
    echo [*] Instalando dependencias desde requirements.txt...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\pip.exe" install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Error durante la instalacion de paquetes.
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas correctamente.
    echo.
)

:: 6. Launch Streamlit Application
echo ========================================================
echo  Iniciando AHTube Studio en Streamlit...
echo ========================================================
echo.
".venv\Scripts\streamlit.exe" run app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] La aplicacion se cerro con codigo de error %ERRORLEVEL%.
    pause
)
