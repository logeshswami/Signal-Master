import cv2
import numpy as np
from utils.calculate_density import model  
from utils.anpr import model_lp  
from utils.anpr_preprocess import preprocess_anpr  
from utils.plot_anpr import reader


def detect_and_recognize(frame):
    frame = cv2.resize(frame,(640,640))
    # Detect vehicles
    vehicle_results = model(frame)
    if vehicle_results is None or len(vehicle_results[0].boxes) == 0:
        return frame  # No vehicles detected, return original frame

    vehicle_boxes = vehicle_results[0].boxes.xyxy.cpu().numpy().astype(np.int32)  # Get bounding boxes
    scores = vehicle_results[0].boxes.conf.cpu().numpy()
    classes = vehicle_results[0].boxes.cls.cpu().numpy()
    names = vehicle_results[0].names
    for score,cls,box in zip(scores,classes,vehicle_boxes):
        x1, y1, x2, y2= box
        name = names[cls]
        vehicle_roi = frame[int(y1):int(y2), int(x1):int(x2)]  

        # Detect license plate in the vehicle ROI
        license_plate_results = model_lp(vehicle_roi)
        if license_plate_results is None or len(license_plate_results[0].boxes) == 0:
            continue  # No license plates detected in this vehicle

        license_plate_boxes = license_plate_results[0].boxes.xyxy.cpu().numpy().astype(np.int32)  # Get bounding boxes

        for lp_box in license_plate_boxes:
            lp_x1, lp_y1, lp_x2, lp_y2 = lp_box
            license_plate_roi = vehicle_roi[int(lp_y1):int(lp_y2), int(lp_x1):int(lp_x2)]  # Crop license plate ROI

            # Preprocess the license plate image
            processed_license_plate = preprocess_anpr(license_plate_roi)

            # Use EasyOCR to extract text
            results = reader.readtext(processed_license_plate)
            license_plate_text = ''
            if results:
                
                license_plate_text = results[0][1]

         
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Vehicle box
            cv2.putText(frame, f'Vehicle: {name}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.rectangle(frame, (int(x1 + lp_x1), int(y1 + lp_y1)), (int(x1 + lp_x2), int(y1 + lp_y2)), (255, 255, 255), 2)  # License plate box
            cv2.putText(frame, license_plate_text if license_plate_text else "", 
                        (int(x1 + lp_x1), int(y1 + lp_y1)-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return frame


def run_arial_anpr(video_path):
    cap = cv2.VideoCapture(video_path)  
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result_frame = detect_and_recognize(frame)

        cv2.imshow('Detection Result', result_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
