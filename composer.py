# composer.py

import pygame
from settings import *

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

class Composer:
    def __init__(self, dancer=None):
        self.sound_energy = 100
        self.max_energy = 100
        self.font = pygame.font.Font(None, 24)  # For UI text
        self.dancer = dancer if dancer is not None else "NULL_DANCER"

        # Ability costs (`Key` is keyboard bind, `value` is ability cost)
        self.ability_costs = {
            COMPOSER_KEY_BINDS[0]: 10,  # Super Jump
            COMPOSER_KEY_BINDS[1]: 10,  # Dash
            COMPOSER_KEY_BINDS[2]: 15,  # Blink
            COMPOSER_KEY_BINDS[3]: 15,  # Shield
            COMPOSER_KEY_BINDS[4]: 10,  # Time slow
            COMPOSER_KEY_BINDS[5]: 10,  # Magnet
            COMPOSER_KEY_BINDS[6]: 10,  # Speeds up tempo
        }
        print(self.ability_costs)

    def use_energy(self, amount):
        if self.sound_energy >= amount:
            self.sound_energy -= amount
            return True
        return False

    def recharge(self, amount):
        self.sound_energy = min(self.sound_energy + amount, self.max_energy)

    def update(self, keys):
        self.handle_input(keys)

    def handle_input(self, keys, dancer):
        # Super Jump - 1
        if keys[pygame.K_1]:
            if self.use_energy(self.ability_costs[1]):
                dancer.super_jump = True
        # Dash - 2
        if keys[pygame.K_s]:
            if self.use_energy(self.ability_costs[2]):
                dancer.can_dash = True
        # Blink - 3
        if keys[pygame.K_3]:
            if self.use_energy(self.ability_costs[3]):
                dancer.blink = True
        # Shield - 4
        if keys[pygame.K_4]:
            if self.use_energy(self.ability_costs[4]):
                dancer.activate_shield = True
        # Time Slow - 5
        if keys[pygame.K_5]:
            if self.use_energy(self.ability_costs[5]):
                dancer.slow_time = True
        # Magnet - 6
        if keys[pygame.K_6]:
            if self.use_energy(self.ability_costs[6]):
                dancer.activate_magnet = True
        # Speeds up temp - 7
        if keys[pygame.K_7]:
            if self.use_energy(self.ability_costs[7]):
                dancer.speed_up_tempo = True

    def collect_notes(self, note_shards):
        collected = pygame.sprite.spritecollide(self.dancer, note_shards, True)
        if collected:
            for shard in collected:
                self.recharge(20)
                # Optionally, you might want to indicate the recharge visually

    def draw_ui(self, screen):
        # Draw sound energy meter
        energy_ratio = self.sound_energy / self.max_energy
        energy_bar_width = 200
        energy_bar_height = 20
        x = 10
        y = 10
        current_width = energy_bar_width * energy_ratio

        # Background bar
        pygame.draw.rect(screen, RED, (x, y, energy_bar_width, energy_bar_height))
        # Current energy
        pygame.draw.rect(screen, GREEN, (x, y, current_width, energy_bar_height))
        # Energy text
        energy_text = self.font.render(f'Energy: {int(self.sound_energy)}', True, WHITE)
        screen.blit(energy_text, (x, y + energy_bar_height + 5))
