import pygame
import sys
import random
from src.config import FPS, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
from src.models.player import Player
from src.models.tree import Tree
from src.models.animal import Animal
from src.models.cat import Cat
from src.models.turkey import Turkey
from src.models.grass import create_grass_clump_sprite, spawn_all_grass_clumps
from src.controllers.game_controller import GameController
from src.views.game_view import GameView
from src.utils.helpers import get_safe_random_pos

def main():
    """Main game function"""
    pygame.init()
    
    # audio disini : adit
    pygame.mixer.init() 
    
    # load musiknya
    pygame.mixer.music.load("assets\\audio\\Searching for a Body.mp3")
    
    # jalanin musik dengan infinite loop
    pygame.mixer.music.play(-1)
    
    # Setup display BEFORE loading any assets
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Exploration Game")
    
    clock = pygame.time.Clock()
    
    # INISIALISASI OBJEK GAME
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

    # Kucing
    cats = []
    safe_x, safe_y = get_safe_random_pos(trees + animals + cats, min_dist=120)
    cats.append(Cat(safe_x, safe_y, "Si Meng", "Kucing kesayangan."))

    # Kalkun
    turkeys = []
    safe_x, safe_y = get_safe_random_pos(trees + animals + cats + turkeys, min_dist=120)
    turkeys.append(Turkey(safe_x, safe_y, "Si Kalkun", "Kalkun yang suka lari-lari."))
    

    print("Menyiapkan rumput...")
    grass_cache = [create_grass_clump_sprite(random.randint(25,40), random.randint(15,30)) for _ in range(5)]
    all_grass = spawn_all_grass_clumps(3000, grass_cache)
    
    
    # Inisialisasi MVC
    controller = GameController(player, trees, animals, cats, turkeys, all_grass)
    view = GameView(screen)
    
    running = True
    
    # GAME LOOP
    while running:
        clock.tick(FPS)
        time_sec = pygame.time.get_ticks() / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            controller.handle_event(event)
        
        # Update
        controller.handle_input(controller.popup is not None)
        controller.update_camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        controller.update_interactions()
        controller.update_cats(controller.popup is not None)
        controller.update_turkeys(controller.popup is not None)
        
        # Render
        view.render(
            player,
            trees,
            animals,
            cats,
            controller.turkeys,
            all_grass,
            controller.camera,
            time_sec,
            controller.popup,
            controller.can_interact_with
        )
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
