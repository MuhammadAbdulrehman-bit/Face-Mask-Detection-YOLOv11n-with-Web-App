from ultralytics import YOLO
import cv2
import threading
import winsound
from datetime import datetime
import csv
import os
import time

log_file = "violations_log.csv"
if not os.path.exists(log_file):
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Status", "Confidence"])


if not os.path.exists("violations"):
    os.makedirs("violations")


model = YOLO("runs\\detect\\train2\\weights\\best.pt")

def beep_alert():
    winsound.Beep(1000, 500)

def save_violation_image(frame):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f"violations/violation_{timestamp}.jpg"
    cv2.imwrite(filepath, frame)

custom_names = {
    0: "Wearing Mask",
    1: "Not Wearing Mask"
}


cap = cv2.VideoCapture(0)


last_violation_time = 0  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    violation_found = False
    highest_conf = 0  

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = f"{custom_names[cls_id]} {conf:.2f}"
            xyxy = box.xyxy[0].cpu().numpy().astype(int)

            
            color = (0, 255, 0) if cls_id == 0 else (0, 0, 255)
            cv2.rectangle(frame, tuple(xyxy[:2]), tuple(xyxy[2:]), color, 2)
            cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            if cls_id == 1:
                violation_found = True
                if conf > highest_conf:
                    highest_conf = conf  

    
    current_time = time.time()
    if violation_found and (current_time - last_violation_time >= 5):
        last_violation_time = current_time
        threading.Thread(target=beep_alert).start()
        save_violation_image(frame)

        
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "No Mask", f"{highest_conf:.2f}"])

    # 
    cv2.imshow("Mask Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
