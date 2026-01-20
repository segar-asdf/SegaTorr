"""
Torrent Manager - Simulated torrent engine for Streamlit Cloud compatibility
Handles torrent lifecycle, file management, and statistics tracking
"""

import os
import time
import random
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import streamlit as st


# Download directory (Streamlit Cloud compatible)
DOWNLOAD_DIR = Path("/tmp/downloads")


class TorrentInfo:
    """Data class for torrent information"""
    
    def __init__(self, torrent_id: str, name: str, magnet_link: str = None, file_path: str = None):
        self.id = torrent_id
        self.name = name
        self.magnet_link = magnet_link
        self.file_path = file_path
        self.status = "downloading"  # downloading, paused, completed, error
        self.progress = 0.0  # 0-100
        self.download_speed = 0.0  # KB/s
        self.upload_speed = 0.0  # KB/s
        self.peers = 0
        self.seeds = 0
        self.total_size = random.randint(100, 5000) * 1024 * 1024  # Random size in bytes
        self.downloaded = 0
        self.eta = None
        self.added_time = datetime.now()
        self.files = []
        self.download_path = DOWNLOAD_DIR / self.name
        
    def update_stats(self):
        """Update torrent statistics (simulated)"""
        if self.status == "downloading":
            # Simulate download progress
            increment = random.uniform(0.5, 3.0)
            self.progress = min(100.0, self.progress + increment)
            
            # Simulate download speed
            self.download_speed = random.uniform(500, 5000)  # KB/s
            self.upload_speed = random.uniform(50, 500)  # KB/s
            
            # Simulate peers and seeds
            self.peers = random.randint(5, 50)
            self.seeds = random.randint(10, 100)
            
            # Calculate downloaded bytes
            self.downloaded = int((self.progress / 100) * self.total_size)
            
            # Calculate ETA
            if self.download_speed > 0:
                remaining_bytes = self.total_size - self.downloaded
                remaining_seconds = (remaining_bytes / 1024) / self.download_speed
                self.eta = timedelta(seconds=int(remaining_seconds))
            
            # Mark as completed if progress reaches 100%
            if self.progress >= 100.0:
                self.status = "completed"
                self.progress = 100.0
                self.download_speed = 0.0
                self.eta = timedelta(0)
                self._create_dummy_files()
                
        elif self.status == "paused":
            self.download_speed = 0.0
            self.upload_speed = 0.0
            self.eta = None
    
    def _create_dummy_files(self):
        """Create dummy files for completed torrents"""
        try:
            self.download_path.mkdir(parents=True, exist_ok=True)
            
            # Create 2-5 dummy files
            num_files = random.randint(2, 5)
            extensions = ['.mp4', '.mkv', '.avi', '.txt', '.pdf', '.zip']
            
            for i in range(num_files):
                ext = random.choice(extensions)
                filename = f"{self.name}_part{i+1}{ext}"
                file_path = self.download_path / filename
                
                # Create a small dummy file
                with open(file_path, 'w') as f:
                    f.write(f"Dummy content for {filename}\n")
                    f.write(f"Torrent: {self.name}\n")
                    f.write(f"This is a simulated download.\n")
                
                file_size = os.path.getsize(file_path)
                self.files.append({
                    'name': filename,
                    'path': str(file_path),
                    'size': file_size
                })
        except Exception as e:
            st.error(f"Error creating files: {e}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'progress': round(self.progress, 2),
            'download_speed': round(self.download_speed, 2),
            'upload_speed': round(self.upload_speed, 2),
            'peers': self.peers,
            'seeds': self.seeds,
            'total_size': self.total_size,
            'downloaded': self.downloaded,
            'eta': str(self.eta) if self.eta else None,
            'added_time': self.added_time.isoformat(),
            'files': self.files
        }


class TorrentManager:
    """Manages all torrent operations"""
    
    def __init__(self):
        self.torrents: Dict[str, TorrentInfo] = {}
        self._initialize_download_dir()
    
    def _initialize_download_dir(self):
        """Create download directory if it doesn't exist"""
        try:
            DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            st.error(f"Failed to create download directory: {e}")
    
    def _generate_torrent_id(self, identifier: str) -> str:
        """Generate unique torrent ID from magnet link or filename"""
        return hashlib.md5(identifier.encode()).hexdigest()[:12]
    
    def add_magnet(self, magnet_link: str) -> tuple[bool, str, Optional[str]]:
        """
        Add torrent from magnet link
        Returns: (success, message, torrent_id)
        """
        # Validate magnet link
        if not magnet_link.startswith("magnet:?"):
            return False, "❌ Invalid magnet link format", None
        
        # Extract name from magnet link (simplified)
        try:
            if "dn=" in magnet_link:
                name = magnet_link.split("dn=")[1].split("&")[0]
                name = name.replace("+", " ").replace("%20", " ")
            else:
                name = f"Torrent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        except:
            name = f"Torrent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate torrent ID
        torrent_id = self._generate_torrent_id(magnet_link)
        
        # Check for duplicates
        if torrent_id in self.torrents:
            return False, "⚠️ Torrent already exists", None
        
        # Create torrent info
        torrent = TorrentInfo(torrent_id, name, magnet_link=magnet_link)
        self.torrents[torrent_id] = torrent
        
        return True, f"✅ Added torrent: {name}", torrent_id
    
    def add_torrent_file(self, uploaded_file) -> tuple[bool, str, Optional[str]]:
        """
        Add torrent from uploaded .torrent file
        Returns: (success, message, torrent_id)
        """
        if not uploaded_file.name.endswith('.torrent'):
            return False, "❌ Invalid file type. Please upload a .torrent file", None
        
        # Generate name and ID from filename
        name = uploaded_file.name.replace('.torrent', '')
        torrent_id = self._generate_torrent_id(uploaded_file.name)
        
        # Check for duplicates
        if torrent_id in self.torrents:
            return False, "⚠️ Torrent already exists", None
        
        # Save torrent file
        try:
            torrent_path = DOWNLOAD_DIR / uploaded_file.name
            with open(torrent_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Create torrent info
            torrent = TorrentInfo(torrent_id, name, file_path=str(torrent_path))
            self.torrents[torrent_id] = torrent
            
            return True, f"✅ Added torrent: {name}", torrent_id
        except Exception as e:
            return False, f"❌ Error saving torrent file: {e}", None
    
    def pause_torrent(self, torrent_id: str) -> tuple[bool, str]:
        """Pause a torrent"""
        if torrent_id not in self.torrents:
            return False, "❌ Torrent not found"
        
        torrent = self.torrents[torrent_id]
        if torrent.status == "completed":
            return False, "⚠️ Cannot pause completed torrent"
        
        torrent.status = "paused"
        return True, f"⏸️ Paused: {torrent.name}"
    
    def resume_torrent(self, torrent_id: str) -> tuple[bool, str]:
        """Resume a paused torrent"""
        if torrent_id not in self.torrents:
            return False, "❌ Torrent not found"
        
        torrent = self.torrents[torrent_id]
        if torrent.status != "paused":
            return False, "⚠️ Torrent is not paused"
        
        torrent.status = "downloading"
        return True, f"▶️ Resumed: {torrent.name}"
    
    def delete_torrent(self, torrent_id: str, delete_files: bool = True) -> tuple[bool, str]:
        """Delete a torrent and optionally its files"""
        if torrent_id not in self.torrents:
            return False, "❌ Torrent not found"
        
        torrent = self.torrents[torrent_id]
        
        # Delete files if requested
        if delete_files and torrent.download_path.exists():
            try:
                import shutil
                shutil.rmtree(torrent.download_path)
            except Exception as e:
                return False, f"❌ Error deleting files: {e}"
        
        # Remove from torrents dict
        del self.torrents[torrent_id]
        return True, f"🗑️ Deleted: {torrent.name}"
    
    def get_torrent(self, torrent_id: str) -> Optional[TorrentInfo]:
        """Get torrent by ID"""
        return self.torrents.get(torrent_id)
    
    def get_all_torrents(self) -> List[TorrentInfo]:
        """Get all torrents"""
        return list(self.torrents.values())
    
    def update_all_stats(self):
        """Update statistics for all active torrents"""
        for torrent in self.torrents.values():
            torrent.update_stats()
    
    def get_torrent_files(self, torrent_id: str) -> List[dict]:
        """Get list of files for a torrent"""
        torrent = self.get_torrent(torrent_id)
        if not torrent:
            return []
        return torrent.files
    
    def delete_file(self, torrent_id: str, filename: str) -> tuple[bool, str]:
        """Delete a specific file from a torrent"""
        torrent = self.get_torrent(torrent_id)
        if not torrent:
            return False, "❌ Torrent not found"
        
        # Find and delete the file
        for file_info in torrent.files:
            if file_info['name'] == filename:
                try:
                    file_path = Path(file_info['path'])
                    if file_path.exists():
                        file_path.unlink()
                    torrent.files.remove(file_info)
                    return True, f"🗑️ Deleted file: {filename}"
                except Exception as e:
                    return False, f"❌ Error deleting file: {e}"
        
        return False, "❌ File not found"


def initialize_torrent_manager():
    """Initialize torrent manager in session state"""
    if 'torrent_manager' not in st.session_state:
        st.session_state.torrent_manager = TorrentManager()


def get_torrent_manager() -> TorrentManager:
    """Get torrent manager from session state"""
    initialize_torrent_manager()
    return st.session_state.torrent_manager
