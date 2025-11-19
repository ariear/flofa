import pygame
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, WHITE, BLACK
)
from src.models.grass import draw_swaying_clump

class GameView:
    def __init__(self):
        pygame.font.init()
        self.font_small = pygame.font.Font(None, 20)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Eksplorasi Alam (Rumput Sprite)")
    
    def render(self, player, trees, animals, grass_clumps, camera, time_sec, popup):
        self.screen.fill(GREEN)
        
        # Sorting untuk depth rendering
        drawables = []
        
        drawables.append(("sprite", player.rect.bottom, player))
        for tree in trees:
            drawables.append(("sprite", tree.rect.bottom, tree))
        for animal in animals:
            drawables.append(("sprite", animal.rect.bottom, animal))

        for clump_data in grass_clumps:
            drawables.append(("grass", clump_data["y"], clump_data))
        
        drawables.sort(key=lambda item: item[1])
        
        for (type, y_pos, data) in drawables:
            if type == "sprite":
                data.draw(self.screen, camera)
            elif type == "grass":
                draw_swaying_clump(self.screen, data, time_sec, camera)
        
        if popup:
            popup.draw(self.screen)
        
        # Instruksi
        inst_text = self.font_small.render("Gunakan WASD/Arrow keys untuk bergerak. Dekati pohon/hewan untuk melihat info.", True, BLACK)
        inst_bg = pygame.Surface((inst_text.get_width() + 20, inst_text.get_height() + 10))
        inst_bg.fill(WHITE)
        inst_bg.set_alpha(200)
        self.screen.blit(inst_bg, (10, 10))
        self.screen.blit(inst_text, (20, 15))
        
        pygame.display.flip()
