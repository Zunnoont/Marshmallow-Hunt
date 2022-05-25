import math
import pygame
import helpers
import storage

pygame.init()
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, character, character_x, character_y):
        super().__init__()
        self.character = character
        self.character_left = pygame.image.load(
        'assets/character_standing_left.png').convert_alpha()
        self.character_right = pygame.image.load(
        'assets/characted_standing.png').convert_alpha()
        self.got_item = pygame.image.load(
                    'assets/obtained_staff.png').convert_alpha()
        self.rect = self.character.get_rect(topleft=(character_x, character_y))
        self.mask = pygame.mask.from_surface(self.character)
        self.health = 3
        self.no_of_heart_crystals = 0
        self.health_sprites3h = [pygame.image.load('assets/health_full.png').convert_alpha(),
                                 pygame.image.load('assets/health_2hearts.png').convert_alpha(),
                                 pygame.image.load('assets/health_1heart.png').convert_alpha()]

        self.health_sprites4h = [pygame.image.load('assets/health_4hearts.png').convert_alpha(),
                                 pygame.image.load('assets/4hp_3_hearts.png').convert_alpha(),
                                 pygame.image.load('assets/4hp_2_hearts.png').convert_alpha(),
                                 pygame.image.load('assets/4hp_1_heart.png').convert_alpha()]
        self.idle_sprites_right = [pygame.image.load(
        'assets/characted_standing.png').convert_alpha(),
                                   pygame.image.load('assets/idle_frame2_right.png').convert_alpha(),
                                   pygame.image.load('assets/idle_frame3_right.png').convert_alpha()]
        self.idle_sprites_left = [pygame.image.load(
        'assets/character_standing_left.png').convert_alpha(),
                                  pygame.image.load('assets/idle_frame2_left.png').convert_alpha(),
                                  pygame.image.load('assets/idle_frame3_left.png').convert_alpha()]
        self.gravity = 0
        self.infinity_frames = 30
        self.was_hit = False
        self.got_staff = False
        self.check_anim = True
        self.speed = 14
        self.walk_count = 0
        self.fly_count = 0
        self.curr_idle_sprite = 0
        self.is_facing_right = False
        self.in_bossfight = False
        self.flying_right = [pygame.image.load('assets/flying_frame_character.png').convert_alpha(
        ), pygame.image.load('assets/flying_frame2_right.png').convert_alpha()]
        self.flying_left = [pygame.image.load('assets/flying_frame_character_left.png').convert_alpha(
        ), pygame.image.load('assets/flying_frame2_left.png').convert_alpha()]
        self.walk_cycle_right = [pygame.image.load(
        'assets/walk_frame1.png'), pygame.image.load('assets/walking_frame2right.png')]
        self.walk_cycle_left = [pygame.image.load(
        'assets/walk_frame1_left.png'), pygame.image.load('assets/walking_frame2left.png')]

    def update(window, character, character_rec):
        window.blit(character, character_rec)

    def move_player_right(self, key_list):
        self.curr_idle_sprite = 0
        self.rect.left += self.speed

        if self.rect.y != 660 and key_list[pygame.K_SPACE] == 1:
            self.character = self.flying_right[0]
            if (self.fly_count) > 1:
                self.fly_count == 0
            if self.fly_count < 2:
                self.character = self.flying_right[math.floor(
                self.fly_count)]
            else:
                self.fly_count = 0
            self.fly_count += 0.075
            self.is_facing_right = True
        elif self.rect.y != 660 and key_list[pygame.K_SPACE] != 1:
            self.character = self.flying_right[0]
            self.is_facing_right = True
        else:
            if (self.walk_count) > 1:
                self.walk_count == 0
            if self.walk_count < 2:
                self.character = self.walk_cycle_right[math.floor(self.walk_count)]
            else:
                self.walk_count = 0
            self.walk_count += 0.1

            self.is_facing_right = True

        self.rect = self.character.get_rect(
            topleft=(self.rect.x, self.rect.y))

    def move_player_left(self, key_list):
        self.curr_idle_sprite = 0
        self.rect.left -= self.speed
        if self.rect.y != 660 and key_list[pygame.K_SPACE] == 1:

            self.character = self.flying_left[0]
            if (self.fly_count) > 1:
                self.fly_count == 0
            if self.fly_count < 2:
                self.character = self.flying_left[math.floor(
                self.fly_count)]
            else:
                self.fly_count = 0
            self.fly_count += 0.075
            self.is_facing_right = False
        elif self.rect.y != 660 and key_list[pygame.K_SPACE] != 1:
            self.character = self.flying_left[0]
            self.is_facing_right = False
        else:
            if (self.walk_count) > 1:
                self.walk_count == 0
            if self.walk_count < 2:
                self.character = self.walk_cycle_left[math.floor(self.walk_count)]
            else:
                self.walk_count = 0
            self.walk_count += 0.1

            self.is_facing_right = False
        self.rect = self.character.get_rect(
            topleft=(self.rect.x, self.rect.y))
    def update_idle_animation(self):
        self.curr_idle_sprite += 0.01
        if self.is_facing_right is True:
            if self.curr_idle_sprite >= len(self.idle_sprites_right):
                self.curr_idle_sprite = 0
            self.character = self.idle_sprites_right[int(self.curr_idle_sprite)]
        else:
            if self.curr_idle_sprite >= len(self.idle_sprites_left):
                self.curr_idle_sprite = 0
            self.character = self.idle_sprites_left[int(self.curr_idle_sprite)]
        self.rect = self.character.get_rect(
            topleft=(self.rect.x, self.rect.y))



class Player_proj(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.image_left = pygame.image.load(
                    'assets/particle_effect_left.png').convert_alpha()
        self.image_right = pygame.image.load(
                    'assets/particle_effect.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 20
        self.direction = False
        self.mask = pygame.mask.from_surface(self.image)
        self.blit_weapon = False

class Isabel(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('assets/Isabel_Idle1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(1100, 665))
        self.curr_sprite = 0
        self.sprites_left = [pygame.image.load('assets/Isabel_Idle1.png').convert_alpha(),
                             pygame.image.load('assets/isabel_idle2_left.png').convert_alpha()]
        self.sprites_right = [pygame.image.load('assets/Isabel_Idle1_right.png').convert_alpha(),
                              pygame.image.load('assets/isabel_idle2_right.png').convert_alpha()]
    def update(self, player_x):
        self.curr_sprite += 0.05
        if player_x > self.rect.x:
            if self.curr_sprite >= len(self.sprites_right):
                self.curr_sprite = 0
            self.image = self.sprites_right[int(self.curr_sprite)]
        else:
            if self.curr_sprite >= len(self.sprites_left):
                self.curr_sprite = 0
            self.image = self.sprites_left[int(self.curr_sprite)]




class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/enemy1_large_left.png').convert_alpha()
        self.sprites = [pygame.image.load('assets/enemy1_large_left.png').convert_alpha(),
                        pygame.image.load('assets/enemy1_large_left_frame2.png').convert_alpha()]
        self.curr_sprite = 0
        self.rect = self.image.get_rect(topleft=(1100, 440))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 4
        self.was_hit = False
        self.is_dead = False

    def update(self):
        self.curr_sprite += 0.02
        if self.curr_sprite >= len(self.sprites):
            self.curr_sprite = 0
        self.image = self.sprites[int(self.curr_sprite)]



class Enemy1_proj(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image = pygame.image.load(
            'assets/dagger_projectile_left.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_position, 1000))
        self.speed = 20
        self.shoot = False
        self.mask = pygame.mask.from_surface(self.image)


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            'assets/enemy2_flying_left.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(1100, 100))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 3
        self.was_hit = False
        self.is_dead = False


class Enemy2_proj(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image = pygame.image.load('assets/e2_proj.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_position, 200))
        self.speed = 20
        self.shoot = False
        self.mask = pygame.mask.from_surface(self.image)


class Enemy3(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image = pygame.image.load('assets/slime_left.png').convert_alpha()
        self.jumping_image = pygame.image.load(
            'assets/slime_left_jumping.png').convert_alpha()
        self.standing = pygame.image.load('assets/slime_left.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_position, 555))
        self.speed = 20
        self.falling = False
        self.is_offscreen = False
        self.mask = pygame.mask.from_surface(self.image)

    def move_jumping_slime(self):
        self.rect.x -= 10
        if self.rect.y == 555 and self.falling is False:
            self.rect.y -= 10
        if self.rect.y != 555 and self.falling is False:
            self.rect.y -= 10
            self.image = self.jumping_image
        elif self.rect.y != 555 and self.falling is True:
            self.rect.y += 10
            self.image = self.standing
        if self.rect.y == 255:
            self.falling = True
        elif self.rect.y == 555:
            self.falling = False
            self.image = self.standing

        if self.rect.x < -200:
            self.is_offscreen = True

        self.rect = self.image.get_rect(topleft= (self.rect.x, self.rect.y))


class Enemy4(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image = pygame.image.load('assets/green_slime_idle.png').convert_alpha()
        self.jumping_image = pygame.image.load(
            'assets/green_slime_jump.png').convert_alpha()
        self.standing = pygame.image.load('assets/green_slime_idle.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_position, 555))
        self.speed = 23
        self.falling = False
        self.is_offscreen = False
        self.mask = pygame.mask.from_surface(self.image)

    def move_jumping_slime_green(self):
        self.rect.x -= 15
        if self.rect.y == 555 and self.falling is False:
            self.rect.y -= 15
        if self.rect.y != 555 and self.falling is False:
            self.rect.y -= 15
            self.image = self.jumping_image
        elif self.rect.y != 555 and self.falling is True:
            self.rect.y += 15
            self.image = self.standing
        if self.rect.y == 255:
            self.falling = True
        elif self.rect.y == 555:
            self.falling = False
            self.image = self.standing

        if self.rect.x < -200:
            self.is_offscreen = True

        self.rect = self.image.get_rect(topleft= (self.rect.x, self.rect.y))

class Enemy5(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image = pygame.image.load('assets/red_slime_idle.png').convert_alpha()
        self.jumping_image = pygame.image.load(
            'assets/red_slime_jump.png').convert_alpha()
        self.standing = pygame.image.load('assets/red_slime_idle.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_position, 555))
        self.speed = 20
        self.falling = False
        self.is_offscreen = False
        self.mask = pygame.mask.from_surface(self.image)

    def move_jumping_slime_red(self):
        self.rect.x -= 20
        if self.rect.y == 555 and self.falling is False:
            self.rect.y -= 20
        if self.rect.y != 555 and self.falling is False:
            self.rect.y -= 20
            self.image = self.jumping_image
        elif self.rect.y != 555 and self.falling is True:
            self.rect.y += 20
            self.image = self.standing
        if self.rect.y == 255:
            self.falling = True
        elif self.rect.y == 555:
            self.falling = False
            self.image = self.standing

        if self.rect.x < -200:
            self.is_offscreen = True

        self.rect = self.image.get_rect(topleft= (self.rect.x, self.rect.y))

class Large_slime(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image = pygame.image.load('assets/large_slime_idle.png').convert_alpha()
        self.jumping_image = pygame.image.load(
            'assets/large_slime.png').convert_alpha()
        self.standing = pygame.image.load('assets/large_slime_idle.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_position, 255))
        self.speed = 20
        self.falling = False
        self.is_offscreen = False
        self.mask = pygame.mask.from_surface(self.image)

    def move_jumping_slime_purple(self):
        self.rect.x -= 20
        if self.rect.y == 555 and self.falling is False:
            self.rect.y -= 5
        if self.rect.y != 555 and self.falling is False:
            self.rect.y -= 5
            self.image = self.jumping_image
        elif self.rect.y != 555 and self.falling is True:
            self.rect.y += 5
            self.image = self.standing
        if self.rect.y == 255:
            self.falling = True
        elif self.rect.y == 555:
            self.falling = False
            self.image = self.standing

        if self.rect.x < -200:
            self.is_offscreen = True

        self.rect = self.image.get_rect(topleft= (self.rect.x, self.rect.y))

class Wizard1(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        self.sprites_right = [pygame.image.load('assets/wizard_right.png').convert_alpha(),
                              pygame.image.load('assets/wizard_right_frame2.png').convert_alpha()]
        self.sprites_left = [pygame.image.load('assets/wizard_left.png').convert_alpha(),
                             pygame.image.load('assets/wizard_left_frame2.png').convert_alpha()]
        self.angry_sprites_left = [pygame.image.load('assets/angry_wiz_frame2_left.png').convert_alpha(),
                                   pygame.image.load('assets/wizard_f2_left.png').convert_alpha()]
        self.angry_sprites_right = [pygame.image.load('assets/wizard_angry_f1_right.png').convert_alpha(),
                                    pygame.image.load('assets/angry_wiz_frame2_right.png').convert_alpha()
                                    ]
        self.curr_sprite = 0
        self.image = self.sprites_left[self.curr_sprite]
        self.blit_image = True
        self.in_bossfight = False
        self.speech_count = 0
        self.rect = self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, player_x):
        self.curr_sprite += 0.025
        if self.in_bossfight is False:

            if player_x > self.rect.x:
                if self.curr_sprite >= len(self.sprites_right):
                    self.curr_sprite = 0
                self.image = self.sprites_right[int(self.curr_sprite)]
            else:
                if self.curr_sprite >= len(self.sprites_left):
                    self.curr_sprite = 0
                self.image = self.sprites_left[int(self.curr_sprite)]
        else:
            if player_x > self.rect.x:
                if self.curr_sprite >= len(self.angry_sprites_right):
                    self.curr_sprite = 0
                self.image = self.angry_sprites_right[int(self.curr_sprite)]
            else:
                if self.curr_sprite >= len(self.angry_sprites_left):
                    self.curr_sprite = 0
                self.image = self.angry_sprites_left[int(self.curr_sprite)]



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

# Main function of Wing It!
def main():
    # Pygame Window
    x_position = 100
    y_position = 660
    window = pygame.display.set_mode((1920, 1060))
    window.fill(('White'))

    # Game name
    pygame.display.set_caption('Wing It!')

    # Character Sprites
    character = pygame.image.load('assets/characted_standing.png').convert_alpha()
    player = Player(character, x_position, y_position)

    # Backgrounds
    grass = pygame.image.load('assets/resize_background_2.png').convert()
    background = pygame.image.load('assets/background_sky.png').convert()
    night_background = pygame.image.load('assets/night_sky_starry.png').convert()
    night_grass = pygame.image.load('assets/night_grass_updated.png').convert()
    tree1 = pygame.image.load('assets/tree1.png').convert_alpha()
    stage3_grass =  pygame.image.load('assets/autumn_grass_first.png').convert_alpha()
    pillar = pygame.image.load('assets/pillar.png').convert_alpha()

    # Game fonts
    font = pygame.font.Font('slkscr.ttf', 50)
    text = font.render('Wing it!', False, 'White')

    # Side character_1
    isabel = Isabel()
    side_1 = pygame.image.load('assets/Isabel_Idle1.png').convert_alpha()
    side_1_rec = side_1.get_rect(topleft=(1100, 665))

    # Enemy 1
    enemy1 = Enemy1()
    enemy1.rect = enemy1.image.get_rect(topleft=(1100, 440))
    enemy1_projectile_x = 1100
    # Enemy 1's projectile
    enemy1_proj = Enemy1_proj(enemy1_projectile_x)

    enemy_high_hp = pygame.image.load('assets/healthbar_high.png')
    enemy_medium_hp = pygame.image.load('assets/healthbar_medium.png')
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

    # Large slime miniboss

    large_slime = Large_slime(1200)

    heart_container1  = Heart_container(485, 60)


    # weapon_particle
    weapon = pygame.image.load('assets/particle_effect.png').convert_alpha()
    weapon_x = 0
    weapon_y = 0

    player_proj = Player_proj(weapon, weapon_x, weapon_y)

    run_program = True
    isabel_interaction = 0

    stage_count = 0

    # Program game loop
    while run_program is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Change stage
        if player.rect.x > 1920 and player.in_bossfight is False:
            stage_count += 1
            player.rect.x = -200
        elif player.rect.x < -300 and player.in_bossfight is False:
            stage_count -= 1
            player.rect.x = 1900

        if stage_count == 0:
            helpers.draw_screen(window, background, grass, isabel.image, isabel.rect, player.character, player.rect,
                        text)
            isabel.update(player.rect.x)

        elif stage_count == 1:
            helpers.draw_forest(window, player.character, player.rect, night_background,
                        night_grass, tree1, enemy1.image, enemy1.rect, enemy1.is_dead)

            helpers.show_enemy_hp(window, enemy1.health, enemy_high_hp,
                          enemy_medium_hp, enemy_low_hp)

            helpers.show_enemy2_hp(window, enemy2.health, enemy_high_hp, enemy_low_hp)
            enemy1.update()
            if enemy2.is_dead is False:
                window.blit(enemy2.image, enemy2.rect)
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
        key_list = pygame.key.get_pressed()

        if key_list[pygame.K_SPACE] == 1:
            player.gravity = -20

        # Check idle position of character
        if key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and player.is_facing_right is True and player.rect.y == 660:
            player.character = player.character_right

        elif key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and player.is_facing_right is False and player.rect.y == 660:
            player.character = player.character_left

        # WEAPON MECHANICS
        # Shoot weapon
        if key_list[pygame.K_f] == 1:
            if player.is_facing_right is False:
                player_proj.direction = False
            else:
                player_proj.direction = True
            player_proj.blit_weapon = True
            weapon_x = player.rect.x
            weapon_y = player.rect.y
            if player.is_facing_right is False:
                player_proj.image = player_proj.image_left
            else:
                player_proj.image = player_proj.image_right

            player_proj.rect = player_proj.image.get_rect(
                topleft=(weapon_x, weapon_y))
            player_proj.speed = 20

        player.rect.y += player.gravity

        # Check if character has clipped into ground
        if player.rect.y > 660:
           # if main_char
            player.rect.y = 660

            if player.is_facing_right is False and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1:
                player.character = player.character_left
            elif player.is_facing_right is True and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1:
                player.character = player.character_right
            player.rect = player.character.get_rect(
                topleft=(player.rect.x, player.rect.y))

        # Jumping Mechanic
        if player.rect.y != 660:
            helpers.player_jump(player, key_list)

        # Movement Right
        if key_list[pygame.K_d] == 1:
            player.move_player_right(key_list)
        # Movement Left
        elif key_list[pygame.K_a] == 1:
            player.move_player_left(key_list)

        isabel_proximity = helpers.calculate_isabel_proximity(player.rect.x, player.rect.y,
                                                      side_1_rec.x, side_1_rec.y)

        if key_list[pygame.K_d] == 0 and key_list[pygame.K_a] == 0 and key_list[pygame.K_SPACE] == 0:
            player.update_idle_animation()

        if isabel_proximity is True and stage_count == 0:
            if key_list[pygame.K_RIGHT] == 1:
                isabel_interaction += 100

            helpers.isabel_speech(window, isabel_interaction,
                          isabel.rect.x, isabel.rect.y)
            if isabel_interaction in range(1300, 1400):
                # Character has gotten the staff
                # and can now use it
                player.got_staff = True
                player.character = player.got_item
                player.rect = player.character.get_rect(
                    topleft=(player.rect.x, player.rect.y))

            elif isabel_interaction in range(1400, 1500):
                player.character = player.character_right
                player.rect = player.character.get_rect(
                    topleft=(player.rect.x, player.rect.y))
            speech = helpers.get_speech()

            if (isabel_interaction // 100) < len(speech):
                isabel_interaction += 1


        # Projectile acceleration
        player_proj.speed = helpers.projectile_acceleration(player_proj.speed, 1.01)

        # Modify x_value of projectile
        weapon_x = helpers.move_projectile(
            player_proj.direction, weapon_x, player_proj.speed)

        # Replay dialogue interaction
        if isabel_proximity is True and key_list[pygame.K_RETURN] == 1:
            isabel_interaction = 0

        # Shoot weapon
        if player_proj.blit_weapon is True and player.got_staff is True:
            player_proj.rect = player_proj.image.get_rect(
                topleft=(weapon_x, weapon_y))
            window.blit(player_proj.image, player_proj.rect)

            offset = (enemy1.rect.x -
                      player_proj.rect.x), (enemy1.rect.y - player_proj.rect.y)
            enemy2_offset = (
                enemy2.rect.x - player_proj.rect.x), (enemy2.rect.y - player_proj.rect.y)
            if player_proj.mask.overlap(enemy1.mask, (offset)) != None and stage_count == 1:

                if enemy1.was_hit is False:
                    enemy1.health -= 1
                    enemy1.was_hit = True
                    if enemy1.health == 0:
                        enemy1.is_dead = True
            else:
                enemy1.was_hit = False

            if player_proj.mask.overlap(enemy2.mask, enemy2_offset) != None:
                if enemy2.was_hit is False:
                    enemy2.health -= 1
                    enemy2.was_hit = True
                    if enemy2.health == 0:
                        enemy2.is_dead = True
            else:
                enemy2.was_hit = False
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
            if player.mask.overlap(enemy1_proj.mask, (x_offset, 0)) != None and player.rect.y == 660:
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
            e2_x_offset = player.rect.x - enemy2_proj.rect.x
            e2_y_offset = player.rect.y - enemy2_proj.rect.y
            if player.mask.overlap(enemy2_proj.mask, (e2_x_offset, e2_y_offset)) != None:
                if player.was_hit is False:
                    player.health -= 1
                    player.was_hit = True
            else:
                player.was_hit = False

            enemy2_projectile_x = helpers.draw_enemy2_proj(
                window, enemy2_proj.image, enemy2_proj.rect, enemy2_projectile_x, enemy2_proj.speed)
            enemy2_proj.rect = enemy2_proj.image.get_rect(
                topleft=(enemy2_projectile_x, 200))
            if enemy2_projectile_x < -250:
                enemy2_proj.shoot = False
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
