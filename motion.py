import cv2

# Create a dictionary to store the previous positions of the body parts
prev_positions = {
    "left_elbow": None,
    "right_elbow": None,
    "left_wrist": None,
    "right_wrist": None
}

# Create a dictionary to store movement directions
directions = {
    "left_elbow": None,
    "right_elbow": None,
    "left_wrist": None,
    "right_wrist": None
}

def is_shaking(current_pos, prev_pos, direction, threshold=100):

    if prev_pos is None:
        return False, direction

    # Calculate change in position (velocity)
    dx = current_pos[0] - prev_pos[0]
    dy = current_pos[1] - prev_pos[1]

    # Check for horizontal (x) or vertical (y) movement beyond a threshold
    if abs(dx) > threshold or abs(dy) > threshold:
        new_direction = "left-right" if abs(dx) > abs(dy) else "up-down"
        # If direction has changed, we consider it a shake
        if new_direction != direction:
            return True, new_direction
        else:
            return False, new_direction
    return False, direction


def processImg(detector, img):
    global prev_positions, directions
    # Find the human pose in the frame
    img = detector.findPose(img)

    lmList, bboxInfo = detector.findPosition(
        img, draw=True, bboxWithHands=False)

    # Check if any body landmarks are detected
    if lmList:
        left_elbow = lmList[13]
        right_elbow = lmList[14]
        left_wrist = lmList[15]
        right_wrist = lmList[16]

        shaking, directions["left_elbow"] = is_shaking(
            left_elbow[1:3], prev_positions["left_elbow"], directions["left_elbow"])
        if shaking:
            print("Left elbow is shaking!")

        prev_positions["left_elbow"] = left_elbow[1:3]
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

        return img
    



