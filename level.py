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
        self.create_harmony_challenges()

    def create_platforms(self):
        # Ground - acts as main rhythm keeper
        ground = Platform(0, HEIGHT - 40, LEVEL_WIDTH, 40)
        self.platforms.add(ground)

        # SECTION 1: INTRO (C Major chord progression)
        # Platforms spaced like quarter notes
        self.platforms.add(Platform(200, 500, 100, 20))  # C
        self.platforms.add(Platform(400, 450, 100, 20))  # E
        self.platforms.add(Platform(600, 400, 100, 20))  # G
        self.platforms.add(Platform(800, 350, 100, 20))  # C

        # SECTION 2: VERSE (Arpeggio pattern)
        for i in range(5):
            self.platforms.add(Platform(1000 + i*150, 500 - (i%3)*50, 80, 15))

        # SECTION 3: CHORUS (Strong beats)
        # Floating platforms requiring rhythm jumps
        self.platforms.add(Platform(1600, 300, 200, 20)) 
        self.platforms.add(Platform(1900, 200, 200, 20))
        self.platforms.add(Platform(2200, 100, 200, 20))

        # SECTION 4: BRIDGE (Key change)
        # Diagonal platform ascent
        for i in range(8):
            self.platforms.add(Platform(2500 + i*120, 400 - i*40, 100, 15))

        # SECTION 5: OUTRO (Coda)
        # Grand finale platform
        self.platforms.add(Platform(3400, 200, 400, 40))

    def create_note_shards(self):
        # SECTION 1: INTRO (C Major scale)
        # Placed in chord positions
        self.note_shards.add(NoteShard(225, 480))  # C (1)
        self.note_shards.add(NoteShard(425, 430))  # E (3)
        self.note_shards.add(NoteShard(625, 380))  # G (5)
        self.note_shards.add(NoteShard(825, 330))  # C (8)

        # SECTION 2: VERSE (Arpeggio targets)
        for i in range(1,6):
            self.note_shards.add(NoteShard(1040 + i*150, 480 - (i%3)*40))

        # SECTION 3: CHORUS (Rhythm targets)
        self.note_shards.add(NoteShard(1700, 270))
        self.note_shards.add(NoteShard(2000, 170))
        self.note_shards.add(NoteShard(2300, 70))

        # SECTION 4: BRIDGE (Key change challenge)
        for i in range(7):
            self.note_shards.add(NoteShard(2550 + i*120, 360 - i*35))

    def create_harmony_challenges(self):
        # Add special platforms that require chord combinations
        # 1. C-E-G Platform (Needs major triad)
        chord_platform1 = HarmonyPlatform(2800, 300, (1,3,5))
        self.platforms.add(chord_platform1)

        # 2. F-A-C Platform (Needs subdominant)
        chord_platform2 = HarmonyPlatform(3200, 200, (4,6,8))
        self.platforms.add(chord_platform2)

        # 3. Final Cadence Platform (G7-C)
        final_platform = HarmonyPlatform(3400, 150, (5,7,2,8))
        self.platforms.add(final_platform)

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

class HarmonyPlatform(Platform):
    """Platform that only appears when correct notes are played together"""
    def __init__(self, x, y, required_notes):
        super().__init__(x, y, 200, 20)
        self.required_notes = set(required_notes)
        self.active = False
        self.image.fill((50, 50, 200))  # Blue hint color

    def update(self, active_notes):
        """Check if required chord is being played"""
        self.active = self.required_notes.issubset(active_notes)
        self.image.set_alpha(255 if self.active else 50)
