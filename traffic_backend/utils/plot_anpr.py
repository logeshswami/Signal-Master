import cv2
import numpy as np
import easyocr  # type: ignore
from utils.anpr_preprocess import preprocess_anpr
from utils.logger import setup_anpr_logger

reader = easyocr.Reader(['en'])

def plot_bboxes(results):
    img = results[0].orig_img  
    names = results[0].names  
    scores = results[0].boxes.conf.numpy()  
    classes = results[0].boxes.cls.numpy()  
    boxes = results[0].boxes.xyxy.numpy().astype(np.int32)  
    anpr_logger = setup_anpr_logger()  
      
    for score, cls, bbox in zip(scores, classes, boxes):  
        class_label = names[cls]  
        label = f"{class_label} : {score:0.2f}" 
        lbl_margin = 3  
        roi = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        processed = preprocess_anpr(roi)
        text = reader.readtext(processed)
        
        if text:
            detected_text = text[0][-2]
            label = f"{class_label} : {detected_text}"
            if(len(detected_text)>5 ):
                anpr_logger.info(label)
        
        img = cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                            color=(0, 0, 255), thickness=1)

        
        label_size = cv2.getTextSize(label, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=1)
        lbl_w, lbl_h = label_size[0]  
        lbl_w += 2 * lbl_margin 
        lbl_h += 2 * lbl_margin

        
        img = cv2.rectangle(img, (bbox[0], bbox[1]), 
                            (bbox[0] + lbl_w, bbox[1] - lbl_h),
                            color=(0, 0, 255), thickness=-1)

        
        cv2.putText(img, label, (bbox[0] + lbl_margin, bbox[1] - lbl_margin),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0,
                    color=(255, 255, 255), thickness=1)

    return img
