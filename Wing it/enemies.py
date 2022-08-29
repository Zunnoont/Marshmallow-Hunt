from curses import is_term_resized
import math
from multiprocessing.reduction import send_handle
from re import L
import pygame
import helpers

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
        self.infinity_frames = 0
        self.was_hit = False
        self.is_dead = False

    def update(self):
        self.curr_sprite += 0.02
        if self.curr_sprite >= len(self.sprites):
            self.curr_sprite = 0
        self.image = self.sprites[int(self.curr_sprite)]
    def check_if_hit(self, player, stage_count):
        offset = (self.rect.x -
                      player.rect.x), (self.rect.y - player.rect.y)
        if player.mask.overlap(self.mask, (offset)) != None and stage_count == 1:

            if self.infinity_frames == 0:
                self.health -= 1
                self.infinity_frames += 20
                if self.health == 0:
                    self.is_dead = True
        else:
            self.was_hit = False

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

class EnemyArcher(pygame.sprite.Sprite):
    def __init__(self):
        self.sprites_right = [pygame.image.load('assets/archer_enemy/archer_f1.png').convert_alpha(),
                              pygame.image.load('assets/archer_enemy/archer_f2.png').convert_alpha()]
        self.attack_cycle = [pygame.image.load('assets/archer_enemy/archer_enemy_attack/enemy3_f1.png').convert_alpha(),
                             pygame.image.load('assets/archer_enemy/archer_enemy_attack/enemy3_f2.png').convert_alpha(),
                             pygame.image.load('assets/archer_enemy/archer_enemy_attack/enemy3_f3.png').convert_alpha(),
                             pygame.image.load('assets/archer_enemy/archer_enemy_attack/enemy3_f4.png').convert_alpha(),
                             pygame.image.load('assets/archer_enemy/archer_enemy_attack/enemy3_f5.png').convert_alpha(),
                             pygame.image.load('assets/archer_enemy/archer_enemy_attack/enemy3_f6.png').convert_alpha()]
        self.curr_sprite = 0
        self.curr_attack_sprite = 0
        self.health = 4
        self.attacking = False
        self.is_alive = True
        self.shoot = False
        self.infinity_frames = 0
        self.image = self.sprites_right[0]
        self.rect = self.image.get_rect(topleft=(100, 642))
        self.mask = pygame.mask.from_surface(self.image)

    def idle_anim(self):
        if self.curr_sprite >= 2:
            self.curr_sprite = 0
        else:
            self.image = self.sprites_right[math.floor(self.curr_sprite)]
        self.curr_sprite += 0.025

    def attack_anim(self):
        self.curr_attack_sprite += 0.05
        if self.curr_attack_sprite >= 6:
            self.curr_attack_sprite = 0
            self.attacking = True
        else:
            self.image = self.attack_cycle[math.floor(self.curr_attack_sprite)]
    def check_if_shoot(self):
        if math.floor(self.curr_attack_sprite) == 5:
            self.shoot = True
        return self.shoot
    def check_if_hit(self, player, stage_count):
        offset = (self.rect.x -
                      player.rect.x), (self.rect.y - player.rect.y)
        if player.mask.overlap(self.mask, (offset)) != None and stage_count == 1:

            if self.infinity_frames == 0:
                self.health -= 1
                self.infinity_frames += 20
                if self.health == 0:
                    self.is_dead = True
        else:
            self.was_hit = False

    def update_infinity_frames(self):
        if self.infinity_frames > 0:
            self.infinity_frames -= 1

    def show_hp(self, window, high_hp, medium_hp, low_hp):
        if self.health == 3:
            window.blit(high_hp, (-35, 530))
        elif self.health == 2:
            window.blit(medium_hp, (-35, 530))
        elif self.health == 1:
            window.blit(low_hp, (-35, 530))

class EnemyArcher_Projectile(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('assets/archer_enemy/archer_enemy_attack/archer_arrow-export.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (100, 642))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 20
        self.arrow_x = 100
        self.shoot = False

    def update_arrow(self):
        self.rect = self.image.get_rect(topleft=(self.arrow_x, 642))
        self.arrow_x += self.speed
        if self.arrow_x > 1980:
            self.arrow_x = 100
            self.shoot = False

    def check_if_shoot(self, curr_attack_sprite):
        if math.floor(curr_attack_sprite) == 5:
            self.shoot = True
    def shoot_arrow(self, window):
        self.rect = self.image.get_rect(topleft=(self.arrow_x, 642))
        self.arrow_x += self.speed
        if self.arrow_x > 1920:
            self.arrow_x = 100
            self.shoot = False
        else:
            self.rect = self.image.get_rect(topleft=(self.arrow_x, 642))
            window.blit(self.image, self.rect)

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