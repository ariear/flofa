import pygame
import os

# KONSTANTA KONFIGURASI GAME
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
PLAYER_SPEED = 3
INTERACTION_DISTANCE = 80

MAP_WIDTH = SCREEN_WIDTH * 3
MAP_HEIGHT = SCREEN_HEIGHT * 3
MAP_RECT = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)
TILE_SIZE = 64 

# WARNA
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BG = (34, 139, 34) 
YELLOW = (255, 255, 0)
BROWN = (101, 67, 33)
GRAY = (200, 200, 200)
BLUE_DOG = (0, 150, 255)

# Palet Warna Rumput
GRASS_COLORS = [
    (30, 100, 40), (40, 120, 50), (50, 140, 60),
    (60, 150, 70), (25, 90, 35)
]

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
