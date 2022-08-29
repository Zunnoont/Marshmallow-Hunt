import math
from multiprocessing.reduction import send_handle
from re import L
import pygame
import helpers
import storage
from player import Player, Player_proj
from enemies import Enemy1, Enemy1_proj, Enemy2, Enemy2_proj, Enemy3, Enemy4, Enemy5, EnemyArcher, EnemyArcher_Projectile, Large_slime, Wizard1

pygame.init()
clock = pygame.time.Clock()
class Title(pygame.sprite.Sprite):
    def __init__(self):
        self.logo_frames = [pygame.image.load('assets/Logo_Frames/logo1.png').convert_alpha(),
                            pygame.image.load('assets/Logo_Frames/logo2.png').convert_alpha(),
                            pygame.image.load('assets/Logo_Frames/logo3.png').convert_alpha(),
                            pygame.image.load('assets/Logo_Frames/logo4.png').convert_alpha(),
                            pygame.image.load('assets/Logo_Frames/logo5.png').convert_alpha()]
        self.image = self.logo_frames[0]
        self.curr_frame = 0
        self.start_game = False
    def title_animation(self):
        if self.curr_frame >= 5:
            self.curr_frame = 0
        else:
            self.image = self.logo_frames[math.floor(self.curr_frame)]
        self.curr_frame += 0.09

class Isabel(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('assets/Isabel_final_idle1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(1100, 627))
        self.curr_sprite = 0
        self.x_range = 300
        self.x_proximity = 1080
        self.interaction = 0
        self.near_player = False
        self.pressed_enter = False
        self.facing_left = True
        self.sprites_left = [pygame.image.load('assets/isabel_final_idle_fr1_left.png').convert_alpha(),
                             pygame.image.load('assets/isabel_final_idle_fr2_left.png').convert_alpha()]
        self.sprites_right = [pygame.image.load('assets/isabel_final_idle_fr1.png').convert_alpha(),
                              pygame.image.load('assets/isabel_final_idle_fr2.png').convert_alpha()]
    def update(self, player_x):
        self.curr_sprite += 0.025
        if player_x > self.rect.x:
            self.facing_left = False
            if self.curr_sprite >= len(self.sprites_right):
                self.curr_sprite = 0
            self.image = self.sprites_right[int(self.curr_sprite)]
        else:
            self.facing_left = True
            if self.curr_sprite >= len(self.sprites_left):
                self.curr_sprite = 0
            self.image = self.sprites_left[int(self.curr_sprite)]
    def check_if_near_player(self, character_x, is_player_in_air):
        if character_x > self.rect.x:
            self.x_proximity = character_x - self.rect.x
        else:
            self.x_proximity = self.rect.x - character_x
        if self.x_proximity <= self.x_range and is_player_in_air is False:
            self.near_player = True
        else:
            self.near_player = False
    def talk_to_isabel(self, window, stage_count, key_list, text_box):
        if self.near_player is True and stage_count == 0 and self.pressed_enter is True:
            if key_list[pygame.K_RIGHT] == 1:
                self.interaction += 100
            helpers.isabel_speech(window, self.interaction,
                          self.rect.x, self.rect.y, text_box)
            speech = helpers.get_speech()
            if (self.interaction // 100) < len(speech):
                self.interaction += 1
        elif self.near_player is True and self.pressed_enter is False and stage_count == 0:
            if self.facing_left is True:
                helpers.draw_speech(window, "Press [T] to talk", 1265, 827, 20, 'white')
            else:
                helpers.draw_speech(window, "Press [T] to talk", 1150, 827, 20, 'white')

class Heart_container(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        self.sprites = []
        self.sprites.append(pygame.image.load('assets/heart_container_frame2.png').convert_alpha())
        self.sprites.append(pygame.image.load('assets/heart_container_frame1.png').convert_alpha())
        self.sprites.append(pygame.image.load('assets/heart_container_frame3.png').convert_alpha())
        self.curr_sprite = 0
        self.image = self.sprites[self.curr_sprite]
        self.blit_image = True
        self.rect = self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.curr_sprite += 0.1
        if self.curr_sprite >= len(self.sprites):
            self.curr_sprite = 0
        self.image = self.sprites[int(self.curr_sprite)]

class Campfire(pygame.sprite.Sprite):
    def __init__(self):
        self.campfire_sprites = [pygame.image.load('assets/Campfire/campfire_v1.png').convert_alpha(),
                pygame.image.load('assets/Campfire/campfire_v2.png').convert_alpha(),
                pygame.image.load('assets/Campfire/campfire_v3.png').convert_alpha()]
        self.curr_sprite = 0
        self.image = self.campfire_sprites[self.curr_sprite]

    def update(self):
        self.curr_sprite += 0.1
        if self.curr_sprite >= len(self.campfire_sprites):
            self.curr_sprite = 0
        self.image = self.campfire_sprites[int(self.curr_sprite)]

# Main function of Wing It!
def main():
    # Pygame Window
    x_position = -20
    y_position = 588
    window = pygame.display.set_mode((1920, 1060))
    window.fill(('White'))

    # Game name
    pygame.display.set_caption('Marshmallow Hunt')

    # Character Sprites
    character = pygame.image.load('assets/main_sitting_f1.png').convert_alpha()
    player = Player(character, x_position, y_position)

    # Backgrounds
    title = Title()
    grass = pygame.image.load('assets/grass_v1.png').convert()
    background = pygame.image.load('assets/night_sky_V1.png').convert()
    night_background = pygame.image.load('assets/night_sky_V1.png').convert()
    night_grass = pygame.image.load('assets/grass_v1.png').convert()
    tree1 = pygame.image.load('assets/tree1.png').convert_alpha()
    stage3_grass =  pygame.image.load('assets/autumn_grass_first.png').convert_alpha()
    pillar = pygame.image.load('assets/pillar.png').convert_alpha()
    rock = pygame.image.load('assets/rock.png').convert_alpha()
    tree2 = pygame.image.load('assets/tree2.png').convert_alpha()
    text_box = pygame.image.load('assets/text_box_npc.png').convert_alpha()
    campfire = Campfire()
    tree_stump = pygame.image.load('assets/tree_stump.png').convert_alpha()

    # Side character_1
    isabel = Isabel()

    # Enemy 1
    enemy1 = Enemy1()
    enemy1.rect = enemy1.image.get_rect(topleft=(1100, 440))
    enemy1_projectile_x = 1100
    # Enemy 1's projectile
    enemy1_proj = Enemy1_proj(enemy1_projectile_x)

    enemy_high_hp = pygame.image.load('assets/healthbar_high.png').convert_alpha()
    enemy_medium_hp = pygame.image.load('assets/healthbar_medium.png').convert_alpha()
    enemy_low_hp = pygame.image.load('assets/healthbar_low.png').convert_alpha()
    # Enemy 2:
    enemy2 = Enemy2()
    enemy2_projectile_x = 1100
    enemy2_proj = Enemy2_proj(enemy2_projectile_x)

    # Enemy 3-5: Slimes:
    enemy3 = Enemy3(1040)
    enemy4 = Enemy4(1040)
    enemy5 = Enemy5(1040)
    wizard1 = Wizard1(650, 670)

    #Enemy archer:
    archer = EnemyArcher()
    archer_arrow = EnemyArcher_Projectile()
    # Large slime miniboss

    large_slime = Large_slime(1200)

    heart_container1  = Heart_container(485, 60)

    # weapon_particle
    weapon = pygame.image.load('assets/particle_effect.png').convert_alpha()
    weapon_x = 0
    weapon_y = 0

    player_proj = Player_proj(weapon, weapon_x, weapon_y)

    run_program = True
    stage_count = 0
    # Program game loop
    while run_program is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # List of keys pressed by user
        key_list = pygame.key.get_pressed()

        # Change stage
        if player.rect.x > 1920 and player.in_bossfight is False:
            stage_count += 1
            player.rect.x = -200
        elif player.rect.x < -300 and player.in_bossfight is False:
            stage_count -= 1
            player.rect.x = 1900

        # Stages
        if title.start_game is False:
            player.health = -1
            key_list = pygame.key.get_pressed()
            helpers.draw_screen(window, background, grass, isabel.image, isabel.rect, player.character, player.rect,
                        rock, tree2, campfire.image, tree_stump)
            campfire.update()
            isabel.update(player.rect.x)
            player.update_idle_animation()
            window.blit(title.image, (420, -150))
            title.title_animation()

            # If key_list contains 1, a key was pressed
            # as 1 represents pressed while 0 represents
            # not pressed
            if 1 in key_list:
                title.start_game = True
                player.health = 3

        elif stage_count == 0:
            helpers.draw_screen(window, background, grass, isabel.image, isabel.rect, player.character, player.rect,
                        rock, tree2, campfire.image, tree_stump)
            isabel.update(player.rect.x)
            is_near_stump = helpers.check_if_near_stump(window, player)
            if is_near_stump is True and key_list[pygame.K_s] == 1:
                player.is_sitting = True
                player.rect.x = -20
                player.rect.y = 588
            campfire.update()
            isabel.check_if_near_player(player.rect.x, player.in_air)
            if key_list[pygame.K_t] == 1 and isabel.near_player is True:
                isabel.pressed_enter = True
        elif stage_count == 1:
            helpers.draw_forest(window, player.character, player.rect, night_background,
                        night_grass, tree1, enemy1.image, enemy1.rect, enemy1.is_dead, archer)

            helpers.show_enemy_hp(window, enemy1.health, enemy_high_hp,
                          enemy_medium_hp, enemy_low_hp)

            helpers.show_enemy2_hp(window, enemy2.health, enemy_high_hp, enemy_low_hp)

            enemy1.update()
            if enemy2.is_dead is False:
                window.blit(enemy2.image, enemy2.rect)
            if archer.is_alive is True and enemy1.is_dead is True:
                archer.idle_anim()
                archer.update_infinity_frames()
                archer.show_hp(window, enemy_high_hp, enemy_medium_hp, enemy_low_hp)
                if player.in_air is False:
                    archer.attack_anim()

        elif stage_count == 2:
            player.rect = player.character.get_rect(
                topleft=(player.rect.x, player.rect.y))
            helpers.draw_forest2(window, player.character, player.rect,
                         night_background, night_grass, tree1)
            if enemy3.is_offscreen is False:
                window.blit(enemy3.image, enemy3.rect)
                enemy3.move_jumping_slime()
                player = helpers.check_for_slime_collission(player, enemy3)
            elif enemy3.is_offscreen is True and enemy4.is_offscreen is False:
                window.blit(enemy4.image, enemy4.rect)
                enemy4.move_jumping_slime_green()
                player = helpers.check_for_slime_collission(player, enemy4)
            elif enemy4.is_offscreen is True and enemy5.is_offscreen is False:
                window.blit(enemy5.image, enemy5.rect)
                enemy5.move_jumping_slime_red()
                player = helpers.check_for_slime_collission(player, enemy5)
            elif enemy5.is_offscreen is True:
                window.blit(large_slime.image, large_slime.rect)
                large_slime.move_jumping_slime_purple()
                player = helpers.check_for_slime_collission(player, large_slime)
        elif stage_count == 3:
            helpers.draw_stage4(window, player.character, player.rect, night_background, night_grass)
            window.blit(wizard1.image, wizard1.rect)
            wizard1.update(player.rect.x)
            if player.rect.x > 1900:
                player.in_bossfight = True
                wizard1.in_bossfight = True
                helpers.draw_speech_wizard(window, ['Very well, if you insist'], 770, 650, 25, 'red', wizard1.speech_count)
            if helpers.calculate_isabel_proximity(player.rect.x, player.rect.y, wizard1.rect.x, wizard1.rect.y):
                speech_wiz = helpers.get_speech_wizard()
                helpers.draw_speech_wizard(window, speech_wiz, 770, 650, 25, 'red', wizard1.speech_count)
                wizard1.speech_count += 1
        elif stage_count == 4:
            helpers.draw_stage3(window, player.character, player.rect, night_background, stage3_grass, pillar, heart_container1)
            heart_container1.update()
            heart_offset = (heart_container1.rect.x - player.rect.x), (heart_container1.rect.y - player.rect.y)
            if player.mask.overlap(heart_container1.mask, heart_offset):
                player.health = 4
                player.no_of_heart_crystals += 1
                heart_container1.blit_image = False

        helpers.display_health(window, player.health_sprites3h, player.health_sprites4h, player.health, player.no_of_heart_crystals)

        if key_list[pygame.K_SPACE] == 1 and player.is_sitting is False:
            player.in_air = True
        if player.in_air is True:
            player.player_jump()

        # Check idle position of character
        player.update_direction_facing(key_list)

        if enemy1.infinity_frames > 0:
            enemy1.infinity_frames -= 1

        #Check if player has hit enemies
        if player.attacking is True:
            player.attack()
            player.rect = player.character.get_rect(
                topleft=(player.rect.x, player.rect.y))
            enemy1.check_if_hit(player, stage_count)
            archer.check_if_hit(player, stage_count)

        # WEAPON MECHANICS
        # Check if attacking
        if key_list[pygame.K_f] == 1 and title.start_game is True:
            player.attacking = True

        # Check if character has clipped into ground
        player.check_if_clipped_into_ground(key_list)

        # Movement Right
        if key_list[pygame.K_d] == 1 and title.start_game is True:
            player.move_player_right(key_list)
        # Movement Left
        elif key_list[pygame.K_a] == 1 and title.start_game is True:
            player.move_player_left(key_list)
        # Update player idle animation if not moving
        if key_list[pygame.K_d] == 0 and key_list[pygame.K_a] == 0 and key_list[pygame.K_SPACE] == 0 and player.in_air is False and player.attacking is False:
            player.update_idle_animation()

        # If player has initialised dialogue, talk to NPC Isabel
        isabel.talk_to_isabel(window, stage_count, key_list, text_box)

        # Projectile acceleration
        player_proj.speed = helpers.projectile_acceleration(player_proj.speed, 1.01)

        # Modify x_value of projectile
        weapon_x = helpers.move_projectile(
            player_proj.direction, weapon_x, player_proj.speed)

        # Replay dialogue interaction
        if isabel.near_player is True and key_list[pygame.K_RETURN] == 1:
            isabel.interaction = 0

        shoot_enemy_weap = helpers.check_enemy1_range(player.rect.y, stage_count)
        shoot_enemy2_weap = helpers.check_enemy2_range(player.rect.y, stage_count)

        if shoot_enemy_weap is True:
            enemy1_proj.shoot = True
        if shoot_enemy2_weap is True:
            enemy2_proj.shoot = True

        # Shoot enemy weapon
        if enemy1_proj.shoot is True and enemy1.is_dead is False and stage_count == 1:
            enemy1_proj.rect = enemy1_proj.image.get_rect(
                topleft=(enemy1_projectile_x, 1000))

            x_offset = player.rect[0] - enemy1_proj.rect[0]
            if player.mask.overlap(enemy1_proj.mask, (x_offset, 0)) != None and player.rect.y == 620:
                if player.was_hit is False:
                    player.health -= 1
                    player.was_hit = True
            else:
                player.was_hit = False
            enemy1_projectile_x = helpers.draw_enemy1_proj(window, enemy1_proj.image, enemy1_proj.rect, enemy1_projectile_x,
                                                   enemy1_proj.speed)
            enemy1_proj.rect = enemy1_proj.image.get_rect(
                topleft=(enemy1_projectile_x, 1000))
            if enemy1_projectile_x < -250:
                enemy1_proj.shoot = False

        if enemy2_proj.shoot is True and enemy2.is_dead is False and stage_count == 1:
            enemy2_proj.rect = enemy2_proj.image.get_rect(
                topleft=(enemy2_projectile_x, 200))
            player.check_if_hit_by_enemy2(enemy2_proj.rect.x, enemy2_proj.rect.y, enemy2_proj.mask)

            enemy2_projectile_x = helpers.draw_enemy2_proj(
                window, enemy2_proj.image, enemy2_proj.rect, enemy2_projectile_x, enemy2_proj.speed)
            enemy2_proj.rect = enemy2_proj.image.get_rect(
                topleft=(enemy2_projectile_x, 200))
            if enemy2_projectile_x < -250:
                enemy2_proj.shoot = False

        #Shoot archer arrow
        archer_arrow.check_if_shoot(archer.curr_attack_sprite)
        if archer_arrow.shoot is True and archer.is_alive is True and stage_count == 1 and enemy1.is_dead is True:
            player.check_if_hit_by_archer(archer_arrow.rect.x, archer_arrow.rect.y, archer_arrow.mask)
            archer_arrow.shoot_arrow(window)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
