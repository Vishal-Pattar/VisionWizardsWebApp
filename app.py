import streamlit as st
import cv2
from PIL import Image
from person_detector import PersonDetector
from video_stream import VideoStream
from notification_system import Notification
import streamlit.ReportThread as ReportThread
from streamlit.server.server import Server

# Constants
VIDEO_PATH = './sample_videos/FallOnEscalator.avi'
MODEL_NAME = "YOLOv5"  # FasterCNN or YOLOv5
MODEL_TYPE = 'n'  # n, s, m, l, x
CONFIDENCE_SCORE = 0.1
COLOR_THRESHOLDS = [1.65, 1.30, 0.70]
FRAMES_TO_SKIP = 9  # Frames to skip to reduce computation
BEEP_ENABLED = True
ALERT_ENABLED = False

# Initialize objects
person_detector = None
video_stream = None
notification_system = None

class SessionState(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def get_session():
    session = getattr(ReportThread, '_session', None)
    if session is None:
        raise RuntimeError("No session state available. Use `session_state.sync()` after `st.experimental_get_query_params()`.")
    return session

def _get_session():
    session = getattr(ReportThread, '_session', None)
    if session is None:
        raise RuntimeError("No session state available. Use `session_state.sync()` after `st.experimental_get_query_params()`.")
    return session

def session_state(**kwargs):
    this_session = _get_session()
    for key, val in kwargs.items():
        if not hasattr(this_session, key):
            setattr(this_session, key, val)
    return this_session

session_state = session_state(logged_in=True, page="Login Page", person_detector=None, video_stream=None, notification_system=None)

# Function to handle login
def login_user(email, password):
    # In a real application, add authentication logic here
    return email == "admin@mahametro.com" and password == "admin123"

# Function to capture frames from camera
def capture_camera():
    while True:
        if session_state.video_stream is None or session_state.person_detector is None or session_state.notification_system is None:
            break
        success, frame = session_state.video_stream.read_frame()
        if not success:
            break
        results, flag_fall = session_state.person_detector.detect_person(frame)
        modified_frame = session_state.person_detector.draw_boxes(frame, results)
        session_state.notification_system.notify(modified_frame, flag_fall)
        yield modified_frame

st.set_page_config(page_title="Vision Wizards", layout="centered")

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
if 'page' not in st.session_state:
    st.session_state.page = "Login Page"
    
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
        MODEL_NAME = st.selectbox("Model Name", ["YOLOv5", "FasterCNN"])
        MODEL_TYPE = st.selectbox("Model Type", ['n', 's', 'm', 'l', 'x'])
        CONFIDENCE_SCORE = st.slider("Confidence Score", 0.0, 1.0, 0.1, 0.05)

        st.subheader("Color Thresholds")
        threshold_1 = st.slider("Threshold 1", 0.0, 2.0, 1.65, 0.05)
        threshold_2 = st.slider("Threshold 2", 0.0, 2.0, 1.30, 0.05)
        threshold_3 = st.slider("Threshold 3", 0.0, 2.0, 0.70, 0.05)

        COLOR_THRESHOLDS = [threshold_1, threshold_2, threshold_3]

        FRAMES_TO_SKIP = st.number_input("Frames to Skip", min_value=1, value=9)

        st.subheader("Notification Settings")
        BEEP_ENABLED = st.checkbox("Enable Beep", value=True)
        ALERT_ENABLED = st.checkbox("Enable Alert", value=False)

        start_button = st.button("Start")
        stop_button = st.button("Stop")

        if start_button:
            session_state.person_detector = PersonDetector(MODEL_NAME, CONFIDENCE_SCORE, COLOR_THRESHOLDS, MODEL_TYPE)
            session_state.video_stream = VideoStream(VIDEO_PATH, FRAMES_TO_SKIP)
            session_state.notification_system = Notification(beep=BEEP_ENABLED, alert=ALERT_ENABLED)
            session_state.notification_system.beep_sound()
            session_state.page = "Admin Panel"

        if stop_button:
            session_state.person_detector = None
            session_state.video_stream = None
            session_state.notification_system = None
            session_state.page = "Settings"

elif st.session_state.page == "Admin Panel":
    st.title("Maha Metro - Admin Panel")
    placeholder = st.empty()  # Placeholder for the live stream
    if not st.session_state.logged_in:
        st.error("You must log in to access the Admin Panel")
        st.session_state.page = "Login Page"
    else:
        st.subheader("Live Streaming")
        # Continuously update the live stream
        for frame in capture_camera():
            # Convert the OpenCV frame to PIL image
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame)
            # Update the placeholder with the new frame
            placeholder.image(pil_img, caption="Live Stream", width=1000)