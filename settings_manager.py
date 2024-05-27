import streamlit as st

DEFAULT_MODEL_NAME = "YOLOv5"
DEFAULT_MODEL_TYPE = 'n'
DEFAULT_CONFIDENCE_SCORE = 0.1
DEFAULT_COLOR_THRESHOLDS = [1.65, 1.30, 0.70]
DEFAULT_FRAMES_TO_SKIP = 9
DEFAULT_BEEP_ENABLED = True
DEFAULT_ALERT_ENABLED = False

class SettingsManager:
    def __init__(self):
        self.reset_to_defaults()

    def reset_to_defaults(self):
        """
        Reset settings to default values.
        """
        st.session_state.model_name = DEFAULT_MODEL_NAME
        st.session_state.model_type = DEFAULT_MODEL_TYPE
        st.session_state.confidence_score = DEFAULT_CONFIDENCE_SCORE
        st.session_state.color_thresholds = DEFAULT_COLOR_THRESHOLDS
        st.session_state.frames_to_skip = DEFAULT_FRAMES_TO_SKIP
        st.session_state.beep_enabled = DEFAULT_BEEP_ENABLED
        st.session_state.alert_enabled = DEFAULT_ALERT_ENABLED

    def display_settings(self):
        """
        Display the settings page in the Streamlit app.
        """
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
            self.reset_to_defaults()
            st.success("Settings reset to default values")