import math
import pygame

# Draw text into the game
def draw_speech(screen, text, position_x, position_y, text_size, color):
    #
    font = pygame.font.Font('slkscr.ttf', text_size)
    text = font.render(text, True, color)

    screen.blit(text, (position_x, position_y))

# Calculates if player is near Isabel
def calculate_isabel_proximity(character_x, character_y, isabel_x, isabel_y):
    if character_x > isabel_x:
        x_proximity = character_x - isabel_x
    else:
        x_proximity = isabel_x - character_x
    x_range = 300
    y_range = 10

    if character_y > isabel_y:
        y_proximity = character_y - isabel_y
    else:
        y_proximity = isabel_y - character_y

    if x_proximity <= x_range and y_proximity <= y_range:
        return True
    else:
        return False
# Draw speech interaction between side character and player onto screen


def projectile_acceleration(projectile_speed, acceleration_factor):
    projectile_speed = projectile_speed * acceleration_factor

    return projectile_speed


def move_projectile(weapon_direc, weapon_x, projectile_speed):
    if weapon_direc == False:
        weapon_x -= projectile_speed
    elif weapon_direc == True:
        weapon_x += projectile_speed

    return weapon_x


def shoot_projectile(blit_weapon, got_staff, weapon, window, weapon_x, weapon_y):
    if blit_weapon == True and got_staff == True:
        weapon_rec = weapon.get_rect(topleft=(weapon_x, weapon_y))
        window.blit(weapon, weapon_rec)

def get_speech():
    isabel_speech = []
    isabel_speech.append('Hey Kid! Stop right there.')
    isabel_speech.append('Where are you headed? It\'s dangerous beyond here')
    isabel_speech.append('Wait...')
    isabel_speech.append('Are those... WINGS?')
    isabel_speech.append('How did a little kid like you get such a.. ')
    isabel_speech.append('Nevermind.  ')
    isabel_speech.append(' Kid are you seriously gonna head past here?')
    isabel_speech.append('Into the Mist Forest?')
    isabel_speech.append(' Kid are you seriously gonna head past here?')
    isabel_speech.append('How are you gonna defend yourself?')
    isabel_speech.append('Here take this atleast')
    isabel_speech.append('This weapon is a Ice blade staff')
    isabel_speech.append('It lets you shoot little magic ice daggers')
    isabel_speech.append('Press F to use it!')
    isabel_speech.append('Now get outta here!')


    return isabel_speech



def isabel_speech(window, isabel_interaction, position_x, position_y):

    speech = get_speech()
    index = isabel_interaction // 100
    if index >= len(speech):
        draw_speech(window, speech[-1], position_x-25, position_y+10, 25, (255, 97, 3))
    else:
        draw_speech(window, speech[index], position_x-25, position_y+10, 25, (255, 97, 3))

def draw_screen(window, background, grass, character_x, side_1_x, side_1_right, side_1_right_rec, side_1, side_1_rec, character, character_rec, text):
    window.blit(background, (0, 0))
    window.blit(grass, (0, 800))
    if character_x > side_1_x:
        window.blit(side_1_right, side_1_right_rec)
    else:
        window.blit(side_1, side_1_rec)
    window.blit(character, character_rec)
    window.blit(text, (800, 0))


def draw_forest(window, character, character_rec, night_background, night_grass, tree1,
                enemy1, enemy1_rec, enemy1_is_dead):

    window.blit(night_background, (0, 0))
    window.blit(night_grass, (0, 800))
    window.blit(tree1, (660, 340))
    window.blit(character, character_rec)
    if enemy1_is_dead == False:
        window.blit(enemy1, enemy1_rec)


def draw_forest2(window, character, character_rec, night_background, night_grass, tree1):
    window.blit(night_background, (0, 0))
    window.blit(night_grass, (0, 800))
    window.blit(tree1, (660, 340))
    window.blit(tree1, (120, 340))
    window.blit(tree1, (1020, 340))
    window.blit(character, character_rec)


def check_enemy1_range(character_y, stage_count):

    if character_y == 660 and stage_count == 1:
        # If character is in line with enemy1, shoot a projectile
        # at the character
        return True
    # Else do nothing
    return False


def check_enemy2_range(character_y, stage_count):
    if character_y < 50 and character_y > -50 and stage_count == 1:
        return True

    return False


def draw_enemy1_proj(window, enemy1_projectile_left, enemy1_proj_rec, enemy1_projectile_x,
                     enemy1_projectile_speed):

    enemy1_proj_rec = enemy1_projectile_left.get_rect(
        topleft=(enemy1_projectile_x, 700))
    enemy1_projectile_x -= enemy1_projectile_speed
    if enemy1_projectile_x < -250:
        enemy1_projectile_x = 1200
    window.blit(enemy1_projectile_left, enemy1_proj_rec)

    return enemy1_projectile_x


def draw_enemy2_proj(window, enemy2_projectile_left, enemy2_proj_rec, enemy2_projectile_x,
                     enemy2_projectile_speed):
    enemy2_proj_rec = enemy2_projectile_left.get_rect(
        topleft=(enemy2_projectile_x, 200))
    enemy2_projectile_x -= enemy2_projectile_speed
    if enemy2_projectile_x < -250:
        enemy2_projectile_x = 1200
    window.blit(enemy2_projectile_left, enemy2_proj_rec)

    return enemy2_projectile_x


def show_enemy_hp(window, enemy_health, high_hp, medium_hp, low_hp):
    if enemy_health == 3:
        window.blit(high_hp, (1200, 600))
    elif enemy_health == 2:
        window.blit(medium_hp, (1200, 600))
    elif enemy_health == 1:
        window.blit(low_hp, (1200, 600))


def show_enemy2_hp(window, enemy_health, high_hp, low_hp):
    if enemy_health == 2:
        window.blit(high_hp, (1230, -50))
    elif enemy_health == 1:
        window.blit(low_hp, (1230, -50))

def display_health(window, character_healthfull_sprite, character_health2_hearts_sprite,
                   character_Health1_heart_sprite, health):
    if health == 3:
        window.blit(character_healthfull_sprite, (-210, -170))
    elif health == 2:
        window.blit(character_health2_hearts_sprite, (-210, -170))
    elif health == 1:
        window.blit(character_Health1_heart_sprite, (-210, -170))