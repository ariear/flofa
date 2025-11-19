import pygame
import cairo
import math
from src.config import PLAYER_SPEED, MAP_RECT

def create_player_sprite(size=40):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()
    ctx.set_source_rgb(0.95, 0.8, 0.7) 
    ctx.arc(size/2, size/3, size/6, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(0.2, 0.4, 0.8) 
    ctx.rectangle(size/2 - size/8, size/3 + size/8, size/4, size/3)
    ctx.fill()
    ctx.set_source_rgb(0.3, 0.2, 0.1) 
    ctx.rectangle(size/2 - size/10, size/3 + size/2.3, size/12, size/6)
    ctx.fill()
    ctx.rectangle(size/2 + size/30, size/3 + size/2.3, size/12, size/6)
    ctx.fill()
    buf = surface.get_data()
    pygame_surface = pygame.image.frombuffer(buf, (size, size), 'ARGB')
    return pygame_surface

class Player:
    def __init__(self, x, y):
        self.sprite = create_player_sprite()
        self.rect = self.sprite.get_rect(center=(x, y))
        self.speed = PLAYER_SPEED
    
    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(MAP_RECT)
    
    def draw(self, surface, camera):
        screen_pos_rect = self.rect.move(-camera.x, -camera.y)
        surface.blit(self.sprite, screen_pos_rect)
