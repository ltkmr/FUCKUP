#!/bin/bash
set -e

# Optional: activate virtualenv if you use one
source venv/bin/activate 2>/dev/null || echo "⚠️ No venv found or activation skipped."

# Set commit message with timestamp
msg="🧭 Update on $(date '+%Y-%m-%d %H:%M:%S')"

# Git operations
echo "📦 Staging changes..."
git add .

echo "✍️ Committing changes..."
git commit -m "$msg" || echo "⚠️ Nothing new to commit."

echo "🚀 Pushing to main..."
git push origin main

echo "✅ Main branch updated successfully."
