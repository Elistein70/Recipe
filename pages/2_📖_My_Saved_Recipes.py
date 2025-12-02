"""
EatKosher - My Saved Recipes Page
Searchable personal recipe box with filters and PDF export
"""

import streamlit as st
import sys
import os
import sqlite3

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import check_authentication, get_current_user_pin, get_current_family_name, logout
from utils.pdf_export import create_recipe_pdf
from utils.recipe_parser import parse_recipe

# Page config
st.set_page_config(
    page_title="EatKosher - Saved Recipes",
    page_icon="📖",
    layout="wide"
)

# Check authentication
check_authentication()

# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("""
        <h1 style='color: #1E3A8A;'>
            📖 My Saved Recipes – ספר מתכונים
        </h1>
    """, unsafe_allow_html=True)
with col2:
    st.write(f"**👨‍👩‍👧‍👦 {get_current_family_name()}**")
    if st.button("Logout", type="secondary"):
        logout()

st.markdown("---")


def get_all_recipes(user_pin):
    """Get all recipes for the current user"""
    db_path = "data/recipes.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        SELECT id, title, tags, prep_time, cook_time, servings,
               rating, full_text, created_at
        FROM recipes
        WHERE user_pin = ?
        ORDER BY created_at DESC
    ''', (user_pin,))

    recipes = []
    for row in c.fetchall():
        recipes.append({
            'id': row[0],
            'title': row[1],
            'tags': row[2] or '',
            'prep_time': row[3] or '',
            'cook_time': row[4] or '',
            'servings': row[5] or '',
            'rating': row[6] or 0,
            'full_text': row[7],
            'created_at': row[8]
        })

    conn.close()
    return recipes


def search_recipes(user_pin, search_term, rating_filter, sort_by):
    """Search and filter recipes"""
    recipes = get_all_recipes(user_pin)

    # Filter by search term
    if search_term:
        search_term = search_term.lower()
        recipes = [
            r for r in recipes
            if (search_term in r['title'].lower() or
                search_term in r['tags'].lower() or
                search_term in r['full_text'].lower())
        ]

    # Filter by rating
    if rating_filter > 0:
        recipes = [r for r in recipes if r['rating'] >= rating_filter]

    # Sort
    if sort_by == "Newest First":
        recipes.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "Oldest First":
        recipes.sort(key=lambda x: x['created_at'])
    elif sort_by == "Highest Rated":
        recipes.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_by == "Title A-Z":
        recipes.sort(key=lambda x: x['title'])

    return recipes


def delete_recipe(recipe_id):
    """Delete a recipe from the database"""
    db_path = "data/recipes.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))

    conn.commit()
    conn.close()


# Search and filter controls
st.subheader("🔍 Find Your Recipes")

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    search_term = st.text_input(
        "Search recipes",
        placeholder="Search by title, tags, or ingredients...",
        key="search_term"
    )

with col2:
    rating_filter = st.selectbox(
        "Minimum Rating",
        options=[0, 1, 2, 3, 4, 5],
        format_func=lambda x: "All" if x == 0 else "⭐" * x,
        key="rating_filter"
    )

with col3:
    sort_by = st.selectbox(
        "Sort By",
        options=["Newest First", "Oldest First", "Highest Rated", "Title A-Z"],
        key="sort_by"
    )

st.markdown("---")

# Get filtered recipes
user_pin = get_current_user_pin()
recipes = search_recipes(user_pin, search_term, rating_filter, sort_by)

# Display count
st.write(f"**Found {len(recipes)} recipe(s)**")

# Display recipes
if not recipes:
    st.info("No recipes found. Start by creating your first recipe on the New Recipe page!")
else:
    for idx, recipe in enumerate(recipes):
        with st.expander(f"{'⭐' * recipe['rating']} {recipe['title']}", expanded=False):
            # Recipe metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                if recipe['prep_time']:
                    st.write(f"**Prep:** {recipe['prep_time']}")
            with col2:
                if recipe['cook_time']:
                    st.write(f"**Cook:** {recipe['cook_time']}")
            with col3:
                if recipe['servings']:
                    st.write(f"**Serves:** {recipe['servings']}")

            # Tags
            if recipe['tags']:
                st.write(f"**Tags:** {recipe['tags']}")

            st.markdown("---")

            # Display full recipe
            st.markdown(recipe['full_text'])

            st.markdown("---")

            # Action buttons
            action_col1, action_col2, action_col3 = st.columns(3)

            with action_col1:
                # Export to PDF
                pdf_content = create_recipe_pdf(recipe['full_text'], recipe['rating'])
                st.download_button(
                    "📄 Export PDF",
                    data=pdf_content,
                    file_name=f"{recipe['title'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{recipe['id']}",
                    use_container_width=True
                )

            with action_col2:
                # Copy to clipboard (show full text in a text area)
                if st.button("📋 View Full Text", key=f"view_{recipe['id']}", use_container_width=True):
                    st.session_state[f"show_text_{recipe['id']}"] = True

            with action_col3:
                # Delete recipe
                if st.button("🗑️ Delete", key=f"delete_{recipe['id']}", use_container_width=True, type="secondary"):
                    st.session_state[f"confirm_delete_{recipe['id']}"] = True

            # Show full text if requested
            if st.session_state.get(f"show_text_{recipe['id']}", False):
                st.text_area(
                    "Full Recipe Text (copy this)",
                    value=recipe['full_text'],
                    height=300,
                    key=f"text_{recipe['id']}"
                )
                if st.button("Close", key=f"close_text_{recipe['id']}"):
                    st.session_state[f"show_text_{recipe['id']}"] = False
                    st.rerun()

            # Confirm delete
            if st.session_state.get(f"confirm_delete_{recipe['id']}", False):
                st.warning(f"⚠️ Are you sure you want to delete **{recipe['title']}**?")
                del_col1, del_col2 = st.columns(2)
                with del_col1:
                    if st.button("Yes, Delete", key=f"confirm_yes_{recipe['id']}", type="primary"):
                        delete_recipe(recipe['id'])
                        st.success("Recipe deleted!")
                        st.session_state[f"confirm_delete_{recipe['id']}"] = False
                        st.rerun()
                with del_col2:
                    if st.button("Cancel", key=f"confirm_no_{recipe['id']}"):
                        st.session_state[f"confirm_delete_{recipe['id']}"] = False
                        st.rerun()

# Sidebar stats
with st.sidebar:
    st.markdown("### 📊 Your Recipe Stats")

    all_recipes = get_all_recipes(user_pin)

    st.metric("Total Recipes", len(all_recipes))

    if all_recipes:
        # Average rating
        avg_rating = sum(r['rating'] for r in all_recipes) / len(all_recipes)
        st.metric("Average Rating", f"{'⭐' * round(avg_rating)}")

        # Most common tags
        all_tags = []
        for r in all_recipes:
            if r['tags']:
                tags = [t.strip() for t in r['tags'].split('|')]
                all_tags.extend(tags)

        if all_tags:
            from collections import Counter
            tag_counts = Counter(all_tags)
            st.markdown("**Most Common Tags:**")
            for tag, count in tag_counts.most_common(5):
                st.write(f"- {tag} ({count})")

    st.markdown("---")
    st.markdown("### 💡 Recipe Box Tips")
    st.markdown("""
    - Use tags to organize recipes
    - Search by ingredients
    - Export PDFs for offline use
    - Rate recipes to find favorites
    """)
