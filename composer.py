# composer.py

import pygame
from settings import *

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
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[5]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[6]].play()
                chord = {COMPOSER_KEY_BINDS_TYPES[0], COMPOSER_KEY_BINDS_TYPES[5], COMPOSER_KEY_BINDS_TYPES[6]}
                # self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[0])
                self.sequence_of_activated_abilities.append(chord)
        # Dash - 2
        if key == pygame.K_2:
            if self.use_energy(ABILITY_COSTS[2]):
                self.dancer.can_dash = True
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[1]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[4]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[6]].play()
                # self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[1])
                chord = {COMPOSER_KEY_BINDS_TYPES[1], COMPOSER_KEY_BINDS_TYPES[4], COMPOSER_KEY_BINDS_TYPES[6]}
                self.sequence_of_activated_abilities.append(chord)
        # Blink - 3
        if key == pygame.K_3:
            if self.use_energy(ABILITY_COSTS[3]):
                self.dancer.can_blink = True
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[2]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[4]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[6]].play()
                # self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[2])
                chord = {COMPOSER_KEY_BINDS_TYPES[2], COMPOSER_KEY_BINDS_TYPES[4], COMPOSER_KEY_BINDS_TYPES[6]}
                self.sequence_of_activated_abilities.append(chord)
        # Shield - 4
        if key == pygame.K_4:
            if self.use_energy(ABILITY_COSTS[4]):
                self.dancer.activate_shield()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[3]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[1]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[6]].play()
                # self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[3])
                chord = {COMPOSER_KEY_BINDS_TYPES[3], COMPOSER_KEY_BINDS_TYPES[1], COMPOSER_KEY_BINDS_TYPES[6]}
                self.sequence_of_activated_abilities.append(chord)
        # Magnet - 5
        if key == pygame.K_5:
            if self.use_energy(ABILITY_COSTS[4]):
                self.dancer.activate_magnet()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[5]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[1]].play()
                self.note_sounds[COMPOSER_KEY_BINDS_TYPES[3]].play()
                # self.sequence_of_activated_abilities.append(COMPOSER_KEY_BINDS[4])
                chord = {COMPOSER_KEY_BINDS_TYPES[5], COMPOSER_KEY_BINDS_TYPES[1], COMPOSER_KEY_BINDS_TYPES[3]}
                self.sequence_of_activated_abilities.append(chord)
        
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
        
        Draw's the progress bar and progress of the `dancer` relative to the level size
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
        
        # Draw progress bar (in relation of `dancer`s x position)
        progress_bar_x = 50  
        progress_bar_y = SCREEN_HEIGHT - 25   # Position will be near the bottom of the screen
        progress_bar_width = SCREEN_WIDTH - (2*progress_bar_x) # center the progress width relative to the screen width
        progress_bar_height = 20
        # make the full progress bar
        pygame.draw.rect(screen, PROGRESS_BAR_BACKGROUND_COLOR, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
        progress_ratio = self.dancer.rect.x / LEVEL_WIDTH
        current_progress_width = progress_ratio * progress_bar_width
        # current progress
        pygame.draw.rect(screen, PROGRESS_COLOR, (progress_bar_x, progress_bar_y, current_progress_width, progress_bar_height))
        percent_value = round(progress_ratio * 100, 2)
        percent_text = self.font.render(f'{max(percent_value, 0.00)}%', True, PERCENT_TEXT_COLOR)
        screen.blit(percent_text, (progress_bar_width / 2, progress_bar_y))    # center the % text
        
        # Draw key binds and cost
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
        Plays chord, and it will point to the next chord to be played.
        
        Note: needs to be in a while loop
        """
        size_of_activated_abilities = len(self.sequence_of_activated_abilities)
        
        if (size_of_activated_abilities <= 0):  # no abilities pressed, return
            return
                
        # Play chord/notes
        chord = self.sequence_of_activated_abilities[self.play_activated_abilities_note_at_index]
        for bind_type in chord: # bind type will be the ability type
            self.note_sounds[bind_type].play()  # play the associated sound with the ability
        
        if (self.play_activated_abilities_note_at_index == size_of_activated_abilities - 1):
            self.play_activated_abilities_note_at_index = 0    # replay the created music composition from the start, cycle
            return

        self.play_activated_abilities_note_at_index += 1    # play the next note in the sequence        
        pygame.time.wait(500)   # wait before going back/playing another note
        
        # # play note
        # key_bind_pressed = self.sequence_of_activated_abilities[self.play_activated_abilities_note_at_index]
        # self.note_sounds[COMPOSER_KEY_BINDS_TYPES[key_bind_pressed - 1]].play()
        # pygame.time.wait(500)   # wait before going back/playing another note
        # # check the note to play, 
        # if (self.play_activated_abilities_note_at_index == size_of_activated_abilities - 1):
        #     self.play_activated_abilities_note_at_index = 0    # replay the created music composition from the start, cycle
        #     return
        # self.play_activated_abilities_note_at_index += 1    # play the next note in the sequence        
        