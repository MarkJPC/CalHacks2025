import pygame
from dancer import Dancer
from composer import Composer
from level import Level

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
DANCER_START_POS = (400, 300)
LEVEL_WIDTH, LEVEL_HEIGHT = 1600, 1200  # Example large level size
FPS = 60

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Camera area
        self.width = width
        self.height = height

    def apply(self, entity):
        """Offset an entity's position based on the camera."""
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """Smoothly follow the target (Dancer)."""
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        # Keep camera within bounds
        x = min(0, x)  # Left boundary
        y = min(0, y)  # Top boundary
        x = max(-(self.width - SCREEN_WIDTH), x)  # Right boundary
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Bottom boundary

        # Smooth camera movement
        self.camera.x += (x - self.camera.x) * 0.1
        self.camera.y += (y - self.camera.y) * 0.1


# Platform class to create more platforms
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Smooth Camera Example")
    clock = pygame.time.Clock()

    # Create a player
    dancer = Dancer(DANCER_START_POS)

    # Create a camera
    camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)

    # Create a composer
    level = Level()
    composer = Composer(dancer, level)

    # Create a simple level (just some platforms)
    platforms = pygame.sprite.Group()

    # Create the ground and set its color to red
    ground = Platform(0, LEVEL_HEIGHT - 450, LEVEL_WIDTH, 40, (255, 0, 0))  # Red ground
    platforms.add(ground)

    # Add more platforms at different heights and positions
    platform1 = Platform(200, 500, 800, 20, (0, 255, 0))  # Green platform
    platform2 = Platform(500, 400, 250, 20, (0, 0, 255))  # Blue platform
    platform3 = Platform(900, 300, 300, 20, (255, 255, 0))  # Yellow platform

    platforms.add(platform1, platform2, platform3)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(dancer, ground, platform1, platform2, platform3)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player and camera
        dancer.update(keys, platforms)
        camera.update(dancer)

        # Draw everything with camera offset
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
