# settings.py
import pygame

# Screen dimensions
WIDTH = 800
HEIGHT = 600
SCREEN_SIZE = (WIDTH, HEIGHT)
LEVEL_WIDTH, LEVEL_HEIGHT = 3000, 1200  # Example large level size

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game settings
FPS = 60

# Dancer settings
DANCER_SPEED = 5
DANCER_JUMP_POWER = 20
SHIELD_DURATION = 3
MAGNET_DURATION = 5
MAGNET_RANGE = 25
DASH_DISTANCE = 100  # Total distance to dash
DASH_SPEED = 5      # Movement per iteration
BLINK_DISTANCE_ALONG_X = int(DASH_DISTANCE / 2) + 20
BLINK_DISTANCE_ALONG_Y = BLINK_DISTANCE_ALONG_X# + 50 # adding a constant 50 allows for blinking through objects along y (idk why either)

# Composer settings
COMPOSER_KEY_BINDS = [1,2,3,4,5,6,7]
    # 1: Super jump
    # 2: Dash
    # 3: Blink
    # 4: Shield
    # 5: Time Slow
    # 6: Magnet
    # 7: Speeds up tempo
COMPOSER_KEY_BINDS_TYPES = ["Super jump", "Dash", "Blink", "Shield", 
                            "Time Slow", "Magnet", "Speeds up tempo"]

# Beats per minute
BPM = 120

# Custom event for metronome tick
METRONOME_EVENT = pygame.USEREVENT + 1

DEATH_EVENT = pygame.USEREVENT

WIN_EVENT = pygame.USEREVENT

MENU_EVENT = pygame.USEREVENT

# Misc.
X_AXIS = 'x'
Y_AXIS = 'y'
SHARD_RECHARGE_RATE = 20
