import math

def calculate_distance(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


FRAMESPERSEC = 10

