import cv2
import numpy as np
def preprocess(img):
    #img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    img = cv2.resize(img,(640,640))
    #denoised_image = cv2.GaussianBlur(image, (3, 3), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    print(mean_brightness)
    if mean_brightness < 50 or mean_brightness > 200:
        print("processing")
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=1.75 ,tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        brightened_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        strong_sharpen = np.array([[0, -0.3, 0], [-0.3, 2.0, -0.3], [0, -0.3, 0]])
        sharpened = cv2.filter2D(brightened_image, -1, strong_sharpen)
        #cv2.imshow("sharp",sharpened)
        blurred = cv2.GaussianBlur(sharpened, (3,3), 0)
        #cv2.imshow("blur",blurred)
        brightened_image = blurred
    else:
        
        strong_sharpen = np.array([[0, -0.3, 0], [-0.3, 2.0, -0.3], [0, -0.3, 0]])
        sharpened = cv2.filter2D(img, -1, strong_sharpen)
        blurred = cv2.GaussianBlur(sharpened, (3,3), 0)
        #cv2.imshow("blur",blurred)
        brightened_image = blurred
        #cv2.imshow("sharp",sharpened)
        #brightened_image = sharpened
        #brightened_image = img
    
    #cv2.imshow('Original Image', img)
    #cv2.imshow('Processed Image', brightened_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    return brightened_image