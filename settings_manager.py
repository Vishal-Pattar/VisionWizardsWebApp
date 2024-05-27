import streamlit as st
import os

DEFAULT_MODEL_NAME = "YOLOv5"
DEFAULT_MODEL_TYPE = 'n'
DEFAULT_CONFIDENCE_SCORE = 0.1
DEFAULT_COLOR_THRESHOLDS = [1.65, 1.30, 0.70]
DEFAULT_FRAMES_TO_SKIP = 9
DEFAULT_BEEP_ENABLED = True
DEFAULT_ALERT_ENABLED = False
DEFAULT_VIDEO_FILE = "sample1.mp4"
DEFAULT_VIDEO_PATH = "sample_videos"

class SettingsManager:
    def __init__(self):
        self.reset_to_defaults()

    def reset_to_defaults(self):
        """
        Reset settings to default values.
        """
        self.model_name = DEFAULT_MODEL_NAME
        self.model_type = DEFAULT_MODEL_TYPE
        self.confidence_score = DEFAULT_CONFIDENCE_SCORE
        self.color_thresholds = DEFAULT_COLOR_THRESHOLDS.copy()
        self.frames_to_skip = DEFAULT_FRAMES_TO_SKIP
        self.beep_enabled = DEFAULT_BEEP_ENABLED
        self.alert_enabled = DEFAULT_ALERT_ENABLED
        self.video_file = DEFAULT_VIDEO_FILE
        self.video_path = DEFAULT_VIDEO_PATH

    def save_settings_to_session_state(self):
        """
        Save settings to session_state.
        """
        st.session_state.model_name = self.model_name
        st.session_state.model_type = self.model_type
        st.session_state.confidence_score = self.confidence_score
        st.session_state.color_thresholds = self.color_thresholds
        st.session_state.frames_to_skip = self.frames_to_skip
        st.session_state.beep_enabled = self.beep_enabled
        st.session_state.alert_enabled = self.alert_enabled
        st.session_state.video_file = self.video_file
        st.session_state.video_path = self.video_path

    def display_settings(self):
        """
        Display the settings page in the Streamlit app.
        """
        st.subheader("Video File")
        option = st.radio("Choose Option:", ("Select from options", "Upload file"))

        if option == "Select from options":
            video_files = os.listdir("sample_videos")
            self.video_file = st.selectbox("Video File", video_files)
            self.video_path = os.path.join("sample_videos", self.video_file)
        else:
            uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "avi"])
            if uploaded_file is not None:
                self.video_file = uploaded_file.name
                self.video_path = os.path.join("uploads", self.video_file)
                with open(self.video_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

        st.subheader("Model Configuration")
        self.model_name = st.selectbox("Model Name", ["YOLOv5", "FasterCNN"], index=["YOLOv5", "FasterCNN"].index(self.model_name))
        self.model_type = st.selectbox("Model Type", ['n', 's', 'm', 'l', 'x'], index=['n', 's', 'm', 'l', 'x'].index(self.model_type))
        self.confidence_score = st.slider("Confidence Score", 0.0, 1.0, self.confidence_score, 0.05)

        st.subheader("Color Thresholds")
        self.color_thresholds[0] = st.slider("Threshold 1", 0.0, 2.0, self.color_thresholds[0], 0.05)
        self.color_thresholds[1] = st.slider("Threshold 2", 0.0, 2.0, self.color_thresholds[1], 0.05)
        self.color_thresholds[2] = st.slider("Threshold 3", 0.0, 2.0, self.color_thresholds[2], 0.05)

        self.frames_to_skip = st.number_input("Frames to Skip", min_value=1, value=self.frames_to_skip)

        st.subheader("Notification Settings")
        self.beep_enabled = st.checkbox("Enable Beep", value=self.beep_enabled)
        self.alert_enabled = st.checkbox("Enable Alert", value=self.alert_enabled)

        if st.button("Save"):
            self.save_settings_to_session_state()
            st.success("Settings saved successfully")

        if st.button("Reset"):
            self.reset_to_defaults()
            st.success("Settings reset to default values")