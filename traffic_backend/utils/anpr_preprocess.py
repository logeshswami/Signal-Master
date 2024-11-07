import cv2
import numpy as np
def preprocess_anpr(img):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("grap",gray)    
    kernel_sharp =np.array([[0, -0.3, 0], [-0.3, 2.0, -0.3], [0, -0.3, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel_sharp)
    #cv2.imshow("sharp",sharpened)
    #cv2.imshow("orginal",img)
    blurred = cv2.GaussianBlur(sharpened, (3, 3), 0)
    #cv2.imshow("blur",blurred)
    _,binary = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow("binary",binary)
    kernel_open = np.ones((3, 3), np.uint8)
    opened_image = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_open)
    #cv2.imshow('Opened Image', opened_image)
    return binary