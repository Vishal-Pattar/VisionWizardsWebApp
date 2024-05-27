import os
import cv2
import requests
from dotenv import load_dotenv

class Notification:
    def __init__(self, beep=False, alert=False):
        self.beep = beep
        self.alert = alert
        load_dotenv()
        self.filename = "Output/fallen_frame.jpg"
        self.webhook_url = os.getenv("API_KEY")
        
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
        pass