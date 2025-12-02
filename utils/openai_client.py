"""
OpenAI client for EatKosher recipe generation
"""

import openai
import streamlit as st


def get_recipe_from_openai(user_request, system_prompt, model="gpt-4o"):
    """
    Calls OpenAI API to generate a recipe based on user request and system prompt.

    Args:
        user_request (str): User's recipe request
        system_prompt (str): System prompt with dietary restrictions
        model (str): OpenAI model to use (default: gpt-4o)

    Returns:
        str: Generated recipe in markdown format
    """
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return "Error: OpenAI API key not found. Please add it to .streamlit/secrets.toml"

        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # Make API call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_request}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        # Extract recipe text
        recipe = response.choices[0].message.content
        return recipe

    except Exception as e:
        return f"Error generating recipe: {str(e)}"


def get_substitutions(original_recipe, missing_ingredients, system_prompt, model="gpt-4o"):
    """
    Calls OpenAI API to suggest kosher substitutes for missing ingredients.

    Args:
        original_recipe (str): The original recipe
        missing_ingredients (list): List of missing ingredients
        system_prompt (str): System prompt with dietary restrictions
        model (str): OpenAI model to use (default: gpt-4o)

    Returns:
        str: Updated recipe with substitutions
    """
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            return "Error: OpenAI API key not found. Please add it to .streamlit/secrets.toml"

        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # Create substitution request
        substitution_request = f"""The user is making this recipe:

{original_recipe}

They are MISSING these ingredients:
{', '.join(missing_ingredients)}

As a Lakewood balabusta, suggest ONLY substitutes that:
1. Keep the dish 95%+ as good
2. Are actually sold in Lakewood-area kosher stores right now
3. Meet all kashrut standards

If NO good substitute exists for an ingredient, you MUST say: "No good kosher substitute available in Lakewood — you must buy this ingredient."

Provide the FULL updated recipe with substitutions clearly marked in the Notes & Substitutions section."""

        # Make API call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": substitution_request}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        # Extract updated recipe
        updated_recipe = response.choices[0].message.content
        return updated_recipe

    except Exception as e:
        return f"Error getting substitutions: {str(e)}"
