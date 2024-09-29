import math

def calculate_distance(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


FRAMESPERSEC = 10
SECSTOWAIT = 1
THRESHOLD = [4, 3, 3, 3, 1, 2, 4, 5]

# KEYS = ["4", "2", "3", "0", "7", "8", "6", "1"]
KEYSL = ["4", "2", "3", "0", "7", "8", "6", "1"]
KEYSR = ["R", "W", "E", "P", "U", "I", "Y", "Q"]

FUNCS = ["flair", "ground_flair", "moonwalk", "backflip", "breakdance_freeze_var1", "breakdance_freeze_var4", "breakdance_swipe", "hiphop"]
