# settings.py
import pygame

# Screen dimensions
WIDTH = 800
HEIGHT = 600
SCREEN_SIZE = (WIDTH, HEIGHT)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game settings
FPS = 60

# Dancer settings
DANCER_SPEED = 5
DANCER_JUMP_POWER = 20
SHIELD_DURATION = 3
MAGNET_DURATION = 3
BLINK_DISTANCE = (DANCER_SPEED / 2)
DASH_DISTANCE = 100  # Total distance to dash
DASH_SPEED = 5      # Movement per iteration

# Composer settings
COMPOSER_KEY_BINDS = [1,2,3,4,5,6,7]
    # 1: Super jump
    # 2: Dash
    # 3: Blink
    # 4: Shield
    # 5: Time Slow
    # 6: Magnet
    # 7:Speeds up tempo

# Beats per minute
BPM = 120

# Custom event for metronome tick
METRONOME_EVENT = pygame.USEREVENT + 1


