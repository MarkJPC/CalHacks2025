# main.py

import pygame
import sys
from settings import *
from dancer import Dancer
from composer import Composer
from level import Level
from camera import Camera

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Tempo Tactics Prototype')
    clock = pygame.time.Clock()

    level = Level()

    # Create game objects
    dancer = Dancer((100, HEIGHT - 100), level)
    composer = Composer(dancer, level)
    dancer.composer = composer
    all_sprites = pygame.sprite.Group()
    all_sprites.add(dancer)
    all_sprites.add(*level.platforms)
    all_sprites.add(*level.note_shards)

    # Create a camera
    camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)

    # Set up metronome timer
    beat_interval = int((60 / BPM) * 1000)  # Convert seconds to milliseconds
    pygame.time.set_timer(METRONOME_EVENT, beat_interval)

    # Load metronome sound
    metronome_sound = pygame.mixer.Sound('assets/sounds/metronome_tick.wav')

    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle keydown events for abilities
                composer.handle_keydown(event.key)
            elif event.type == METRONOME_EVENT:
                metronome_sound.play()

        # Get key states
        keys = pygame.key.get_pressed()

        # Update
        dancer.update(keys, level.platforms)
        composer.update(keys)

        camera.update(dancer)

        # Clear screen ONCE
        screen.fill(BLACK)

        # Draw all sprites at their camera-adjusted positions
        for sprite in all_sprites:
            screen_position = camera.apply(sprite)
            screen.blit(sprite.image, screen_position)

        # Check for note shard collection
        collected_shards = pygame.sprite.spritecollide(dancer, level.note_shards, True)
        if collected_shards:
            for shard in collected_shards:
                composer.recharge(SHARD_RECHARGE_RATE)
                #collect_sound = pygame.mixer.Sound('assets/sounds/collect.wav')
                #collect_sound.play()

        # Draw
        #screen.fill(BLACK)
        #all_sprites.draw(screen)
        composer.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
