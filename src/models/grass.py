import random
import cairo
import math
import pygame
from src.config import MAP_WIDTH, MAP_HEIGHT, GRASS_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

def create_grass_clump_sprite(width, height):
    """
    Membuat satu gambar (Surface) gumpalan rumput dengan PyCairo.
    """
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    
   
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()

    num_blades = random.randint(7, 12) 
    
    for i in range(num_blades):
       
        if i < num_blades // 2:
            color = random.choice(GRASS_COLORS)[:3] 
            color = (color[0]*0.7, color[1]*0.7, color[2]*0.7) 
        else:
            color = random.choice(GRASS_COLORS)
        
        ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)

    
        base_x = width / 2 + random.uniform(-width * 0.4, width * 0.4)
        base_y = height 
        

        tip_x = base_x + random.uniform(-width * 0.2, width * 0.2)
        tip_y = random.uniform(height * 0.1, height * 0.4) #
        
    
        ctrl_x1 = base_x + random.uniform(-width * 0.1, width * 0.1)
        ctrl_y1 = height * 0.7
        ctrl_x2 = tip_x + random.uniform(-width * 0.1, width * 0.1)
        ctrl_y2 = height * 0.3

        
        ctx.move_to(base_x - 2, base_y) 
        ctx.curve_to(ctrl_x1, ctrl_y1, ctrl_x2, ctrl_y2, tip_x, tip_y) 
        ctx.line_to(base_x + 2, base_y) 
        ctx.close_path()
        ctx.fill()

    buf = surface.get_data()
    pygame_surface = pygame.image.frombuffer(buf, (width, height), 'ARGB')
    return pygame_surface


def spawn_all_grass_clumps(total_clumps, sprite_cache):
    """Menyebar gumpalan rumput di SELURUH MAP."""
    clumps = []
    for _ in range(total_clumps):
        x_base = random.randint(0, MAP_WIDTH)
        y_base = random.randint(0, MAP_HEIGHT)
        

        sprite = random.choice(sprite_cache)
        
        amplitude = random.randint(3, 8)
        speed = random.uniform(0.5, 1.5)
        offset = random.uniform(0, 2 * math.pi)
        

        clumps.append({
            "x": x_base,
            "y": y_base,
            "sprite": sprite,
            "amp": amplitude,
            "spd": speed,
            "off": offset
        })
    return clumps


def draw_swaying_clump(surface, clump_data, time_sec, camera):
    """Menggambar satu GUMPALAN sprite rumput yang bergoyang."""
    sway = math.sin(time_sec * clump_data["spd"] + clump_data["off"]) * clump_data["amp"]
 
    sprite = clump_data["sprite"]
    sprite_width = sprite.get_width()
    sprite_height = sprite.get_height()

    screen_x = clump_data["x"] - camera.x - (sprite_width / 2) + sway
    screen_y = clump_data["y"] - camera.y - sprite_height 
    

    if screen_x < -sprite_width or screen_x > SCREEN_WIDTH or \
       screen_y < -sprite_height or screen_y > SCREEN_HEIGHT:
        return
    

    surface.blit(sprite, (screen_x, screen_y))
