"""
API Layer for Streamlit Torrent Downloader
Provides Streamlit-compatible API using query parameters and forms
"""

import streamlit as st
import json
from typing import Dict, Any
from torrent_manager import get_torrent_manager
from auth import validate_credentials


def check_api_mode() -> bool:
    """Check if app is in API mode based on query parameters"""
    query_params = st.query_params
    return 'api' in query_params and query_params['api'] == 'true'


def authenticate_api_request(credentials: Dict[str, str]) -> bool:
    """Authenticate API request using credentials"""
    username = credentials.get('username', '')
    password = credentials.get('password', '')
    return validate_credentials(username, password)


def api_response(success: bool, message: str, data: Any = None) -> Dict:
    """Create standardized API response"""
    response = {
        'success': success,
        'message': message,
        'timestamp': st.session_state.get('current_time', '')
    }
    if data is not None:
        response['data'] = data
    return response


def handle_api_request():
    """Handle API requests based on query parameters"""
    query_params = st.query_params
    
    st.markdown("# 🔌 API Mode")
    st.markdown("---")
    
    # Get action from query params
    action = query_params.get('action', 'help')
    
    if action == 'help':
        render_api_help()
        return
    
    # API authentication form
    st.markdown("### 🔐 Authentication")
    
    with st.form("api_auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Action-specific inputs
        st.markdown(f"### 📋 Action: `{action}`")
        
        request_data = {}
        
        if action == 'add_magnet':
            magnet_link = st.text_input("Magnet Link", placeholder="magnet:?xt=urn:btih:...")
            request_data['magnet_link'] = magnet_link
        
        elif action == 'pause':
            torrent_id = st.text_input("Torrent ID")
            request_data['torrent_id'] = torrent_id
        
        elif action == 'resume':
            torrent_id = st.text_input("Torrent ID")
            request_data['torrent_id'] = torrent_id
        
        elif action == 'delete':
            torrent_id = st.text_input("Torrent ID")
            delete_files = st.checkbox("Delete Files", value=True)
            request_data['torrent_id'] = torrent_id
            request_data['delete_files'] = delete_files
        
        elif action == 'list_torrents':
            status_filter = st.selectbox("Status Filter", ['all', 'downloading', 'completed', 'paused', 'error'])
            request_data['status'] = status_filter
        
        elif action == 'list_files':
            torrent_id = st.text_input("Torrent ID")
            request_data['torrent_id'] = torrent_id
        
        submit = st.form_submit_button("🚀 Execute API Call")
        
        if submit:
            # Authenticate
            if not authenticate_api_request({'username': username, 'password': password}):
                response = api_response(False, "Authentication failed")
                st.error("❌ Authentication Failed")
                st.json(response)
                return
            
            # Process action
            response = process_api_action(action, request_data)
            
            # Display response
            if response['success']:
                st.success("✅ Success")
            else:
                st.error("❌ Error")
            
            st.json(response)


def process_api_action(action: str, data: Dict[str, Any]) -> Dict:
    """Process API action and return response"""
    tm = get_torrent_manager()
    
    try:
        if action == 'add_magnet':
            magnet_link = data.get('magnet_link', '')
            if not magnet_link:
                return api_response(False, "Magnet link is required")
            
            success, message, torrent_id = tm.add_magnet(magnet_link)
            return api_response(success, message, {'torrent_id': torrent_id} if success else None)
        
        elif action == 'pause':
            torrent_id = data.get('torrent_id', '')
            if not torrent_id:
                return api_response(False, "Torrent ID is required")
            
            success, message = tm.pause_torrent(torrent_id)
            return api_response(success, message)
        
        elif action == 'resume':
            torrent_id = data.get('torrent_id', '')
            if not torrent_id:
                return api_response(False, "Torrent ID is required")
            
            success, message = tm.resume_torrent(torrent_id)
            return api_response(success, message)
        
        elif action == 'delete':
            torrent_id = data.get('torrent_id', '')
            if not torrent_id:
                return api_response(False, "Torrent ID is required")
            
            delete_files = data.get('delete_files', True)
            success, message = tm.delete_torrent(torrent_id, delete_files)
            return api_response(success, message)
        
        elif action == 'list_torrents':
            status_filter = data.get('status', 'all')
            torrents = tm.get_all_torrents()
            
            if status_filter != 'all':
                torrents = [t for t in torrents if t.status == status_filter]
            
            torrent_list = [t.to_dict() for t in torrents]
            return api_response(True, f"Found {len(torrent_list)} torrents", {'torrents': torrent_list})
        
        elif action == 'list_files':
            torrent_id = data.get('torrent_id', '')
            if not torrent_id:
                return api_response(False, "Torrent ID is required")
            
            files = tm.get_torrent_files(torrent_id)
            return api_response(True, f"Found {len(files)} files", {'files': files})
        
        else:
            return api_response(False, f"Unknown action: {action}")
    
    except Exception as e:
        return api_response(False, f"Error processing request: {str(e)}")


def render_api_help():
    """Render API documentation"""
    st.markdown("""
    ## 📚 API Documentation
    
    This Streamlit app provides a simple API interface using query parameters and forms.
    
    ### 🔐 Authentication
    All API requests require authentication with the following credentials:
    - **Username**: `segar`
    - **Password**: `s2e5g0a3r#`
    
    ### 🌐 Usage
    
    To use the API, add `?api=true&action=<action_name>` to the URL.
    
    ### 📋 Available Actions
    
    #### 1. Add Magnet Link
    ```
    ?api=true&action=add_magnet
    ```
    **Parameters:**
    - `magnet_link`: The magnet link to add
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Added torrent: Example",
        "data": {
            "torrent_id": "abc123def456"
        }
    }
    ```
    
    ---
    
    #### 2. Pause Torrent
    ```
    ?api=true&action=pause
    ```
    **Parameters:**
    - `torrent_id`: ID of the torrent to pause
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Paused: Example Torrent"
    }
    ```
    
    ---
    
    #### 3. Resume Torrent
    ```
    ?api=true&action=resume
    ```
    **Parameters:**
    - `torrent_id`: ID of the torrent to resume
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Resumed: Example Torrent"
    }
    ```
    
    ---
    
    #### 4. Delete Torrent
    ```
    ?api=true&action=delete
    ```
    **Parameters:**
    - `torrent_id`: ID of the torrent to delete
    - `delete_files`: Whether to delete files (true/false)
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Deleted: Example Torrent"
    }
    ```
    
    ---
    
    #### 5. List Torrents
    ```
    ?api=true&action=list_torrents
    ```
    **Parameters:**
    - `status`: Filter by status (all, downloading, completed, paused, error)
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Found 3 torrents",
        "data": {
            "torrents": [...]
        }
    }
    ```
    
    ---
    
    #### 6. List Files
    ```
    ?api=true&action=list_files
    ```
    **Parameters:**
    - `torrent_id`: ID of the torrent
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Found 5 files",
        "data": {
            "files": [...]
        }
    }
    ```
    
    ---
    
    ### 💡 Example Usage
    
    1. Navigate to: `http://your-app.streamlit.app/?api=true&action=add_magnet`
    2. Fill in the authentication form
    3. Enter the required parameters
    4. Click "Execute API Call"
    5. View the JSON response
    
    ### ⚠️ Notes
    - This is a simplified API for Streamlit Cloud compatibility
    - For production use, consider implementing a proper REST API with FastAPI or Flask
    - All operations are session-based and data is ephemeral
    """)
