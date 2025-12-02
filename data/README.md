# EatKosher Database

This folder contains the SQLite database for EatKosher app.

## 📦 What's Stored Here

- `recipes.db` - Your family accounts and saved recipes

## 🔄 How Persistence Works

### For GitHub Backups (Manual)

When you want to back up your data to GitHub:

```bash
git add data/recipes.db
git commit -m "Backup recipes and accounts"
git push
```

### For Streamlit Cloud

- The database is automatically included when you deploy
- Your recipes will persist across app updates
- **Important:** If you redeploy or the app restarts, use the latest database from GitHub

## 🔒 Security Note

The database contains:
- Hashed PINs (SHA-256) - secure
- Recipe data - not sensitive
- Family names - minimal personal info

**This is safe for family use**, but don't share your GitHub repo publicly if you want to keep recipes private.

## 📋 How to Backup Regularly

### Option 1: Manual Backup (Recommended)

After adding new recipes you want to keep:

```bash
cd /path/to/Recipe
git add data/recipes.db
git commit -m "Update recipes - [date]"
git push
```

### Option 2: Automatic (Advanced)

You could set up a GitHub Action to auto-backup, but manual is fine for family use.

## 🔄 How to Restore

If you need to restore from GitHub:

```bash
git pull
# Your recipes are back!
```

## ⚠️ Important Notes

1. **Don't delete this database** - it contains all your recipes and accounts
2. **Back up regularly** - Commit to GitHub after adding important recipes
3. **One database per family** - This works best for single-family use
4. **Database conflicts** - If multiple people use different instances, you may get conflicts. Last push wins.

## 📊 Database Schema

### Users Table
- `pin` (TEXT, PRIMARY KEY) - Hashed PIN
- `family_name` (TEXT)
- `created_at` (TIMESTAMP)

### Recipes Table
- `id` (INTEGER, PRIMARY KEY)
- `user_pin` (TEXT, FOREIGN KEY)
- `title`, `tags`, `ingredients`, `instructions`, `notes`
- `prep_time`, `cook_time`, `servings`
- `rating` (1-5 stars)
- `full_text` (complete recipe markdown)
- `created_at` (TIMESTAMP)
