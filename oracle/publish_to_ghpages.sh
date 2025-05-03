#!/bin/bash
set -e  # Exit on error

# === CONFIGURATION ===
REPO_DIR=$(pwd)
WEB_DIR="$REPO_DIR/web"
BRANCH="gh-pages"
TMP_DIR="$REPO_DIR/.gh-pages-temp"

echo "📦 Preparing to publish $WEB_DIR to GitHub Pages..."

# === 1. Safety Checks ===
if [ ! -d "$WEB_DIR" ]; then
  echo "❌ Error: web/ directory not found!"
  exit 1
fi

# === 2. Clean up stale worktree references ===
git worktree prune

# === 3. Remove leftover worktree folder if it exists ===
rm -rf "$TMP_DIR"

# === 4. Check if branch exists remotely ===
if git ls-remote --exit-code --heads origin "$BRANCH" > /dev/null; then
  echo "📥 Remote branch '$BRANCH' exists. Checking it out..."
  git fetch origin "$BRANCH"
  git worktree add "$TMP_DIR" "$BRANCH"
else
  echo "🌱 Remote branch '$BRANCH' does not exist. Creating it..."
  git worktree add -B "$BRANCH" "$TMP_DIR"
  (
    cd "$TMP_DIR"
    git commit --allow-empty -m "🌱 Initial gh-pages branch"
    git push origin "$BRANCH"
  )
fi

# === 5. Copy web contents ===
echo "🧹 Cleaning existing files..."
rm -rf "$TMP_DIR"/*

echo "📁 Copying files to branch worktree..."
cp -r "$WEB_DIR"/* "$TMP_DIR"

# === 6. Commit and push ===
cd "$TMP_DIR"
git add .
git commit -m "🔄 Update web archive $(date '+%Y-%m-%d %H:%M:%S')" || echo "ℹ️ No changes to commit."
git push origin "$BRANCH"

# === 7. Cleanup ===
cd "$REPO_DIR"
git worktree remove "$TMP_DIR"
rm -rf "$TMP_DIR"

echo "✅ GitHub Pages updated successfully on branch '$BRANCH'."
