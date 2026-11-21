<#
.SYNOPSIS
    AHTube Studio - Modern PowerShell Launcher
.DESCRIPTION
    Validates Git status, checks Python 3.10+, bootstraps virtualenv,
    installs requirements, and launches Streamlit with Sky/Slate Studio theme.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

function Write-StudioHeader {
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "       AHTube Studio - Multi-Platform Launcher          " -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Status([string]$Label, [string]$Message, [ConsoleColor]$Color) {
    Write-Host "[$Label] " -NoNewline -ForegroundColor $Color
    Write-Host $Message
}

Write-StudioHeader

# 1. Git Status Inspection
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Status "INFO" "Inspeccionando repositorio Git..." Gray
    try {
        $gitStatus = git status --porcelain 2>$null
        if ($gitStatus) {
            Write-Status "WARN" "Se detectaron cambios locales no confirmados en el repo." Yellow
        } else {
            Write-Status "OK" "Repositorio Git limpio y sincronizado." Green
        }
    } catch {
        Write-Status "WARN" "No se pudo consultar el estado de Git." Yellow
    }
    Write-Host ""
}

# 2. Python 3.10+ Validation
Write-Status "INFO" "Verificando intérprete Python..." Gray
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Status "ERROR" "Python no está instalado o no se encuentra en el PATH." Red
    Write-Host "Descárgalo e instálalo desde https://www.python.org/ (versión 3.10 o superior)." -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir..."
    exit 1
}

$versionCheck = & $pythonCmd.Source -c "import sys; min_v = (3, 10); sys.exit(0 if sys.version_info >= min_v else 1)" 2>$null
if ($LASTEXITCODE -ne 0) {
    $currentVer = & $pythonCmd.Source --version
    Write-Status "ERROR" "Se requiere Python 3.10 o superior. Versión actual: $currentVer" Red
    Read-Host "Presiona Enter para salir..."
    exit 1
}

$pythonVersionStr = & $pythonCmd.Source --version
Write-Status "OK" "$pythonVersionStr detectado correctamente." Green
Write-Host ""

# 3. Virtual Environment Check & Bootstrap
$venvDir = Join-Path $PSScriptRoot ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$venvStreamlit = Join-Path $venvDir "Scripts\streamlit.exe"

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Status "INFO" "Creando entorno virtual .venv..." Gray
    try {
        & $pythonCmd.Source -m venv "$venvDir"
        Write-Status "OK" "Entorno virtual creado en $venvDir" Green
    } catch {
        Write-Status "ERROR" "Error al crear entorno virtual: $_" Red
        Read-Host "Presiona Enter para salir..."
        exit 1
    }
    Write-Host ""
}

# 4. Dependency Synchronization
if (-not (Test-Path -LiteralPath $venvStreamlit)) {
    Write-Status "INFO" "Instalando paquetes requeridos desde requirements.txt..." Gray
    $venvPip = Join-Path $venvDir "Scripts\pip.exe"
    try {
        & $venvPython -m pip install --upgrade pip
        & $venvPip install -r (Join-Path $PSScriptRoot "requirements.txt")
        Write-Status "OK" "Dependencias instaladas con éxito." Green
    } catch {
        Write-Status "ERROR" "Error al instalar paquetes de requirements.txt: $_" Red
        Read-Host "Presiona Enter para salir..."
        exit 1
    }
    Write-Host ""
}

# 5. Launch Streamlit Application
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Iniciando AHTube Studio en Streamlit...               " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

try {
    & $venvStreamlit run (Join-Path $PSScriptRoot "app.py")
} catch {
    Write-Status "ERROR" "La ejecución de Streamlit falló: $_" Red
    Read-Host "Presiona Enter para salir..."
    exit 1
}
