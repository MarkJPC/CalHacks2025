# level.py

import pygame
from settings import *

# Define colors
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)

class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.note_shards = pygame.sprite.Group()
        self.create_platforms()
        self.create_note_shards()

    def create_platforms(self):
        # Ground
        ground = Platform(0, HEIGHT - 40, WIDTH, 40)
        self.platforms.add(ground)

        # Platform 1
        platform1 = Platform(200, 450, 200, 20)
        self.platforms.add(platform1)

        # Platform 2
        platform2 = Platform(450, 350, 150, 20)
        self.platforms.add(platform2)

        # Add more platforms as needed

    def create_note_shards(self):
        # Note Shard 1
        shard1 = NoteShard(250, 420)
        self.note_shards.add(shard1)

        # Note Shard 2
        shard2 = NoteShard(500, 320)
        self.note_shards.add(shard2)

        # Add more note shards as needed

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))

class NoteShard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        pygame.draw.polygon(self.image, YELLOW, [(10, 0), (20, 10), (10, 20), (0, 10)])
        self.rect = self.image.get_rect(center=(x, y))
