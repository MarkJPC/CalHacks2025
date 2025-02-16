# level.py
import pygame
import math
from settings import *  # Ensure your settings provide HEIGHT, LEVEL_WIDTH, etc.

# Define colors
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.note_shards = pygame.sprite.Group()
        self.create_level()
        self.create_musical_sections()
        self.create_finale()

    def create_level(self):
        # start platform
        ground = Platform(0, LEVEL_HEIGHT - 40, 300, 40)
        self.platforms.add(ground)

        # jump
        p1 = Platform(500, LEVEL_HEIGHT - 300, 120, 20)
        self.platforms.add(p1)

        # dash
        p2 = Platform(900, LEVEL_HEIGHT - 150, 300, 20)
        self.platforms.add(p2)

        # blink
        p3 = BlinkGate(1050, LEVEL_HEIGHT - 550, 15, 600)
        self.platforms.add(p3)

        s1 = NoteShard(1300, LEVEL_HEIGHT - 600)
        self.note_shards.add(s1)

        # jump
        p4 = Platform(1400, LEVEL_HEIGHT - 300, 120, 20)
        self.platforms.add(p4)

        s2 = NoteShard(1800, LEVEL_HEIGHT - 350)
        self.note_shards.add(s2)

        # dash
        p5 = Platform(1800, LEVEL_HEIGHT - 150, 300, 20)
        self.platforms.add(p5)

        # blink
        p6 = BlinkGate(1950, LEVEL_HEIGHT - 550, 15, 600)
        self.platforms.add(p6)

        s3 = NoteShard(2200, LEVEL_HEIGHT - 600)
        self.note_shards.add(s3)
        
        # jump  
        p7 = Platform(2240, LEVEL_HEIGHT - 400, 150, 20)
        self.platforms.add(p7)

        s4 = NoteShard(2600, LEVEL_HEIGHT - 850)
        self.note_shards.add(s4)
        
        # jump  
        p8 = Platform(2640, LEVEL_HEIGHT - 700, 150, 20)
        self.platforms.add(p8)

        s5 = NoteShard(3000, LEVEL_HEIGHT - 1150)
        self.note_shards.add(s5)
        
        # jump  
        p9 = Platform(3040, LEVEL_HEIGHT - 1000, 150, 20)
        self.platforms.add(p9)

        s6 = NoteShard(3400, LEVEL_HEIGHT - 1450)
        self.note_shards.add(s6)
        
        # jump  
        p10 = Platform(3440, LEVEL_HEIGHT - 1300, 150, 20)
        self.platforms.add(p10)

        # A hazardous section that requires the dancer to activate Shield (Key 4)
        shield_section = ShieldPlatform(3900, LEVEL_HEIGHT - 1300, 150, 20)
        self.platforms.add(shield_section)

        s7 = NoteShard(3975, LEVEL_HEIGHT - 1340)
        self.note_shards.add(s7)

        # A moving platform that challenges timing.
        moving_platform = MovingPlatform(4200, LEVEL_HEIGHT - 1400, 200, 20, speed=2)
        self.platforms.add(moving_platform)

        # blink
        b3 = BlinkGate(4300, LEVEL_HEIGHT - 2000, 15, 600)
        self.platforms.add(b3)

    def create_musical_sections(self):
        # --- Section 1: Rhythmic Launch (Keys 1 & 2: Super Jump / Dash) ---
        # Create a series of staggered platforms that force the dancer to
        # use a super jump and dash to reach each one.
        '''
        for i in range(4):
            x = 300 + i * 250
            y = LEVEL_HEIGHT - 100 - (i % 2) * 50  # Alternate vertical positioning.
            platform = Platform(x, y, 150, 20)
            self.platforms.add(platform)
            # Place a note shard above the platform.
            shard = NoteShard(x + 75, y - 30)
            self.note_shards.add(shard)
        '''

        # --- Section 2: Spectral Passage (Keys 3 & 4: Blink / Shield) ---
        base_x = 1300

        # A hazardous section that requires the dancer to activate Shield (Key 4)
        #shield_section = ShieldPlatform(base_x + 300, LEVEL_HEIGHT - 300, 150, 20)
        #self.platforms.add(shield_section)

        # shard
        #shard2 = NoteShard(base_x + 375, LEVEL_HEIGHT - 330)
        #self.note_shards.add(shard2)

        # --- Section 3: Magnetic Finale (Key 5: Magnet) ---
        base_x = 2200
        # A moving platform that challenges timing.
        #moving_platform = MovingPlatform(base_x, LEVEL_HEIGHT - 150, 200, 20, speed=2)
        #self.platforms.add(moving_platform)



    def create_finale(self):

        # Final note shard—could be made to “magnetize” toward the dancer.
        final_shard = FinalNoteShard(LEVEL_WIDTH - 100, LEVEL_HEIGHT - 1600)
        self.note_shards.add(final_shard)

        # Final platform to finish the level.
        final_platform = Platform(LEVEL_WIDTH - 200, LEVEL_HEIGHT - 1600, 200, 20)
        self.platforms.add(final_platform)

# ---------------------------
# Basic platform class.
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))

# ---------------------------
# Note shard collectible.
class NoteShard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Use SRCALPHA to allow transparency.
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Draw a simple diamond shape.
        pygame.draw.polygon(self.image, YELLOW, [(10, 0), (20, 10), (10, 20), (0, 10)])
        self.rect = self.image.get_rect(center=(x, y))

# ---------------------------
# A gate that the dancer can pass only by using Blink (Key 3).
class BlinkGate(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill(RED)  # Red to indicate danger.
    # You can later add a method here to check if the blink buff is active.

# ---------------------------
# A platform that is hazardous unless the dancer's Shield (Key 4) is active.
class ShieldPlatform(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.base_color = BLUE
        self.image.fill(self.base_color)
        self.solid = False  # Example property: only becomes solid/safe when shielded.
    
    def update(self, is_shielded):
        # If shield buff is active, the platform becomes “safe.”
        if is_shielded:
            self.image.fill(GREEN)  # Change color to indicate safety.
            self.solid = True
        else:
            self.image.fill(self.base_color)
            self.solid = False

    def check_hazard(self, dancer):
        # If the dancer is not shielded and collides with the platform, apply damage
        if not dancer.shielded:
            dancer.apply_damage(1)

# ---------------------------
# A platform that moves horizontally.
class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, speed=1):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.direction = 1  # Moving right initially.
        self.initial_x = x

    def update(self):
        self.rect.x += self.speed * self.direction
        # Reverse direction when 100 pixels away from the starting position.
        if abs(self.rect.x - self.initial_x) > 150:
            self.direction *= -1

# ---------------------------
# The final note shard collectible (can be used to signal level completion).
class FinalNoteShard(NoteShard):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Change the color to green to indicate its special status.
        self.image.fill(GREEN)
