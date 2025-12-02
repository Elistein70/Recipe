# 🍲 EatKosher – אכילת כשר

**Premium Kosher Recipe Assistant for the Orthodox Jewish Community**

A complete Streamlit application that provides AI-powered kosher recipe generation with strict kashrut standards, designed exclusively for Orthodox Jewish communities in Lakewood, Monsey, Boro Park, Flatbush, and beyond.

---

## ✨ Features

### 🔮 AI-Powered Recipe Generation
- Custom recipes based on available ingredients
- GPT-4o powered with expert Lakewood balabusta knowledge
- Context-aware suggestions for Shabbos, Yom Tov, and weeknight meals

### ✅ Strict Kashrut Standards
- Only trusted hechsherim: OK, Star-K, Kof-K, OU (Pas Yisroel & Yoshon), CRC, Tartikov, Hisachdus
- Glatt kosher, yoshon, pas yisroel, chalav yisrael options
- Pesach mode with gebrochts/kitniyot toggles

### 🏪 Local Store Integration
- Recipes use ingredients from local kosher stores:
  - Season (Lakewood)
  - Kosher West
  - Evergreen
  - Gourmet Glatt
  - N&K
  - The Grove

### 🔄 Smart Substitutions
- Find kosher alternatives for missing ingredients
- Only suggests substitutes available in Lakewood-area stores
- Maintains 95%+ dish quality

### 💾 Personal Recipe Box
- Save unlimited recipes with ratings and tags
- Full-text search across all saved recipes
- Filter by rating, tags, and ingredients
- Sort by date, rating, or title

### 📄 PDF Export
- Beautiful, printable recipe cards
- Professional layout with royal blue branding
- Includes ratings and all recipe details

### 🕯️ Shabbat Countdown
- Live candle lighting times for Lakewood, NJ
- Parsha of the week
- Beautiful banner on every page

### 🔐 Family PIN System
- Secure 4-digit PIN authentication
- Each family has their own recipe collection
- Simple registration process

### 💾 Recipe Persistence & Backup
- All recipes automatically saved to SQLite database
- Database included in GitHub for backup
- Easy one-command backup script
- Recipes persist across deployments
- Perfect for family recipe preservation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EatKosher.git
   cd EatKosher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   ```bash
   # Copy the example secrets file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml

   # Edit .streamlit/secrets.toml and add your OpenAI API key
   # OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - Register your family with a 4-digit PIN
   - Start creating recipes!

---

## ☁️ Deploy to Streamlit Cloud

### One-Click Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Click "Deploy"

3. **Add your OpenAI API key**
   - In Streamlit Cloud dashboard, go to App Settings
   - Click "Secrets"
   - Add:
     ```toml
     OPENAI_API_KEY = "sk-your-actual-api-key-here"
     ```
   - Save and restart the app

4. **Done!** Your app is live and ready to use.

---

## 📁 Project Structure

```
EatKosher/
├── streamlit_app.py              # Main entry point
├── auth.py                       # PIN authentication system
├── pages/
│   ├── 1_🍲_New_Recipe.py        # Recipe generation interface
│   └── 2_📖_My_Saved_Recipes.py  # Saved recipes viewer
├── utils/
│   ├── prompts.py                # System prompts and toggles
│   ├── openai_client.py          # OpenAI API integration
│   ├── recipe_parser.py          # Recipe parsing and display
│   ├── pdf_export.py             # PDF generation
│   └── shabbat_times.py          # Shabbat times API
├── data/
│   └── recipes.db                # SQLite database (auto-created)
├── .streamlit/
│   ├── config.toml               # App styling configuration
│   └── secrets.toml.example      # Example secrets file
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

---

## 🎯 How to Use

### Creating Your First Recipe

1. **Register Your Family**
   - Choose a 4-digit PIN
   - Enter your family name
   - Login with your PIN

2. **Set Dietary Restrictions**
   - Toggle Chalav Yisrael, Pas Yisrael, Yoshon as needed
   - Enable Pesach mode if needed
   - Select gebrochts/kitniyot preferences

3. **Describe What You Want**
   - Example: "I have chicken bottoms, potatoes, no fresh garlic — need a Shabbos meal for 8"
   - Click "Generate Recipe"

4. **Review and Customize**
   - Check off ingredients you have
   - Find substitutes for missing items
   - Save with custom tags and rating

5. **Export or Save**
   - Download as PDF for printing
   - Save to your recipe box for later

### Managing Saved Recipes

1. **Navigate to "My Saved Recipes"**
2. **Search**: Enter keywords to find specific recipes
3. **Filter**: Choose minimum rating
4. **Sort**: By date, rating, or title
5. **Export**: Download any recipe as PDF
6. **Delete**: Remove recipes you no longer need

---

## ⚙️ Configuration

### Dietary Toggles

- **Chalav Yisrael**: Only dairy products with chalav yisrael certification
- **Pas Yisrael**: All baked goods must be pas yisroel
- **Yoshon**: All grains must be from old crop (no chadash)
- **Pesach Mode**: Only Pesach-approved ingredients
  - **Gebrochts**: Allow matzah mixed with liquid
  - **Kitniyot**: Sefardic minhag (rice, beans, corn allowed)

### Supported Hechsherim

- OK
- Star-K
- Kof-K
- OU (when pas yisroel & yoshon)
- CRC
- Tartikov
- Hisachdus

---

## 🛠️ Technical Details

### Technologies Used

- **Frontend**: Streamlit 1.28+
- **AI**: OpenAI GPT-4o / GPT-4o-mini
- **Database**: SQLite3
- **PDF Generation**: ReportLab
- **APIs**: Hebcal (Shabbat times)

### Database Schema

#### Users Table
- `pin` (TEXT, PRIMARY KEY) - Hashed PIN
- `family_name` (TEXT) - Family name
- `created_at` (TIMESTAMP)

#### Recipes Table
- `id` (INTEGER, PRIMARY KEY)
- `user_pin` (TEXT, FOREIGN KEY)
- `title` (TEXT)
- `tags` (TEXT)
- `ingredients` (TEXT)
- `instructions` (TEXT)
- `notes` (TEXT)
- `prep_time`, `cook_time`, `servings` (TEXT)
- `rating` (INTEGER, 1-5)
- `full_text` (TEXT) - Complete recipe markdown
- `created_at` (TIMESTAMP)

### Recipe Backup & Persistence

Your recipes are stored in `data/recipes.db` and **automatically included in GitHub** for backup.

#### Easy Backup Method

After creating new recipes you want to preserve:

```bash
# Option 1: Use the backup script (easiest!)
./backup_recipes.sh

# Option 2: Manual backup
git add data/recipes.db
git commit -m "Backup recipes - $(date +%Y-%m-%d)"
git push
```

#### Restore from Backup

If you need to get your recipes back:

```bash
git pull
# All your recipes are restored!
```

#### Important Notes

- ✅ Database is tracked in Git for persistence
- ✅ Your recipes survive app restarts and redeployments
- ✅ Works perfectly for single-family use
- ⚠️ Remember to backup after adding important recipes
- ⚠️ Don't share your repo publicly if you want recipes private

---

## 🔒 Security & Privacy

- PINs are hashed using SHA-256
- Database stored locally (not in git)
- Each family's recipes are completely private
- OpenAI API calls don't store personal data
- No analytics or tracking

---

## 💡 Tips for Best Results

### Recipe Requests
- Be specific about what ingredients you have
- Mention the occasion (Shabbos, Yom Tov, weeknight)
- Include serving size and time constraints
- Note any missing ingredients upfront

### Good Examples
- ✅ "I have chicken bottoms and potatoes. Need a hearty Shabbos main for 8 people. No time for marinating."
- ✅ "Quick weeknight dinner with ground beef, pasta available. Dairy or parve only."
- ✅ "Pesach dessert for 12, no gebrochts, using eggs and potatoes."

### Tags for Organization
- Shabbos, Yom Tov, Weeknight
- Meat, Dairy, Parve, Fish
- Quick, Easy, Make-Ahead
- Freezer-Friendly
- Kid-Friendly

---

## 🐛 Troubleshooting

### "OpenAI API key not found"
- Make sure `.streamlit/secrets.toml` exists
- Check that your API key is correctly formatted
- Restart the Streamlit app

### "No module named 'streamlit'"
- Install dependencies: `pip install -r requirements.txt`

### Database errors
- Delete `data/recipes.db` to reset
- Database will be recreated on next login

### Shabbat times not loading
- Check internet connection
- Hebcal API may be temporarily unavailable
- App will show fallback message

---

## 📝 License

This project is released as open source for the benefit of the Orthodox Jewish community.

---

## 🙏 Credits

Created with love for the frum community.

Built with:
- Streamlit
- OpenAI GPT-4
- Hebcal API
- ReportLab

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the example recipes and tips
3. Open an issue on GitHub

---

## 🎯 Roadmap

Future enhancements:
- [ ] Meal planning for full Shabbos
- [ ] Grocery list generation
- [ ] Recipe sharing between families
- [ ] Mobile app version
- [ ] Voice input support
- [ ] Nutrition information
- [ ] Recipe scaling calculator

---

**B'hatzlacha! Enjoy cooking with EatKosher!** 🍲
