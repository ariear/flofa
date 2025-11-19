import pygame
import sys
import random
from src.config import FPS, MAP_WIDTH, MAP_HEIGHT
from src.models.player import Player
from src.models.tree import Tree
from src.models.animal import Animal
from src.models.grass import create_grass_clump_sprite, spawn_all_grass_clumps
from src.controllers.game_controller import GameController
from src.views.game_view import GameView

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # INISIALISASI OBJEK GAME
    player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)
    
    trees = [
        Tree(MAP_WIDTH // 2 - 400, MAP_HEIGHT // 2 - 200, "oak", "Pohon Oak", "Pohon oak adalah pohon besar yang kokoh dengan daun lebar. Kayunya sering digunakan untuk furniture dan konstruksi. Pohon ini dapat hidup hingga ratusan tahun."),
        Tree(MAP_WIDTH // 2 + 300, MAP_HEIGHT // 2 - 150, "pine", "Pohon Pinus", "Pohon pinus memiliki daun berbentuk jarum dan menghasilkan kerucut. Mereka tumbuh subur di iklim dingin dan sering digunakan sebagai pohon Natal."),
        Tree(MAP_WIDTH // 2 - 100, MAP_HEIGHT // 2 + 200, "oak", "Pohon Maple", "Pohon maple terkenal dengan daun berwarna cerah di musim gugur. Getahnya dapat diolah menjadi sirup maple yang manis dan lezat."),
        Tree(MAP_WIDTH // 2 + 500, MAP_HEIGHT // 2 + 250, "pine", "Pohon Cemara", "Pohon cemara adalah pohon hijau abadi yang tetap hijau sepanjang tahun. Mereka memiliki aroma khas dan sering ditanam sebagai tanaman hias."),
    ]
    
    animals = [
        Animal(MAP_WIDTH // 2, MAP_HEIGHT // 2 - 100, "rabbit", "Kelinci", "Kelinci adalah hewan herbivora yang lincah dengan telinga panjang. Mereka hidup dalam liang dan aktif pada pagi dan sore hari.", (200, 200, 200)),
        Animal(MAP_WIDTH // 2 + 200, MAP_HEIGHT // 2 + 100, "deer", "Rusa", "Rusa adalah hewan mamalia anggun dengan tanduk bercabang (pada jantan). Mereka hidup berkelompok dan memakan dedaunan serta rumput.", (160, 120, 80)),
        Animal(MAP_WIDTH // 2 - 300, MAP_HEIGHT // 2 + 200, "bird", "Burung Pipit", "Burung pipit adalah burung kecil yang sering ditemui di sekitar pemukiman. Mereka memakan biji-bijian dan serangga kecil.", (100, 150, 200)),
        Animal(MAP_WIDTH // 2 + 400, MAP_HEIGHT // 2 - 200, "rabbit", "Kelinci Hutan", "Kelinci hutan lebih besar dari kelinci peliharaan dan memiliki bulu coklat keabu-abuan. Mereka sangat waspada terhadap predator.", (150, 130, 100)),
    ]
    
    print("Membuat sprite rumput... (Mungkin butuh beberapa detik)")
    grass_clump_sprites_cache = []
    for _ in range(5): 
        w = random.randint(25, 40)
        h = random.randint(15, 30)
        grass_clump_sprites_cache.append(create_grass_clump_sprite(w, h))
    print("Sprite rumput selesai dibuat.")
    
    all_grass_clumps = spawn_all_grass_clumps(2500, grass_clump_sprites_cache)
    
    # Inisialisasi MVC
    controller = GameController(player, trees, animals, all_grass_clumps)
    view = GameView()
    
    running = True
    
    # MAIN GAME LOOP
    while running:
        clock.tick(FPS)
        time_sec = pygame.time.get_ticks() / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            controller.handle_event(event)
        
        controller.update()
        
        view.render(
            player,
            trees,
            animals,
            all_grass_clumps,
            controller.camera,
            time_sec,
            controller.popup
        )
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
