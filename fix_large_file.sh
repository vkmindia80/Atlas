#!/bin/bash
set -e

echo "🔍 Checking for git-filter-repo..."
if ! command -v git-filter-repo &> /dev/null
then
    echo "⚠️ git-filter-repo not found. Installing via pip..."
    pip install git-filter-repo
fi

echo "🚀 Removing large cache file from history..."
git filter-repo --path frontend/node_modules/.cache/default-development/3.pack --invert-paths

echo "📝 Updating .gitignore..."
cat <<EOL >> .gitignore

# Ignore node_modules and cache
node_modules/
.cache/
EOL

git add .gitignore
git commit -m "Ignore node_modules and cache files"

echo "📤 Force pushing cleaned branch to GitHub..."
git push origin main --force

echo "✅ Done! Large file removed and repo cleaned."
echo "⚠️ Reminder: Anyone who cloned this repo must reclone because history was rewritten."
