import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, BLACK, GRAY

class InfoPopup:
    def __init__(self, name, description, image_surface):
        self.name = name
        self.description = description
        self.width, self.height = 500, 280
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        
        # Font initialization
        pygame.font.init()
        self.font_title = pygame.font.Font(None, 32)
        self.font_text = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
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
        title_surf = self.font_title.render(self.name, True, YELLOW)
        surface.blit(title_surf, (text_start_x, self.y + 25))
        pygame.draw.line(surface, GRAY, (text_start_x, self.y + 60), (self.x + self.width - 20, self.y + 60), 2)
        
        words = self.description.split()
        lines = []
        current_line = ""
        max_text_width = self.width - 170 

        for word in words:
            test_line = current_line + word + " "
            if self.font_text.size(test_line)[0] < max_text_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        y_off = self.y + 75
        for line in lines:
            txt = self.font_text.render(line, True, WHITE)
            surface.blit(txt, (text_start_x, y_off))
            y_off += 25
            
        close_txt = self.font_small.render("[ESC] Tutup", True, GRAY)
        surface.blit(close_txt, (self.x + self.width - 100, self.y + self.height - 25))
