from cvzone.PoseModule import PoseDetector
from motion import processImg
from pyautogui import press, typewrite, hotkey
from collections import Counter
import cv2
import numpy as np
import utils

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
# Loop to continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    keys_idx = []
    for _ in range(utils.FRAMESPERSEC * utils.SECSTOWAIT):
        success, img = cap.read()

        if not success:
            print("Failed to capture image")
            break

        # Get the height and width of the image
        height, width, _ = img.shape

        # # Split the image vertically into two parts
        # img_left = img[:, :width // 2]   # Left half
        # img_right = img[:, width // 2:]  # Right half

        # img_left_processed_new = processImg(detector, img_left, True)
        # if img_left_processed_new is not None:
        #     img_left_processed = img_left_processed_new

        # img_right_processed_new = processImg(detector, img_right, False)
        # if img_right_processed_new is not None:
        #     img_right_processed = img_right_processed_new

        # print(img_left_processed.shape, img_right_processed.shape)
        # if img_left_processed is not None and img_right_processed is not None:
        #     img = np.hstack((img_left_processed, img_right_processed))

        #     # Display the frame in a window

        
        #     cv2.imshow("Image", img)

        img, idx = processImg(detector, img, True)

        if img is not None:
            cv2.imshow("Image", img)
            if idx is not None and idx != -1:
                keys_idx.append(idx)

        cv2.waitKey(1000 // utils.FRAMESPERSEC)
    
    if len(keys_idx) > 0:
        idx, count = Counter(keys_idx).most_common(1)[0]
        if count >= utils.THRESHOLD[idx]:
            print("FINAL RENDER: ", utils.FUNCS[idx])
            key = utils.KEYS[idx]
            press(key)

    i += 1
