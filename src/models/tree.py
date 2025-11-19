import pygame
import cairo
import math
from src.config import YELLOW

def create_tree_sprite(size=60, tree_type="oak"):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()
    if tree_type == "oak":
        ctx.set_source_rgb(0.4, 0.26, 0.13)
        ctx.rectangle(size/2 - size/12, size/2, size/6, size/2.5)
        ctx.fill()
        ctx.set_source_rgb(0.13, 0.55, 0.13)
        ctx.arc(size/2, size/2.5, size/3, 0, 2 * math.pi)
        ctx.fill()
    elif tree_type == "pine":
        ctx.set_source_rgb(0.4, 0.26, 0.13)
        ctx.rectangle(size/2 - size/15, size/1.8, size/7.5, size/2.2)
        ctx.fill()
        ctx.set_source_rgb(0.0, 0.4, 0.0)
        ctx.move_to(size/2, size/6)
        ctx.line_to(size/4, size/2)
        ctx.line_to(size*3/4, size/2)
        ctx.close_path()
        ctx.fill()
        ctx.move_to(size/2, size/3)
        ctx.line_to(size/5, size/1.5)
        ctx.line_to(size*4/5, size/1.5)
        ctx.close_path()
        ctx.fill()
    buf = surface.get_data()
    pygame_surface = pygame.image.frombuffer(buf, (size, size), 'ARGB')
    return pygame_surface

class Tree:
    def __init__(self, x, y, tree_type, name, desc):
        self.sprite = create_tree_sprite(tree_type=tree_type)
        self.rect = self.sprite.get_rect(center=(x, y))
        self.name = name
        self.description = desc
        self.type = "tree"
        self.highlight = False
    
    def draw(self, surface, camera):
        screen_pos_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_pos_rect.center, 35, 3)
        surface.blit(self.sprite, screen_pos_rect)
    
    def get_info(self):
        return {"name": self.name, "description": self.description}
