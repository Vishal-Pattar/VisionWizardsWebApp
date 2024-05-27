import streamlit as st
import cv2
from person_detector import PersonDetector
from video_stream import VideoStream
from notification_system import Notification

DEFAULT_VIDEO_PATH = './sample_videos/FallOnEscalator.avi'

def capture_camera():
    """
    Generator function to capture frames from the video stream.
    """
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

class StreamManager:
    def __init__(self):
        self.is_streaming = False
        self.is_paused = False

    def start_streaming(self):
        """
        Start the video streaming process.
        """
        st.session_state.person_detector = PersonDetector(st.session_state.model_name, st.session_state.confidence_score, st.session_state.color_thresholds, st.session_state.model_type)
        st.session_state.video_stream = VideoStream(DEFAULT_VIDEO_PATH, st.session_state.frames_to_skip)
        st.session_state.notification_system = Notification(beep=st.session_state.beep_enabled, alert=st.session_state.alert_enabled)
        st.session_state.notification_system.beep_sound()
        self.is_streaming = True
        self.is_paused = False

    def pause_streaming(self):
        """
        Pause or resume the video streaming process.
        """
        self.is_paused = not self.is_paused

    def stop_streaming(self):
        """
        Stop the video streaming process.
        """
        st.session_state.person_detector = None
        st.session_state.video_stream = None
        st.session_state.notification_system = None
        self.is_streaming = False
        self.is_paused = False

    def process_frame(self, frame):
        """
        Process a frame for display.

        :param frame: The frame to process
        :return: Processed frame
        """
        # Convert the OpenCV frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
