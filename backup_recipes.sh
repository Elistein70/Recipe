#!/bin/bash
# EatKosher Recipe Backup Script
# Run this whenever you want to save your recipes to GitHub

echo "🍲 EatKosher Recipe Backup"
echo "=========================="
echo ""

# Check if there are changes to the database
if git diff --quiet data/recipes.db; then
    echo "✅ No new recipes to backup"
    echo ""
    echo "Your recipes are already saved in GitHub!"
else
    echo "📦 Found new recipes to backup..."
    echo ""

    # Add the database
    git add data/recipes.db

    # Get current date
    DATE=$(date +"%Y-%m-%d %H:%M")

    # Commit with timestamp
    git commit -m "Backup recipes - $DATE"

    # Push to GitHub
    echo ""
    echo "☁️  Pushing to GitHub..."
    git push

    echo ""
    echo "✅ Recipes backed up successfully!"
    echo ""
    echo "Your recipes are now safe in GitHub 🎉"
fi

echo ""
echo "Run this script anytime to backup new recipes!"
