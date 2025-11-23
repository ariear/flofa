import pygame
import os
from src.config import YELLOW
from src.utils.asset_loader import load_image_safe

class Tree:
    def __init__(self, x, y, tree_type, name, desc):
        self.name = name
        self.description = desc
        self.type = "tree"
        self.highlight = False

        path = os.path.join("assets", "Plants", f"{tree_type}.png")
        self.sprite = load_image_safe(path, scale=0.3) 
        self.rect = self.sprite.get_rect(midbottom=(x, y))
    
    def draw(self, surface, camera):
        screen_pos_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_pos_rect.midbottom, 40, 3)
        surface.blit(self.sprite, screen_pos_rect)
