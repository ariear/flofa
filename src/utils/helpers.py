import math

def calculate_distance(obj1_rect, obj2_rect):
    x1 = obj1_rect.centerx
    y1 = obj1_rect.centery
    x2 = obj2_rect.centerx
    y2 = obj2_rect.centery
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
