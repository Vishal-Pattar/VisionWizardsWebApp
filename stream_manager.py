import cv2
from person_detector import PersonDetector
from video_stream import VideoStream
from notification_system import Notification

class StreamManager:
    def __init__(self, video_path, model_name, confidence_score, color_thresholds, model_type, frames_to_skip, beep_enabled, alert_enabled):
        self.person_detector = PersonDetector(model_name, confidence_score, color_thresholds, model_type)
        self.video_stream = VideoStream(video_path, frames_to_skip)
        self.notification_system = Notification(beep=beep_enabled, alert=alert_enabled)
        self.is_streaming = False
        self.is_paused = False
        self.current_frame = None

    def start_streaming(self):
        self.is_streaming = True
        self.is_paused = False

    def pause_streaming(self):
        self.is_paused = not self.is_paused

    def stop_streaming(self):
        self.is_streaming = False
        self.is_paused = False
        self.person_detector = None
        self.video_stream = None
        self.notification_system = None

    def read_frame(self):
        success, frame = self.video_stream.read_frame()
        if success:
            results, flag_fall = self.person_detector.detect_person(frame)
            self.current_frame = self.person_detector.draw_boxes(frame, results)
            self.notification_system.notify(self.current_frame, flag_fall)
        return success

    def process_frame(self):
        if self.current_frame is not None:
            frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            return frame
        return None

def capture_camera(stream_manager):
    while stream_manager.is_streaming:
        if not stream_manager.is_paused:
            success = stream_manager.read_frame()
            if not success:
                break
        yield stream_manager.process_frame()