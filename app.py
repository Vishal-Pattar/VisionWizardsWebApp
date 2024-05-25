import streamlit as st
import cv2
from PIL import Image
from person_detector import PersonDetector
from video_stream import VideoStream
from notification_system import Notification

# Constants
VIDEO_PATH = './sample_videos/FallOnEscalator.avi'
MODEL_NAME = "YOLOv5"  # FasterCNN or YOLOv5
MODEL_TYPE = 'n'  # n, s, m, l, x
CONFIDENCE_SCORE = 0.1
COLOR_THRESHOLDS = [1.65, 1.30, 0.70]
FRAMES_TO_SKIP = 9  # Frames to skip to reduce computation

# Initialize objects
person_detector = PersonDetector(MODEL_NAME, CONFIDENCE_SCORE, COLOR_THRESHOLDS, MODEL_TYPE)
video_stream = VideoStream(VIDEO_PATH, FRAMES_TO_SKIP)
notification_system = Notification(beep=True, alert=False)

# Function to handle login
def login_user(email, password):
    # In a real application, add authentication logic here
    return email == "admin@mahametro.com" and password == "admin123"

# Function to capture frames from camera
def capture_camera():
    while True:
        success, frame = video_stream.read_frame()
        if not success:
            break
        results, flag_fall = person_detector.detect_person(frame)
        modified_frame = person_detector.draw_boxes(frame, results)
        notification_system.notify(modified_frame, flag_fall)
        yield modified_frame

# Main function to define the Streamlit app
def main():
    st.set_page_config(page_title="Maha Metro", layout="wide")

    # Initialize session state variables if they don't exist
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True
    if 'page' not in st.session_state:
        st.session_state.page = "Login Page"

    # Sidebar navigation with buttons
    st.sidebar.title("Maha Metro")
    if st.sidebar.button("Login Page"):
        st.session_state.page = "Login Page"
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
                st.session_state.page = "Admin Panel"
                st.experimental_rerun()
            else:
                st.error("Invalid email or password")

    elif st.session_state.page == "Admin Panel":
        if st.session_state.logged_in:
            st.title("Maha Metro - Admin Panel")
            st.subheader("Live Streaming")
            placeholder = st.empty()  # Placeholder for the live stream

            # Continuously update the live stream
            for frame in capture_camera():
                # Convert the OpenCV frame to PIL image
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame)
                # Update the placeholder with the new frame
                placeholder.image(pil_img, caption="Live Stream", width=800)
        else:
            st.error("You must log in to access the Admin Panel")
            st.session_state.page = "Login Page"
            st.experimental_rerun()

if __name__ == "__main__":
    main()