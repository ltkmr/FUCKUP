#!/bin/bash
set -e

echo "🌐 Updating main branch on GitHub..."

# Make sure we're in the root and on main
cd "$(dirname "$0")"
git checkout master

# Stage all local changes
echo "📦 Staging changes..."
git add .

# Create commit (if needed)
if git diff --cached --quiet; then
  echo "✅ No changes to commit."
else
  git commit -m "🔄 Update project state $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Push to GitHub
echo "🚀 Pushing to main..."
git push origin master

echo "✅ Main branch is up to date."
