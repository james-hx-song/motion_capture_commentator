from cvzone.PoseModule import PoseDetector
from motion import processImg
from pyautogui import press, typewrite, hotkey
from collections import Counter
import cv2
import numpy as np
import utils
import time

# Initialize the webcam and set it to the third camera (index 2)
cap = cv2.VideoCapture(0)

# Initialize the PoseDetector class with the given parameters
detector = PoseDetector(staticMode=False,
                        modelComplexity=1,
                        smoothLandmarks=True,
                        enableSegmentation=False,
                        smoothSegmentation=True,
                        detectionCon=0.5,
                        trackCon=0.5)




i = 0
img_left_processed, img_right_processed = None, None
time_left, time_right = 0, 0
# Loop to continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    keys_idx = []
    keys_idx_l, keys_idx_r = [], []
    for _ in range(int(utils.FRAMESPERSEC * utils.SECSTOWAIT)):
        success, img = cap.read()

        if not success:
            print("Failed to capture image")
            break

        # Get the height and width of the image
        height, width, _ = img.shape

        # # Split the image vertically into two parts
        img_left = img[:, width // 2:]   # Left half
        img_right = img[:, :width // 2]  # Right half

        img_left_processed_new, idx_l = processImg(detector, img_left, True)
        if img_left_processed_new is not None:
            img_left_processed = img_left_processed_new
            if idx_l is not None and idx_l != -1:
                keys_idx_l.append(idx_l)

        img_right_processed_new, idx_r = processImg(detector, img_right, False)
        if img_right_processed_new is not None:
            img_right_processed = img_right_processed_new
            if idx_r is not None and idx_r != -1:
                keys_idx_r.append(idx_r)

        # print(img_left_processed.shape, img_right_processed.shape)
        if img_left_processed is not None and img_right_processed is not None:
            img = np.hstack((img_right_processed, img_left_processed))





            # Display the frame in a window

        
        cv2.imshow("Image", img)

        # img, idx = processImg(detector, img, True)

        # if img is not None:
        #     cv2.imshow("Image", img)
        #     if idx is not None and idx != -1:
        #         keys_idx.append(idx)

        cv2.waitKey(1000 // utils.FRAMESPERSEC)
    
    # if len(keys_idx) > 0:
    #     idx, count = Counter(keys_idx).most_common(1)[0]
    #     if count >= utils.THRESHOLD[idx]:
    #         print("FINAL RENDER: ", utils.FUNCS[idx])
    #         key = utils.KEYS[idx]
    #         press(key)
    
    if len(keys_idx_l) > 0:
        idx, count = Counter(keys_idx_l).most_common(1)[0]
        # curr_time = time.time()
        if count >= utils.THRESHOLD[idx]:
            print("FINAL RENDER (L): ", utils.FUNCS[idx])
            key = utils.KEYSL[idx]
            press(key)
            # time_left = time.time()
    
    if len(keys_idx_r) > 0:
        idx, count = Counter(keys_idx_r).most_common(1)[0]
        # curr_time = time.time()
        if count >= utils.THRESHOLD[idx]:
            print("FINAL RENDER (R): ", utils.FUNCS[idx])
            key = utils.KEYSR[idx]
            press(key)
            # time_right = time.time()

        
    i += 1
