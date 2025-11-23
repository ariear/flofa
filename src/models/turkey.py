import pygame
import random
import math
from src.config import MAP_RECT, MAP_WIDTH, MAP_HEIGHT, YELLOW
from src.utils.asset_loader import get_asset_path


class Turkey:
    def __init__(self, x, y, name, desc):
        self.name = name
        self.description = desc
        self.type = "turkey"
        self.highlight = False

        # Load Spritesheet Kalkun
        full_path = get_asset_path("assets", "animals_move", "turkey.png")
        self.idle_frames = []
        self.walk_frames = []
        self.run_frames = []
        self.sleep_frames = []

        try:
            sprite_sheet = pygame.image.load(full_path).convert_alpha()
            # Estimasi ukuran frame dari gambar (sekitar 32x32 pixel per frame)
            FRAME_W, FRAME_H = 32, 32
            SCALE_FACTOR = 2.5 # Perbesar agar terlihat jelas

            def load_specific_row(row_index, frame_count):
                frames = []
                target_w = int(FRAME_W * SCALE_FACTOR)
                target_h = int(FRAME_H * SCALE_FACTOR)
                y = row_index * FRAME_H
                for col in range(frame_count):
                    x = col * FRAME_W
                    if x + FRAME_W > sprite_sheet.get_width() or y + FRAME_H > sprite_sheet.get_height():
                        break
                    rect = pygame.Rect(x, y, FRAME_W, FRAME_H)
                    image_big = sprite_sheet.subsurface(rect)
                    image_small = pygame.transform.scale(image_big, (target_w, target_h))
                    frames.append(image_small)
                return frames

            self.idle_frames = load_specific_row(0, 6)
            self.walk_frames = load_specific_row(2, 6)
            self.run_frames = load_specific_row(4, 4)
            self.sleep_frames = load_specific_row(6, 4)

        except Exception as e:
            print(f"[ERROR] Gagal load turkey: {e}")
            dummy = pygame.Surface((50, 50))
            dummy.fill((200, 50, 50))
            self.idle_frames = [dummy]

        if not self.idle_frames: self.idle_frames = [pygame.Surface((50,50))]
        if not self.walk_frames: self.walk_frames = self.idle_frames
        if not self.run_frames: self.run_frames = self.idle_frames
        if not self.sleep_frames: self.sleep_frames = self.idle_frames

        self.current_animation = self.idle_frames
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.current_animation[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = random.uniform(0.8, 1.5)
        self.state = "idle"
        self.move_timer = 0
        self.move_duration = 0
        self.target_pos = (x, y)
        self.facing_right = True

    def set_animation(self, animation_frames, animation_speed=0.15):
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
                if rand_val < 0.6:
                    self.state = "walking"; self.move_duration = random.randint(60, 200); self.speed = random.uniform(0.8, 1.8)
                elif rand_val < 0.8:
                    self.state = "running"; self.move_duration = random.randint(40, 100); self.speed = random.uniform(2.0, 3.0)
                else:
                    self.state = "sleeping"; self.move_duration = random.randint(100, 250)
            elif self.state in ["walking", "running"]:
                self.state = random.choice(["idle", "sleeping"]); self.move_duration = random.randint(100, 200)
            elif self.state == "sleeping":
                self.state = "idle"; self.move_duration = random.randint(60, 120)

            if self.state in ["walking", "running"]:
                 self.target_pos = (random.randint(max(0, self.rect.centerx - 300), min(MAP_WIDTH, self.rect.centerx + 300)),
                                    random.randint(max(0, self.rect.centery - 300), min(MAP_HEIGHT, self.rect.centery + 300)))
            self.move_timer = self.move_duration

        if self.state in ["walking", "running"]:
            anim = self.walk_frames if self.state == "walking" else self.run_frames
            spd = 0.2 if self.state == "walking" else 0.3
            self.set_animation(anim, animation_speed=spd)
            
            dx = self.target_pos[0] - self.rect.centerx; dy = self.target_pos[1] - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > self.speed: 
                self.rect.x += (dx / dist) * self.speed; self.rect.y += (dy / dist) * self.speed
                if dx < 0: self.facing_right = False
                elif dx > 0: self.facing_right = True
            else: self.state = "idle" 
            self.rect.clamp_ip(MAP_RECT)

        elif self.state == "idle":
            self.set_animation(self.idle_frames)
        elif self.state == "sleeping":
            self.set_animation(self.sleep_frames, animation_speed=0.05)

    def update(self):
        self.update_movement()
        self.update_animation()

    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_rect.center, 40, 3)
        surface.blit(self.image, screen_rect)