from curses import is_term_resized
import math
from multiprocessing.reduction import send_handle
from re import L
import pygame
import helpers

class Player(pygame.sprite.Sprite):
    def __init__(self, character, character_x, character_y):
        super().__init__()
        self.character = character
        self.character_left = pygame.image.load(
        'assets/character_standing_left.png').convert_alpha()
        self.character_right = pygame.image.load(
        'assets/main_char.png').convert_alpha()
        self.got_item = pygame.image.load(
                    'assets/obtained_staff.png').convert_alpha()
        self.rect = self.character.get_rect(topleft=(character_x, character_y))
        self.mask = pygame.mask.from_surface(self.character)
        self.health = 3
        self.no_of_heart_crystals = 0
        self.health_sprites3h = [pygame.image.load('assets/Hp_frames/health_full.png').convert_alpha(),
                                 pygame.image.load('assets/Hp_frames/health_2hearts.png').convert_alpha(),
                                 pygame.image.load('assets/Hp_frames/health_1heart.png').convert_alpha()]

        self.health_sprites4h = [pygame.image.load('assets/Hp_frames/health_4hearts.png').convert_alpha(),
                                 pygame.image.load('assets/Hp_frames/4hp_3_hearts.png').convert_alpha(),
                                 pygame.image.load('assets/Hp_frames/4hp_2_hearts.png').convert_alpha(),
                                 pygame.image.load('assets/Hp_frames/4hp_1_heart.png').convert_alpha()]
        self.hit_frames = [pygame.image.load('assets/Mc_damage_taken/main_char_taken_damage1.png').convert_alpha(),
                           pygame.image.load('assets/Mc_damage_taken/main_char_taken_damage2.png').convert_alpha(),
                           pygame.image.load('assets/Mc_damage_taken/main_char_taken_damage3.png').convert_alpha(),
                           pygame.image.load('assets/Mc_damage_taken/main_char_taken_damage4.png').convert_alpha(),
                           pygame.image.load('assets/Mc_damage_taken/main_char_taken_damage5.png').convert_alpha(),
                           pygame.image.load('assets/Mc_damage_taken/main_char_taken_damage6.png').convert_alpha(),
                           pygame.image.load('assets/Mc_damage_taken/main_char_taken_damage7.png').convert_alpha()]
        self.idle_sprites_right = [pygame.image.load(
        'assets/main_char.png').convert_alpha(),
                                   pygame.image.load('assets/idle_frame1_main.png').convert_alpha(),
                                   ]
        self.idle_sprites_left = [pygame.image.load(
        'assets/main_char_left.png').convert_alpha(),
                                  pygame.image.load('assets/idle_frame1_main_left.png').convert_alpha()]

        self.gravity = 0
        self.infinity_frames = 30
        self.was_hit = False
        self.got_staff = False
        self.check_anim = True
        self.speed = 17
        self.walk_count = 0
        self.fly_count = 0
        self.curr_idle_sprite = 0
        self.taken_damage_frame = 0
        self.attack_frame = 0
        self.attacking = False
        self.is_facing_right = False
        self.in_bossfight = False
        self.in_air = False
        self.is_sitting = True
        self.flying_right = [
        pygame.image.load('assets/Jump_main/main_character2.png').convert_alpha(
        ),
        pygame.image.load('assets/Jump_main/main_character3.png').convert_alpha(
        ),
        pygame.image.load('assets/Jump_main/main_character4.png').convert_alpha(
        ),
        pygame.image.load('assets/Jump_main/main_character5.png').convert_alpha(
        ),
        pygame.image.load('assets/Jump_main/main_character6.png').convert_alpha(
        ),
        pygame.image.load('assets/Jump_main/main_character7.png').convert_alpha(
        )
        ,pygame.image.load('assets/Jump_main/main_character8.png').convert_alpha(
        ),
        pygame.image.load('assets/Jump_main/main_character9.png').convert_alpha(
        ),
        pygame.image.load('assets/Jump_main/main_character9.png').convert_alpha(
        )]
        self.flying_left = [pygame.image.load('assets/flying_frame_character_left.png').convert_alpha(
        ), pygame.image.load('assets/flying_frame2_left.png').convert_alpha()]

        self.sitting_cycle = [pygame.image.load('assets/main_sitting_f1.png').convert_alpha(),
                              pygame.image.load('assets/main_sitting_f2.png').convert_alpha()]
        self.walk_cycle_right = [pygame.image.load(
        'assets/mc_walk_f1.png').convert_alpha(),
        pygame.image.load('assets/main_walk_f2.png').convert_alpha(),
        pygame.image.load('assets/mc_walk_f3.png').convert_alpha(),
        pygame.image.load('assets/walk_f4.png').convert_alpha(),
        pygame.image.load('assets/walk_f5.png').convert_alpha(),
        pygame.image.load('assets/main_char.png').convert_alpha()
        ]
        self.walk_cycle_left = [pygame.image.load(
        'assets/mc_walk_f1_left.png').convert_alpha(),
        pygame.image.load('assets/main_walk_f2_left.png').convert_alpha(),
        pygame.image.load('assets/mc_walk_f3_left.png').convert_alpha(),
        pygame.image.load('assets/walk_f4_left.png').convert_alpha(),
        pygame.image.load('assets/walk_f5_left.png').convert_alpha()
        ]
        self.attack_cycle = [pygame.image.load('assets/Attack_frames/attack_v1.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v2.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v3.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v4.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v5.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v6.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v7.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v8.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v9.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v10.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v11.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v12.png').convert_alpha(),
                            pygame.image.load('assets/Attack_frames/attack_v13.png').convert_alpha()
                            ]
        self.attack_cycle_left = [
            pygame.image.load('assets/Attack_frames_left/attack_v1_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v2_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v3_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v4_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v5_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v6_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v7_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v8_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v9_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v10_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v11_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v12_left.png').convert_alpha(),
            pygame.image.load('assets/Attack_frames_left/attack_v13_left.png').convert_alpha()
        ]

    def update(window, character, character_rec):
        window.blit(character, character_rec)

    def move_player_right(self, key_list):
        if self.is_sitting is True:
            self.is_sitting = False
            self.rect.y = 620
        self.curr_idle_sprite = 0
        self.rect.left += self.speed

        if self.in_air is True:
            if self.fly_count >= 9:
                self.fly_count = 0
            self.is_facing_right = True
        else:
            if (self.walk_count) > 4:
                self.walk_count == 0
            if self.walk_count < 5:
                self.character = self.walk_cycle_right[math.floor(self.walk_count)]
            else:
                self.walk_count = 0
            self.walk_count += 0.2

            self.is_facing_right = True

        self.rect = self.character.get_rect(
            topleft=(self.rect.x, self.rect.y))

    def move_player_left(self, key_list):
        self.is_sitting = False
        self.curr_idle_sprite = 0
        self.rect.left -= self.speed
        if self.rect.y != 620 and key_list[pygame.K_SPACE] == 1:

            self.character = self.flying_left[0]
            if (self.fly_count) > 1:
                self.fly_count == 0
            if self.fly_count < 2:
                self.character = self.flying_left[math.floor(
                self.fly_count)]
            else:
                self.fly_count = 0
            self.fly_count += 0.4
            self.is_facing_right = False
        elif self.rect.y != 620 and key_list[pygame.K_SPACE] != 1:
            self.character = self.flying_left[0]
            self.is_facing_right = False
        else:
            if (self.walk_count) > 4:
                self.walk_count == 0
            if self.walk_count < 5:
                self.character = self.walk_cycle_left[math.floor(self.walk_count)]
            else:
                self.walk_count = 0
            self.walk_count += 0.2

            self.is_facing_right = False
        self.rect = self.character.get_rect(
            topleft=(self.rect.x, self.rect.y))
    def update_idle_animation(self):
        if self.is_sitting is True:
            self.curr_idle_sprite += 0.01
            if self.curr_idle_sprite >= len(self.sitting_cycle):
                self.curr_idle_sprite = 0
            self.character = self.sitting_cycle[int(self.curr_idle_sprite)]
        else:
            self.curr_idle_sprite += 0.03
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
    def player_jump(self):
        self.rect.y = 420
        if self.fly_count >= 8:
            self.fly_count = 0
            self.in_air = False
            self.rect.y = 620
            self.character = self.flying_right[8]
        if self.is_facing_right is True:
            if self.fly_count >= 9:
                self.fly_count = 0
                self.in_air = False
                self.rect.y = 620
                self.character = self.flying_right[8]
            self.character = self.flying_right[math.floor(
            self.fly_count)]
            self.fly_count += 0.3

    def attack(self):
        if self.attack_frame >= 13:
            self.attack_frame = 0
            self.attacking = False
        if self.is_facing_right is True:
            self.character = self.attack_cycle[math.floor(
            self.attack_frame)]
            self.attack_frame += 0.4
        else:
            self.character = self.attack_cycle_left[math.floor(
            self.attack_frame)]
            self.attack_frame += 0.4
    def update_direction_facing(self, key_list):
        # Check idle position of character
        if key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and self.is_facing_right is True and self.rect.y == 620 and self.in_air is False:
            self.character = self.character_right
        elif key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and self.is_facing_right is False and self.rect.y == 620 and self.in_air is False:
            self.character = self.character_left
    def check_if_clipped_into_ground(self, key_list):
        # Check if character has clipped into ground
        if self.rect.y > 620:
           # if main_char
            self.rect.y = 620
            if self.is_facing_right is False and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1:
                self.character = self.character_left
            elif self.is_facing_right is True and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1:
                self.character = self.character_right
            self.rect = self.character.get_rect(
                topleft=(self.rect.x, self.rect.y))
    def check_if_hit_by_archer(self, archer_x, archer_y, archer_mask):
        archer_x_offset = self.rect.x - archer_x
        archer_y_offset = self.rect.y - archer_y
        if self.mask.overlap(archer_mask, (archer_x_offset, archer_y_offset)) != None:
            if self.mask.overlap(archer_mask, (archer_x_offset, archer_y_offset)) != None:
                if self.was_hit is False:
                    self.health -= 1
                    self.was_hit = True
        else:
            self.was_hit = False
    def check_if_hit_by_enemy2(self, enemy2_proj_x, enemy2_proj_y, enemy2_mask):
        e2_x_offset = self.rect.x - enemy2_proj_x
        e2_y_offset = self.rect.y - enemy2_proj_y
        if self.mask.overlap(enemy2_mask, (e2_x_offset , e2_y_offset)) != None:
            if self.was_hit is False:
                self.health -= 1
                self.was_hit = True
        else:
            self.was_hit = False
    def damage_taken_animation(self):
        if self.taken_damage_frame >= 7:
            self.curr_frame = 0
        else:
            self.image = self.hit_frames[math.floor(self.taken_damage_frame)]
        self.taken_damage_frame += 0.09

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