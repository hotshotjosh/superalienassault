"""
Level Module.
"""
import random
import pygame
import constants
from player import Enemy

class Platform(pygame.sprite.Sprite):
 
    def __init__(self, width, height):
        # Platform constructor.
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLUEGREEN)
        self.rect = self.image.get_rect()

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. 
    """

    platform_list = None
    background = None
    world_shift = 0
    global x
    x = 0
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.player = player
 
    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        global x

        x = (self.world_shift // 3) # +1
        if x == constants.SCREEN_WIDTH:
            x = 0

        screen.fill(constants.GREYGREEN)
        screen.blit(self.background, (x, 0))
        screen.blit(self.background2,(x + constants.SCREEN_WIDTH -25, 0))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)

        # Use repeating background
        self.background = pygame.image.load("background.png").convert()
        self.background2 = pygame.image.load("background.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.background2.set_colorkey(constants.WHITE)
        self.level_limit = -1500
        # Add random factor for level generation, so each playthrough
        # is different
        xbump = 500+random.randint(-50,50)
        ybump = -100+random.randint(-50,50)
 
        # Array with width, height, x, and y of platform
        level = [[50, 450, 200, 0],
                 [50, 200, 50, 400],
                 [200, 50, 50, 400],
                 [200, 50, 750, 450],
                 [150, 50, 550, 250],
                 [200, 50, 1050, 320],
                 [50, 200, 1200, 320],
                 [210, 30, 450+xbump, 570+ybump],
                 [210, 30, 850+xbump, 420+ybump],
                 [210, 30, 1000+xbump, 520+ybump],
                 [210, 30, 1120+xbump, 280+ybump],
                 [210, 30, 450+xbump*2, 570+ybump],
                 [210, 30, 850+xbump*2, 420+ybump],
                 [210, 30, 1000+xbump*2, 520+ybump],
                 [210, 30, 1120+xbump*2, 280+ybump],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 2. """
 
        # Call the parent constructor
        Level.__init__(self, player)

        # Scrolling repeating background so we don't have to upload a huge png
        self.background = pygame.image.load("background2.png").convert()
        self.background2 = pygame.image.load("background2.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.background2.set_colorkey(constants.WHITE)
        # Add random factor for level generation, so each playthrough
        # is different
        self.level_limit = -1500
        xbump = 520 +random.randint(-50,50)
        ybump = -120 +random.randint(-50,50)
 
        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 [50, 450, 200, 0],
                 [50, 200, 50, 100],
                 [200, 50, 50, 200],
                 [200, 50, 750, 450],
                 [150, 50, 550, 250],
                 [200, 50, 1050, 320],
                 [50, 280, 1200, 320],
                 [210, 30, 450+xbump, 570+ybump],
                 [210, 30, 850+xbump, 420+ybump],
                 [210, 30, 1000+xbump, 520+ybump],
                 [210, 30, 1120+xbump, 280+ybump],
                 [210, 30, 450+xbump*2, 570+ybump],
                 [210, 30, 850+xbump*2, 420+ybump],
                 [210, 30, 1000+xbump*2, 520+ybump],
                 [210, 30, 1120+xbump*2, 280+ybump],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Level_03(Level):
    """ Definition for level 3. """
 
    def __init__(self, player):
        """ Create level 3. """
 
        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background3.png").convert()
        self.background2 = pygame.image.load("background3.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.background2.set_colorkey(constants.WHITE)
        self.level_limit = -1500
        # Add random factor for level generation, so each playthrough
        # is different
        self.level_limit = -1500
        xbump = 480 +random.randint(-50,50)
        ybump = -80 +random.randint(-50,50)
 
        # Array with width, height, x, and y of platform
        level = [[50, 350, 200, 0],
                 [50, 200, 50, 400],
                 [200, 50, 50, 400],
                 [200, 50, 750, 450],
                 [150, 50, 550+xbump, 250+ybump],
                 [200, 50, 1050+xbump, 320+ybump],
                 [50, 200, 1200+xbump, 320+ybump],
                 [210, 30, 450+xbump, 570+ybump],
                 [210, 30, 850+xbump, 420+ybump],
                 [210, 30, 1000+xbump, 520+ybump],
                 [210, 30, 1120+xbump, 280+ybump],
                 [210, 30, 450+xbump*2, 570+ybump],
                 [210, 30, 850+xbump*2, 420+ybump],
                 [210, 30, 1000+xbump*2, 520+ybump],
                 [210, 30, 1120+xbump*2, 280+ybump],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)