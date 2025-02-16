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
        self.create_foundational_platforms()
        self.create_musical_sections()
        self.create_finale()

    def create_foundational_platforms(self):
        # Ground spanning the entire level.
        ground = Platform(0, LEVEL_HEIGHT - 40, LEVEL_WIDTH, 40)
        self.platforms.add(ground)

    def create_musical_sections(self):
        # --- Section 1: Rhythmic Launch (Keys 1 & 2: Super Jump / Dash) ---
        # Create a series of staggered platforms that force the dancer to
        # use a super jump and dash to reach each one.
        for i in range(4):
            x = 300 + i * 250
            y = LEVEL_HEIGHT - 100 - (i % 2) * 50  # Alternate vertical positioning.
            platform = Platform(x, y, 150, 20)
            self.platforms.add(platform)
            # Place a note shard above the platform.
            shard = NoteShard(x + 75, y - 30)
            self.note_shards.add(shard)

        # --- Section 2: Spectral Passage (Keys 3 & 4: Blink / Shield) ---
        base_x = 1300
        # A platform the dancer must reach.
        p1 = Platform(base_x, LEVEL_HEIGHT - 200, 200, 20)
        self.platforms.add(p1)

        # A BlinkGate obstacle: the dancer should use Blink (Key 3) to bypass it.
        blink_gate = BlinkGate(base_x + 220, LEVEL_HEIGHT - 240, 15, 200)
        self.platforms.add(blink_gate)

        # A hazardous section that requires the dancer to activate Shield (Key 4)
        shield_section = ShieldPlatform(base_x + 300, LEVEL_HEIGHT - 300, 150, 20)
        self.platforms.add(shield_section)

        # shard
        shard2 = NoteShard(base_x + 375, LEVEL_HEIGHT - 330)
        self.note_shards.add(shard2)

        # --- Section 3: Magnetic Finale (Key 5: Magnet) ---
        base_x = 2200
        # A moving platform that challenges timing.
        moving_platform = MovingPlatform(base_x, LEVEL_HEIGHT - 150, 200, 20, speed=2)
        self.platforms.add(moving_platform)

        # Final note shard—could be made to “magnetize” toward the dancer.
        final_shard = FinalNoteShard(base_x + 100, LEVEL_HEIGHT - 180)
        self.note_shards.add(final_shard)

    def create_finale(self):
        # Final platform to finish the level.
        final_platform = Platform(LEVEL_WIDTH - 200, LEVEL_HEIGHT - 100, 200, 20)
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
        if abs(self.rect.x - self.initial_x) > 100:
            self.direction *= -1

# ---------------------------
# The final note shard collectible (can be used to signal level completion).
class FinalNoteShard(NoteShard):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Change the color to green to indicate its special status.
        self.image.fill(GREEN)
