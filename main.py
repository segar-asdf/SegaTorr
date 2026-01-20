"""
TorrentCloud - Seedr.cc-like Torrent Downloader for Streamlit
Main application entry point

Author: Segar
Compatible with: Streamlit Community Cloud
"""

import streamlit as st
import time
from datetime import datetime

# Import modules
from auth import (
    initialize_auth_state,
    is_authenticated,
    render_login_page,
    render_logout_button
)
from torrent_manager import initialize_torrent_manager, get_torrent_manager
from ui import (
    render_theme_toggle,
    render_sidebar,
    render_main_content,
    apply_theme_css
)
from api import check_api_mode, handle_api_request


# Page configuration
st.set_page_config(
    page_title="TorrentCloud - Torrent Downloader",
    page_icon="🌩️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# TorrentCloud\nA Seedr.cc-like torrent downloader built with Streamlit"
    }
)


def initialize_session_state():
    """Initialize all session state variables"""
    initialize_auth_state()
    initialize_torrent_manager()
    
    if 'selected_torrent' not in st.session_state:
        st.session_state.selected_torrent = None
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True


def auto_refresh_torrents():
    """Auto-refresh torrent statistics"""
    if not st.session_state.auto_refresh:
        return
    
    current_time = time.time()
    
    # Update every 3 seconds
    if current_time - st.session_state.last_update >= 3:
        tm = get_torrent_manager()
        tm.update_all_stats()
        st.session_state.last_update = current_time
        
        # Check if there are active downloads
        torrents = tm.get_all_torrents()
        has_active = any(t.status == 'downloading' for t in torrents)
        
        if has_active:
            time.sleep(0.1)  # Small delay to prevent too rapid updates
            st.rerun()


def render_header():
    """Render application header"""
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0;'>
                <h1 style='margin: 0;'>🌩️ TorrentCloud</h1>
                <p style='color: #888; margin: 0;'>Your Personal Torrent Downloader</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")


def main():
    """Main application logic"""
    # Initialize session state
    initialize_session_state()
    
    # Check if in API mode
    if check_api_mode():
        handle_api_request()
        return
    
    # Check authentication
    if not is_authenticated():
        render_login_page()
        return
    
    # Authenticated user interface
    render_sidebar()
    render_theme_toggle()
    render_logout_button()
    
    # Main content
    render_header()
    render_main_content()
    
    # Auto-refresh for active downloads
    auto_refresh_torrents()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #888; padding: 1rem;'>
            <p>TorrentCloud v1.0 | Built with ❤️ using Streamlit</p>
            <p style='font-size: 0.8rem;'>⚠️ Files are stored in ephemeral storage and will be lost when session ends</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
