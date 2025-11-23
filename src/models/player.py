import pygame
import os
from src.config import PLAYER_SPEED, MAP_RECT
from src.utils.asset_loader import load_spritesheet_safe

class Player:
    def __init__(self, x, y):
        self.frames = load_spritesheet_safe(os.path.join("assets", "player.png"), 64, 64, scale=2)
        if not self.frames:
            dummy = pygame.Surface((64, 64)); dummy.fill((0, 0, 255)); self.frames = [dummy]

        self.frame_index = 0
        self.animation_speed = 0.18
        self.direction = "down"
        self.moving = False
        self.anim_start = {"down": 0, "left": 8, "right": 16, "up": 24}
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_SPEED

    def update_animation(self):
        if len(self.frames) <= 1: return
        start = self.anim_start.get(self.direction, 0)
        end = start + 8
        if end > len(self.frames): end = len(self.frames)

        if self.moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= end: self.frame_index = start
        else: self.frame_index = start
        idx = int(self.frame_index)
        if idx < len(self.frames):
            self.image = self.frames[idx]

    def update_direction_from_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.direction = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]: self.direction = "left"
        elif keys[pygame.K_UP] or keys[pygame.K_w]: self.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]: self.direction = "down"

    def move(self, dx, dy):
        self.update_direction_from_keys()
        self.moving = (dx != 0 or dy != 0)
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(MAP_RECT)
        self.update_animation()

    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        surface.blit(self.image, screen_rect)
