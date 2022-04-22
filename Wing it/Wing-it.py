import math
import pygame
import helpers

pygame.init()
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, character, character_x, character_y):
        super().__init__()
        self.character = character
        self.rect = self.character.get_rect(topleft=(character_x, character_y))
        self.mask = pygame.mask.from_surface(self.character)
        self.health = 3
        self.mask = pygame.mask.from_surface(self.character)
        self.gravity = 0
        self.infinity_frames = 30
        self.was_hit = False
        self.speed = 14

    def update(window, character, character_rec):
        window.blit(character, character_rec)
#

class Player_proj(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 20
        self.direction = False
        self.mask = pygame.mask.from_surface(self.image)


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/enemy1_large_left.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(1100, 440))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 4
        self.was_hit = False
        self.is_dead = False


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
        self.mask = pygame.mask.from_surface(self.image)


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
    character_left = pygame.image.load(
        'assets/character_standing_left.png').convert_alpha()
    character_right = pygame.image.load(
        'assets/characted_standing.png').convert_alpha()
    character_got_item = pygame.image.load(
                    'assets/obtained_staff.png').convert_alpha()

    player = Player(character, x_position, y_position)

    # Character Health
    character_healthfull_sprite = pygame.image.load('assets/health_full.png')
    character_health2_hearts_sprite = pygame.image.load('assets/health_2hearts.png')
    character_Health1_heart_sprite = pygame.image.load('assets/health_1heart.png')

    # Flight sprites
    character_flying1_right = pygame.image.load(
        'assets/flying_frame_character.png').convert_alpha()
    character_flying1_left = pygame.image.load(
        'assets/flying_frame_character_left.png').convert_alpha()
    character_flying_right = [pygame.image.load('assets/flying_frame_character.png').convert_alpha(
    ), pygame.image.load('assets/flying_frame2_right.png').convert_alpha()]
    character_flying_left = [pygame.image.load('assets/flying_frame_character_left.png').convert_alpha(
    ), pygame.image.load('assets/flying_frame2_left.png').convert_alpha()]

    # Backgrounds
    grass = pygame.image.load('assets/resize_background_2.png').convert()
    background = pygame.image.load('assets/background_sky.png').convert()
    night_background = pygame.image.load('assets/night_sky_starry.png').convert()
    night_grass = pygame.image.load('assets/night_grass_updated.png').convert()
    tree1 = pygame.image.load('assets/tree1.png').convert_alpha()

    # Array of walking right frames
    walking_right = [pygame.image.load(
        'assets/walk_frame1.png'), pygame.image.load('assets/walking_frame2right.png')]
    walking_left = [pygame.image.load(
        'assets/walk_frame1_left.png'), pygame.image.load('assets/walking_frame2left.png')]

    # Game fonts
    font = pygame.font.Font('slkscr.ttf', 50)
    text = font.render('Wing it!', False, 'White')

    # Side character_1
    side_1 = pygame.image.load('assets/Isabel_Idle1.png').convert_alpha()
    side_1_rec = side_1.get_rect(topleft=(1100, 665))
    side_1_right = pygame.image.load('assets/Isabel_Idle1_right.png').convert_alpha()
    side_1_right_rec = side_1_right.get_rect(topleft=(1050, 665))

    # Enemy 1
    enemy1 = Enemy1()
    enemy1.rect = enemy1.image.get_rect(topleft=(1100, 440))
    enemy1_projectile_x = 1100
    # Enemy 1's projectile
    enemy1_proj = Enemy1_proj(enemy1_projectile_x)

    enemy_full_hp = pygame.image.load('assets/healthbar_full.png')
    enemy_high_hp = pygame.image.load('assets/healthbar_high.png')
    enemy_medium_hp = pygame.image.load('assets/healthbar_medium.png')
    enemy_low_hp = pygame.image.load('assets/healthbar_low.png').convert_alpha()
    check_anim = True

    # Enemy 2:
    enemy2 = Enemy2()
    enemy2_projectile_x = 1100
    enemy2_proj = Enemy2_proj(enemy2_projectile_x)

    # Enemy 3:
    enemy3 = Enemy3(1040)

    # False signifies that character is facing left,
    # True signifies character is facing right
    check_position = False

    # weapon_particle
    weapon = pygame.image.load('assets/particle_effect.png').convert_alpha()
    weapon_x = 0
    weapon_y = 0

    player_proj = Player_proj(weapon, weapon_x, weapon_y)

    run_program = True
    isabel_interaction = 0

    blit_weapon = False
    # Check if character has talked with Isabel
    # And recieved the staff.
    got_staff = False

    walk_count = 0
    fly_count = 0

    stage_count = 0
    # Program game loop
    while run_program is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if player.rect.x > 1920:
            stage_count += 1
            player.rect.x = -200
        elif player.rect.x < -300:
            stage_count -= 1
            player.rect.x = 1900

        if stage_count == 0:
            helpers.draw_screen(window, background, grass, player.rect.x, side_1_rec.x, side_1_right,
                        side_1_right_rec, side_1, side_1_rec, player.character, player.rect,
                        text)

        elif stage_count == 1:
            helpers.draw_forest(window, player.character, player.rect, night_background,
                        night_grass, tree1, enemy1.image, enemy1.rect, enemy1.is_dead)

            helpers.show_enemy_hp(window, enemy1.health, enemy_high_hp,
                          enemy_medium_hp, enemy_low_hp)

            helpers.show_enemy2_hp(window, enemy2.health, enemy_high_hp, enemy_low_hp)
            if enemy2.is_dead is False:
                window.blit(enemy2.image, enemy2.rect)
        elif stage_count == 2:
            helpers.draw_forest2(window, player.character, player.rect,
                         night_background, night_grass, tree1)
            window.blit(enemy3.image, enemy3.rect)

            enemy3.rect.x -= 10
            if enemy3.rect.y == 555 and enemy3.falling is False:
                enemy3.rect.y -= 10
            if enemy3.rect.y != 555 and enemy3.falling is False:
                enemy3.rect.y -= 10
                enemy3.image = enemy3.jumping_image
            elif enemy3.rect.y != 555 and enemy3.falling is True:
                enemy3.rect.y += 10
                enemy3.image = enemy3.standing

            if enemy3.rect.y == 255:
                enemy3.falling = True
            elif enemy3.rect.y == 555:
                enemy3.falling = False
                enemy3.image = enemy3.standing

        helpers.display_health(window, character_healthfull_sprite, character_health2_hearts_sprite,
                   character_Health1_heart_sprite, player.health)

        key_list = pygame.key.get_pressed()

        if key_list[pygame.K_SPACE] == 1:
            player.gravity = -20
        # Check idle position of character
        if key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and check_position is True and player.rect.y == 660:
            player.character = character_right

        elif key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and check_position is False and player.rect.y == 660:
            player.character = character_left

        # WEAPON MECHANICS
        # Shoot weapon
        if key_list[pygame.K_f] == 1:
            if check_position is False:
                player_proj.direction = False
            else:
                player_proj.direction = True
            blit_weapon = True
            weapon_x = player.rect.x
            weapon_y = player.rect.y
            if check_position is False:
                player_proj.image = pygame.image.load(
                    'assets/particle_effect_left.png').convert_alpha()
            else:
                player_proj.image = pygame.image.load(
                    'assets/particle_effect.png').convert_alpha()

            player_proj.rect = player_proj.image.get_rect(
                topleft=(weapon_x, weapon_y))
            player_proj.speed = 20

        player.rect.y += player.gravity

        # Check if character has clipped into ground
        if player.rect.y > 660:
           # if main_char
            player.rect.y = 660

            if check_position is False and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1:
                player.character = character_left
            elif check_position is True and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1:
                player.character = character_right
            player.rect = player.character.get_rect(
                topleft=(player.rect.x, player.rect.y))

        # Jumping Mechanic
        if player.rect.y != 660:
            if check_anim is False:
                if key_list[pygame.K_SPACE] == 1 and check_position is True:
                    player.character = character_flying1_right
                    if (fly_count) > 1:
                        fly_count == 0

                    if fly_count < 2:
                        player.character = character_flying_right[math.floor(
                            fly_count)]
                    else:
                        fly_count = 0
                    fly_count += 0.075
                elif key_list[pygame.K_SPACE] == 1 and check_position is False:
                    player.character = character_flying1_left
                    if (fly_count) > 1:
                        fly_count == 0
                    if fly_count < 2:
                        player.character = character_flying_left[math.floor(
                            fly_count)]
                    else:
                        fly_count = 0
                    fly_count += 0.075
                elif check_position is False and key_list[pygame.K_SPACE] != 1:
                    player.character = character_flying1_left
                elif check_position is True and key_list[pygame.K_SPACE] != 1:
                    player.character = character_flying1_right
                player.rect = character.get_rect(
                    topleft=(player.rect.x, player.rect.y))
            else:
                if check_position is False:
                    player.character = character_left
                else:
                    player.character = character_right
                player.rect = player.character.get_rect(
                    topleft=(player.rect.x, player.rect.y))

                check_anim = False
            player.rect = player.character.get_rect(
                topleft=(player.rect.x, player.rect.y))
            player.gravity += 1

        # Movement Right
        if key_list[pygame.K_d] == 1:
            player.rect.left += player.speed

            if player.rect.y != 660 and key_list[pygame.K_SPACE] == 1:
                player.character = character_flying1_right
                if (fly_count) > 1:
                    fly_count == 0
                if fly_count < 2:
                    player.character = character_flying_right[math.floor(
                        fly_count)]
                else:
                    fly_count = 0
                fly_count += 0.075
                check_position = True
            elif player.rect.y != 660 and key_list[pygame.K_SPACE] != 1:
                player.character = character_flying1_right
                check_position = True
            else:
                if (walk_count) > 1:
                    walk_count == 0
                if walk_count < 2:
                    player.character = walking_right[math.floor(walk_count)]
                else:
                    walk_count = 0
                walk_count += 0.1

                check_position = True

            player.rect = player.character.get_rect(
                topleft=(player.rect.x, player.rect.y))
        # Movement Left
        elif key_list[pygame.K_a] == 1:
            player.rect.left -= player.speed
            if player.rect.y != 660 and key_list[pygame.K_SPACE] == 1:

                player.character = character_flying1_left
                if (fly_count) > 1:
                    fly_count == 0
                if fly_count < 2:
                    player.character = character_flying_left[math.floor(
                        fly_count)]
                else:
                    fly_count = 0
                fly_count += 0.075
                check_position = False
            elif player.rect.y != 660 and key_list[pygame.K_SPACE] != 1:
                player.character = character_flying1_left
                check_position = False
            else:

                if (walk_count) > 1:
                    walk_count == 0
                if walk_count < 2:
                    player.character = walking_left[math.floor(walk_count)]
                else:
                    walk_count = 0
                walk_count += 0.1

                check_position = False
            player.rect = player.character.get_rect(
                topleft=(player.rect.x, player.rect.y))

        isabel_proximity = helpers.calculate_isabel_proximity(player.rect.x, player.rect.y,
                                                      side_1_rec.x, side_1_rec.y)

        if isabel_proximity is True and stage_count == 0:
            if key_list[pygame.K_RIGHT] == 1:
                isabel_interaction += 100

            helpers.isabel_speech(window, isabel_interaction,
                          side_1_rec.x, side_1_rec.y)
            if isabel_interaction in range(1300, 1400):
                # Character has gotten the staff
                # and can now use it
                got_staff = True
                player.character = character_got_item
                player.rect = player.character.get_rect(
                    topleft=(player.rect.x, player.rect.y))

            elif isabel_interaction in range(1400, 1500):
                player.character = character_right
                player.rect = character.get_rect(
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
        if blit_weapon is True and got_staff is True:
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

            #player.rect = player.character.get_rect(topleft = (player.rect.x, player.rect.y))

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
