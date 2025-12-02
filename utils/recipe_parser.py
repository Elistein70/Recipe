"""
Recipe parser for EatKosher - extracts and displays recipe components
"""

import re
import streamlit as st


def parse_recipe(recipe_text):
    """
    Parses recipe markdown and extracts components.

    Args:
        recipe_text (str): Recipe in markdown format

    Returns:
        dict: Dictionary with keys:
            - title (str)
            - tags (str)
            - prep_time (str)
            - cook_time (str)
            - servings (str)
            - ingredients (list of str)
            - instructions (str)
            - notes (str)
    """
    recipe_data = {
        'title': '',
        'tags': '',
        'prep_time': '',
        'cook_time': '',
        'servings': '',
        'ingredients': [],
        'instructions': '',
        'notes': ''
    }

    # Extract title (first # heading)
    title_match = re.search(r'^#\s+(.+)$', recipe_text, re.MULTILINE)
    if title_match:
        recipe_data['title'] = title_match.group(1).strip()

    # Extract tags
    tags_match = re.search(r'\*\*Tags:\*\*\s*(.+)$', recipe_text, re.MULTILINE)
    if tags_match:
        recipe_data['tags'] = tags_match.group(1).strip()

    # Extract prep time
    prep_match = re.search(r'\*\*Prep:\*\*\s*(.+?)(?:\s+\*\*|$)', recipe_text)
    if prep_match:
        recipe_data['prep_time'] = prep_match.group(1).strip()

    # Extract cook time
    cook_match = re.search(r'\*\*Cook:\*\*\s*(.+?)(?:\s+\*\*|$)', recipe_text)
    if cook_match:
        recipe_data['cook_time'] = cook_match.group(1).strip()

    # Extract servings
    servings_match = re.search(r'\*\*Serves:\*\*\s*(.+)$', recipe_text, re.MULTILINE)
    if servings_match:
        recipe_data['servings'] = servings_match.group(1).strip()

    # Extract ingredients (lines starting with - or * under ## Ingredients)
    ingredients_section = re.search(
        r'##\s+Ingredients\s*\n(.*?)(?=\n##|\Z)',
        recipe_text,
        re.DOTALL | re.IGNORECASE
    )
    if ingredients_section:
        ingredients_text = ingredients_section.group(1)
        # Find all list items
        ingredients = re.findall(r'^\s*[-*]\s+(.+)$', ingredients_text, re.MULTILINE)
        recipe_data['ingredients'] = [ing.strip() for ing in ingredients]

    # Extract instructions
    instructions_section = re.search(
        r'##\s+Step-by-Step Instructions\s*\n(.*?)(?=\n##|\Z)',
        recipe_text,
        re.DOTALL | re.IGNORECASE
    )
    if instructions_section:
        recipe_data['instructions'] = instructions_section.group(1).strip()

    # Extract notes
    notes_section = re.search(
        r'##\s+Notes & Substitutions\s*\n(.*?)(?=\n##|\Z)',
        recipe_text,
        re.DOTALL | re.IGNORECASE
    )
    if notes_section:
        recipe_data['notes'] = notes_section.group(1).strip()

    return recipe_data


def display_recipe_with_checkboxes(recipe_text):
    """
    Displays recipe with interactive checkboxes for ingredients.

    Args:
        recipe_text (str): Recipe in markdown format

    Returns:
        list: List of unchecked ingredients (items user doesn't have)
    """
    recipe_data = parse_recipe(recipe_text)

    # Display title
    if recipe_data['title']:
        st.title(recipe_data['title'])

    # Display metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        if recipe_data['prep_time']:
            st.metric("⏱️ Prep Time", recipe_data['prep_time'])
    with col2:
        if recipe_data['cook_time']:
            st.metric("🔥 Cook Time", recipe_data['cook_time'])
    with col3:
        if recipe_data['servings']:
            st.metric("🍽️ Serves", recipe_data['servings'])

    # Display tags
    if recipe_data['tags']:
        st.markdown(f"**Tags:** {recipe_data['tags']}")

    st.markdown("---")

    # Display ingredients with checkboxes
    st.subheader("📝 Ingredients")
    missing_ingredients = []

    if 'ingredient_checkboxes' not in st.session_state:
        st.session_state.ingredient_checkboxes = {}

    for idx, ingredient in enumerate(recipe_data['ingredients']):
        # Create unique key for each checkbox
        checkbox_key = f"ingredient_{idx}_{hash(ingredient)}"

        # Initialize checkbox state if not exists
        if checkbox_key not in st.session_state.ingredient_checkboxes:
            st.session_state.ingredient_checkboxes[checkbox_key] = True

        # Display checkbox
        has_ingredient = st.checkbox(
            ingredient,
            value=st.session_state.ingredient_checkboxes[checkbox_key],
            key=checkbox_key
        )

        # Track missing ingredients
        if not has_ingredient:
            missing_ingredients.append(ingredient)

    st.markdown("---")

    # Display instructions
    if recipe_data['instructions']:
        st.subheader("👩‍🍳 Step-by-Step Instructions")
        st.markdown(recipe_data['instructions'])

    st.markdown("---")

    # Display notes
    if recipe_data['notes']:
        st.subheader("📌 Notes & Substitutions")
        st.markdown(recipe_data['notes'])

    return missing_ingredients


def get_recipe_for_save(recipe_text):
    """
    Extracts recipe data for saving to database.

    Args:
        recipe_text (str): Recipe in markdown format

    Returns:
        dict: Recipe data ready for database
    """
    recipe_data = parse_recipe(recipe_text)

    # Combine ingredients into text
    ingredients_text = "\n".join([f"- {ing}" for ing in recipe_data['ingredients']])

    return {
        'title': recipe_data['title'],
        'tags': recipe_data['tags'],
        'ingredients': ingredients_text,
        'instructions': recipe_data['instructions'],
        'notes': recipe_data['notes'],
        'prep_time': recipe_data['prep_time'],
        'cook_time': recipe_data['cook_time'],
        'servings': recipe_data['servings'],
        'full_text': recipe_text
    }
