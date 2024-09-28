from cvzone.PoseModule import PoseDetector
import cv2
import numpy as np

# Initialize the webcam and set it to the third camera (index 2)
cap = cv2.VideoCapture(1)

# Initialize the PoseDetector class with the given parameters
detector = PoseDetector(staticMode=False,
                        modelComplexity=1,
                        smoothLandmarks=True,
                        enableSegmentation=False,
                        smoothSegmentation=True,
                        detectionCon=0.5,
                        trackCon=0.5)


def processImg(img):
    # Find the human pose in the frame
    img = detector.findPose(img)

    lmList, bboxInfo = detector.findPosition(
        img, draw=True, bboxWithHands=False)

    # Check if any body landmarks are detected
    if lmList:
        # Get the center of the bounding box around the body
        center = bboxInfo["center"]

        # Draw a circle at the center of the bounding box
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        # Calculate the distance between landmarks 11 and 15 and draw it on the image
        length, img, info = detector.findDistance(lmList[11][0:2],
                                                  lmList[15][0:2],
                                                  img=img,
                                                  color=(255, 0, 0),
                                                  scale=10)

        # Calculate the angle between landmarks 11, 13, and 15 and draw it on the image
        angle, img = detector.findAngle(lmList[11][0:2],
                                        lmList[13][0:2],
                                        lmList[15][0:2],
                                        img=img,
                                        color=(0, 0, 255),
                                        scale=10)

        # Check if the angle is close to 50 degrees with an offset of 10
        isCloseAngle50 = detector.angleCheck(myAngle=angle,
                                             targetAngle=50,
                                             offset=10)

        # Print the result of the angle check
        print(isCloseAngle50)
        return img


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

    if i % 2 == 0:
        img_left_processed = processImg(img_left)
        img_left_processed = img_left if 'img_left_processed' not in locals() else img_left_processed

    else:
        img_right_processed = processImg(img_right)
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
    cv2.waitKey(10)
    i += 1
