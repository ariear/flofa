import pygame
from src.config import MAP_RECT, INTERACTION_DISTANCE
from src.utils.helpers import calculate_distance
from src.views.info_popup import InfoPopup

class GameController:
    def __init__(self, player, trees, animals, cats, turkeys , grass_clumps):
        self.player = player
        self.trees = trees
        self.animals = animals
        self.cats = cats
        self.turkeys = turkeys
        self.grass_clumps = grass_clumps
        self.camera = pygame.Rect(0, 0, 0, 0)  # Will be set in update_camera
        self.popup = None
        self.can_interact_with = None
    
    def handle_input(self, popup_active):
        """Handle input dari keyboard"""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if not popup_active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1
            self.player.move(dx, dy)
    
    def update_camera(self, screen_width, screen_height):
        """Update posisi kamera mengikuti player"""
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)
        self.camera.center = self.player.rect.center
        self.camera.clamp_ip(MAP_RECT)
    
    def update_interactions(self):
        """Update highlight dan deteksi interaksi"""
        self.can_interact_with = None
        min_dist = float('inf')
        
        # Reset highlight
        for obj in self.trees + self.animals + self.cats + self.turkeys:
            obj.highlight = False
        
        # Cari objek terdekat
        for obj in self.trees + self.animals + self.cats + self.turkeys: 
            dist = calculate_distance(self.player.rect, obj.rect)
            if dist < INTERACTION_DISTANCE and dist < min_dist:
                min_dist = dist
                self.can_interact_with = obj
        
        if self.can_interact_with: 
            self.can_interact_with.highlight = True
    
    def update_cats(self, popup_active):
        """Update animasi kucing"""
        if not popup_active: 
            for cat_obj in self.cats:
                cat_obj.update()

    def update_turkeys(self, popup_active):
        """Update animasi dan gerakan kalkun"""
        # Kalkun cuma boleh gerak kalau tidak sedang ada popup
        if not popup_active:
            for turkey in self.turkeys:
                turkey.update() # <--- INI PERINTAH "JALAN!" NYA
    
    def handle_event(self, event):
        """Handle event pygame"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                if self.popup: 
                    self.popup = None
                    return
            
            if event.key == pygame.K_SPACE and not self.popup:
                if self.can_interact_with:
                    img_to_show = None
                    if hasattr(self.can_interact_with, 'sprite'): 
                        img_to_show = self.can_interact_with.sprite
                    elif hasattr(self.can_interact_with, 'image'): 
                        img_to_show = self.can_interact_with.image
                    
                    if img_to_show: 
                        self.popup = InfoPopup(
                            self.can_interact_with.name, 
                            self.can_interact_with.description, 
                            img_to_show
                        )
