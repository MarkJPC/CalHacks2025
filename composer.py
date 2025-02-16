# composer.py

import pygame
from settings import *

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (122, 122, 122)

class Composer:
    def __init__(self, dancer=None, level=None):
        self.level = level
        self.sound_energy = 100
        self.max_energy = 100
        self.font = pygame.font.Font(None, 24)  # For UI text
        self.dancer = dancer if dancer is not None else "NULL_DANCER"
        self.level = level if level is not None else "NULL_LEVEL"
        self.sequence_of_activated_abilities = [] # records the keys pressed (the key bind for each ability)
        
        # Load note sounds
        self.note_sounds = {
            'super_jump': pygame.mixer.Sound('assets/sounds/note_A.wav'),
            'dash': pygame.mixer.Sound('assets/sounds/note_B.wav'),
            'blink': pygame.mixer.Sound('assets/sounds/note_C.wav'),
            'shield': pygame.mixer.Sound('assets/sounds/note_D.wav'),
            'time_slow': pygame.mixer.Sound('assets/sounds/note_E.wav'),
            'magnet': pygame.mixer.Sound('assets/sounds/note_F.wav'),
            'speed_up_tempo': pygame.mixer.Sound('assets/sounds/note_G.wav'),
        }
        
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

    def use_energy(self, amount):
        if self.sound_energy >= amount:
            self.sound_energy -= amount
            return True
        return False

    def recharge(self, amount):
        self.sound_energy = min(self.sound_energy + amount, self.max_energy)

    def update(self, keys):
        #self.handle_input(keys)
        pass

    def handle_keydown(self, key):
        # Super jump - 1
        if key == pygame.K_1:
            if self.use_energy(self.ability_costs[1]):
                self.dancer.can_super_jump = True
                self.note_sounds['super_jump'].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[0])
        # Dash - 2
        if key == pygame.K_2:
            if self.use_energy(self.ability_costs[2]):
                self.dancer.can_dash = True
                self.note_sounds['dash'].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[1])
        # Blink - 3
        if key == pygame.K_3:
            if self.use_energy(self.ability_costs[3]):
                self.dancer.can_blink = True
                self.note_sounds['blink'].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[2])
        # Shield - 4
        if key == pygame.K_4:
            if self.use_energy(self.ability_costs[4]):
                self.dancer.activate_shield()
                self.note_sounds['shield'].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[3])
        # Magnet - 6
        if key == pygame.K_6:
            if self.use_energy(self.ability_costs[5]):
                self.dancer.activate_magnet()
                self.note_sounds['magnet'].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[5])

        print(self.sequence_of_activated_abilities)
        # LEVEL WIDE AFFECTS
        # # Speeds up tempo - 7
        # if key == pygame.K_7:
        #     if self.use_energy(self.ability_costs[7]):
        #         self.dancer.speed_up_tempo = True
        # # Time Slow - 5
        # if key == pygame.K_5:
        #     if self.use_energy(self.ability_costs[5]):
        #         self.dancer.slow_time = True
        
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
        energy_text = self.font.render(f'Tempo: {int(self.sound_energy)}', True, WHITE)
        energy_text_x = x
        energy_text_y = y + energy_bar_height + 5
        screen.blit(energy_text, (energy_text_x, energy_text_y))
        
        # Draw key binds
        key_bind_text_x = x
        key_bind_text_y = energy_text_y + 30
        key_bind_text = self.font.render('--Ability Keybinds--', True, WHITE)
        screen.blit(key_bind_text, (key_bind_text_x, key_bind_text_y)) # draw the text at `x` and `y` locations
        
        offset_amount = 20
        key_bind_text_offset = key_bind_text_y + offset_amount
        counter = 0
        for key_bind, bind_type in zip(COMPOSER_KEY_BINDS, COMPOSER_KEY_BINDS_TYPES):
            key_bind_text = ''
            # check if the ability was implmented
            if (bind_type != COMPOSER_KEY_BINDS_TYPES[4] and bind_type != COMPOSER_KEY_BINDS_TYPES[6]):
                key_bind_type = self.font.render(f'{key_bind}: {bind_type}', True, WHITE)
            # not implemented yet
            else:
                key_bind_type = self.font.render(f'{key_bind}: {bind_type} [COMING SOON]', True, GRAY)
            screen.blit(key_bind_type, (key_bind_text_x, key_bind_text_offset))
            key_bind_text_offset += offset_amount
            counter += 1
    
    def play_composed_music(self):
        for key_bind_pressed in self.sequence_of_activated_abilities:
            self.note_sounds[COMPOSER_KEY_BINDS_TYPES[key_bind_pressed - 1]].play()
        print("Playing composed music")


# composer.play_composed_music()  # play the composed song from the abilities activated
