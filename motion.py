import cv2

from utils import calculate_distance
import utils
import numpy as np



class MotionDetector:
    def __init__(self, lm_list=None, flag: bool = False):
        self.lm_list = lm_list

        self.flag = "left" if flag else "right"

        self.position_history = {
            "left_shoulder": [],
            "right_shoulder": [],
            "left_wrist": [],
            "right_wrist": [],
            "torso": [],
            "left_knee": [],
            "right_knee": [],
            "head": []
        }

        self.swipe_threshold = 50
        self.torso_stability_threshold = 10

        self.history_length = utils.FRAMESPERSEC

    def update_lm_list(self, lm_list):
        self.lm_list = lm_list

        left_shoulder = lm_list[11] if lm_list else None
        right_shoulder = lm_list[12] if lm_list else None

        left_wrist = lm_list[15] if lm_list else None
        right_wrist = lm_list[16] if lm_list else None

        torso = lm_list[11] if lm_list else None

        left_knee = lm_list[25] if lm_list else None
        right_knee = lm_list[26] if lm_list else None

        if lm_list:
            self.update_position_history("left_shoulder", left_shoulder)
            self.update_position_history("right_shoulder", right_shoulder)
            self.update_position_history("left_wrist", left_wrist)
            self.update_position_history("right_wrist", right_wrist)
            self.update_position_history("torso", torso)
            self.update_position_history("left_knee", left_knee)
            self.update_position_history("right_knee", right_knee)
            self.update_position_history("head", lm_list[0])
        


    def update_position_history(self, key, position):
        # Append the new position to history and ensure it doesn't exceed the history length
        self.position_history[key].append(position)
        if len(self.position_history[key]) > self.history_length:
            self.position_history[key].pop(0)


    def is_backflip(self, ) -> bool:
        # Hold wrist above head
        if self.lm_list is None:
            print("Update Landmark List!!")
            return False

        left_wrist, right_wrist = self.lm_list[15], self.lm_list[16]
        head = self.lm_list[0]

        if left_wrist is None or right_wrist is None or head is None:
            return False
        
        
        # Check if the hands are above the head
        # print(left_wrist[1], head[1], right_wrist[1])
        if left_wrist[1] < head[1] and right_wrist[1] < head[1]:
            print("Backflip detected! ", self.flag)
            # press("0")
            return True
        
        return False

    def is_moonwalk(self, eps=100):
        # Knee close to hip
        if self.lm_list is None:
            print("Update Landmark List!!")
            return False
        # Knees close to hip
        left_knee, right_knee = self.lm_list[25], self.lm_list[26]
        left_hip, right_hip = self.lm_list[23], self.lm_list[24]

        left_dist = calculate_distance(left_knee, left_hip)
        right_dist = calculate_distance(right_knee, right_hip)
        if left_dist < eps or right_dist < eps:
            print("Moonwalk detected! ", self.flag)
            # press("3")
            return True

        return False
    
    def is_flair(self, threshold=50):
        # Spinning
        if len(self.position_history["left_shoulder"]) < self.history_length:
            return False
        
        left_initial = self.position_history["left_shoulder"][0]
        left_final = self.position_history["left_shoulder"][-1]
        right_initial = self.position_history["right_shoulder"][0]
        right_final = self.position_history["right_shoulder"][-1]

        left_movement = left_final[0] - left_initial[0]
        right_movement = right_final[0] - right_initial[0]

        if abs(left_movement) > threshold and abs(right_movement) > threshold and left_movement * right_movement < 0:
            print("Flair (Spinning) detected! ", self.flag)
            # press("4")
            return True
        
        return False
    
    def is_ground_flair(self, threshold=50):
        # Spinning
        if self.lm_list is None:
            print("Update Landmark List!!")
            return False
        
        left_wrist, right_wrist = self.lm_list[15], self.lm_list[16]
        left_feet, right_feet = self.lm_list[27], self.lm_list[28]

        left_dist = calculate_distance(left_wrist, left_feet)
        right_dist = calculate_distance(right_wrist, right_feet)

        if left_dist < threshold and right_dist < threshold:
            print("Ground Flair detected! ", self.flag)
            return True
        
        return False
    
    def is_breakdance_swipe(self, ):
        # Left or right swipe

        if len(self.position_history["left_wrist"]) < self.history_length:
            return False
        
        left_initial = self.position_history["left_wrist"][0]
        left_final = self.position_history["left_wrist"][-1]
        right_initial = self.position_history["right_wrist"][0]
        right_final = self.position_history["right_wrist"][-1]
        torso_initial = self.position_history["torso"][0]
        torso_final = self.position_history["torso"][-1]


        # Calculate torso movement to ensure it's relatively still
        torso_movement = calculate_distance(torso_initial, torso_final)

        # Check if either wrist has moved horizontally more than the threshold and the torso has moved minimally
        left_wrist_movement = abs(left_final[0] - left_initial[0])
        right_wrist_movement = abs(right_final[0] - right_initial[0])
        # print(left_wrist_movement, right_wrist_movement, torso_movement)
        if (left_wrist_movement > self.swipe_threshold or right_wrist_movement > self.swipe_threshold) and torso_movement < self.torso_stability_threshold:
            print("BreakDance Swipe detected! ", self.flag)
            # press("6")
            return True
    

        return False

    def is_breakdance_freeze_var4(self, ):
        # Left Right Cross

        if len(self.position_history["left_wrist"]) < self.history_length:
            return False
        
        left_initial = self.position_history["left_wrist"][0]
        left_final = self.position_history["left_wrist"][-1]
        right_initial = self.position_history["right_wrist"][0]
        right_final = self.position_history["right_wrist"][-1]
        torso_initial = self.position_history["torso"][0]
        torso_final = self.position_history["torso"][-1]

        torso_movement = calculate_distance(torso_initial, torso_final)

        left_wrist_movement = left_final[0] - left_initial[0]
        right_wrist_movement = right_final[0] - right_initial[0]
        if torso_movement < self.torso_stability_threshold and left_wrist_movement * right_wrist_movement < 0 and abs(left_wrist_movement) > self.swipe_threshold and abs(right_wrist_movement) > self.swipe_threshold:
            print("BreakDance Freeze Var4 detected! ", self.flag)
            # press("8")
            return True
        
        return False

    def is_breakdance_freeze_var1(self, ):
        # Right hand above head
        if len(self.position_history["left_wrist"]) < self.history_length:
            return False
        
        left_wrist, right_wrist = self.lm_list[15], self.lm_list[16]
        head = self.lm_list[0]

        if left_wrist is None or right_wrist is None or head is None:
            return False
        
        if left_wrist[1] <= head[1] and right_wrist[1] >= head[1]:
            print("BreakDance Freeze Var1 detected! ", self.flag)
            # press("7")
            return True

        return False

    def is_hiphop(self, ):
        # Head Duck

        if len(self.position_history["head"]) < self.history_length:
            return False
        
        head_initial = self.position_history["head"][0]
        head_final = self.position_history["head"][-1]

        head_movement = head_final[1] - head_initial[1]

        if head_movement < -150:
            print("HipHop detected! ", self.flag)
            # press("1")
            return True

        return False

    
    

    def is_what_motion(self,):
        # Check for all motions

        # funcs = [self.is_flair, self.is_ground_flair, self.is_moonwalk, self.is_backflip, self.is_breakdance_freeze_var1, self.is_breakdance_freeze_var4, self.is_breakdance_swipe, self.is_hiphop]
        funcs = [self.is_flair, self.is_backflip, self.is_moonwalk]
        idx = [0, 3, 2]
        # vals = [func() for func in funcs]

        for i, func in enumerate(funcs):
            if func():
                return idx[i]
            
        return -1
        # self.is_flair()
        # self.is_moonwalk()
        # self.is_hiphop()




# motionDetector = MotionDetector()
motionDetectorL = MotionDetector(flag=True)
motionDetectorR = MotionDetector(flag=False)
def processImg(detector, img, left: bool,):

    # global motionDetector
    global motionDetectorL, motionDetectorR
    # Find the human pose in the frame
    img = detector.findPose(img)

    lmList, bboxInfo = detector.findPosition(
        img, draw=True, bboxWithHands=False)
    
    
    if left:
        motionDetector = motionDetectorL
    else:
        motionDetector = motionDetectorR

    motionDetector.update_lm_list(lmList)
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
        # if is_backflip(lmList):
        #     string = "left" if left else "right"
        #     print(f"Hands up! {string}")

        # if motionDetector.is_breakdance_swipe():
        #     string = "left" if left else "right"
        #     print(f"Action detected! {string}")

        idx = motionDetector.is_what_motion()

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
        
        length, img, info = detector.findDistance(lmList[12][0:2],
                                                  lmList[16][0:2],
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
        
        angle, img = detector.findAngle(lmList[12][0:2],
                                        lmList[14][0:2],
                                        lmList[16][0:2],
                                        img=img,
                                        color=(0, 0, 255),
                                        scale=10)

        return img, idx
    
    return img, None
    



