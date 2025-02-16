# dancer.py

import pygame
from settings import *
import math
from level import *

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Dancer(pygame.sprite.Sprite):

    # Initialize the dancer
    def __init__(self, pos, level=None):
        super().__init__()
        self.level = level if level is not None else "NULL_LEVEL"
        self.composer = ''
        self.image = pygame.Surface((40, 80), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        # # debug
        print(self.rect)
        # print(self.rect.x //2)
        # print(self.rect.y//2)
        # print(self.image.get_width() // 2)

        # health
        self.health = 100
        self.alive = True
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.on_moving_platform = None
        
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

        # animation
        self.animation_frame = 0  # Frame counter for animation
        self.animation_speed = 0.1  # Determines how fast the animation plays

        # Draw dancer
        self.draw_stick_figure()
        self.center_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        print("intitial pos:",self.center_pos)

    def apply_damage(self, damage):
        # Apply damage to the dancer
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def die(self):
        print("Dancer has died")

    def draw_stick_figure(self):
    # Clear surface
        self.image.fill((0, 0, 0, 0))
        # Draw stick figure parts
        self.center_x = self.image.get_width() // 2

        # Head
        pygame.draw.circle(self.image, WHITE, (self.center_x, 15), 10, 2)

        # Body
        pygame.draw.line(self.image, WHITE, (self.center_x, 25), (self.center_x, 55), 2)

        # Animation offsets
        leg_offset = math.sin(self.animation_frame) * 10
        arm_offset = math.sin(self.animation_frame + math.pi) * 10

        # Arms
        pygame.draw.line(self.image, WHITE, (self.center_x, 35),
                        (self.center_x - 15, 35 + arm_offset), 2)
        pygame.draw.line(self.image, WHITE, (self.center_x, 35),
                        (self.center_x + 15, 35 - arm_offset), 2)

        # Legs
        pygame.draw.line(self.image, WHITE, (self.center_x, 55),
                        (self.center_x - 10, 75 + leg_offset), 2)
        pygame.draw.line(self.image, WHITE, (self.center_x, 55),
                        (self.center_x + 10, 75 - leg_offset), 2)

        # Shield indicator with pulsating glow effect
        if self.shielded:
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5  # Value between 0 and 1
            for i in range(5):
                alpha = int(50 * (1 - (i / 5)) * pulse)
                glow_radius = 35 + (i * 5) + (pulse * 5)
                glow_surface = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (0, 0, 255, alpha), (self.center_x, 40), int(glow_radius))
                self.image.blit(glow_surface, (0, 0))

    def apply_gravity(self):
        self.velocity.y += 1  # Adjust gravity as needed

    def update(self, keys, platforms):
        """
        Updates the `dancer`, handles keyboard inputs, movments, and ability/buffing
        """
        # animation update
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2 * math.pi:
            self.animation_frame -= 2 * math.pi

        # Update animation frame only if moving
        if self.velocity.x != 0 or self.velocity.y != 0:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= 2 * math.pi:
                self.animation_frame -= 2 * math.pi
        else:
            self.animation_frame = 0  # Reset to starting position

        # Physical updates
        self.handle_input(keys)
        self.apply_gravity()
        self.rect.x += self.velocity.x
        self.check_collisions(X_AXIS, platforms)
        self.rect.y += self.velocity.y
        self.check_collisions(Y_AXIS, platforms)

        # Check if the magnet collects any `music shards`
        self.handle_magnet()
        
        # Update abilities
        self.update_ability_timers()

        # Redraw stick figure to update visuals (e.g., shield indicator)
        self.draw_stick_figure()

    def draw_health_bar(self, screen, camera):
        # Get the position of the dancer adjusted by the camera
        screen_rect = camera.apply(self)

        # Define health bar dimensions
        bar_width = 40
        bar_height = 5

        # Position the health bar above the dancer's sprite
        bar_x = screen_rect.x + self.image.get_width() // 2 - bar_width // 2
        bar_y = screen_rect.y - 10  # 10 pixels above the dancer

        # Calculate health ratio
        health_ratio = self.health / 100

        # Draw background bar (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Draw current health (green)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def check_shield_platforms(self, platforms):
        for platform in platforms:
            if isinstance(platform, ShieldPlatform):
                platform.check_hazard(self)
        
    def calc_magnitude(self, x, y):
        return math.sqrt(x**2 + y**2)

    def handle_magnet(self):
        if not self.enable_magnet:
            return
        
        if self.level != "NULL_LEVEL":
            for shard in self.level.note_shards:
                # print(shard.rect.x, shard.rect.y)  # Access position
                shard_vector_length = self.calc_magnitude(shard.rect.x, shard.rect.y)
                dancer_vector_length = self.calc_magnitude(self.rect.x, self.rect.y)
                
                # if the vector lengths is within `MAGNET_RANGE` -> collect the `shard`
                if (abs(shard_vector_length - dancer_vector_length) <= MAGNET_RANGE):
                    shard.kill()    # remove the `shard` as its colleted
                    self.composer.recharge(SHARD_RECHARGE_RATE)
                    print("removed shard at:", shard.rect.x, ", ", shard.rect.y)    # debug
                
    def handle_input(self, keys):
        """
        Handles key inputs and activates proper movement and associated abilities if they are active. 
        """
        self.velocity.x = 0

        if keys[pygame.K_LEFT]:
            self.velocity.x = -DANCER_SPEED
            self.direction.x = -1  

            # dash ability
            if (self.can_dash):
                self.dash()

            # Blink ability
            if self.can_blink:
                self.blink(X_AXIS)

        elif keys[pygame.K_RIGHT]:
            self.velocity.x = DANCER_SPEED
            self.direction.x = 1

            # dash ability
            if (self.can_dash):
                self.dash()

            # Blink ability
            if self.can_blink:
                self.blink(X_AXIS)
        else:
            # If not moving, reset velocity.x
            self.velocity.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            
            if self.can_blink:
                self.blink(Y_AXIS)
                self.velocity.y = -DANCER_JUMP_POWER
                
            if self.on_ground:
                if self.can_super_jump:
                    self.super_jump()
                else:
                    self.velocity.y = -DANCER_JUMP_POWER
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            
            if self.can_blink:
                self.blink(Y_AXIS)
        
        # update center pos
        self.center_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)

        # Check if the `dancer` exceeds the `level height`
        if (self.center_pos.y >= LEVEL_HEIGHT):
            print("EXCEEDED LOWER-HEIGHT. (kill dancer)")
            self.health = -1

    def check_collisions(self, axis, platforms):
        if axis == X_AXIS:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                for hit in hits:
                    if isinstance(hit, BlinkGate):
                        # Push the dancer off the BlinkGate
                        if self.velocity.x > 0:
                            self.rect.right = hit.rect.left
                        elif self.velocity.x < 0:
                            self.rect.left = hit.rect.right
                    else:
                        if self.velocity.x > 0:
                            self.rect.right = hit.rect.left
                        elif self.velocity.x < 0:
                            self.rect.left = hit.rect.right
        if axis == Y_AXIS:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                if self.velocity.y > 0:
                    self.rect.bottom = hits[0].rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                    # Check if standing on a moving platform
                    if isinstance(hits[0], MovingPlatform):
                        self.on_moving_platform = hits[0]
                    else:
                        self.on_moving_platform = None
                    if isinstance(hits[0], ShieldPlatform):
                        self.check_shield_platforms(platforms)

                if self.velocity.y < 0:
                    self.rect.top = hits[0].rect.bottom
                    self.velocity.y = 0
            else:
                self.on_ground = False
                self.on_moving_platform = None

            # If standing on a moving platform, move with it
            if self.on_moving_platform:
                # Move with the platform
                move_x = self.on_moving_platform.speed * self.on_moving_platform.direction
                self.rect.x += move_x

                # After moving, check for collisions in the X-axis
                hits = pygame.sprite.spritecollide(self, platforms, False)
                # Exclude the platform we're standing on
                hits = [hit for hit in hits if hit != self.on_moving_platform]
                if hits:
                    for hit in hits:
                        if isinstance(hit, BlinkGate):
                            # Collision with BlinkGate - push the dancer off the moving platform
                            # Adjust position to avoid overlap
                            if move_x > 0:
                                self.rect.right = hit.rect.left
                            elif move_x < 0:
                                self.rect.left = hit.rect.right
                            # Remove the dancer from the moving platform
                            self.on_moving_platform = None
                            self.on_ground = False  # Dancer is no longer on ground/platform
                            break
                        else:
                            # Handle collisions with other platforms if necessary
                            # Adjust position to avoid overlap
                            if move_x > 0:
                                self.rect.right = hit.rect.left
                            elif move_x < 0:
                                self.rect.left = hit.rect.right
                            # Optionally remove from moving platform
                            self.on_moving_platform = None
                            self.on_ground = False
                            break

    def update_ability_timers(self):
        """
        Decrements all timers by 1 second.
        
        Includes: `shield_timer` and `magnet_timer`
        """
        # Update shield timer
        if self.shielded:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shielded = False
        # Update magnet timer
        if self.enable_magnet:
            self.magnet_timer -= 1
            if self.magnet_timer <= 0:
                self.enable_magnet = False
    # Ability methods (skeletons)

    def super_jump(self):
        print("super jump")
        self.velocity.y = -DANCER_JUMP_POWER * 1.5
        self.can_super_jump = False

    def dash(self):
        """
        Dashes the `dancer` until it stops or hits a object.
        
        Sets:
        
        `can_dash` to `False`
        """
        # Direction: -1 for left, 1 for right
        steps = int(DASH_DISTANCE / DASH_SPEED)
        for _ in range(steps):
            # Move the dancer incrementally
            self.rect.x += DASH_SPEED * self.direction.x
            # Check for collisions
            if self.check_collisions(X_AXIS, self.level.platforms):
                # Collision occurred; stop the dash
                break
        self.can_dash = False
        # pass

    def blink(self, axis):
        """
        Blinks along the entered axis (x or y axis).
        
        Blink can go through walls along the x-axis but not the y-axis.
        
        Sets:

        `can_blink` to `False` after call. 
        """  
        # Blink along the x-direction
        if (axis == X_AXIS):
            if (not self.check_collisions(X_AXIS, self.level.platforms)):
                self.rect.x += BLINK_DISTANCE_ALONG_X * self.direction.x
                # print("blink on x:", int(BLINK_DISTANCE) * self.direction.x) # debug

        # Blink along the y-direction
        elif (axis == Y_AXIS):
            if (not self.check_collisions(Y_AXIS, self.level.platforms)):
                self.rect.y += BLINK_DISTANCE_ALONG_Y * self.direction.y        
                # print("blink on y:", int(BLINK_DISTANCE_ALONG_Y) * self.direction.y) # debug        
        self.can_blink = False

    def activate_shield(self):
        print("shield activated..")
        # Activate shield and set timer
        self.shielded = True
        self.shield_timer = FPS * SHIELD_DURATION  # Shield lasts 3 seconds (default)

    def activate_magnet(self):
        print("magnet activated..")
        self.enable_magnet = True
        self.magnet_timer = FPS * MAGNET_DURATION # magnet lasts 3 seconds (default)
        
    # Additional methods for other abilities can be added here
