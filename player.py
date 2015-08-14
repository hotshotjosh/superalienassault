"""
Player Module. Includes Player, Bullet, BulletCasing, Enemy classes
"""
import random
import pygame
from pygame.sprite import Sprite, Group
import constants
from spritesheet_functions import SpriteSheet

#Player Class
class Player(pygame.sprite.Sprite):

    # Set speed vector of player
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []

    # What direction is the player facing?
    direction = "R"
 
    # List of sprites we can bump against
    level = None
 
    # Methods
    def __init__(self, loc, bounds):
        
        # Call parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Player PNG
        sprite_sheet = SpriteSheet("p1_gunwalk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(64, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(128, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(192, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(256, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(320, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(640, 0, 64, 78)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(64, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(128, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(192, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(256, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(320, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(640, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
 
        # Reference the image rect.
        self.rect = self.image.get_rect()

        self.rect.center = loc
        self.bounds = bounds
        self.bullets = Group()
        self.bulletcasings = Group()
 
    # Move player
    def update(self):
        # Gravity
        self.calc_grav()

        # Left/Right Movement
        self.rect.x += self.change_x
        global world_shift_global
        global platform_list_global
        platform_list_global = self.level.platform_list
        world_shift_global = self.level.world_shift
        pos = self.rect.x + self.level.world_shift

        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # Did player hit a platform?
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Adjust player's position based on if they hit the left
            # or right side of the object
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Up/Down Movement
        self.rect.y += self.change_y

        # Did player hit a platform?
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Adjust player's position based on if they hit the top
            # or bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop vertical movement
            self.change_y = 0

        # Did player hit an enemy?
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Adjust player's position based on if they hit the top
            # or bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop vertical movement
            self.change_y = 0

    # Gravity
    def calc_grav(self):
        
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .33
 
        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    # Player Jump
    def jump(self):
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it's ok to jump, do it
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        # Player hits left arrow
        self.change_x = -7
        self.direction = "L"
 
    def go_right(self):
        # Player hits right arrow
        self.change_x = 7
        self.direction = "R"
 
    def stop(self):
        # Player stops hitting keys
        self.change_x = 0

    def shoot(self):
        if not self.alive():
            return
        shoot_sound = pygame.mixer.Sound("gunshot.ogg")

        bullet = Bullet(self.bounds, self.direction)
        bulletcasing = BulletCasing(self.bounds, self.direction)
        self.bullets.add(bullet)
        self.bulletcasings.add(bulletcasing)
        shoot_sound.play()

        if self.direction == "L":
            # recoil and bullet casing drop after a left shot
            self.change_x += (10 - self.change_x)*.1
            self.change_y += (-2 - self.change_y)*.9
            bullet.rect.x = self.rect.x -30
            bulletcasing.rect.x = self.rect.x +30
            bullet.rect.y = self.rect.centery -10
            bulletcasing.rect.y = self.rect.y +40
        else:
            # recoil and bullet casing drop after a right shot
            self.change_x += (10 - self.change_x)*-.1
            self.change_y += (-2 - self.change_y)*.9
            bullet.rect.x = self.rect.x +40
            bulletcasing.rect.x = self.rect.x +30
            bullet.rect.y = self.rect.centery -10
            bulletcasing.rect.y = self.rect.y +40

# Bullet class
class Bullet(Sprite):
    speed = 1
    accuracy = 1
    
    bullet_frames = []

    # Adding the direction argument took me entirely too long to figure out
    def __init__(self, bounds, direction): 
        # Bullet constructor.
        pygame.sprite.Sprite.__init__(self)

        self.direction = direction
        self.bounds = bounds

        # Add some random inaccuracy
        self.accuracy = random.randint(-1, 1)

        # Laser PNG
        sprite_sheet = SpriteSheet("laser.png")
        # Load all images into a list
        image = sprite_sheet.get_image(0, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(48, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(96, 0, 48, 46)
        self.bullet_frames.append(image)

        # Set the image the Bullet starts with
        self.image = self.bullet_frames[0]
 
        # Reference the image rect.
        self.rect = self.image.get_rect()

    # Bullet Direction and Speed
    def update(self):
        super().__init__()
        
        pos = self.rect.x
        # Attempt at gun flash using some more easing/tweening
        if self.direction == "L":
            pos = int(self.rect.x)
            frame = (pos // 30) % len(self.bullet_frames)
            frame += int((2 - frame)/.7)
            self.image = self.bullet_frames[frame]
        else:
            pos = int(self.rect.x)
            frame = (pos // 40) % len(self.bullet_frames)
            frame += int((2 - frame)/.7)
            self.image = self.bullet_frames[frame]

        self.rect.x += self.speed
        self.rect.y += self.accuracy
        pygame.sprite.Sprite.__init__(self)
        # Delete bullet if it's out of bounds
        if self.rect.x > 1000 or self.rect.x < -1000:
            self.kill()
        # Shoot bullet rightwards if that's the way the player is facing
        elif self.direction == "R":
            self.speed += (70 - self.speed)*.03
        # Otherwise, shoot left
        else:
            self.speed += (-70 - self.speed)*.03

# Bullet class
class BulletCasing(Sprite):
    speed = 1
    accuracy = -1

    # Set speed vector of casing
    change_x = 0
    change_y = 0

    # What direction is the casing 'facing'?
    direction = "L"

    # List of sprites we can bump against
    level = None

    # Adding the direction argument took me entirely too long to figure out
    def __init__(self, bounds, direction): 
        # Bullet constructor.
        pygame.sprite.Sprite.__init__(self)

        self.direction = direction
        self.bounds = bounds

        # Add some random inaccuracy
        self.accuracy = random.randint(-4, -1)

        # Casing PNG
        self.image = pygame.image.load("casing.png").convert()

        # Reference the image rect.
        self.rect = self.image.get_rect()

    # Bullet Direction and Speed
    def update(self):
        super().__init__()
        # Gravity
        self.calc_grav()
        
        pos = self.rect.x + world_shift_global
        self.rect.x += self.speed
        self.rect.y += self.accuracy
        pygame.sprite.Sprite.__init__(self)
        # Delete casing if it's out of bounds
        if self.rect.x > 1000 or self.rect.x < -1000:
            self.kill()
        # Shoot casing in the opposite direction the player is facing
        elif self.direction == "R":
            self.speed += (-3 - self.speed)*.03
        else:
            self.speed += (+3 - self.speed)*.03

        block_hit_list = pygame.sprite.spritecollide(self, platform_list_global, False)
        for block in block_hit_list:
            # Adjust casing's position based on if they hit the left
            # or right side of the object
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.direction = "L"
                self.change_x *= -1
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.direction = "R"
                self.change_x *= -1

        # Up/Down Movement
        self.rect.y += self.change_y
        if self.change_y < 1 and self.change_y > -1:
            self.change_x = 0

        # Did casing hit anything?
        block_hit_list = pygame.sprite.spritecollide(self, platform_list_global, False)
        for block in block_hit_list:

            # Adjust casing's position based on if they hit the top
            # or bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop vertical movement
            self.change_y = 0
            self.change_x = 0

    # Gravity
    def calc_grav(self):
        
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

#Enemy Class
class Enemy(pygame.sprite.Sprite):

    # Set speed vector of enemy
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our Enemy
    walking_frames_l = []
    walking_frames_r = []

    # What direction is the Enemy facing?
    direction = "L"
 
    # List of sprites we can bump against
    level = None
 
    # Methods
    def __init__(self, loc):
        
        # Call parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Enemy PNG
        sprite_sheet = SpriteSheet("e1_gunwalk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(64, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(128, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(192, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(256, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(320, 0, 64, 78)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(640, 0, 64, 78)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(64, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(128, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(192, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(256, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(320, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(640, 0, 64, 78)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the Enemy starts with
        self.image = self.walking_frames_r[0]
 
        # Reference the image rect.
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.change_x = -5
 
    # Move Enemy
    def update(self):
        # Gravity
        self.calc_grav()

        # Left/Right Movement adjusted for world shift
        self.rect.x += self.change_x
        pos = int(self.rect.x + world_shift_global)
        if self.direction == "L":
            if world_shift_global > 0:
                self.change_x = -5
            frame = (pos // 40) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
        elif self.direction == "R":
            if world_shift_global < 0:
                self.change_x = 5
            frame = (pos // 40) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        
        # Did enemy hit something?
        block_hit_list = pygame.sprite.spritecollide(self, platform_list_global, False)
        for block in block_hit_list:
            # Reverse direction
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.direction = "L"
                self.change_x *= -1
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.direction = "R"
                self.change_x *= -1

        # Up/Down Movement
        self.rect.y += self.change_y

        # Did Enemy hit anything?
        block_hit_list = pygame.sprite.spritecollide(self, platform_list_global, False)
        for block in block_hit_list:

            # Adjust Enemy's position based on if they hit the top
            # or bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop vertical movement
            self.change_y = 0

    # Gravity
    def calc_grav(self):
        
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height