from ultralytics import YOLO #type:ignore
from utils.plot_anpr import plot_bboxes
import cv2
import numpy as np
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir,"..")
lp_mdl_path = base_dir+r"\model\anpr\license_plate_detector.pt"
model_lp =  YOLO(lp_mdl_path)


def run_anpr(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file")

    print("ANPR started Successfully")
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break  
        results = model_lp(frame)
        output_frame = plot_bboxes(results)

        cv2.imshow('YOLO Prediction', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  
    cap.release()
    print("ANPR closed successfully")
    cv2.destroyAllWindows()