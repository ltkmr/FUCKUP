#!/bin/bash
set -e  # Exit on error

# === CONFIGURATION ===
REPO_DIR=$(pwd)
WEB_DIR="$REPO_DIR/web"
BRANCH="gh-pages"
TMP_DIR="$REPO_DIR/.gh-pages-temp"
TMP_NAME=$(basename "$TMP_DIR")
GIT_WORKTREE_DIR="$REPO_DIR/.git/worktrees/$TMP_NAME"

echo "📦 Preparing to publish $WEB_DIR to GitHub Pages..."

# === 1. Safety Checks ===
if [ ! -d "$WEB_DIR" ]; then
  echo "❌ Error: web/ directory not found!"
  exit 1
fi

# === 2. Clean up old or broken worktree state ===
echo "🧼 Cleaning up stale Git worktree references..."
git worktree prune

if [ -d "$GIT_WORKTREE_DIR" ]; then
  echo "⚰️  Removing stale metadata from .git/worktrees/$TMP_NAME..."
  rm -rf "$GIT_WORKTREE_DIR"
fi

if [ -d "$TMP_DIR" ]; then
  echo "🧹 Removing leftover temp directory..."
  rm -rf "$TMP_DIR"
fi

# === 3. Sync local branch to remote before worktree is created ===
if git ls-remote --exit-code --heads origin "$BRANCH" > /dev/null; then
  echo "📥 Remote branch '$BRANCH' exists. Syncing and checking out..."
  git fetch origin "$BRANCH"
  git branch -f "$BRANCH" "origin/$BRANCH"
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

# === 4. Copy web contents ===
echo "🧹 Cleaning existing files in worktree..."
rm -rf "$TMP_DIR"/*

echo "📁 Copying files to branch worktree..."
shopt -s dotglob  # Include dotfiles like .nojekyll
cp -r "$WEB_DIR"/* "$TMP_DIR"
shopt -u dotglob

# === 5. Optional: Add .nojekyll to bypass GitHub’s Jekyll processing
touch "$TMP_DIR/.nojekyll"

# === 6. Commit and push ===
cd "$TMP_DIR"
git add .
git commit -m "🔄 Update web archive $(date '+%Y-%m-%d %H:%M:%S')" || echo "ℹ️ No changes to commit."
git push origin "$BRANCH"

# === 7. Cleanup ===
cd "$REPO_DIR"
git worktree remove --force "$TMP_DIR"
rm -rf "$TMP_DIR"

echo "✅ GitHub Pages updated successfully on branch '$BRANCH'."
