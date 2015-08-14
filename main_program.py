"""
FINAL LAB Josh Thomas
'Super Alien Assault' *
programarcadegames.com
Game Art provided by Kenney @ http://kenney.nl
Soundtrack provided by Beardmont @ https://soundcloud.com/beardmont
"""
import random

import pygame
from pygame.sprite import Group, GroupSingle, groupcollide
import constants
import levels
from player import Player
from player import Enemy

def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    bounds = screen.get_rect()
    pygame.display.set_caption("Super Alien Assault!")
 
    # Load the sound mixer:
    pygame.mixer.pre_init(44100, -16, 2, 2048) 
    # This is supposed to help stop sound lag
 
    # Create the player
    player = Player(bounds.center, bounds)
    player_grp = GroupSingle(player)

    # Create an enemy
    enemies = pygame.sprite.Group()
 
    # Create all the levels
    lindex = random.randrange(3,9)

    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))
    level_list.append(levels.Level_03(player))
    for i in range(lindex):
        level_list.append(levels.Level_01(player))
        level_list.append(levels.Level_02(player))
        level_list.append(levels.Level_03(player))

    # Initialize variables
    score = 0
    spawn_counter = 0
    tween_diff = 1

    # Select the font to use
    font = pygame.font.SysFont("calibri",48)
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # List of each block
    block_list = pygame.sprite.Group()

    # Set current level for player and inital x,y position
    player.level = current_level
    player.rect.x = 340
    player.rect.y = 200
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Play "Hot Nights" by Beardmont / Three Chain Links
    # Available under Creative Commons attribution license from:
    # https://soundcloud.com/beardmont
    pygame.mixer.music.load('HotNights.ogg')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()

 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.constants.USEREVENT:
            # This event is triggered when the song stops playing.
            #
            # Next, play "Happiest Days" by Beardmont / Three Chain Links
            # Available under Creative Commons attribution license from:
            # https://soundcloud.com/beardmont
                pygame.mixer.music.load('HappiestDays.ogg')
                pygame.mixer.music.play()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_q:
                    done = True
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_r and not player.alive():
                    main()
 
            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update items in the level
        current_level.update()
        player_grp.update()
        player.bullets.update()
        player.bulletcasings.update()
        enemies.update()

        # Messing around with easing the enemy spawn counter
        # They should gradually trickle in at first and then build
        # to a flood of enemies then recede kind of like a tide
        spawn_counter += (101 - spawn_counter)*.1
        if spawn_counter >= 100:
            n = random.randrange(3)
            for i in range(n):
                x = random.randint(900, 1000)
                y = random.randint(100, 520)
                enemy = Enemy((x, y))
                enemies.add(enemy)
            spawn_counter = 0

        # Collision between player and enemies results in player death
        groupcollide(player_grp, enemies, True, False)

        # Add 1 point to score for every enemy the player kills
        for enemy in groupcollide(enemies, player.bullets, True, True):
            if player.alive():
                score += 1

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 310:
            diff = player.rect.x - 310
            # add some tweening/easing for momentum
            tween_diff += (diff - tween_diff)*.1
            player.rect.x = 310
            current_level.shift_world(int(-tween_diff))
            # also adjust enemies and bulletcasings by the world shift
            for enemy in enemies:
                enemy.rect.x += (int(-tween_diff))
            for bulletcasing in player.bulletcasings:
                bulletcasing.rect.x += (int(-tween_diff))


        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 290:
            diff = 290 - player.rect.x
            # add some tweening/easing for momentum
            tween_diff += (diff - tween_diff)*.1
            player.rect.x = 290
            current_level.shift_world(int(tween_diff))
            # also adjust enemies and bulletcasings by the world shift
            for enemy in enemies:
                enemy.rect.x += (int(tween_diff))
            for bulletcasing in player.bulletcasings:
                bulletcasing.rect.x += (int(tween_diff))

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        player_grp.draw(screen)
        player.bullets.draw(screen)
        player.bulletcasings.draw(screen)
        enemies.draw(screen)

        # Blit the current score
        score_text = font.render("Score: %08d"%score, True, constants.PEACH)
        screen.blit(score_text, (5,5))

        # If player dies, blit the respawn menu
        if not player.alive():
            gameover = font.render("Press R to Respawn or ESC to Quit", True, constants.PEACH)
            rect = gameover.get_rect()
            rect.center = screen.get_rect().center
            screen.blit(gameover, rect)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()
