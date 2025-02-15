# dancer.py

import pygame
from settings import *

class Dancer(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 80), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

        # Ability-related attributes
        self.shielded = False
        self.shield_timer = 0

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
        self.handle_input(keys)
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.check_collisions('x', platforms)
        self.rect.y += self.velocity.y
        self.check_collisions('y', platforms)

        # Update abilities
        if self.shielded:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shielded = False
            self.draw_stick_figure()  # Refresh shield visual

    def handle_input(self, keys):
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -DANCER_SPEED
        if keys[pygame.K_RIGHT]:
            self.velocity.x = DANCER_SPEED
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = -DANCER_JUMP_POWER

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

    # Ability methods
    def super_jump(self):
        self.velocity.y = -DANCER_JUMP_POWER * 1.5

    def dash(self, direction):
        dash_distance = 50
        self.rect.x += dash_distance * direction

    def activate_shield(self):
        self.shielded = True
        self.shield_timer = FPS * 3  # Shield lasts 3 seconds

