import os
import cv2
import requests
from dotenv import load_dotenv
import numpy as np
import pyaudio

class Notification:
    def __init__(self, beep=False, alert=False):
        self.beep = beep
        self.alert = alert
        load_dotenv()
        self.filename = "Output/fallen_frame.jpg"
        self.webhook_url = os.getenv("API_KEY")
        
        if self.beep:
            self.frequency = 2500
            self.duration = 0.5
            self.sample_rate = 44100
            self.t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
            self.samples = (np.sin(2 * np.pi * self.frequency * self.t)).astype(np.float32)
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True)
    
    def notify(self, modified_frame, flagFall):
        if flagFall and self.beep:
            self.play_beep()
        
        if flagFall and self.alert:
            self.send_webhook(modified_frame)
    
    def send_webhook(self, frame):
        cv2.imwrite(self.filename, frame)
        with open(self.filename, "rb") as f:
            files = {"file": (self.filename, f)}
            requests.post(self.webhook_url, files=files)
        if os.path.exists(self.filename):
            os.remove(self.filename)
    
    def play_beep(self):
        self.stream.write(self.samples.tobytes())
    
    def __del__(self):
        if self.beep:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()