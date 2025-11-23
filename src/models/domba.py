import pygame
import random
import math
from src.config import MAP_RECT, MAP_WIDTH, MAP_HEIGHT, YELLOW
from src.utils.asset_loader import get_asset_path

class Domba:
    def __init__(self, x, y, name, desc):
        self.name = name
        self.description = desc
        self.type = "animal"
        self.highlight = False

        # --- LOAD ASSET ---
        self.all_frames = []
        full_path = get_asset_path("assets", "animals_move", "domba.png")
        
        try:
            sprite_sheet = pygame.image.load(full_path).convert_alpha()
            sheet_w, sheet_h = sprite_sheet.get_size()
            
            #Grid Sesuai Gambar (6 Kolom, 8 Baris) ---
            cols = 6 
            rows = 8 
            
            frame_w = sheet_w // cols
            frame_h = sheet_h // rows
            
     
            SCALE_FACTOR = 2.8 
            
            target_w = int(frame_w * SCALE_FACTOR)
            target_h = int(frame_h * SCALE_FACTOR)
            

            for row in range(rows):
                for col in range(cols):
                    rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
                    image_big = sprite_sheet.subsurface(rect)
                    image_small = pygame.transform.scale(image_big, (target_w, target_h))
                    self.all_frames.append(image_small)
                    
        except Exception as e:
            print(f"[ERROR] Gagal load domba: {e}")
            dummy = pygame.Surface((50, 50))
            dummy.fill((200, 200, 200))
            self.all_frames = [dummy] * 48


        def get_frames(start_index, count):
           
            return self.all_frames[start_index : start_index + count]

      
        self.walk_frames = get_frames(12, 6)
        
       
        self.idle_frames = get_frames(24, 4)
        
        
        self.sleep_frames = get_frames(36, 4)

      
        self.current_animation = self.idle_frames
        self.frame_index = 0
        self.animation_speed = 0.12 
        
        self.image = self.current_animation[0]
        self.rect = self.image.get_rect(center=(x, y))

        
        self.true_x = float(x)
        self.true_y = float(y)
        
        self.speed = random.uniform(0.5, 0.9)
        self.state = "idle"
        self.move_timer = 0
        self.move_duration = 0
        self.target_pos = (x, y)
        self.facing_right = True

    def set_animation(self, animation_frames, animation_speed=0.12):
      
        if self.current_animation != animation_frames:
            self.current_animation = animation_frames
            self.frame_index = 0
            self.animation_speed = animation_speed
           
            self.rect = self.image.get_rect(center=self.rect.center)

    def update_animation(self):
        if not self.current_animation: return

        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.current_animation):
            self.frame_index = 0
        
        idx = int(self.frame_index)
        
      
        if idx < len(self.current_animation):
            frame_img = self.current_animation[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(frame_img, True, False)
            else:
                self.image = frame_img
            
          
            self.rect = self.image.get_rect(center=(int(self.true_x), int(self.true_y)))

    def update_movement(self):
        self.move_timer -= 1
       
        if self.move_timer <= 0:
            rand = random.random()
            
            if self.state == "idle":
                if rand < 0.6:
                    self.state = "walking"
                    self.move_duration = random.randint(100, 200)
                
                    tx = random.randint(max(0, int(self.true_x) - 150), min(MAP_WIDTH, int(self.true_x) + 150))
                    ty = random.randint(max(0, int(self.true_y) - 150), min(MAP_HEIGHT, int(self.true_y) + 150))
                    self.target_pos = (tx, ty)
                else:
                    self.state = random.choice(["idle", "sleeping"])
                    self.move_duration = random.randint(100, 200)
            
            elif self.state == "walking":
                self.state = "idle"
                self.move_duration = random.randint(50, 100)
                
            elif self.state == "sleeping":
                self.state = "idle"
                self.move_duration = random.randint(50, 100)

            self.move_timer = self.move_duration


        if self.state == "walking":
            self.set_animation(self.walk_frames, 0.15)
            

            dx = self.target_pos[0] - self.true_x
            dy = self.target_pos[1] - self.true_y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > self.speed:

                self.true_x += (dx / dist) * self.speed
                self.true_y += (dy / dist) * self.speed
                

                if dx < 0: self.facing_right = False
                elif dx > 0: self.facing_right = True
            else:
                self.state = "idle"

        elif self.state == "idle":
            self.set_animation(self.idle_frames, 0.08)
            
        elif self.state == "sleeping":
            self.set_animation(self.sleep_frames, 0.05)

        
        self.true_x = max(0, min(MAP_WIDTH, self.true_x))
        self.true_y = max(0, min(MAP_HEIGHT, self.true_y))
        
        
        self.rect.centerx = int(self.true_x)
        self.rect.centery = int(self.true_y)

    def update(self):
        self.update_movement()
        self.update_animation()

    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        
        if self.highlight:
            circle_pos = (screen_rect.centerx, screen_rect.centery + 10) 
            pygame.draw.circle(surface, YELLOW, circle_pos, 30, 2)
            
        surface.blit(self.image, screen_rect)