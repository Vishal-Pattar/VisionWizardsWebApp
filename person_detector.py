import cv2
import time
import torch
import yolov5
from torchvision.transforms import functional as F

class ModelLoader:
    def load_fastercnn_model(self, model_path):
        return torch.load(model_path)

    def load_yolov5_model(self, model_path):
        return yolov5.load(model_path)

class PersonDetector:
    def __init__(self, model_name, confidence_score, color_thresholds, model_type='s'):
        self.model_name = model_name
        self.confidence_score = confidence_score
        self.color_thresholds = color_thresholds
        self.model_type = model_type
        self.model_loader = ModelLoader()
        
        if self.model_name == 'FasterCNN':
            self.model = self.model_loader.load_fastercnn_model("./models/fasterrcnn_resnet50_fpn_model.pth")
            self.model.eval()
        elif self.model_name == 'YOLOv5':
            model_path = f'./models/yolov5{self.model_type}.pt'
            self.model = self.model_loader.load_yolov5_model(model_path)
            self.initialize_yolo_parameters()
        else:
            raise ValueError("Invalid model type. Supported types are 'FasterCNN' and 'YOLOv5'.")
        
    def initialize_yolo_parameters(self):
        self.model.conf = self.confidence_score
        self.model.iou = 0.10
        self.model.agnostic = False
        self.model.multi_label = False
        self.model.max_det = 4
        
    def get_color(self, score):
        color_map = {"Green": (0, 255, 0), "Yellow": (0, 128, 139), "Red": (0, 0, 255), "White": (255, 255, 255)}
        if score > self.color_thresholds[0]:
            return color_map["Green"]
        elif self.color_thresholds[1] <= score <= self.color_thresholds[0]:
            return color_map["Yellow"]
        elif self.color_thresholds[1] >= score >= self.color_thresholds[2]:
            return color_map["Red"]
        else:
            return color_map["White"]
        
    def get_class(self, score):
        if score > self.color_thresholds[0]:
            return "Standing"
        elif self.color_thresholds[0] >= score >= self.color_thresholds[1]:
            return "Neutral"
        elif self.color_thresholds[1] >= score >= self.color_thresholds[2]:
            return "Fallen"
        else:
            return "Unknown"
        
    def get_area(self, height, width):
        area = int(height * width)
        if area >= 100000:
            return False
        else:
            return True
        
    def draw_boxes(self, frame, results):
        for box, ratio, color, classLabel, area in results:
            if area:
                cls = classLabel + " " + str(ratio)
                frame = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
                (text_width, text_height), baseline = cv2.getTextSize(cls, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2)
                frame = cv2.rectangle(frame, (box[0], box[1] - text_height - 4), (box[0] + text_width + 4, box[1]), color, -1)
                frame = cv2.putText(frame, cls, (box[0] + 2, box[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        return frame
        
    def detect_person_yolo(self, frame):
        predictions = self.model(frame).pred[0]
        
        flagFall = False
        results = []
        
        for box, score, label in zip(predictions[:, :4], predictions[:, 4], predictions[:, 5]):
            if label.item() == 0 and score > self.confidence_score:
                box = [int(b) for b in box]
                ratio = round(float((box[3] - box[1]) / (box[2] - box[0])), 2)
                color = self.get_color(ratio)
                class_label = self.get_class(ratio)
                area = self.get_area((box[3] - box[1]), (box[2] - box[0]))
                if class_label == "Fallen" and area:
                    flagFall = True
                results.append((box, ratio, color, class_label, area))
            
        return results, flagFall

    def detect_person_fastercnn(self, frame):
        image = F.to_pil_image(frame)
        image_tensor = F.to_tensor(image)
        image_tensor = image_tensor.unsqueeze(0)

        with torch.no_grad():
            prediction = self.model(image_tensor)
        
        flagFall = False
        results = []
        
        for score, label, box in zip(prediction[0]['scores'], prediction[0]['labels'], prediction[0]['boxes']):
            if label.item() == 1 and score > self.confidence_score:
                box = [int(b) for b in box]
                ratio = round(float((box[3] - box[1]) / (box[2] - box[0])), 2)
                color = self.get_color(ratio)
                class_label = self.get_class(ratio)
                area = self.get_area((box[3] - box[1]), (box[2] - box[0]))
                if class_label == "Fallen" and area:
                    flagFall = True
                results.append((box, ratio, color, class_label, area))
                
        return results, flagFall

    def detect_person(self, frame):
        if self.model_name == 'FasterCNN':
            return self.detect_person_fastercnn(frame)
        elif self.model_name == 'YOLOv5':
            return self.detect_person_yolo(frame)