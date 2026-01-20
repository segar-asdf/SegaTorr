"""
UI Components for Streamlit Torrent Downloader
Provides modern, responsive interface with light/dark mode support
"""

import streamlit as st
from datetime import datetime
from pathlib import Path
import zipfile
import io
from torrent_manager import get_torrent_manager, TorrentInfo


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_speed(speed_kbps: float) -> str:
    """Format speed in KB/s to human-readable format"""
    if speed_kbps < 1024:
        return f"{speed_kbps:.1f} KB/s"
    else:
        return f"{speed_kbps/1024:.1f} MB/s"


def render_theme_toggle():
    """Render light/dark mode toggle in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Settings")
    
    # Initialize theme in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Theme toggle
    theme_options = {'🌙 Dark Mode': 'dark', '☀️ Light Mode': 'light'}
    selected_theme = st.sidebar.radio(
        "Theme",
        options=list(theme_options.keys()),
        index=0 if st.session_state.theme == 'dark' else 1,
        label_visibility="collapsed"
    )
    st.session_state.theme = theme_options[selected_theme]
    
    # Apply theme CSS
    apply_theme_css(st.session_state.theme)


def apply_theme_css(theme: str):
    """Apply custom CSS based on theme"""
    if theme == 'dark':
        bg_color = "#0e1117"
        card_bg = "#1e2130"
        text_color = "#fafafa"
        border_color = "#2e3548"
        accent_color = "#00d4ff"
    else:
        bg_color = "#ffffff"
        card_bg = "#f0f2f6"
        text_color = "#262730"
        border_color = "#d0d0d0"
        accent_color = "#0068c9"
    
    st.markdown(f"""
        <style>
        .torrent-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .torrent-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
        }}
        .torrent-header {{
            font-size: 1.2rem;
            font-weight: 600;
            color: {accent_color};
            margin-bottom: 0.5rem;
        }}
        .torrent-stats {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1rem;
        }}
        .stat-item {{
            flex: 1;
            min-width: 120px;
        }}
        .stat-label {{
            font-size: 0.8rem;
            color: #888;
            text-transform: uppercase;
        }}
        .stat-value {{
            font-size: 1rem;
            font-weight: 600;
            color: {text_color};
        }}
        .status-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .status-downloading {{
            background-color: #00d4ff;
            color: #000;
        }}
        .status-completed {{
            background-color: #00ff88;
            color: #000;
        }}
        .status-paused {{
            background-color: #ffaa00;
            color: #000;
        }}
        .status-error {{
            background-color: #ff4444;
            color: #fff;
        }}
        .file-item {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .progress-container {{
            margin: 1rem 0;
        }}
        </style>
    """, unsafe_allow_html=True)


def render_add_torrent_form():
    """Render form to add new torrents"""
    st.markdown("### ➕ Add New Torrent")
    
    tab1, tab2 = st.tabs(["🧲 Magnet Link", "📁 Upload .torrent"])
    
    with tab1:
        with st.form("magnet_form", clear_on_submit=True):
            magnet_link = st.text_input(
                "Magnet Link",
                placeholder="magnet:?xt=urn:btih:...",
                help="Paste a magnet link to start downloading"
            )
            submit_magnet = st.form_submit_button("🚀 Add Torrent", use_container_width=True)
            
            if submit_magnet and magnet_link:
                tm = get_torrent_manager()
                success, message, torrent_id = tm.add_magnet(magnet_link)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        with st.form("file_form", clear_on_submit=True):
            uploaded_file = st.file_uploader(
                "Upload .torrent file",
                type=['torrent'],
                help="Upload a .torrent file to start downloading"
            )
            submit_file = st.form_submit_button("🚀 Add Torrent", use_container_width=True)
            
            if submit_file and uploaded_file:
                tm = get_torrent_manager()
                success, message, torrent_id = tm.add_torrent_file(uploaded_file)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def render_torrent_card(torrent: TorrentInfo):
    """Render a single torrent card with stats and controls"""
    
    # Status badge
    status_class = f"status-{torrent.status}"
    status_emoji = {
        'downloading': '⬇️',
        'completed': '✅',
        'paused': '⏸️',
        'error': '❌'
    }
    
    st.markdown(f"""
        <div class="torrent-card">
            <div class="torrent-header">
                {status_emoji.get(torrent.status, '📦')} {torrent.name}
            </div>
            <span class="status-badge {status_class}">{torrent.status.upper()}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    if torrent.status in ['downloading', 'paused']:
        st.progress(torrent.progress / 100, text=f"{torrent.progress:.1f}%")
    elif torrent.status == 'completed':
        st.progress(1.0, text="100%")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-label">Downloaded</div>
                <div class="stat-value">{format_bytes(torrent.downloaded)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-label">Size</div>
                <div class="stat-value">{format_bytes(torrent.total_size)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-label">Speed</div>
                <div class="stat-value">{format_speed(torrent.download_speed)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-label">ETA</div>
                <div class="stat-value">{str(torrent.eta) if torrent.eta else 'N/A'}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Additional stats
    col5, col6 = st.columns(2)
    with col5:
        st.caption(f"👥 Peers: {torrent.peers} | 🌱 Seeds: {torrent.seeds}")
    with col6:
        st.caption(f"📅 Added: {torrent.added_time.strftime('%Y-%m-%d %H:%M')}")
    
    # Control buttons
    st.markdown("---")
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    
    tm = get_torrent_manager()
    
    with btn_col1:
        if torrent.status == 'downloading':
            if st.button("⏸️ Pause", key=f"pause_{torrent.id}", use_container_width=True):
                success, message = tm.pause_torrent(torrent.id)
                if success:
                    st.toast(message)
                    st.rerun()
                else:
                    st.error(message)
        elif torrent.status == 'paused':
            if st.button("▶️ Resume", key=f"resume_{torrent.id}", use_container_width=True):
                success, message = tm.resume_torrent(torrent.id)
                if success:
                    st.toast(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with btn_col2:
        if torrent.status == 'completed':
            if st.button("📂 View Files", key=f"files_{torrent.id}", use_container_width=True):
                st.session_state.selected_torrent = torrent.id
                st.rerun()
    
    with btn_col3:
        if torrent.status == 'completed' and torrent.files:
            # Create ZIP of all files
            zip_buffer = create_zip_from_torrent(torrent)
            if zip_buffer:
                st.download_button(
                    label="📦 Download ZIP",
                    data=zip_buffer,
                    file_name=f"{torrent.name}.zip",
                    mime="application/zip",
                    key=f"zip_{torrent.id}",
                    use_container_width=True
                )
    
    with btn_col4:
        if st.button("🗑️ Delete", key=f"delete_{torrent.id}", use_container_width=True, type="secondary"):
            success, message = tm.delete_torrent(torrent.id, delete_files=True)
            if success:
                st.toast(message)
                st.rerun()
            else:
                st.error(message)


def create_zip_from_torrent(torrent: TorrentInfo) -> bytes:
    """Create a ZIP file from torrent files"""
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_info in torrent.files:
                file_path = Path(file_info['path'])
                if file_path.exists():
                    zip_file.write(file_path, arcname=file_info['name'])
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except Exception as e:
        st.error(f"Error creating ZIP: {e}")
        return None


def render_file_manager(torrent_id: str):
    """Render file manager for a specific torrent"""
    tm = get_torrent_manager()
    torrent = tm.get_torrent(torrent_id)
    
    if not torrent:
        st.error("❌ Torrent not found")
        if st.button("⬅️ Back to Torrents"):
            st.session_state.selected_torrent = None
            st.rerun()
        return
    
    st.markdown(f"### 📂 Files: {torrent.name}")
    
    if st.button("⬅️ Back to Torrents"):
        st.session_state.selected_torrent = None
        st.rerun()
    
    st.markdown("---")
    
    if not torrent.files:
        st.info("ℹ️ No files available yet. Files will appear when download completes.")
        return
    
    # Display files
    for file_info in torrent.files:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**📄 {file_info['name']}**")
            st.caption(f"Size: {format_bytes(file_info['size'])}")
        
        with col2:
            # Download button
            try:
                file_path = Path(file_info['path'])
                if file_path.exists():
                    with open(file_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download",
                            data=f.read(),
                            file_name=file_info['name'],
                            key=f"dl_{torrent_id}_{file_info['name']}",
                            use_container_width=True
                        )
            except Exception as e:
                st.error(f"Error: {e}")
        
        with col3:
            # Delete button
            if st.button("🗑️", key=f"del_{torrent_id}_{file_info['name']}", use_container_width=True):
                success, message = tm.delete_file(torrent_id, file_info['name'])
                if success:
                    st.toast(message)
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown("---")


def render_sidebar():
    """Render sidebar with navigation and torrent list"""
    st.sidebar.markdown("# 🌩️ TorrentCloud")
    st.sidebar.markdown("---")
    
    # Stats summary
    tm = get_torrent_manager()
    torrents = tm.get_all_torrents()
    
    active_count = sum(1 for t in torrents if t.status == 'downloading')
    completed_count = sum(1 for t in torrents if t.status == 'completed')
    
    st.sidebar.metric("Active Downloads", active_count)
    st.sidebar.metric("Completed", completed_count)
    st.sidebar.metric("Total Torrents", len(torrents))
    
    st.sidebar.markdown("---")
    
    # Quick torrent list
    if torrents:
        st.sidebar.markdown("### 📋 Quick Access")
        for torrent in torrents[:5]:  # Show first 5
            status_emoji = {
                'downloading': '⬇️',
                'completed': '✅',
                'paused': '⏸️',
                'error': '❌'
            }
            emoji = status_emoji.get(torrent.status, '📦')
            
            if st.sidebar.button(
                f"{emoji} {torrent.name[:20]}...",
                key=f"sidebar_{torrent.id}",
                use_container_width=True
            ):
                st.session_state.selected_torrent = torrent.id
                st.rerun()


def render_main_content():
    """Render main content area"""
    # Check if viewing specific torrent files
    if 'selected_torrent' in st.session_state and st.session_state.selected_torrent:
        render_file_manager(st.session_state.selected_torrent)
        return
    
    # Add torrent form
    render_add_torrent_form()
    
    st.markdown("---")
    st.markdown("## 📦 Your Torrents")
    
    # Get all torrents
    tm = get_torrent_manager()
    torrents = tm.get_all_torrents()
    
    if not torrents:
        st.info("ℹ️ No torrents yet. Add a magnet link or upload a .torrent file to get started!")
        return
    
    # Filter options
    filter_col1, filter_col2 = st.columns([3, 1])
    with filter_col1:
        filter_status = st.selectbox(
            "Filter by status",
            options=['All', 'Downloading', 'Completed', 'Paused', 'Error'],
            index=0
        )
    
    # Apply filter
    if filter_status != 'All':
        torrents = [t for t in torrents if t.status == filter_status.lower()]
    
    # Display torrents
    for torrent in torrents:
        render_torrent_card(torrent)
        st.markdown("<br>", unsafe_allow_html=True)
