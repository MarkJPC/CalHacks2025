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
        self.play_activated_abilities_note_at_index = 0
        
        # Load note sounds
        self.note_sounds = {
            COMPOSER_KEY_BINDS_TYPES[0]: pygame.mixer.Sound('assets/sounds/note_A.wav'),
            COMPOSER_KEY_BINDS_TYPES[1]: pygame.mixer.Sound('assets/sounds/note_B.wav'),
            COMPOSER_KEY_BINDS_TYPES[2]: pygame.mixer.Sound('assets/sounds/note_C.wav'),
            COMPOSER_KEY_BINDS_TYPES[3]: pygame.mixer.Sound('assets/sounds/note_D.wav'),
            COMPOSER_KEY_BINDS_TYPES[4]: pygame.mixer.Sound('assets/sounds/note_E.wav'),
            COMPOSER_KEY_BINDS_TYPES[5]: pygame.mixer.Sound('assets/sounds/note_F.wav'),
            COMPOSER_KEY_BINDS_TYPES[6]: pygame.mixer.Sound('assets/sounds/note_G.wav'),
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
            if self.use_energy(ABILITY_COSTS[1]):
                self.dancer.can_super_jump = True
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[0]].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[0])
        # Dash - 2
        if key == pygame.K_2:
            if self.use_energy(ABILITY_COSTS[2]):
                self.dancer.can_dash = True
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[1]].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[1])
        # Blink - 3
        if key == pygame.K_3:
            if self.use_energy(ABILITY_COSTS[3]):
                self.dancer.can_blink = True
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[2]].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[2])
        # Shield - 4
        if key == pygame.K_4:
            if self.use_energy(ABILITY_COSTS[4]):
                self.dancer.activate_shield()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[3]].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[3])
        # Magnet - 5
        if key == pygame.K_5:
            if self.use_energy(ABILITY_COSTS[4]):
                self.dancer.activate_magnet()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[5]].play()
                self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[4])

        print(self.sequence_of_activated_abilities)
        # LEVEL WIDE AFFECTS
        # # Speeds up tempo - 7
        # if key == pygame.K_7:
        #     if self.use_energy(ABILITY_COSTS[7]):
        #         self.dancer.speed_up_tempo = True
        # # Time Slow - 6
        # if key == pygame.K_6:
        #     if self.use_energy(ABILITY_COSTS[6]):
        #         self.dancer.slow_time = True
        
    def draw_ui(self, screen):
        """
        Draw's sound energy meter (tempo meter)
        
        Draw's the key bindings for abilities and costs
        """
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
        key_bind_text = self.font.render('--Ability Keybinds | Cost--', True, WHITE)
        screen.blit(key_bind_text, (key_bind_text_x, key_bind_text_y)) # draw the text at `x` and `y` locations
        
        offset_amount = 20
        key_bind_text_offset = key_bind_text_y + offset_amount
        counter = 0
        for key_bind, bind_type in zip(COMPOSER_KEY_BINDS, COMPOSER_KEY_BINDS_TYPES):
            key_bind_text = ''
            # check if the ability was implmented
            if (bind_type != COMPOSER_KEY_BINDS_TYPES[5] and bind_type != COMPOSER_KEY_BINDS_TYPES[6]):
                key_bind_type = self.font.render(f'{key_bind}: {bind_type} | {ABILITY_COSTS[key_bind]}', True, WHITE)
            # not implemented yet
            else:
                key_bind_type = self.font.render(f'{key_bind}: {bind_type} [COMING SOON]', True, GRAY)
            screen.blit(key_bind_type, (key_bind_text_x, key_bind_text_offset))
            key_bind_text_offset += offset_amount
            counter += 1
    
    def play_composed_music(self):
        """
        Plays one note, and it will point to the next note to be played.
        
        Note: needs to be in a while loop
        """
        size_of_activated_abilities = len(self.sequence_of_activated_abilities)
        
        if (size_of_activated_abilities <= 0):  # no abilities pressed, return
            return

        # play note
        key_bind_pressed = self.sequence_of_activated_abilities[self.play_activated_abilities_note_at_index]
        self.note_sounds[COMPOSER_KEY_BINDS_TYPES[key_bind_pressed - 1]].play()
        pygame.time.wait(500)   # wait before going back/playing another note
        # check the note to play, 
        if (self.play_activated_abilities_note_at_index == size_of_activated_abilities - 1):
            self.play_activated_abilities_note_at_index = 0    # replay the created music composition from the start, cycle
            return
        self.play_activated_abilities_note_at_index += 1    # play the next note in the sequence        
        
    # def play_composed_music_PRIVATE(self):
    #     key_bind_pressed = self.sequence_of_activated_abilities[self.play_activated_abilities_note_at_index]
    #     self.note_sounds[COMPOSER_KEY_BINDS_TYPES[key_bind_pressed - 1]].play()
    #     pygame.time.wait(500)   # wait before going back/playing another note
    #     if (self.play_activated_abilities_note_at_index == len(self.sequence_of_activated_abilities) - 1):
    #         self.play_activated_abilities_note_at_index = 0    # replay from the start the created music composition
    #         return
    #     self.play_activated_abilities_note_at_index += 1    # play the next note in the sequence
        
    #     # for key_bind_pressed in self.sequence_of_activated_abilities:
    #     #     self.note_sounds[COMPOSER_KEY_BINDS_TYPES[key_bind_pressed - 1]].play()
    #     #     pygame.time.wait(1000)
