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
    
    def notify(self, modified_frame, flagFall):
        if flagFall and self.beep:
            self.beep_sound()
        
        if flagFall and self.alert:
            self.send_webhook(modified_frame)
            
    def send_webhook(self, frame):
        cv2.imwrite(self.filename, frame)
        with open(self.filename, "rb") as f:
            files = {"file": (self.filename, f)}
            requests.post(self.webhook_url, files=files)
        if os.path.exists(self.filename):
            os.remove(self.filename)
            
    def beep_sound(self):
        frequency = 2500  # Frequency of the beep (Hz)
        duration = 0.5    # Duration of the beep (seconds)
        sample_rate = 44100  # Sampling rate (samples per second)

        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        samples = (np.sin(2 * np.pi * frequency * t)).astype(np.float32)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
        stream.write(samples.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()