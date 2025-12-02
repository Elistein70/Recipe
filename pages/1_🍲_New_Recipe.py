"""
EatKosher - New Recipe Page
Main interface for generating kosher recipes with OpenAI
"""

import streamlit as st
import sys
import os
import sqlite3

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import check_authentication, get_current_user_pin, get_current_family_name, logout
from utils.shabbat_times import display_shabbat_banner
from utils.prompts import get_system_prompt
from utils.openai_client import get_recipe_from_openai, get_substitutions
from utils.recipe_parser import display_recipe_with_checkboxes, get_recipe_for_save, parse_recipe
from utils.pdf_export import create_recipe_pdf

# Page config
st.set_page_config(
    page_title="EatKosher - New Recipe",
    page_icon="🍲",
    layout="wide"
)

# Check authentication
check_authentication()

# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("""
        <h1 style='color: #1E3A8A;'>
            🍲 EatKosher – אכילת כשר
        </h1>
    """, unsafe_allow_html=True)
with col2:
    st.write(f"**👨‍👩‍👧‍👦 {get_current_family_name()}**")
    if st.button("Logout", type="secondary"):
        logout()

# Shabbat countdown banner
display_shabbat_banner()

st.markdown("---")

# Dietary toggles toolbar
st.subheader("⚙️ Dietary Restrictions")

col1, col2, col3 = st.columns(3)

with col1:
    chalav_yisrael = st.checkbox("Chalav Yisrael Only", value=False, key="chalav_yisrael")
    pas_yisrael = st.checkbox("Pas Yisrael Only", value=True, key="pas_yisrael")

with col2:
    yoshon = st.checkbox("Yoshon Only", value=True, key="yoshon")
    pesach_mode = st.checkbox("Pesach Mode", value=False, key="pesach_mode")

with col3:
    if pesach_mode:
        gebrochts = st.checkbox("Gebrochts (Matzah + Liquid OK)", value=False, key="gebrochts")
        kitniyot = st.checkbox("Kitniyot (Sefardic)", value=False, key="kitniyot")
    else:
        gebrochts = False
        kitniyot = False
        st.write("")
        st.write("")

st.markdown("---")

# Recipe request area
st.subheader("📝 What would you like to cook?")

user_request = st.text_area(
    "Describe what you have or what you're looking for",
    placeholder="Example: I have chicken bottoms, potatoes, no fresh garlic — need a Shabbos meal",
    height=120,
    key="user_request"
)

# Generate recipe button
if st.button("🔮 Generate Recipe", type="primary", use_container_width=True):
    if not user_request.strip():
        st.error("Please describe what you'd like to cook!")
    else:
        with st.spinner("Consulting the Lakewood balabusta... 👵"):
            # Prepare toggles
            toggles = {
                'chalav_yisrael': chalav_yisrael,
                'pas_yisrael': pas_yisrael,
                'yoshon': yoshon,
                'pesach_mode': pesach_mode,
                'gebrochts': gebrochts,
                'kitniyot': kitniyot
            }

            # Get system prompt with toggles
            system_prompt = get_system_prompt(toggles)

            # Generate recipe
            recipe = get_recipe_from_openai(user_request, system_prompt)

            # Store in session state
            st.session_state.current_recipe = recipe
            st.session_state.current_toggles = toggles

        st.success("Recipe generated! Scroll down to view.")

# Display current recipe if it exists
if 'current_recipe' in st.session_state and st.session_state.current_recipe:
    st.markdown("---")
    st.markdown("## 📖 Your Recipe")

    # Display recipe with checkboxes
    missing_ingredients = display_recipe_with_checkboxes(st.session_state.current_recipe)

    st.markdown("---")

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        # Find substitutes button
        if missing_ingredients:
            if st.button("🔄 Find Kosher Substitutes", use_container_width=True):
                with st.spinner("Finding kosher substitutes..."):
                    system_prompt = get_system_prompt(st.session_state.current_toggles)
                    updated_recipe = get_substitutions(
                        st.session_state.current_recipe,
                        missing_ingredients,
                        system_prompt
                    )
                    st.session_state.current_recipe = updated_recipe
                    # Reset checkboxes
                    st.session_state.ingredient_checkboxes = {}
                    st.rerun()
        else:
            st.button("🔄 Find Kosher Substitutes", disabled=True, use_container_width=True)
            st.caption("Check off missing ingredients first")

    with col2:
        # Save recipe button
        if st.button("💾 Save Recipe", type="primary", use_container_width=True):
            st.session_state.show_save_dialog = True

    with col3:
        # Export PDF button
        recipe_data = parse_recipe(st.session_state.current_recipe)
        if recipe_data['title']:
            pdf_content = create_recipe_pdf(st.session_state.current_recipe)
            st.download_button(
                "📄 Export as PDF",
                data=pdf_content,
                file_name=f"{recipe_data['title'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    # Save dialog
    if st.session_state.get('show_save_dialog', False):
        st.markdown("---")
        st.subheader("💾 Save This Recipe")

        recipe_data = get_recipe_for_save(st.session_state.current_recipe)

        save_col1, save_col2 = st.columns(2)

        with save_col1:
            # Add custom tags
            custom_tags = st.text_input(
                "Add Tags (optional)",
                placeholder="e.g., Easy, Quick, Family Favorite",
                key="custom_tags"
            )

        with save_col2:
            # Rating
            rating = st.select_slider(
                "Rate This Recipe",
                options=[1, 2, 3, 4, 5],
                value=5,
                format_func=lambda x: "⭐" * x,
                key="rating"
            )

        save_button_col1, save_button_col2 = st.columns(2)

        with save_button_col1:
            if st.button("✅ Confirm Save", type="primary", use_container_width=True):
                # Save to database
                db_path = "data/recipes.db"
                conn = sqlite3.connect(db_path)
                c = conn.cursor()

                # Combine original tags with custom tags
                all_tags = recipe_data['tags']
                if custom_tags:
                    all_tags += f" | {custom_tags}"

                c.execute('''
                    INSERT INTO recipes (
                        user_pin, title, tags, ingredients, instructions,
                        notes, prep_time, cook_time, servings, rating, full_text
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    get_current_user_pin(),
                    recipe_data['title'],
                    all_tags,
                    recipe_data['ingredients'],
                    recipe_data['instructions'],
                    recipe_data['notes'],
                    recipe_data['prep_time'],
                    recipe_data['cook_time'],
                    recipe_data['servings'],
                    rating,
                    st.session_state.current_recipe
                ))

                conn.commit()
                conn.close()

                st.success("✅ Recipe saved to your collection!")
                st.session_state.show_save_dialog = False
                st.balloons()

        with save_button_col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_save_dialog = False
                st.rerun()

# Sidebar with tips
with st.sidebar:
    st.markdown("### 💡 Tips for Best Results")
    st.markdown("""
    - Be specific about what you have
    - Mention the occasion (Shabbos, weeknight, Yom Tov)
    - Include dietary needs
    - Note time constraints
    - Specify serving size

    **Example:**
    *"I have chicken bottoms and potatoes. Need a hearty Shabbos main for 8 people. No time for marinating."*
    """)

    st.markdown("---")
    st.markdown("### 🏪 Trusted Stores")
    st.markdown("""
    - Season (Lakewood)
    - Kosher West
    - Evergreen
    - Gourmet Glatt
    - N&K
    - The Grove
    """)
