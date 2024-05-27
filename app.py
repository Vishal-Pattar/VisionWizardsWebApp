import streamlit as st
import cv2
from PIL import Image
from person_detector import PersonDetector
from video_stream import VideoStream
from notification_system import Notification

# Constants
DEFAULT_VIDEO_PATH = './sample_videos/FallOnEscalator.avi'
DEFAULT_MODEL_NAME = "YOLOv5"  # FasterCNN or YOLOv5
DEFAULT_MODEL_TYPE = 'n'  # n, s, m, l, x
DEFAULT_CONFIDENCE_SCORE = 0.1
DEFAULT_COLOR_THRESHOLDS = [1.65, 1.30, 0.70]
DEFAULT_FRAMES_TO_SKIP = 9  # Frames to skip to reduce computation
DEFAULT_BEEP_ENABLED = True
DEFAULT_ALERT_ENABLED = False

# Function to handle login
def login_user(email, password):
    # In a real application, add authentication logic here
    return email == "admin@mahametro.com" and password == "admin123"

# Function to capture frames from camera
def capture_camera():
    while True:
        if st.session_state.video_stream is None or st.session_state.person_detector is None or st.session_state.notification_system is None:
            break
        success, frame = st.session_state.video_stream.read_frame()
        if not success:
            break
        results, flag_fall = st.session_state.person_detector.detect_person(frame)
        modified_frame = st.session_state.person_detector.draw_boxes(frame, results)
        st.session_state.notification_system.notify(modified_frame, flag_fall)
        yield modified_frame

st.set_page_config(page_title="Vision Wizards", layout="wide")

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Login Page"
if 'person_detector' not in st.session_state:
    st.session_state.person_detector = None
if 'video_stream' not in st.session_state:
    st.session_state.video_stream = None
if 'notification_system' not in st.session_state:
    st.session_state.notification_system = None
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False
if 'is_paused' not in st.session_state:
    st.session_state.is_paused = False

# Default settings
def reset_to_defaults():
    st.session_state.model_name = DEFAULT_MODEL_NAME
    st.session_state.model_type = DEFAULT_MODEL_TYPE
    st.session_state.confidence_score = DEFAULT_CONFIDENCE_SCORE
    st.session_state.color_thresholds = DEFAULT_COLOR_THRESHOLDS
    st.session_state.frames_to_skip = DEFAULT_FRAMES_TO_SKIP
    st.session_state.beep_enabled = DEFAULT_BEEP_ENABLED
    st.session_state.alert_enabled = DEFAULT_ALERT_ENABLED

reset_to_defaults()  # Initialize settings with default values

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
        # Add UI elements for settings
        st.subheader("Model Configuration")
        st.session_state.model_name = st.selectbox("Model Name", ["YOLOv5", "FasterCNN"], index=["YOLOv5", "FasterCNN"].index(st.session_state.model_name))
        st.session_state.model_type = st.selectbox("Model Type", ['n', 's', 'm', 'l', 'x'], index=['n', 's', 'm', 'l', 'x'].index(st.session_state.model_type))
        st.session_state.confidence_score = st.slider("Confidence Score", 0.0, 1.0, st.session_state.confidence_score, 0.05)

        st.subheader("Color Thresholds")
        st.session_state.color_thresholds[0] = st.slider("Threshold 1", 0.0, 2.0, st.session_state.color_thresholds[0], 0.05)
        st.session_state.color_thresholds[1] = st.slider("Threshold 2", 0.0, 2.0, st.session_state.color_thresholds[1], 0.05)
        st.session_state.color_thresholds[2] = st.slider("Threshold 3", 0.0, 2.0, st.session_state.color_thresholds[2], 0.05)

        st.session_state.frames_to_skip = st.number_input("Frames to Skip", min_value=1, value=st.session_state.frames_to_skip)

        st.subheader("Notification Settings")
        st.session_state.beep_enabled = st.checkbox("Enable Beep", value=st.session_state.beep_enabled)
        st.session_state.alert_enabled = st.checkbox("Enable Alert", value=st.session_state.alert_enabled)

        if st.button("Save"):
            st.success("Settings saved successfully")

        if st.button("Reset"):
            reset_to_defaults()
            st.success("Settings reset to default values")

elif st.session_state.page == "Admin Panel":
    st.title("Maha Metro - Admin Panel")
    placeholder = st.empty()  # Placeholder for the live stream
    if not st.session_state.logged_in:
        st.error("You must log in to access the Admin Panel")
        st.session_state.page = "Login Page"
    else:
        st.subheader("Live Streaming")

        if st.button("Start"):
            st.session_state.person_detector = PersonDetector(st.session_state.model_name, st.session_state.confidence_score, st.session_state.color_thresholds, st.session_state.model_type)
            st.session_state.video_stream = VideoStream(DEFAULT_VIDEO_PATH, st.session_state.frames_to_skip)
            st.session_state.notification_system = Notification(beep=st.session_state.beep_enabled, alert=st.session_state.alert_enabled)
            st.session_state.notification_system.beep_sound()
            st.session_state.is_streaming = True
            st.session_state.is_paused = False

        if st.button("Pause"):
            st.session_state.is_paused = not st.session_state.is_paused

        if st.button("Stop"):
            st.session_state.person_detector = None
            st.session_state.video_stream = None
            st.session_state.notification_system = None
            st.session_state.is_streaming = False
            st.session_state.is_paused = False

        if st.session_state.is_streaming:
            for frame in capture_camera():
                if st.session_state.is_paused:
                    continue
                # Convert the OpenCV frame to PIL image
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame)
                # Update the placeholder with the new frame
                placeholder.image(pil_img, caption="Live Stream", width=1000)