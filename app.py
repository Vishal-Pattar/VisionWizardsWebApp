import streamlit as st
from PIL import Image
from user_auth import login_user
from settings_manager import SettingsManager
from stream_manager import StreamManager, capture_camera

# Initialize Streamlit page configuration
st.set_page_config(page_title="Vision Wizards", layout="wide")

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Login Page"
if 'stream_manager' not in st.session_state:
    st.session_state.stream_manager = None

# Sidebar navigation with buttons
st.sidebar.title("Navigation Bar")
if st.sidebar.button("Login Page"):
    st.session_state.page = "Login Page"
if st.sidebar.button("Settings"):
    st.session_state.page = "Settings"
if st.sidebar.button("Admin Panel"):
    st.session_state.page = "Admin Panel"

# Page navigation based on session state
if st.session_state.page == "Login Page":
    st.title("Welcome to Pune Metro")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login:
        if login_user(email, password):
            st.success("Logged in successfully")
            st.session_state.logged_in = True
            st.session_state.page = "Settings"
        else:
            st.error("Invalid email or password")

elif st.session_state.page == "Settings":
    st.title("Settings")
    
    if not st.session_state.logged_in:
        st.error("You must log in to access the Settings")
        st.session_state.page = "Login Page"
    else:
        settings_manager = SettingsManager()
        settings_manager.display_settings()

elif st.session_state.page == "Admin Panel":
    st.title("Maha Metro - Admin Panel")
    
    if not st.session_state.logged_in:
        st.error("You must log in to access the Admin Panel")
        st.session_state.page = "Login Page"
    else:
        st.subheader("Live Streaming")
        placeholder = st.empty()  # Placeholder for the live stream

        if st.button("Start"):
            st.session_state.stream_manager = StreamManager(
                video_path=st.session_state.video_path,
                model_name=st.session_state.model_name,
                confidence_score=st.session_state.confidence_score,
                color_thresholds=st.session_state.color_thresholds,
                model_type=st.session_state.model_type,
                frames_to_skip=st.session_state.frames_to_skip,
                beep_enabled=st.session_state.beep_enabled,
                alert_enabled=st.session_state.alert_enabled
            )
            st.session_state.stream_manager.start_streaming()

        if st.session_state.stream_manager and st.session_state.stream_manager.is_streaming:
            if st.button("Pause" if not st.session_state.stream_manager.is_paused else "Resume"):
                st.session_state.stream_manager.pause_streaming()

        if st.button("Stop"):
            if st.session_state.stream_manager:
                st.session_state.stream_manager.stop_streaming()

        if st.session_state.stream_manager and st.session_state.stream_manager.is_streaming:
            for frame in capture_camera(st.session_state.stream_manager):
                if frame is not None:
                    pil_img = Image.fromarray(frame)
                    placeholder.image(pil_img, caption="Live Stream", width=1000)