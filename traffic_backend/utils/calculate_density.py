import math
import cv2
from .density_preprocessing import preprocess
from ultralytics import YOLO # type: ignore
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir,"..")
mdl_path = base_dir+r"\model\70_epoch\weights\last.pt"
model = YOLO(mdl_path,verbose=False)

def calc_density(video_path):
    density = {"car":0,"tri-wheeler":0,"two-wheeler":0,"truck":0,"bus":0}
    frame_cnt = 0
    cap = cv2.VideoCapture(video_path)
    if(not cap.isOpened()):
        print("Error opening video file")
    
    while(cap.isOpened() and  frame_cnt<20):
        ret , frame = cap.read()
        
        if not ret:
            break
        frame = preprocess(frame)
        result = model(frame)
        class_ids = result[0].boxes.cls.cpu().numpy()
        for class_id in class_ids:
            class_name = model.names[int(class_id)]
            if class_name in density:
                density[class_name] += 1 
        #print(f"{frame_cnt} : {result}")
        frame_cnt+=1
    if(frame_cnt>0):
        for class_name in density:
            density[class_name] = math.ceil(density[class_name] / frame_cnt)
            
    #print(density)

    return density