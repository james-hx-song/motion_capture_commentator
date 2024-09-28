import cv2

# Create a dictionary to store the previous positions of the body parts
prev_positions_lr = [{
    "left_elbow": None,
    "right_elbow": None,
    "left_wrist": None,
    "right_wrist": None
}, {
    "left_elbow": None,
    "right_elbow": None,
    "left_wrist": None,
    "right_wrist": None
}]

# Create a dictionary to store movement directions
directions_lr = [{
    "left_elbow": None,
    "right_elbow": None,
    "left_wrist": None,
    "right_wrist": None
},{
    "left_elbow": None,
    "right_elbow": None,
    "left_wrist": None,
    "right_wrist": None
}]

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


def is_backflip(lm_list, ):
    # Hands above head
    left_wrist, right_wrist = lm_list[15], lm_list[16]
    head = lm_list[0]

    if left_wrist is None or right_wrist is None or head is None:
        return False
    
    # Check if the hands are above the head
    # print(left_wrist[1], head[1], right_wrist[1])
    if left_wrist[1] < head[1] and right_wrist[1] < head[1]:
        return True
    
    return False

def is_moonwalk(lm_list, ):
    # Knees close to hip

    return 



def processImg(detector, img, left: bool):
    global prev_positions_lr, directions_lr

    prev_positions = prev_positions_lr[0] if left else prev_positions_lr[1]
    directions = directions_lr[0] if left else directions_lr[1]
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


        # shaking, directions["left_elbow"] = is_shaking(
        #     left_elbow[1:3], prev_positions["left_elbow"], directions["left_elbow"])
        # if shaking:
        #     string = "left" if left else "right"
        #     print(f"Left elbow is shaking! {string}")

        # prev_positions["left_elbow"] = left_elbow[1:3]
        if is_backflip(lmList):
            string = "left" if left else "right"
            print(f"Hands up! {string}")

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
    



