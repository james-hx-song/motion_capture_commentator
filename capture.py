from cvzone.PoseModule import PoseDetector
from motion import processImg
import cv2
import numpy as np

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

# Loop to continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    success, img = cap.read()

    if not success:
        print("Failed to capture image")
        break

    # Get the height and width of the image
    height, width, _ = img.shape

    # Split the image vertically into two parts
    img_left = img[:, :width // 2]   # Left half
    img_right = img[:, width // 2:]  # Right half

    img_left_processed = processImg(detector, img_left)
    img_left_processed = img_left if 'img_left_processed' not in locals() else img_left_processed
    img_right_processed = processImg(detector, img_right)
    img_right_processed = img_right if 'img_right_processed' not in locals(
    ) else img_right_processed

    # Combine the two images back into one
    if i > 1:
        if img_left_processed is not None and img_right_processed is not None:
            img = np.hstack((img_left_processed, img_right_processed))
        else:
            img = img_left if img_left_processed is not None else img_right
    else:
        img = img_left

    # Display the frame in a window
    cv2.imshow("Image", img)

    # Wait for 1 millisecond between each frame
    cv2.waitKey(100)
    i += 1
