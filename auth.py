"""
Authentication module for Streamlit Torrent Downloader
Handles session-based authentication with hardcoded credentials
"""

import streamlit as st
import hashlib


# Hardcoded credentials (as per requirements)
VALID_USERNAME = "segar"
VALID_PASSWORD = "s2e5g0a3r#"


def hash_password(password: str) -> str:
    """Hash password for secure comparison"""
    return hashlib.sha256(password.encode()).hexdigest()


def initialize_auth_state():
    """Initialize authentication session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None


def validate_credentials(username: str, password: str) -> bool:
    """Validate user credentials against hardcoded values"""
    return username == VALID_USERNAME and password == VALID_PASSWORD


def login(username: str, password: str) -> bool:
    """
    Attempt to log in with provided credentials
    Returns True if successful, False otherwise
    """
    if validate_credentials(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False


def logout():
    """Log out the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()


def is_authenticated() -> bool:
    """Check if user is currently authenticated"""
    return st.session_state.get('authenticated', False)


def require_auth(func):
    """Decorator to require authentication for a function"""
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("⚠️ Please log in to access this feature")
            return None
        return func(*args, **kwargs)
    return wrapper


def render_login_page():
    """Render the login page UI"""
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🌩️ TorrentCloud")
        st.markdown("### Secure Torrent Downloader")
        st.markdown("---")
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                elif login(username, password):
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        
  


def render_logout_button():
    """Render logout button in sidebar"""
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()
