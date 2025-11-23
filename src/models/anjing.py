import pygame
import random
import math
from src.config import MAP_RECT, MAP_WIDTH, MAP_HEIGHT, YELLOW
from src.utils.asset_loader import get_asset_path

class Anjing:
    def __init__(self, x, y, name, desc):
        self.name = name
        self.description = desc
        self.type = "animal"
        self.highlight = False

        self.all_frames = []
        full_path = get_asset_path("assets", "animals_move", "anjing.png")

        try:
            sprite_sheet = pygame.image.load(full_path).convert_alpha()

            row_lengths = [7, 7, 7, 3]

            sheet_w, sheet_h = sprite_sheet.get_size()

            frame_w = sheet_w // 7 
            frame_h = sheet_h // 5

            SCALE_FACTOR = 0.47

            for row, cols in enumerate(row_lengths):
                for col in range(cols):
                    rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)

                    frame = sprite_sheet.subsurface(rect).copy()

                    PADDING_TOP = 6
                    new_surface = pygame.Surface((frame_w, frame_h + PADDING_TOP), pygame.SRCALPHA)
                    new_surface.blit(frame, (0, PADDING_TOP))
                    frame = new_surface

                    target_w = int(frame.get_width() * SCALE_FACTOR)
                    target_h = int(frame.get_height() * SCALE_FACTOR)
                    frame = pygame.transform.scale(frame, (target_w, target_h))

                    self.all_frames.append(frame)

        except Exception as e:
            print(f"[ERROR] Gagal load anjing: {e}")


        def get_frames(start, count):
            safe_count = min(count, len(self.all_frames) - start)
            if safe_count <= 0: return [self.all_frames[0]]
            return self.all_frames[start : start + safe_count]

        self.idle_frames = self.all_frames[0:14] 
        self.walk_frames = self.all_frames[14:21]   
        self.sleep_frames = self.all_frames[21:22]  
        self.sit_frames = self.all_frames[22:24]  
        self.run_frames = self.walk_frames 

        self.current_animation = self.idle_frames
        self.frame_index = 0
        self.animation_speed = 0.17 
        
        if self.current_animation:
            self.image = self.current_animation[0]
        else:
            self.image = pygame.Surface((43, 43))
            
        self.rect = self.image.get_rect(center=(x, y))
        
        self.speed = random.uniform(0.8, 1.6)
        self.state = "idle"
        self.move_timer = 0
        self.move_duration = 0
        self.target_pos = (x, y)
        self.facing_right = True

    def set_animation(self, animation_frames, animation_speed=0.17):
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
                if rand_val < 0.75:
                    self.state = "walking"
                    self.move_duration = random.randint(60, 140)
                    self.speed = random.uniform(0.8, 1.6)
                elif rand_val < 0.85: 
                    self.state = "running"
                    self.move_duration = random.randint(40, 80)
                    self.speed = random.uniform(1.5, 2.2)
                else:
                    self.state = random.choice(["idle", "sleeping"])
                    self.move_duration = random.randint(70, 150)
            elif self.state in ["walking", "running"]:
                self.state = random.choice(["idle", "sleeping"])
                self.move_duration = random.randint(70, 150)
            elif self.state == "sleeping":
                self.state = "idle"
                self.move_duration = random.randint(50, 90)

            if self.state in ["walking", "running"]:
                self.target_pos = (
                    random.randint(max(0, self.rect.centerx - 180), min(MAP_WIDTH, self.rect.centerx + 180)),
                    random.randint(max(0, self.rect.centery - 180), min(MAP_HEIGHT, self.rect.centery + 180))
                )
            
            self.move_timer = self.move_duration

        if self.state == "walking":
            self.set_animation(self.walk_frames, animation_speed=0.19)
            
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > self.speed:
                self.rect.x += int((dx / dist) * self.speed)
                self.rect.y += int((dy / dist) * self.speed)
                if dx < 0: self.facing_right = False
                elif dx > 0: self.facing_right = True
            else:
                self.state = "idle"
            self.rect.clamp_ip(MAP_RECT)

        elif self.state == "running":
            self.set_animation(self.run_frames, animation_speed=0.25)
            
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > self.speed:
                self.rect.x += int((dx / dist) * self.speed)
                self.rect.y += int((dy / dist) * self.speed)
                if dx < 0: self.facing_right = False
                elif dx > 0: self.facing_right = True
            else:
                self.state = "idle"
            self.rect.clamp_ip(MAP_RECT)

        elif self.state == "idle":
            self.set_animation(self.idle_frames)
            
        elif self.state == "sleeping":
            self.set_animation(self.sleep_frames, animation_speed=0.07)

    def update(self):
        self.update_movement()
        self.update_animation()

    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_rect.center, 34, 3)
        surface.blit(self.image, screen_rect)
