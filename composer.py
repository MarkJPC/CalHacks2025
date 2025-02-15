# composer.py

import pygame
from settings import *

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

class Composer:
    def __init__(self):
        self.sound_energy = 100
        self.max_energy = 100
        self.font = pygame.font.Font(None, 24)  # For UI text

        # Ability costs
        self.ability_costs = {
            'A': 10,  # Super Jump
            'B': 10,  # Dash
            'C': 15,  # Blink
            'D': 15,  # Shield
            # Add other abilities as needed
        }

    def use_energy(self, amount):
        if self.sound_energy >= amount:
            self.sound_energy -= amount
            return True
        return False

    def recharge(self, amount):
        self.sound_energy = min(self.sound_energy + amount, self.max_energy)

    def update(self, keys, dancer):
        self.handle_input(keys, dancer)

    def handle_input(self, keys, dancer):
        # Super Jump - A
        if keys[pygame.K_a]:
            if self.use_energy(self.ability_costs['A']):
                dancer.super_jump()
        # Dash - B
        if keys[pygame.K_s]:
            if self.use_energy(self.ability_costs['B']):
                direction = 1 if keys[pygame.K_RIGHT] else -1
                dancer.dash(direction)
        # Shield - D
        if keys[pygame.K_f]:
            if self.use_energy(self.ability_costs['D']):
                dancer.activate_shield()
        # Implement other abilities similarly...

    def collect_notes(self, dancer, note_shards):
        collected = pygame.sprite.spritecollide(dancer, note_shards, True)
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
