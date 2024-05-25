import cv2

class VideoStream:
    def __init__(self, video_path, frames_to_skip=0):
        self.video_path = video_path
        self.frames_to_skip = frames_to_skip
        self.cap = cv2.VideoCapture(video_path)

    def read_frame(self):
        frames_to_skip = self.frames_to_skip
        while frames_to_skip >= 0:
            success, frame = self.cap.read()
            frames_to_skip -= 1
        return success, frame