import math
import time
import cv2
import torch #type:ignore
from utils.deep_sort import ObjectTracking
from utils.density_preprocessing import preprocess
from utils.calculate_density import model


def track(video_path):
    objectTracking = ObjectTracking()
    deepsort = objectTracking.initialize_deepsort()
    cap = cv2.VideoCapture(video_path)
    ClassNames = ['car', 'three-wheeler', 'bus', 'truck', 'two-wheeler']
    # ctime = 0
    # ptime = 0
    count = 0
    print("vehicle tracking started successfullly")
    while True:
        xywh_bboxs = []
        confs = []
        oids = []
        outputs = []
        ret, frame = cap.read()
        if ret:
            count += 1
            print(f"Frame Count: {count}")
            frame = preprocess(frame)
            results = model.predict(frame, conf = 0.20)
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    print(box.xyxy[0])
                    if torch.isnan(box.xyxy[0]).any():
                        print("Found NaN in bounding box coordinates, skipping this box.")
                        continue
                    x1, y1, x2, y2 = box.xyxy[0] 
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # Find the center coordinates of the bouding boxes
                    cx, cy = int((x1 + x2)/2), int((y1 + y2)/2)
                    #Find the height and width of the bounding boxes
                    bbox_width = abs(x1 - x2)
                    bbox_height = abs(y1 - y2)
                    xcycwh = [cx, cy, bbox_width, bbox_height]
                    xywh_bboxs.append(xcycwh)
                    conf = math.ceil(box.conf[0] * 100)/100
                    confs.append(conf)
                    classNameInt = int(box.cls[0])
                    oids.append(classNameInt)
            if len(xywh_bboxs) > 0 and len(confs) > 0:
                xywhs = torch.tensor(xywh_bboxs)
                confidence = torch.tensor(confs)
                outputs = deepsort.update(xywhs, confidence, oids, frame)
                if len(outputs) > 0:
                    bbox_xyxy = outputs[:, :4]
                    identities = outputs[:, -2]
                    classID = outputs[:, -1]
                    objectTracking.draw_boxes(frame, bbox_xyxy, identities, classID)
            else:
                print("No detections found for this frame.")

            
            '''ctime = time.time()
            fps = 1 / (ctime - ptime)
            ptime = ctime
            cv2.putText(frame, f"FPS: {str(int(fps))}", (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
            cv2.putText(frame, f"Frame Count: {str(count)}", (10, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)'''
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    print("tracking stopped successfully")
        
    cv2.destroyAllWindows()