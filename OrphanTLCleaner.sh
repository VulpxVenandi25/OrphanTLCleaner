#!/bin/bash

# Obtener la ruta absoluta del directorio del script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Nombre de la carpeta del entorno virtual (puedes cambiarlo si usas otro, por ejemplo .venv)
VENV_DIR=".venv"

echo "=== Iniciando verificaciones para Limpiador de TLs Huérfanas ==="

# 1. Verificar si el entorno virtual existe. Si no, crearlo e instalar dependencias.
if [ ! -d "$VENV_DIR" ]; then
    echo "[!] No se encontró el entorno virtual '$VENV_DIR'. Creando uno nuevo..."
    python3 -m venv "$VENV_DIR"
    
    echo "[*] Activando el entorno virtual e instalando dependencias..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    
    # Si tienes un archivo requirements.txt, lo instala. Si instalas el paquete en modo editable (ej. pip install -e .), ajústalo aquí.
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "[*] Instalando dependencias básicas (pywebview y PyQt)..."
        pip install pywebview PyQt5
        # Si tu proyecto es instalable localmente, descomenta la siguiente línea:
        # pip install -e .
    fi
else
    # Si ya existe, lo activamos
    source "$VENV_DIR/bin/activate"
fi

# 2. Verificar si falta alguna dependencia crítica (ejemplo: pywebview o webview)
if ! python3 -c "import webview" &> /dev/null; then
    echo "[!] Se detectó que falta la librería 'pywebview'. Reinstalando dependencias..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        pip install pywebview PyQt5
    fi
fi

# 3. Configurar variables de entorno específicas para Linux (evita problemas de GPU/Sandboxing en WebView)
export QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu --no-sandbox --disable-gpu-compositing"

echo "[*] Ejecutando la aplicación..."
python3 main.py

# Desactivar el entorno al salir (opcional)
deactivate
