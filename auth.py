"""
Simple PIN authentication for EatKosher
Each family has a 4-digit PIN and their own saved recipes
"""

import streamlit as st
import sqlite3
import hashlib
import os


def init_auth_db():
    """Initialize authentication database"""
    db_path = "data/recipes.db"
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            pin TEXT PRIMARY KEY,
            family_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create recipes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_pin TEXT NOT NULL,
            title TEXT NOT NULL,
            tags TEXT,
            ingredients TEXT,
            instructions TEXT,
            notes TEXT,
            prep_time TEXT,
            cook_time TEXT,
            servings TEXT,
            rating INTEGER,
            full_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_pin) REFERENCES users(pin)
        )
    ''')

    conn.commit()
    conn.close()


def hash_pin(pin):
    """Hash PIN for secure storage"""
    return hashlib.sha256(pin.encode()).hexdigest()


def create_user(pin, family_name):
    """Create a new user account"""
    db_path = "data/recipes.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    try:
        hashed_pin = hash_pin(pin)
        c.execute('INSERT INTO users (pin, family_name) VALUES (?, ?)',
                  (hashed_pin, family_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_pin(pin):
    """Verify PIN and return family name if valid"""
    db_path = "data/recipes.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    hashed_pin = hash_pin(pin)
    c.execute('SELECT family_name FROM users WHERE pin = ?', (hashed_pin,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]
    return None


def login_page():
    """Display login/registration page"""
    st.markdown("""
        <h1 style='text-align: center; color: #1E3A8A;'>
            🍲 EatKosher – אכילת כשר
        </h1>
        <p style='text-align: center; font-size: 1.2em; color: #4B5563;'>
            Your Premium Kosher Recipe Assistant
        </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Initialize auth database
    init_auth_db()

    tab1, tab2 = st.tabs(["🔑 Login", "📝 New Family Registration"])

    with tab1:
        st.subheader("Enter Your 4-Digit Family PIN")

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4,
            key="login_pin",
            placeholder="Enter 4-digit PIN"
        )

        if st.button("Login", type="primary", use_container_width=True):
            if len(pin) == 4 and pin.isdigit():
                family_name = verify_pin(pin)
                if family_name:
                    st.session_state.authenticated = True
                    st.session_state.user_pin = hash_pin(pin)
                    st.session_state.family_name = family_name
                    st.success(f"Welcome back, {family_name} family!")
                    st.rerun()
                else:
                    st.error("Invalid PIN. Please try again or register a new family.")
            else:
                st.error("Please enter a valid 4-digit PIN.")

    with tab2:
        st.subheader("Register Your Family")

        new_family_name = st.text_input(
            "Family Name",
            placeholder="e.g., Cohen, Goldstein, Schwartz"
        )

        new_pin = st.text_input(
            "Choose a 4-Digit PIN",
            type="password",
            max_chars=4,
            key="register_pin",
            placeholder="Create 4-digit PIN"
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            max_chars=4,
            key="confirm_pin",
            placeholder="Re-enter PIN"
        )

        if st.button("Register Family", type="primary", use_container_width=True):
            if not new_family_name:
                st.error("Please enter your family name.")
            elif len(new_pin) != 4 or not new_pin.isdigit():
                st.error("PIN must be exactly 4 digits.")
            elif new_pin != confirm_pin:
                st.error("PINs do not match. Please try again.")
            else:
                if create_user(new_pin, new_family_name):
                    st.success(f"✅ {new_family_name} family registered successfully!")
                    st.info("Please use the Login tab to access your account.")
                else:
                    st.error("This PIN is already registered. Please choose a different one.")


def check_authentication():
    """Check if user is authenticated, show login page if not"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        login_page()
        st.stop()


def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user_pin = None
    st.session_state.family_name = None
    st.rerun()


def get_current_user_pin():
    """Get current logged-in user's PIN hash"""
    return st.session_state.get('user_pin')


def get_current_family_name():
    """Get current logged-in family name"""
    return st.session_state.get('family_name', 'Family')
