#!/bin/bash

# Fail fast if any command errors
set -e

# Project root
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "🔮 Bootstrapping FUCKUP² Oracle Machine..."
echo "Project directory: $PROJECT_DIR"
echo "-------------------------------------------"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Check for pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Installing..."
    sudo apt update
    sudo apt install python3-pip -y
fi

# Check for virtualenv
if [ ! -d "$VENV_DIR" ]; then
    echo "🧪 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip inside venv
echo "🚀 Upgrading pip..."
pip install --upgrade pip

# Install or verify dependencies
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "🔍 Verifying Python dependencies..."

    # Use pip check to see if anything is missing
    MISSING=$(pip freeze --exclude-editable | grep -vf "$PROJECT_DIR/requirements.txt" || true)

    if [ -n "$MISSING" ]; then
        echo "⚠️ Missing packages detected:"
        echo "$MISSING"
        echo "📦 Installing all dependencies from requirements.txt..."
        pip install -r "$PROJECT_DIR/requirements.txt"
    else
        echo "✅ All required Python packages are already installed."
    fi
else
    echo "⚠️ requirements.txt not found! Skipping Python package installation."
fi

# Prepare directories
echo "🗂️  Ensuring data folders exist..."
mkdir -p "$PROJECT_DIR/data" "$PROJECT_DIR/logs" "$PROJECT_DIR/archive" "$PROJECT_DIR/oracle"

# Check printer status
echo "🖨️  Checking printer status..."
if lpstat -p | grep -q "enabled"; then
    echo "✅ Printer is enabled and ready."
else
    echo "⚠️ Printer may not be ready. Check printer configuration."
fi

# Check disk space
echo "💾 Disk space overview:"
df -h /

# Optional: Print test page
echo "🖨️  Printing test page..."
echo "FUCKUP² Oracle bootstrapped successfully at $(date)" | lp || echo "⚠️ Printer test failed."

# Final message
echo "-------------------------------------------"
echo "✅ Bootstrap complete! Environment is ready."
echo "To activate the virtual environment manually later:"
echo "source venv/bin/activate"
echo "-------------------------------------------"

