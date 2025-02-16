# main.py

import pygame
import sys
from settings import *
from dancer import Dancer
from composer import Composer
from level import Level
from camera import Camera
from level import *

# Game states
START = 'start'
GAME = 'game'
DEAD = 'dead'
VICTORY = 'victory'

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Tempo Tactics Prototype')
    clock = pygame.time.Clock()

    game_state = START

    running = True
    while running:
        clock.tick(FPS)

        if game_state == START:
            running = handle_start_screen(screen)

            if not running:
                break  # Exit the game

            # Initialize game objects after starting the game
            dancer, composer, level, camera, all_sprites, metronome_sound = initialize_game()
            game_state = GAME
        elif game_state == GAME:
            # Existing game loop code
            game_state = handle_gameplay(screen, clock, dancer, composer, level,
                                         camera, all_sprites, metronome_sound)
            if game_state is None:
                running = False  # Exit the game
        elif game_state == DEAD:
            running = handle_death_screen(screen)

            if running:
                # Restart the game
                dancer, composer, level, camera, all_sprites, metronome_sound = initialize_game()
                game_state = GAME
            else:
                break  # Exit the game
        elif game_state == VICTORY:
            running = handle_victory_screen(screen)

            if running:
                # Restart the game
                dancer, composer, level, camera, all_sprites, metronome_sound = initialize_game()
                game_state = GAME
            else:
                break  # Exit the game

    pygame.quit()
    sys.exit()

def initialize_game():
    print("initializing game")
    # Create level object
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

    return dancer, composer, level, camera, all_sprites, metronome_sound

def handle_gameplay(screen, clock, dancer, composer, level, camera, all_sprites, metronome_sound):
            # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
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

        # update camera
        camera.update(dancer)

        # update moving platforms and shield platforms
        for platform in level.platforms:
            if isinstance(platform, MovingPlatform):
                platform.update()
            if isinstance(platform, ShieldPlatform):
                platform.update(dancer.shielded)

        # Clear screen ONCE
        screen.fill(BLACK)

        # Draw all sprites at their camera-adjusted positions
        for sprite in all_sprites:
            screen_position = camera.apply(sprite)
            screen.blit(sprite.image, screen_position)

        dancer.draw_health_bar(screen, camera)

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

        # Check for death
        if dancer.health <= 0:
            return DEAD

        # Check for victory
        if dancer.rect.x >= LEVEL_WIDTH - dancer.rect.width:
            return VICTORY
        
        return GAME
        
def handle_start_screen(screen):
    font = pygame.font.SysFont('Arial', 50)
    title_text = font.render('Tempo Tactics', True, (255, 255, 255))
    play_text = font.render('Play', True, (255, 255, 255))
    exit_text = font.render('Exit', True, (255, 255, 255))

    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

    pygame.time.set_timer(DEATH_EVENT, 1)    
    menu_sound = pygame.mixer.Sound('assets/sounds/menu.wav')

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)

        # menu_sound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit the game                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    return True  # Start the game
                    pygame.mixer.pause('assets/sounds/menu.wav')
                elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                    return False  # Exit the game
                    pygame.mixer.pause('assets/sounds/menu.wav')

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def handle_death_screen(screen):
    font = pygame.font.SysFont('Arial', 50)
    death_text = font.render('You Died', True, (255, 0, 0))
    play_text = font.render('Play Again', True, (255, 255, 255))
    exit_text = font.render('Exit', True, (255, 255, 255))

    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

    pygame.time.set_timer(DEATH_EVENT, 1)    
    death_sound = pygame.mixer.Sound('assets/sounds/death.wav')

    death_sound.play()

    while True:
        screen.fill(BLACK)
        screen.blit(death_text, death_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    return True  # Play again
                elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                    return False  # Exit the game

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def handle_victory_screen(screen):
    font = pygame.font.SysFont('Arial', 50)
    victory_text = font.render('You Won!', True, (0, 255, 0))
    play_text = font.render('Play Again', True, (255, 255, 255))
    exit_text = font.render('Exit', True, (255, 255, 255))

    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

    pygame.time.set_timer(WIN_EVENT, 1)    
    win_sound = pygame.mixer.Sound('assets/sounds/win.wav')

    win_sound.play()

    while True:
        screen.fill(BLACK)
        screen.blit(victory_text, victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    return True  # Play again
                elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                    return False  # Exit the game

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == '__main__':
    main()
