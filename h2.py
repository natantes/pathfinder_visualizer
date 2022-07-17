
import math

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return int(math.sqrt((x1 - x2)**2  + (y1 - y2)**2))