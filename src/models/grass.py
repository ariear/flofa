import pygame
import cairo
import random
import math
from src.config import GRASS_COLORS, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

def create_grass_clump_sprite(width, height):
    """Membuat sprite rumput menggunakan PyCairo"""
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()
    num_blades = random.randint(7, 12) 
    for i in range(num_blades):
        color = random.choice(GRASS_COLORS)
        if i < num_blades // 2: color = (color[0]*0.7, color[1]*0.7, color[2]*0.7) 
        ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
        base_x = width/2 + random.uniform(-width*0.4, width*0.4)
        base_y = height 
        tip_x = base_x + random.uniform(-width*0.2, width*0.2)
        tip_y = random.uniform(height*0.1, height*0.4) 
        ctx.move_to(base_x - 2, base_y) 
        ctx.curve_to(base_x, height*0.7, tip_x, height*0.3, tip_x, tip_y) 
        ctx.line_to(base_x + 2, base_y) 
        ctx.close_path(); ctx.fill()
    buf = surface.get_data()
    return pygame.image.frombuffer(buf, (width, height), 'ARGB')

def spawn_all_grass_clumps(total_clumps, sprite_cache):
    """Menyebar gumpalan rumput di seluruh map"""
    clumps = []
    for _ in range(total_clumps):
        clumps.append({
            "x": random.randint(0, MAP_WIDTH),
            "y": random.randint(0, MAP_HEIGHT),
            "sprite": random.choice(sprite_cache),
            "amp": random.randint(3, 8), "spd": random.uniform(0.5, 1.5), "off": random.uniform(0, 6.28)
        })
    return clumps

def draw_swaying_clump(surface, clump, time_sec, camera):
    """Menggambar rumput bergoyang"""
    sway = math.sin(time_sec * clump["spd"] + clump["off"]) * clump["amp"]
    sx = clump["x"] - camera.x - (clump["sprite"].get_width()/2) + sway
    sy = clump["y"] - camera.y - clump["sprite"].get_height()
    if -50 < sx < SCREEN_WIDTH and -50 < sy < SCREEN_HEIGHT:
        surface.blit(clump["sprite"], (sx, sy))
