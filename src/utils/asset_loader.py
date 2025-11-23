import os
import pygame
from src.config import BASE_DIR

def get_asset_path(*paths):
    """Mendapatkan path lengkap ke asset"""
    return os.path.join(BASE_DIR, *paths)

def load_image_safe(relative_path, scale=1, flags=0):
    """Load image dengan error handling"""
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
    """Load spritesheet dengan error handling"""
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
