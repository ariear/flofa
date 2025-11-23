import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN_BG, WHITE, BLACK, MAP_WIDTH, MAP_HEIGHT, YELLOW
from src.models.grass import draw_swaying_clump

class GameView:
    def __init__(self, screen):
        pygame.font.init()
        self.font_small = pygame.font.Font(None, 20)
        self.font_pixel = pygame.font.Font(None, 28)
        self.screen = screen
    
    def render(self, player, trees, animals, cats, turkeys ,grass_clumps, camera, time_sec, popup, can_interact_with):
        """Render semua elemen game"""
        self.screen.fill(GREEN_BG)
        
        # Sorting untuk depth rendering
        drawables = []
        drawables.append(("sprite", player.rect.bottom, player))
        for t in trees: drawables.append(("sprite", t.rect.bottom, t))
        for a in animals: drawables.append(("sprite", a.rect.bottom, a))
        for c in cats: drawables.append(("sprite", c.rect.bottom, c))
        for tky in turkeys: drawables.append(("sprite", tky.rect.bottom, tky))
        for g in grass_clumps: drawables.append(("grass", g["y"], g))

        
        drawables.sort(key=lambda item: item[1])
        
        for type, y, data in drawables:
            if type == "sprite": data.draw(self.screen, camera)
            elif type == "grass": draw_swaying_clump(self.screen, data, time_sec, camera)
        
        # Interaction prompt
        if can_interact_with and not popup:
            prompt_text = self.font_pixel.render("[SPASI]", True, WHITE)
            prompt_bg = pygame.Surface((prompt_text.get_width() + 10, prompt_text.get_height() + 6))
            prompt_bg.fill(BLACK); prompt_bg.set_alpha(180)
            px = player.rect.centerx - camera.x - prompt_bg.get_width() // 2
            py = player.rect.top - camera.y - 40
            self.screen.blit(prompt_bg, (px, py))
            self.screen.blit(prompt_text, (px + 5, py + 3))

        # Minimap
        self._draw_minimap(player, trees, animals, cats, turkeys, camera)
        
        # Popup
        if popup: popup.draw(self.screen)
            
        # Instructions
        inst_bg = pygame.Surface((600, 30)); inst_bg.set_alpha(200); inst_bg.fill(WHITE)
        self.screen.blit(inst_bg, (10, 10))
        self.screen.blit(self.font_small.render("WASD: Jalan | [SPASI]: Interaksi | ESC: Tutup", True, BLACK), (15, 15))

        pygame.display.flip()
    
    def _draw_minimap(self, player, trees, animals, cats, turkeys, camera):
        """Menggambar minimap"""
        SCALE = 0.08
        MW, MH = int(MAP_WIDTH * SCALE), int(MAP_HEIGHT * SCALE)
        minimap = pygame.Surface((MW, MH)); minimap.fill((20, 50, 20))
        pygame.draw.rect(minimap, WHITE, (0,0,MW,MH), 2)
        for t in trees: pygame.draw.circle(minimap, (0, 255, 0), (int(t.rect.centerx*SCALE), int(t.rect.centery*SCALE)), 3)
        for a in animals: pygame.draw.circle(minimap, (255, 200, 0), (int(a.rect.centerx*SCALE), int(a.rect.centery*SCALE)), 3)
        for c in cats: pygame.draw.circle(minimap, (255, 150, 0), (int(c.rect.centerx*SCALE), int(c.rect.centery*SCALE)), 3)
        for tky in turkeys: pygame.draw.circle(minimap, (255, 0, 0), (int(tky.rect.centerx*SCALE), int(tky.rect.centery*SCALE)), 3)
        pygame.draw.circle(minimap, (255, 0, 0), (int(player.rect.centerx*SCALE), int(player.rect.centery*SCALE)), 4)
        self.screen.blit(minimap, (SCREEN_WIDTH - MW - 10, 10))
