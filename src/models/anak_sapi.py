import pygame
import random
import math
from src.config import MAP_RECT, MAP_WIDTH, MAP_HEIGHT, YELLOW
from src.utils.asset_loader import get_asset_path

class AnakSapi:
    def __init__(self, x, y, name, desc):
        self.name = name
        self.description = desc
        self.type = "animal"
        self.highlight = False

        full_path = get_asset_path("assets", "animals_move", "anak_sapi.png")

        self.all_frames = []
        try:
            sprite_sheet = pygame.image.load(full_path).convert_alpha()

            sheet_w, sheet_h = sprite_sheet.get_size()

            COLS = 6
            ROWS = 8

            frame_w = sheet_w // COLS
            frame_h = sheet_h // ROWS

            SCALE = 1.8
            target_w = int(frame_w * SCALE)
            target_h = int(frame_h * SCALE)

            for row in range(ROWS):
                frames_in_row = 6 if row < 4 else 4

                for col in range(frames_in_row):
                    rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
                    img_big = sprite_sheet.subsurface(rect)
                    img_small = pygame.transform.scale(img_big, (target_w, target_h))
                    self.all_frames.append(img_small)

        except Exception as e:
            print(f"[ERROR] gagal load anak_sapi: {e}")
            dummy = pygame.Surface((40, 40))
            dummy.fill((160, 82, 45))
            self.all_frames = [dummy] * 64


        def row(start_row, frames):
            start = sum([6]*4 + [4]*(start_row-4)) if start_row > 4 else start_row*6
            return self.all_frames[start : start + frames]

        self.walk_front  = row(0, 6) 
        self.walk_back   = row(1, 6) 
        self.walk_left   = row(2, 6) 
        self.walk_right  = row(3, 6) 

        self.idle_front  = row(4, 4)
        self.idle_back   = row(5, 4)
        self.idle_left   = row(6, 4)
        self.idle_right  = row(7, 4)

        self.current_animation = self.idle_front
        self.frame_index = 0
        self.animation_speed = 0.14

        if self.current_animation:
            self.image = self.current_animation[0]
        else:
            self.image = pygame.Surface((40, 40))

        self.rect = self.image.get_rect(center=(x, y))

        self.speed = random.uniform(0.6, 1.2)
        self.state = "idle"
        self.direction = "front" 
        self.move_timer = 0
        self.move_duration = 0
        self.target_pos = (x, y)


    def set_animation(self, anim_list, speed):
        if self.current_animation != anim_list:
            self.current_animation = anim_list
            self.frame_index = 0
        self.animation_speed = speed

    def update_animation(self):
        if not self.current_animation:
            return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0

        idx = int(self.frame_index)
        self.image = self.current_animation[idx]

    def update_movement(self):
        self.move_timer -= 1

        if self.move_timer <= 0:
            rand = random.random()

            if self.state == "idle":
                if rand < 0.6:
                    self.state = "walking"
                    self.move_duration = random.randint(60, 180)
                else:
                    self.state = random.choice(["idle", "sleeping"])
                    self.move_duration = random.randint(100, 200)

            elif self.state == "walking":
                self.state = random.choice(["idle", "sleeping"])
                self.move_duration = random.randint(100, 200)

            elif self.state == "sleeping":
                self.state = "idle"
                self.move_duration = random.randint(80, 150)

            if self.state == "walking":
                self.target_pos = (
                    random.randint(max(0, self.rect.centerx - 140), min(MAP_WIDTH, self.rect.centerx + 140)),
                    random.randint(max(0, self.rect.centery - 140), min(MAP_HEIGHT, self.rect.centery + 140))
                )

            self.move_timer = self.move_duration

        if self.state == "walking":
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = math.sqrt(dx*dx + dy*dy)

            if abs(dx) > abs(dy): 
                self.direction = "right" if dx > 0 else "left"
            else:                 
                self.direction = "front" if dy > 0 else "back"

            anim = {
                "front":  self.walk_front,
                "back":   self.walk_back,
                "left":   self.walk_left,
                "right":  self.walk_right
            }[self.direction]

            self.set_animation(anim, 0.16)

            if dist > self.speed:
                self.rect.x += (dx / dist) * self.speed
                self.rect.y += (dy / dist) * self.speed
            else:
                self.state = "idle"

            self.rect.clamp_ip(MAP_RECT)

        elif self.state == "idle":
            anim = {
                "front":  self.idle_front,
                "back":   self.idle_back,
                "left":   self.idle_left,
                "right":  self.idle_right
            }[self.direction]

            self.set_animation(anim, 0.10)

        elif self.state == "sleeping":
            self.set_animation(self.idle_front, 0.05)

    def update(self):
        self.update_movement()
        self.update_animation()

    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_rect.center, 30, 3)
        surface.blit(self.image, screen_rect)
