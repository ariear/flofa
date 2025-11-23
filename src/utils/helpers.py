import math

def calculate_distance(r1, r2):
    """Menghitung jarak Euclidean antara dua rect"""
    return math.sqrt((r1.centerx-r2.centerx)**2 + (r1.centery-r2.centery)**2)

def get_safe_random_pos(existing_objects, margin=200, min_dist=150):
    """Mendapatkan posisi random yang aman tanpa collision"""
    import random
    from src.config import MAP_WIDTH, MAP_HEIGHT
    
    max_attempts = 100 
    for _ in range(max_attempts):
        x = random.randint(margin, MAP_WIDTH - margin)
        y = random.randint(margin, MAP_HEIGHT - margin)
        
        collision = False
        for obj in existing_objects:
            if hasattr(obj, 'rect'):
                dist = math.sqrt((x - obj.rect.centerx)**2 + (y - obj.rect.centery)**2)
                if dist < min_dist:
                    collision = True
                    break
        
        if not collision:
            return x, y
    
    return random.randint(margin, MAP_WIDTH - margin), random.randint(margin, MAP_HEIGHT - margin)
