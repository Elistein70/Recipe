"""
EatKosher - Premium Kosher Recipe Assistant
Main entry point for Streamlit app

This is the landing page that redirects to the New Recipe page
"""

import streamlit as st
from auth import check_authentication, get_current_family_name, logout
from utils.shabbat_times import display_shabbat_banner

# Page config
st.set_page_config(
    page_title="EatKosher - Home",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication
check_authentication()

# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("""
        <h1 style='text-align: center; color: #1E3A8A; font-size: 3em;'>
            🍲 EatKosher – אכילת כשר
        </h1>
        <p style='text-align: center; font-size: 1.3em; color: #4B5563;'>
            Your Premium Kosher Recipe Assistant for the Orthodox Jewish Community
        </p>
    """, unsafe_allow_html=True)
with col2:
    st.write(f"**👨‍👩‍👧‍👦 {get_current_family_name()}**")
    if st.button("Logout", type="secondary"):
        logout()

st.markdown("---")

# Shabbat countdown
display_shabbat_banner()

st.markdown("---")

# Welcome message
st.markdown("""
## Welcome to EatKosher!

Your personal kosher recipe assistant, designed exclusively for the Orthodox Jewish community in Lakewood, Monsey, Boro Park, and Flatbush.

### 🌟 Features:

- **🍲 AI-Powered Recipe Generation**: Get custom recipes based on what you have in your kitchen
- **✅ Strict Kashrut Standards**: Only trusted hechsherim (OK, Star-K, Kof-K, OU, CRC, Tartikov, Hisachdus)
- **🏪 Local Store Focus**: Recipes use ingredients from Season, Kosher West, Evergreen, Gourmet Glatt, N&K, The Grove
- **⚙️ Dietary Options**: Chalav Yisrael, Pas Yisrael, Yoshon, Pesach mode (with gebrochts/kitniyot options)
- **🔄 Smart Substitutions**: Find kosher alternatives for missing ingredients
- **💾 Personal Recipe Box**: Save, search, and organize your favorite recipes
- **📄 PDF Export**: Print beautiful recipe cards for offline use
- **🕯️ Shabbat Times**: Always know when to light candles

### 📖 How to Use:

1. **Create a Recipe**: Go to "New Recipe" page and describe what you want to cook
2. **Set Restrictions**: Toggle your dietary requirements (Chalav Yisrael, Pas Yisrael, etc.)
3. **Check Ingredients**: Review the recipe and check off what you have
4. **Find Substitutes**: Missing something? Get kosher substitutes from local stores
5. **Save & Organize**: Rate and tag your recipes for easy finding later
6. **Export**: Download PDFs to print or share

### 🎯 Perfect For:

- Planning Shabbos and Yom Tov meals
- Quick weeknight dinners
- Using up ingredients in your pantry
- Discovering new kosher recipes
- Teaching children to cook
- Building your family recipe collection

---

### 👉 Get Started

Click **"New Recipe"** in the sidebar to begin, or visit **"My Saved Recipes"** to view your collection!
""")

# Quick stats in columns
st.markdown("---")
st.subheader("📊 Your EatKosher Stats")

import sqlite3
from auth import get_current_user_pin

db_path = "data/recipes.db"
try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    user_pin = get_current_user_pin()

    # Count recipes
    c.execute('SELECT COUNT(*) FROM recipes WHERE user_pin = ?', (user_pin,))
    recipe_count = c.fetchone()[0]

    # Count 5-star recipes
    c.execute('SELECT COUNT(*) FROM recipes WHERE user_pin = ? AND rating = 5', (user_pin,))
    five_star_count = c.fetchone()[0]

    conn.close()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📖 Total Recipes", recipe_count)
    with col2:
        st.metric("⭐ 5-Star Recipes", five_star_count)
    with col3:
        st.metric("👨‍👩‍👧‍👦 Family", get_current_family_name())

except Exception:
    st.info("Start creating recipes to see your stats here!")

# Sidebar
with st.sidebar:
    st.markdown("### 🏪 Trusted Local Stores")
    st.markdown("""
    - **Season** (Lakewood)
    - **Kosher West**
    - **Evergreen**
    - **Gourmet Glatt**
    - **N&K**
    - **The Grove**
    """)

    st.markdown("---")

    st.markdown("### ✅ Trusted Hechsherim")
    st.markdown("""
    - OK
    - Star-K
    - Kof-K
    - OU (Pas Yisroel & Yoshon)
    - CRC
    - Tartikov
    - Hisachdus
    """)

    st.markdown("---")

    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - Be specific about occasions (Shabbos, Yom Tov, weeknight)
    - Mention serving sizes
    - Include time constraints
    - Note missing ingredients
    """)
