import torch
import pyttsx3
import cv2
import numpy as np

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 'yolov5s' is a small, fast model
model.classes = [0, 39]  # Optional: Select specific classes (e.g., person, bottle)

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB for YOLO
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Inference
    results = model(rgb_frame)

    # Parse results
    for *box, conf, cls in results.xyxy[0]:  # Bounding box coordinates, confidence, class
        label = model.names[int(cls)]  # Get class label
        tts_engine.say(f"Detected: {label}")
        tts_engine.runAndWait()

        # Draw bounding box and label
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Object Detection", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()