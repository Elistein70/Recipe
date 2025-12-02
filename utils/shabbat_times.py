"""
Shabbat times for Lakewood, NJ using Hebcal API
"""

import requests
from datetime import datetime, timedelta
import streamlit as st


def get_shabbat_times(city="Lakewood", state="NJ", country="US"):
    """
    Gets candle lighting time for this Friday in Lakewood, NJ.

    Args:
        city (str): City name
        state (str): State code
        country (str): Country code

    Returns:
        dict: Dictionary with candle_lighting time and date, or None if error
    """
    try:
        # Hebcal API endpoint for Shabbat times
        url = "https://www.hebcal.com/shabbat"

        params = {
            "cfg": "json",
            "geonameid": "5099133",  # Lakewood, NJ
            "M": "on",  # Use Jewish calendar
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        # Find candle lighting time
        candle_lighting = None
        havdalah = None

        for item in data.get('items', []):
            if item.get('category') == 'candles':
                candle_lighting = item.get('title')
                date_str = item.get('date')
            elif item.get('category') == 'havdalah':
                havdalah = item.get('title')

        if candle_lighting:
            # Parse the date
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

            return {
                'candle_lighting': candle_lighting,
                'havdalah': havdalah,
                'date': date_obj.strftime('%B %d, %Y'),
                'parsha': data.get('title', 'Shabbat')
            }

        return None

    except Exception as e:
        st.error(f"Could not fetch Shabbat times: {str(e)}")
        return None


def display_shabbat_banner():
    """
    Displays a banner with this week's Shabbat times for Lakewood.
    """
    shabbat_info = get_shabbat_times()

    if shabbat_info:
        # Create a beautiful banner
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
                    padding: 20px;
                    border-radius: 10px;
                    color: white;
                    text-align: center;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h3 style="margin: 0; font-size: 1.5em;">🕯️ {shabbat_info['parsha']}</h3>
            <p style="margin: 10px 0 0 0; font-size: 1.2em;">
                <strong>{shabbat_info['date']}</strong><br>
                Candle Lighting: {shabbat_info['candle_lighting'].replace('Candle lighting: ', '')}<br>
                {shabbat_info['havdalah'] if shabbat_info['havdalah'] else ''}
            </p>
            <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.9;">
                Lakewood, NJ
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback banner if API fails
        st.info("🕯️ Shabbat Shalom from EatKosher!")
