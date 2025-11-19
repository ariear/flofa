import pygame
from src.config import (
    MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,
    INTERACTION_DISTANCE
)
from src.utils.helpers import calculate_distance
from src.views.info_popup import InfoPopup

class GameController:
    def __init__(self, player, trees, animals, grass_clumps):
        self.player = player
        self.trees = trees
        self.animals = animals
        self.grass_clumps = grass_clumps
        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.popup = None
        self.current_nearby_object = None
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        self.player.move(dx, dy)
    
    def update_camera(self):
        self.camera.center = self.player.rect.center
        self.camera.left = max(0, self.camera.left)
        self.camera.right = min(MAP_WIDTH, self.camera.right)
        self.camera.top = max(0, self.camera.top)
        self.camera.bottom = min(MAP_HEIGHT, self.camera.bottom)
    
    def update_interactions(self):
        nearest_object = None
        nearest_distance = float('inf')
        
        for tree in self.trees:
            tree.highlight = False
        for animal in self.animals:
            animal.highlight = False
        
        for tree in self.trees:
            distance = calculate_distance(self.player.rect, tree.rect)
            if distance < INTERACTION_DISTANCE and distance < nearest_distance:
                nearest_distance = distance
                nearest_object = tree
        
        for animal in self.animals:
            distance = calculate_distance(self.player.rect, animal.rect)
            if distance < INTERACTION_DISTANCE and distance < nearest_distance:
                nearest_distance = distance
                nearest_object = animal
        
        if nearest_object:
            nearest_object.highlight = True
            if self.current_nearby_object != nearest_object:
                self.current_nearby_object = nearest_object
                info = nearest_object.get_info()
                self.popup = InfoPopup(info["name"], info["description"])
        else:
            if self.popup:
                self.popup = None
            self.current_nearby_object = None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.popup:
                    self.popup = None
                    self.current_nearby_object = None
    
    def update(self):
        self.handle_input()
        self.update_camera()
        self.update_interactions()
