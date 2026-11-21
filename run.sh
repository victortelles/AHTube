#!/usr/bin/env bash
# ========================================================
#       AHTube Studio - POSIX Shell Launcher
#       Compatible with Linux, macOS, and Git Bash
# ========================================================

set -e

# ANSI Color Codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================================${NC}"
echo -e "${CYAN}       AHTube Studio - Multi-Platform Launcher          ${NC}"
echo -e "${CYAN}========================================================${NC}"
echo ""

# 1. Resolve Script Directory Anchor
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 2. Check Git Status
if command -v git >/dev/null 2>&1; then
    echo -e "${GRAY}[*] Verificando repositorio Git...${NC}"
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        echo -e "${YELLOW}[i] Nota: Se detectaron cambios locales no confirmados en Git.${NC}"
    else
        echo -e "${GREEN}[OK] Repositorio Git limpio y sincronizado.${NC}"
    fi
    echo ""
fi

# 3. Detect Python 3.10+ Interpreter
echo -e "${GRAY}[*] Verificando intérprete Python 3.10+...${NC}"
PYTHON_BIN=""

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
fi

if [ -z "$PYTHON_BIN" ]; then
    echo -e "${RED}[ERROR] Python no está instalado o no se encuentra en el PATH.${NC}"
    echo -e "Instala Python 3.10 o superior (ej: sudo apt install python3 python3-venv).${NC}"
    exit 1
fi

if ! "$PYTHON_BIN" -c "import sys; min_v = (3, 10); sys.exit(0 if sys.version_info >= min_v else 1)" 2>/dev/null; then
    CURRENT_VER=$("$PYTHON_BIN" --version 2>&1)
    echo -e "${RED}[ERROR] Se requiere Python 3.10 o superior. Detectado: $CURRENT_VER${NC}"
    exit 1
fi

echo -e "${GREEN}[OK] $($PYTHON_BIN --version) detectado.${NC}"
echo ""

# 4. Bootstrap Virtual Environment (.venv)
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_STREAMLIT="$VENV_DIR/bin/streamlit"

# Handle Windows Git Bash / MSYS paths if applicable
if [ ! -f "$VENV_PYTHON" ] && [ -f "$VENV_DIR/Scripts/python.exe" ]; then
    VENV_PYTHON="$VENV_DIR/Scripts/python.exe"
    VENV_STREAMLIT="$VENV_DIR/Scripts/streamlit.exe"
fi

if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${GRAY}[*] Creando entorno virtual .venv...${NC}"
    "$PYTHON_BIN" -m venv "$VENV_DIR"
    echo -e "${GREEN}[OK] Entorno virtual creado exitosamente.${NC}"
    echo ""
    # Re-evaluate binary path after venv creation
    if [ -f "$VENV_DIR/bin/python" ]; then
        VENV_PYTHON="$VENV_DIR/bin/python"
        VENV_STREAMLIT="$VENV_DIR/bin/streamlit"
    else
        VENV_PYTHON="$VENV_DIR/Scripts/python.exe"
        VENV_STREAMLIT="$VENV_DIR/Scripts/streamlit.exe"
    fi
fi

# 5. Dependency Synchronization
if [ ! -f "$VENV_STREAMLIT" ]; then
    echo -e "${GRAY}[*] Instalando dependencias desde requirements.txt...${NC}"
    "$VENV_PYTHON" -m pip install --upgrade pip
    "$VENV_PYTHON" -m pip install -r "$SCRIPT_DIR/requirements.txt"
    echo -e "${GREEN}[OK] Dependencias instaladas correctamente.${NC}"
    echo ""
fi

# 6. Launch Streamlit Application
echo -e "${CYAN}========================================================${NC}"
echo -e "${CYAN}  Iniciando AHTube Studio en Streamlit...               ${NC}"
echo -e "${CYAN}========================================================${NC}"
echo ""

exec "$VENV_STREAMLIT" run "$SCRIPT_DIR/app.py"
