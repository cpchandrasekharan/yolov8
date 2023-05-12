import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import Tracker

model = YOLO('best.pt')
cap = cv2.VideoCapture('surf.mp4')
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
tracker = Tracker()

while True:    
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1020, 500))
    frame = cv2.flip(frame, 1)
    results = model.predict(frame)
    objects_rect = []
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result
        if conf > 0.5:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            objects_rect.append((x1, y1, x2-x1, y2-y1))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, class_list[int(cls)], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    
    # Update the tracker with the detected objects
    objects_bbs_ids = tracker.update(objects_rect)
    for object_bb_id in objects_bbs_ids:
        x1, y1, w, h, object_id = object_bb_id
        cv2.putText(frame, "ID: " + str(object_id), (x1, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
