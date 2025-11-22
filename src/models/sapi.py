import pygame
import random
import math
from src.config import MAP_RECT, MAP_WIDTH, MAP_HEIGHT, YELLOW
from src.utils.asset_loader import get_asset_path

class Sapi:
    def __init__(self, x, y, name, desc):
        self.name = name
        self.description = desc
        self.type = "animal"
        self.highlight = False

        self.all_frames = []
        full_path = get_asset_path("assets", "animals_move", "sapi.png")

        try:
            sprite_sheet = pygame.image.load(full_path).convert_alpha()
            sheet_w, sheet_h = sprite_sheet.get_size()

            cols = 6
            rows = 8
            frame_w = sheet_w // cols
            frame_h = sheet_h // rows

            SCALE_FACTOR = 1.9
            target_w = int(frame_w * SCALE_FACTOR)
            target_h = int(frame_h * SCALE_FACTOR)

            frames_per_row = [6, 6, 6, 6, 4, 4, 4, 4]

            self.row_frames = [] 

            for row in range(rows):
                row_list = []
                limit = frames_per_row[row]

                for col in range(limit):
                    rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
                    raw = sprite_sheet.subsurface(rect)
                    scaled = pygame.transform.scale(raw, (target_w, target_h))
                    row_list.append(scaled)

                self.row_frames.append(row_list)

        except Exception as e:
            print(f"[ERROR] Gagal load sapi: {e}")
            dummy = pygame.Surface((50, 50))
            dummy.fill((139, 69, 19))
            self.row_frames = [[dummy] * 4] * 8

        self.idle_front  = self.row_frames[0]
        self.idle_back   = self.row_frames[1]
        self.idle_left   = self.row_frames[2]
        self.idle_right  = self.row_frames[3]

        self.walk_down   = self.row_frames[4]
        self.walk_up     = self.row_frames[5]
        self.walk_left   = self.row_frames[6]
        self.walk_right  = self.row_frames[7]

        self.current_animation = self.idle_front
        self.frame_index = 0
        self.animation_speed = 0.1 
        
        if self.current_animation:
            self.image = self.current_animation[0]
        else:
            self.image = pygame.Surface((50, 50))
            
        self.rect = self.image.get_rect(center=(x, y))
        
        self.speed = random.uniform(0.3, 0.8) 
        self.state = "idle"
        self.move_timer = 0
        self.move_duration = 0
        self.target_pos = (x, y)
        self.facing_right = True

    def set_animation(self, animation_frames, animation_speed=0.1):
        if self.current_animation != animation_frames and len(animation_frames) > 0:
            self.current_animation = animation_frames
            self.frame_index = 0
            self.animation_speed = animation_speed

    def update_animation(self):
        if not self.current_animation: return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0
        
        idx = int(self.frame_index)
        if idx < len(self.current_animation):
            current_frame_image = self.current_animation[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(current_frame_image, True, False)
            else:
                self.image = current_frame_image

    def update_movement(self):
        self.move_timer -= 1
        if self.move_timer <= 0:
            rand_val = random.random()
            if self.state == "idle":
                if rand_val < 0.4:
                    self.state = "walking"
                    self.move_duration = random.randint(60, 150)
                    self.speed = random.uniform(0.3, 0.8)
                else:
                    self.state = random.choice(["idle", "sleeping"])
                    self.move_duration = random.randint(150, 300)
            elif self.state == "walking":
                self.state = random.choice(["idle", "sleeping"])
                self.move_duration = random.randint(150, 300)
            elif self.state == "sleeping":
                self.state = "idle"
                self.move_duration = random.randint(80, 150)

            if self.state == "walking":
                self.target_pos = (
                    random.randint(max(0, self.rect.centerx - 120), min(MAP_WIDTH, self.rect.centerx + 120)),
                    random.randint(max(0, self.rect.centery - 120), min(MAP_HEIGHT, self.rect.centery + 120))
                )

            self.move_timer = self.move_duration

        if self.state == "walking":
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)

            if abs(dx) > abs(dy):
                if dx > 0:
                    self.set_animation(self.walk_right, animation_speed=0.12)
                    self.facing_right = True
                else:
                    self.set_animation(self.walk_left, animation_speed=0.12)
                    self.facing_right = False
            else:
                if dy > 0:
                    self.set_animation(self.walk_down, animation_speed=0.12)
                else:
                    self.set_animation(self.walk_up, animation_speed=0.12)

            if dist > self.speed:
                self.rect.x += (dx / dist) * self.speed
                self.rect.y += (dy / dist) * self.speed
            else:
                self.state = "idle"

            self.rect.clamp_ip(MAP_RECT)

        elif self.state == "idle":
            if abs(self.target_pos[0] - self.rect.centerx) > abs(self.target_pos[1] - self.rect.centery):
                self.set_animation(self.idle_right if self.facing_right else self.idle_left)
            else:
                self.set_animation(self.idle_front)

        elif self.state == "sleeping":
            self.set_animation(self.walk_down[:1], animation_speed=0.02)


    def update(self):
        self.update_movement()
        self.update_animation()

    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_rect.center, 40, 3)
        surface.blit(self.image, screen_rect)
