import pygame
import sys
import math
import cairo
import random
import os

# --- INISIALISASI ---
pygame.init()

# --- KONSTANTA ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
PLAYER_SPEED = 3
INTERACTION_DISTANCE = 80

MAP_WIDTH = SCREEN_WIDTH * 3
MAP_HEIGHT = SCREEN_HEIGHT * 3
MAP_RECT = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)
TILE_SIZE = 64 

# --- WARNA ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BG = (34, 139, 34) 
YELLOW = (255, 255, 0)
BROWN = (101, 67, 33)
GRAY = (200, 200, 200)
BLUE_DOG = (0, 150, 255) # Warna untuk minimap anjing

# Palet Warna Rumput
GRASS_COLORS = [
    (30, 100, 40), (40, 120, 50), (50, 140, 60),
    (60, 150, 70), (25, 90, 35)
]

# --- SETUP DISPLAY ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Eksplorasi Alam (Fixed)")
clock = pygame.time.Clock()

# Font
pygame.font.init()
font_title = pygame.font.Font(None, 32)
font_text = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 20)
font_pixel = pygame.font.Font(None, 28)

# =============================================================================
# 1. MANAJEMEN FILE
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*paths):
    return os.path.join(BASE_DIR, *paths)

def load_image_safe(relative_path, scale=1, flags=0):
    full_path = get_asset_path(relative_path)
    try:
        image = pygame.image.load(full_path).convert_alpha()
        if scale != 1:
            image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        return image
    except FileNotFoundError:
        dummy = pygame.Surface((40, 40))
        dummy.fill((255, 0, 0)) 
        return dummy

def load_spritesheet_safe(relative_path, frame_width, frame_height, scale=1, flags=0):
    full_path = get_asset_path(relative_path)
    try:
        sheet = pygame.image.load(full_path).convert_alpha()
        sheet_w, sheet_h = sheet.get_size()
        frames = []
        
        cols = sheet_w // frame_width
        rows = sheet_h // frame_height
        
        for row in range(rows):
            for col in range(cols):
                x = col * frame_width
                y = row * frame_height
                
                if x + frame_width <= sheet_w and y + frame_height <= sheet_h:
                    frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                    if scale != 1:
                        frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
                    frames.append(frame)
                    
        return frames
    except FileNotFoundError:
        print(f"[WARNING] Spritesheet tidak ditemukan: {relative_path}")
        return []
    except Exception as e:
        print(f"[ERROR] Gagal load spritesheet {relative_path}: {e}")
        return []

# =============================================================================
# 2. FUNGSI PEMBUAT RUMPUT
# =============================================================================

def create_grass_clump_sprite(width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()
    num_blades = random.randint(7, 12) 
    for i in range(num_blades):
        color = random.choice(GRASS_COLORS)
        if i < num_blades // 2: color = (color[0]*0.7, color[1]*0.7, color[2]*0.7) 
        ctx.set_source_rgb(color[0]/255, color[1]/255, color[2]/255)
        base_x = width/2 + random.uniform(-width*0.4, width*0.4)
        base_y = height 
        tip_x = base_x + random.uniform(-width*0.2, width*0.2)
        tip_y = random.uniform(height*0.1, height*0.4) 
        ctx.move_to(base_x - 2, base_y) 
        ctx.curve_to(base_x, height*0.7, tip_x, height*0.3, tip_x, tip_y) 
        ctx.line_to(base_x + 2, base_y) 
        ctx.close_path(); ctx.fill()
    buf = surface.get_data()
    return pygame.image.frombuffer(buf, (width, height), 'ARGB')

# =============================================================================
# 3. CLASSES
# =============================================================================

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

class Animal:
    def __init__(self, x, y, animal_type, name, desc):
        self.animal_type = animal_type
        self.name = name
        self.description = desc
        self.type = "animal"
        self.highlight = False

        path = os.path.join("assets", "animals", f"{animal_type}.png")
        self.image = load_image_safe(path, scale=2)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface, camera):
        screen_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_rect.center, 35, 3)
        surface.blit(self.image, screen_rect)

class Cat:
    def __init__(self, x, y, name, desc):
        self.name = name
        self.description = desc
        self.type = "cat" 
        self.highlight = False

        # Load Kucing & Scale Down
        self.all_frames = []
        full_path = get_asset_path("assets", "animals_move", "kucing.png")
        
        try:
            sprite_sheet = pygame.image.load(full_path).convert_alpha()
            sheet_w, sheet_h = sprite_sheet.get_size()
            
            cols = 8
            rows = 4
            frame_w = sheet_w // cols
            frame_h = sheet_h // rows
            
            SCALE_FACTOR = 0.4 
            
            target_w = int(frame_w * SCALE_FACTOR)
            target_h = int(frame_h * SCALE_FACTOR)
            
            for row in range(rows):
                for col in range(cols):
                    rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
                    image_big = sprite_sheet.subsurface(rect)
                    image_small = pygame.transform.scale(image_big, (target_w, target_h))
                    self.all_frames.append(image_small)
                    
        except Exception as e:
            print(f"[ERROR] Gagal load kucing: {e}")
            dummy = pygame.Surface((40, 40))
            dummy.fill((255, 140, 0))
            self.all_frames = [dummy] * 32

        def get_frames(start, count):
            safe_count = min(count, len(self.all_frames) - start)
            if safe_count <= 0: return [self.all_frames[0]]
            return self.all_frames[start : start + safe_count]

        self.idle_frames = get_frames(0, 8)       
        self.walk_frames = get_frames(8, 8)       
        self.run_frames = get_frames(16, 8)       
        self.sleep_frames = get_frames(24, 4)  

        self.current_animation = self.idle_frames
        self.frame_index = 0
        self.animation_speed = 0.15 
        
        if self.current_animation:
            self.image = self.current_animation[0] 
        else:
            self.image = pygame.Surface((40, 40))
            
        self.rect = self.image.get_rect(center=(x, y))
        
        self.speed = random.uniform(0.5, 1.5) 
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
                if rand_val < 0.5: # Jalan
                    self.state = "walking"
                    self.move_duration = random.randint(60, 180) 
                    self.speed = random.uniform(0.8, 1.8)
                elif rand_val < 0.7: # Lari
                    self.state = "running"
                    self.move_duration = random.randint(60, 120) 
                    self.speed = random.uniform(2.0, 3.5)
                else: # Tidur
                    self.state = "sleeping"
                    self.move_duration = random.randint(120, 300) 
            elif self.state in ["walking", "running"]:
                self.state = random.choice(["idle", "sleeping"])
                self.move_duration = random.randint(120, 300)
            elif self.state == "sleeping":
                self.state = "idle"
                self.move_duration = random.randint(60, 120)

            if self.state in ["walking", "running"]:
                 self.target_pos = (
                    random.randint(max(0, self.rect.centerx - 200), min(MAP_WIDTH, self.rect.centerx + 200)),
                    random.randint(max(0, self.rect.centery - 200), min(MAP_HEIGHT, self.rect.centery + 200))
                )
            
            self.move_timer = self.move_duration

        if self.state in ["walking", "running"]:
            anim = self.walk_frames if self.state == "walking" else self.run_frames
            spd = 0.2 if self.state == "walking" else 0.3
            self.set_animation(anim, animation_speed=spd)
            
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > self.speed: 
                self.rect.x += (dx / dist) * self.speed
                self.rect.y += (dy / dist) * self.speed
                if dx < 0: self.facing_right = False
                elif dx > 0: self.facing_right = True
            else: 
                self.state = "idle" 
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
            pygame.draw.circle(surface, YELLOW, screen_rect.center, 35, 3)
        surface.blit(self.image, screen_rect)

class Tree:
    def __init__(self, x, y, tree_type, name, desc):
        self.name = name
        self.description = desc
        self.type = "tree"
        self.highlight = False

        path = os.path.join("assets", "Plants", f"{tree_type}.png")
        self.sprite = load_image_safe(path, scale=0.2) 
        self.rect = self.sprite.get_rect(midbottom=(x, y))
    
    def draw(self, surface, camera):
        screen_pos_rect = self.rect.move(-camera.x, -camera.y)
        if self.highlight:
            pygame.draw.circle(surface, YELLOW, screen_pos_rect.midbottom, 40, 3)
        surface.blit(self.sprite, screen_pos_rect)

class InfoPopup:
    def __init__(self, name, description, image_surface):
        self.name = name
        self.description = description
        self.width, self.height = 500, 220
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        
        target_size = 100
        original_w, original_h = image_surface.get_size()
        
        if original_w == 0 or original_h == 0:
            self.preview_image = pygame.Surface((target_size, target_size), pygame.SRCALPHA)
            self.preview_image.fill((255, 0, 0, 100))
        else:
            scale_factor = target_size / max(original_w, original_h)
            new_w = int(original_w * scale_factor)
            new_h = int(original_h * scale_factor)
            self.preview_image = pygame.transform.scale(image_surface, (new_w, new_h))
    
    def draw(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        rect_bg = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, WHITE, rect_bg, border_radius=4)
        pygame.draw.rect(surface, (30, 30, 30), rect_bg.inflate(-6, -6), border_radius=4)

        img_x = self.x + 20
        img_y = self.y + (self.height - self.preview_image.get_height()) // 2
        pygame.draw.rect(surface, (50, 50, 50), (img_x - 5, img_y - 5, self.preview_image.get_width() + 10, self.preview_image.get_height() + 10), border_radius=5)
        surface.blit(self.preview_image, (img_x, img_y))
        
        text_start_x = self.x + 150
        title_surf = font_title.render(self.name, True, YELLOW)
        surface.blit(title_surf, (text_start_x, self.y + 25))
        pygame.draw.line(surface, GRAY, (text_start_x, self.y + 60), (self.x + self.width - 20, self.y + 60), 2)
        
        words = self.description.split()
        lines = []
        current_line = ""
        max_text_width = self.width - 170 

        for word in words:
            test_line = current_line + word + " "
            if font_text.size(test_line)[0] < max_text_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        y_off = self.y + 75
        for line in lines:
            txt = font_text.render(line, True, WHITE)
            surface.blit(txt, (text_start_x, y_off))
            y_off += 25
            
        close_txt = font_small.render("[ESC] Tutup", True, GRAY)
        surface.blit(close_txt, (self.x + self.width - 100, self.y + self.height - 25))

# =============================================================================
# 4. SETUP & HELPER FUNCTIONS
# =============================================================================

def spawn_all_grass_clumps(total_clumps, sprite_cache):
    clumps = []
    for _ in range(total_clumps):
        clumps.append({
            "x": random.randint(0, MAP_WIDTH),
            "y": random.randint(0, MAP_HEIGHT),
            "sprite": random.choice(sprite_cache),
            "amp": random.randint(3, 8), "spd": random.uniform(0.5, 1.5), "off": random.uniform(0, 6.28)
        })
    return clumps

def draw_swaying_clump(surface, clump, time_sec, camera):
    sway = math.sin(time_sec * clump["spd"] + clump["off"]) * clump["amp"]
    sx = clump["x"] - camera.x - (clump["sprite"].get_width()/2) + sway
    sy = clump["y"] - camera.y - clump["sprite"].get_height()
    if -50 < sx < SCREEN_WIDTH and -50 < sy < SCREEN_HEIGHT:
        surface.blit(clump["sprite"], (sx, sy))

# --- PERBAIKAN DI SINI (Removed dogs parameter) ---
def draw_minimap(surface, player, trees, animals, cats, camera): 
    SCALE = 0.08; MW, MH = int(MAP_WIDTH * SCALE), int(MAP_HEIGHT * SCALE)
    minimap = pygame.Surface((MW, MH)); minimap.fill((20, 50, 20))
    pygame.draw.rect(minimap, WHITE, (0,0,MW,MH), 2)
    for t in trees: pygame.draw.circle(minimap, (0, 255, 0), (int(t.rect.centerx*SCALE), int(t.rect.centery*SCALE)), 3)
    for a in animals: pygame.draw.circle(minimap, (255, 200, 0), (int(a.rect.centerx*SCALE), int(a.rect.centery*SCALE)), 3)
    for c in cats: pygame.draw.circle(minimap, (255, 150, 0), (int(c.rect.centerx*SCALE), int(c.rect.centery*SCALE)), 3) 
    
    # Bagian anjing dihapus sementara karena data dogs tidak dikirim
    
    pygame.draw.circle(minimap, (255, 0, 0), (int(player.rect.centerx*SCALE), int(player.rect.centery*SCALE)), 4)
    surface.blit(minimap, (SCREEN_WIDTH - MW - 10, 10))

def calculate_distance(r1, r2): return math.sqrt((r1.centerx-r2.centerx)**2 + (r1.centery-r2.centery)**2)

def get_safe_random_pos(existing_objects, margin=200, min_dist=150):
    max_attempts = 100 
    for _ in range(max_attempts):
        x = random.randint(margin, MAP_WIDTH - margin)
        y = random.randint(margin, MAP_HEIGHT - margin)
        
        collision = False
        for obj in existing_objects:
            if hasattr(obj, 'rect'):
                dist = math.sqrt((x - obj.rect.centerx)**2 + (y - obj.rect.centery)**2)
                if dist < min_dist:
                    collision = True
                    break
        
        if not collision:
            return x, y
    
    return random.randint(margin, MAP_WIDTH - margin), random.randint(margin, MAP_HEIGHT - margin)


# --- INISIALISASI OBJEK ---
player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)

CX = MAP_WIDTH // 2
CY = MAP_HEIGHT // 2

trees = [
    Tree(CX - 800, CY - 500, "beringin", "Pohon Beringin", "Pohon besar yang mempunyai akar di atas dan mirip rambut."),
    Tree(CX + 800, CY - 500, "oak", "Pohon Oak", "Pohon besar dan kokoh."),
    Tree(CX - 800, CY + 500, "maple", "Pohon Maple", "Terkenal dengan sirupnya."),
    Tree(CX + 800, CY + 500, "pine", "Pohon Cemara", "Pohon hijau abadi."),
    Tree(CX - 400, CY, "mangga", "Pohon Mangga", "Pohon dengan buah termanis didunia dan kalian semua pasti suka."),
    Tree(CX + 400, CY, "alpukat", "Pohon Alpukat", "Pohon dengan buah yang sangat penuh gizi dan sangaat bagus untuk tubuh."),
    Tree(CX, CY - 400, "rambutan", "Pohon Rambutan", "Pohon dengan buah eksotis dengan ciri khas buahnya berbulu dengan rasa yang manis."),
    Tree(CX, CY + 400, "sakura", "Pohon Sakura", "Pohon dengan asli Jepang dengan keindahan bunga berwarna merah mudanya yang sangat cantik.")
]

animals_data = [
    ("sapi", "Sapi", "Penghasil susu."),
    ("anak_sapi", "Anak Sapi", "Sapi kecil."),
    ("itik", "Itik", "Suka berenang."),
    ("domba", "Domba", "Bulu tebal."),
    ("babi", "Babi", "Hewan cerdas."),
    ("ayam", "Ayam", "Berkokok pagi hari."),
    ("kambing", "Kambing", "Suka memanjat."),
    ("pitik_walik", "Pitik Walik", "Bulu terbalik.")
]

animals = []
for a_type, a_name, a_desc in animals_data:
    safe_x, safe_y = get_safe_random_pos(trees + animals, min_dist=100) 
    animals.append(Animal(safe_x, safe_y, a_type, a_name, a_desc))

# --- KUCING ---
cats = []
safe_x, safe_y = get_safe_random_pos(trees + animals + cats, min_dist=120)
cats.append(Cat(safe_x, safe_y, "Si Meng", "Kucing kesayangan."))

print("Menyiapkan rumput...")
grass_cache = [create_grass_clump_sprite(random.randint(25,40), random.randint(15,30)) for _ in range(5)]
all_grass = spawn_all_grass_clumps(3000, grass_cache)

camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
popup = None
running = True

# =============================================================================
# 5. GAME LOOP UTAMA
# =============================================================================

while running:
    clock.tick(FPS)
    time_sec = pygame.time.get_ticks() / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                if popup: popup = None

            if event.key == pygame.K_SPACE and not popup:
                target_obj = None
                min_d = float('inf')
                # Gabung semua list objek untuk cek jarak interaksi
                for obj in trees + animals + cats:
                    d = calculate_distance(player.rect, obj.rect)
                    if d < INTERACTION_DISTANCE and d < min_d:
                        min_d = d
                        target_obj = obj
                
                if target_obj:
                    img_to_show = None
                    if hasattr(target_obj, 'sprite'): 
                        img_to_show = target_obj.sprite
                    elif hasattr(target_obj, 'image'): 
                        img_to_show = target_obj.image
                    
                    if img_to_show: 
                        popup = InfoPopup(target_obj.name, target_obj.description, img_to_show)

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if not popup:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1
        player.move(dx, dy)
    
    camera.center = player.rect.center
    camera.clamp_ip(MAP_RECT)

    if not popup: 
        for cat_obj in cats:
            cat_obj.update()


    can_interact_with = None
    min_dist = float('inf')
    for obj in trees + animals + cats:
        obj.highlight = False
    
    for obj in trees + animals + cats: 
        dist = calculate_distance(player.rect, obj.rect)
        if dist < INTERACTION_DISTANCE and dist < min_dist:
            min_dist = dist
            can_interact_with = obj
    if can_interact_with: can_interact_with.highlight = True

    screen.fill(GREEN_BG)
    
    drawables = []
    drawables.append(("sprite", player.rect.bottom, player))
    for t in trees: drawables.append(("sprite", t.rect.bottom, t))
    for a in animals: drawables.append(("sprite", a.rect.bottom, a))
    for c in cats: drawables.append(("sprite", c.rect.bottom, c)) 
    for g in all_grass: drawables.append(("grass", g["y"], g))
    
    drawables.sort(key=lambda item: item[1])
    
    for type, y, data in drawables:
        if type == "sprite": data.draw(screen, camera)
        elif type == "grass": draw_swaying_clump(screen, data, time_sec, camera)
    
    if can_interact_with and not popup:
        prompt_text = font_pixel.render("[SPASI]", True, WHITE)
        prompt_bg = pygame.Surface((prompt_text.get_width() + 10, prompt_text.get_height() + 6))
        prompt_bg.fill(BLACK); prompt_bg.set_alpha(180)
        px = player.rect.centerx - camera.x - prompt_bg.get_width() // 2
        py = player.rect.top - camera.y - 40
        screen.blit(prompt_bg, (px, py))
        screen.blit(prompt_text, (px + 5, py + 3))

    draw_minimap(screen, player, trees, animals, cats, camera)
    if popup: popup.draw(screen)
        
    inst_bg = pygame.Surface((600, 30)); inst_bg.set_alpha(200); inst_bg.fill(WHITE)
    screen.blit(inst_bg, (10, 10))
    screen.blit(font_small.render("WASD: Jalan | [SPASI]: Interaksi | ESC: Tutup", True, BLACK), (15, 15))

    pygame.display.flip()

pygame.quit()
sys.exit()