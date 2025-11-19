import pygame
from src.config import YELLOW, BROWN

class Animal:
    def __init__(self, x, y, animal_type, name, desc, color):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.animal_type = animal_type
        self.name = name
        self.description = desc
        self.color = color
        self.type = "animal"
        self.highlight = False
    
    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_rect.center, 30, 3)
        if self.animal_type == "rabbit":
            pygame.draw.ellipse(surface, self.color, (screen_rect.x, screen_rect.y + 10, 35, 25))
            pygame.draw.circle(surface, self.color, (screen_rect.x + 27, screen_rect.y + 12), 10)
            pygame.draw.ellipse(surface, self.color, (screen_rect.x + 22, screen_rect.y, 6, 15))
            pygame.draw.ellipse(surface, self.color, (screen_rect.x + 30, screen_rect.y, 6, 15))
        elif self.animal_type == "deer":
            pygame.draw.ellipse(surface, self.color, (screen_rect.x, screen_rect.y + 10, 40, 25))
            pygame.draw.circle(surface, self.color, (screen_rect.x + 35, screen_rect.y + 8), 8)
            pygame.draw.line(surface, BROWN, (screen_rect.x + 35, screen_rect.y + 8), 
                                 (screen_rect.x + 32, screen_rect.y), 2)
            pygame.draw.line(surface, BROWN, (screen_rect.x + 35, screen_rect.y + 8), 
                                 (screen_rect.x + 38, screen_rect.y), 2)
        elif self.animal_type == "bird":
            pygame.draw.ellipse(surface, self.color, (screen_rect.x + 10, screen_rect.y + 15, 20, 15))
            pygame.draw.circle(surface, self.color, (screen_rect.x + 25, screen_rect.y + 18), 7)
            pygame.draw.polygon(surface, self.color, [
                (screen_rect.x + 10, screen_rect.y + 20),
                (screen_rect.x, screen_rect.y + 15),
                (screen_rect.x + 5, screen_rect.y + 25)
            ])
    
    def get_info(self):
        return {"name": self.name, "description": self.description}
