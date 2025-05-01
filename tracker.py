import cv2
import json
from ultralytics import YOLO

#model = YOLO("yolov8n.pt")  # You can fine-tune or use a custom model
model = YOLO("last.pt")

def track_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    results = []

    frame_number = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        detections = model(frame)[0]  # Detect in current frame
        frame_data = {
            'frame': frame_number,
            'timestamp': frame_number / fps,
            'objects': []
        }

        for box in detections.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            if label in ['person', 'sports ball']:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                frame_data['objects'].append({
                    'label': label,
                    'bbox': [x1, y1, x2, y2],
                    'confidence': float(box.conf[0])
                })

        results.append(frame_data)
        frame_number += 1

    cap.release()
    return results
