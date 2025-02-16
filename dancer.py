# dancer.py

import pygame
from settings import *

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Dancer(pygame.sprite.Sprite):

    # Initialize the dancer
    def __init__(self, pos, level=None):
        super().__init__()
        self.level = level if level is not None else "NULL_LEVEL"

        self.image = pygame.Surface((40, 80), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        
        self.direction = pygame.math.Vector2(0, 0)
        
        # Set ability-related attributes (ability booleans)
        self.can_super_jump = False
        self.can_dash = False
        self.can_blink = False
        self.enable_magnet = False
        self.magnet_timer = 0
                
        # Shield attributes
        self.shielded = False
        self.shield_timer = 0

        # Draw dancer
        self.draw_stick_figure()

    def draw_stick_figure(self):
        # Clear surface
        self.image.fill((0, 0, 0, 0))
        # Draw stick figure parts
        center_x = self.image.get_width() // 2
        # Head
        pygame.draw.circle(self.image, WHITE, (center_x, 15), 10, 2)
        # Body
        pygame.draw.line(self.image, WHITE, (center_x, 25), (center_x, 55), 2)
        # Arms
        pygame.draw.line(self.image, WHITE, (center_x, 35), (center_x - 15, 45), 2)
        pygame.draw.line(self.image, WHITE, (center_x, 35), (center_x + 15, 45), 2)
        # Legs
        pygame.draw.line(self.image, WHITE, (center_x, 55), (center_x - 10, 75), 2)
        pygame.draw.line(self.image, WHITE, (center_x, 55), (center_x + 10, 75), 2)
        # Shield indicator
        if self.shielded:
            pygame.draw.circle(self.image, BLUE, (center_x, 40), 35, 2)

    def apply_gravity(self):
        self.velocity.y += 1  # Adjust gravity as needed

    def update(self, keys, platforms):
        # Physical updates
        self.handle_input(keys)
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.check_collisions('x', platforms)
        self.rect.y += self.velocity.y
        self.check_collisions('y', platforms)

        # Check abilities
        #self.check_abilities()

        # Update abilities
        self.update_ability_timers()

        # Redraw stick figure to update visuals (e.g., shield indicator)
        self.draw_stick_figure()

    def handle_input(self, keys):
        self.velocity.x = 0

        if keys[pygame.K_LEFT]:
            self.velocity.x = -DANCER_SPEED
            self.direction.x = -1  

            # dash ability
            if (self.can_dash):
                self.dash()
                self.can_dash = False  

            # Blink ability
            if self.can_blink:
                self.blink()
                self.can_blink = False  # Reset after use

        elif keys[pygame.K_RIGHT]:
            self.velocity.x = DANCER_SPEED
            self.direction.x = 1

            # dash ability
            if (self.can_dash):
                self.dash()
                self.can_dash = False  

            # Blink ability
            if self.can_blink:
                self.blink()
                self.can_blink = False  # Reset after use
        else:
            # If not moving, reset velocity.x
            self.velocity.x = 0

        if keys[pygame.K_UP]:
            if self.on_ground:
                if self.can_super_jump:
                    self.super_jump()
                else:
                    self.velocity.y = -DANCER_JUMP_POWER
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1

    def check_collisions(self, direction, platforms):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                if self.velocity.x > 0:
                    self.rect.right = hits[0].rect.left
                if self.velocity.x < 0:
                    self.rect.left = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                if self.velocity.y > 0:
                    self.rect.bottom = hits[0].rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                if self.velocity.y < 0:
                    self.rect.top = hits[0].rect.bottom
                    self.velocity.y = 0
            else:
                self.on_ground = False

    def update_ability_timers(self):
        # Update shield timer
        if self.shielded:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shielded = False

    # Ability methods (skeletons)

    def super_jump(self):
        print("super jump")
        self.velocity.y = -DANCER_JUMP_POWER * 1.5
        self.can_super_jump = False

    def dash(self):
        # Direction: -1 for left, 1 for right
        steps = int(DASH_DISTANCE / DASH_SPEED)
        for _ in range(steps):
            # Move the dancer incrementally
            self.rect.x += DASH_SPEED * self.direction.x
            # Check for collisions
            if self.check_collisions('x', self.level.platforms):
                # Collision occurred; stop the dash
                self.can_dash = False
                break
        pass

    def blink(self):
        # self.rect.x += BLINK_DISTANCE * direction.x
        # self.rect.y += BLINK_DISTANCE * direction.y        
        
        if (not self.check_collisions('x', self.level.platforms)):
                self.rect.x += int(BLINK_DISTANCE) * self.direction.x
        if (not self.check_collisions('y', self.level.platforms)):
                self.rect.y += int(BLINK_DISTANCE) * self.direction.y        
        pass

    def activate_shield(self):
        # Activate shield and set timer
        self.shielded = True
        self.shield_timer = FPS * SHIELD_DURATION  # Shield lasts 3 seconds (default)

    def activate_magnet(self):
        self.magnet_enabled = True
        self.magnet_timer = FPS * MAGNET_DURATION # magnet lasts 3 seconds (default)
    # Additional methods for other abilities can be added here
