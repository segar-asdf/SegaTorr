# 🌩️ TorrentCloud - Streamlit Torrent Downloader

A Seedr.cc-like torrent cloud downloader built with Streamlit, fully compatible with Streamlit Community Cloud hosting.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 🔐 **Secure Authentication** - Session-based login system
- 🧲 **Magnet Link Support** - Add torrents via magnet links
- 📁 **File Upload** - Upload .torrent files directly
- ⚡ **Live Statistics** - Real-time progress, speed, peers, and ETA
- 📦 **File Management** - Download individual files or entire folders as ZIP
- 🎨 **Modern UI** - Beautiful interface with light/dark mode
- 📱 **Mobile Responsive** - Works seamlessly on all devices
- 🔌 **API Access** - Streamlit-compatible API for automation
- ⏸️ **Torrent Control** - Pause, resume, and delete torrents

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SegaTorr
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Login with default credentials (see below)

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `main.py` as the main file
   - Click "Deploy"

## 🔐 Default Credentials

```
Username: segar
Password: s2e5g0a3r#
```

> ⚠️ **Note**: These are hardcoded credentials for demo purposes. Change them for production use.

## 📖 Usage Guide

### Adding Torrents

1. **Via Magnet Link**
   - Click on the "🧲 Magnet Link" tab
   - Paste your magnet link
   - Click "🚀 Add Torrent"

2. **Via .torrent File**
   - Click on the "📁 Upload .torrent" tab
   - Upload your .torrent file
   - Click "🚀 Add Torrent"

### Managing Torrents

- **Pause**: Click the "⏸️ Pause" button on any downloading torrent
- **Resume**: Click the "▶️ Resume" button on paused torrents
- **View Files**: Click "📂 View Files" on completed torrents
- **Download ZIP**: Click "📦 Download ZIP" to download all files
- **Delete**: Click "🗑️ Delete" to remove torrent and files

### File Management

1. Navigate to a completed torrent
2. Click "📂 View Files"
3. Download individual files or delete them
4. Click "⬅️ Back to Torrents" to return

### Theme Toggle

- Use the sidebar to switch between 🌙 Dark Mode and ☀️ Light Mode

## 🔌 API Usage

Access the API by adding `?api=true&action=<action>` to the URL.

### Available Actions

- `add_magnet` - Add a torrent via magnet link
- `pause` - Pause a torrent
- `resume` - Resume a paused torrent
- `delete` - Delete a torrent
- `list_torrents` - List all torrents
- `list_files` - List files in a torrent

### Example

```
http://your-app.streamlit.app/?api=true&action=list_torrents
```

For detailed API documentation, visit: `?api=true&action=help`

## 📁 Project Structure

```
SegaTorr/
├── main.py              # Main application entry point
├── auth.py              # Authentication module
├── torrent_manager.py   # Torrent engine and management
├── ui.py                # UI components and rendering
├── api.py               # API layer
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## ⚠️ Important Limitations

### Streamlit Cloud Constraints

1. **Ephemeral Storage**: Files in `/tmp/downloads` are lost when the session ends or app restarts
2. **Simulated Engine**: Uses a simulated torrent engine for demo purposes (real P2P downloading requires a VPS)
3. **No Background Processes**: Torrents stop when the session ends
4. **Memory Limits**: Limited to Streamlit Cloud's resource constraints

### Security Notes

- Hardcoded credentials are for demo/personal use only
- File access is restricted to `/tmp/downloads`
- All inputs are sanitized to prevent security issues

## 🛠️ Technical Details

### Technology Stack

- **Framework**: Streamlit 1.28+
- **Language**: Python 3.10+
- **Storage**: Ephemeral filesystem (`/tmp`)
- **Session Management**: Streamlit session state

### Key Components

1. **Authentication** (`auth.py`)
   - Session-based authentication
   - Hardcoded credential validation
   - Login/logout UI

2. **Torrent Manager** (`torrent_manager.py`)
   - Simulated torrent engine
   - Lifecycle management (add, pause, resume, delete)
   - Statistics tracking
   - File management

3. **UI** (`ui.py`)
   - Modern, responsive interface
   - Torrent cards with progress bars
   - File manager
   - Theme toggle (light/dark)

4. **API** (`api.py`)
   - Query parameter-based routing
   - Form-based input
   - JSON responses
   - Authentication required

## 🎨 Screenshots

> Add screenshots of your app here after deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Segar**

## 🙏 Acknowledgments

- Inspired by [Seedr.cc](https://seedr.cc)
- Built with [Streamlit](https://streamlit.io)

---

**⚡ Built for Streamlit Community Cloud** | **🌩️ TorrentCloud v1.0**
