#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "🔮 Bootstrapping FUCKUP² Oracle Machine..."
echo "Project directory: $PROJECT_DIR"
echo "-------------------------------------------"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Install Python 3 first."
    exit 1
fi

# Check python3-venv module
if ! python3 -m venv --help > /dev/null 2>&1; then
    echo "❌ python3-venv module is missing. Installing..."
    sudo apt update
    sudo apt install python3-venv -y
fi

# Check and (re)create virtual environment if necessary
if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "🧪 Virtual environment missing or incomplete. Creating fresh venv..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip and setuptools
echo "🚀 Upgrading pip and setuptools..."
pip install --upgrade pip setuptools

# Install dependencies robustly
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "🔍 Checking Python dependencies..."
    pip check > /dev/null 2>&1 || {
        echo "📦 Installing Python dependencies from requirements.txt..."
        pip install -r "$PROJECT_DIR/requirements.txt"
    }
else
    echo "⚠️ No requirements.txt found. Skipping package installation."
fi

# Check essential directories
echo "🗂️ Ensuring data folders exist..."
mkdir -p "$PROJECT_DIR/data" "$PROJECT_DIR/logs" "$PROJECT_DIR/archive" "$PROJECT_DIR/oracle"

# Check disk space
echo "💾 Disk space:"
df -h /

# Check printer status
echo "🖨️ Printer status:"
if lpstat -p | grep -q "enabled"; then
    echo "✅ Printer is enabled."
else
    echo "⚠️ Printer may not be ready. Check printer configuration."
fi

# Optional: Check network (for data fetching later)
echo "🌐 Checking internet connectivity..."
if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
    echo "✅ Internet connectivity: OK"
else
    echo "⚠️ No internet connectivity detected. Data fetching might fail."
fi

# Optional: Print test page
echo "🖨️ Printing bootstrap test page..."
echo "FUCKUP² Oracle bootstrapped successfully at $(date)" | lp || echo "⚠️ Printer test failed."

# Final status
echo "-------------------------------------------"
echo "✅ Bootstrap complete! Oracle is operational."
echo "Activate environment manually with:"
echo "source venv/bin/activate"
echo "-------------------------------------------"

