import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY

class InfoPopup:
    def __init__(self, name, description):
        pygame.font.init()
        self.font_title = pygame.font.Font(None, 32)
        self.font_text = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        self.active = True
        self.name = name
        self.description = description
        self.width = 400
        self.height = 250
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
    
    def draw(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 3, border_radius=10)
        title_surf = self.font_title.render(self.name, True, BLACK)
        surface.blit(title_surf, (self.x + 20, self.y + 20))
        info_text = self.font_small.render("(Tekan ESC atau berjalan menjauh untuk menutup)", True, GRAY)
        surface.blit(info_text, (self.x + 20, self.y + 55))
        words = self.description.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font_text.size(test_line)[0] < self.width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        y_offset = self.y + 90
        for line in lines:
            text_surf = self.font_text.render(line, True, BLACK)
            surface.blit(text_surf, (self.x + 20, y_offset))
            y_offset += 30
