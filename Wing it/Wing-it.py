from re import L
import pygame,sys
import math
pygame.init()
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, character, character_x, character_y):
        super().__init__()
        self.character = character 
        self.rect = self.character.get_rect(topleft = (character_x, character_y))
        self.mask = pygame.mask.from_surface(self.character)
        self.health = 3
        self.mask = pygame.mask.from_surface(self.character)
        self.gravity = 0
        self.infinity_frames = 30
        self.was_hit = False
        
        
    def update(window, character, character_rec):
        window.blit(character, character_rec)
#
class Player_proj(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speed = 20
        self.direction = False
        self.mask = pygame.mask.from_surface(self.image)
        
class Enemy1(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy1_large_left.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (1100, 440))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 4
        self.was_hit = False
        self.is_dead = False 
 
class Enemy1_proj(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image =  pygame.image.load('dagger_projectile_left.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x_position, 1000))
        self.speed = 15
        self.shoot = False
        self.mask = pygame.mask.from_surface(self.image)   
        
    
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
        weapon_rec = weapon.get_rect(topleft = (weapon_x, weapon_y))
        window.blit(weapon, weapon_rec)
    
def isabel_speech(window, isabel_interaction, position_x, position_y):
    if isabel_interaction < 100:
        draw_speech(window, 'Hey Kid! Stop right there.', position_x-25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 200 and isabel_interaction > 100:
        draw_speech(window, 'Where are you headed? It\'s dangerous beyond here', position_x-100, position_y+10, 15, (255,97,3))
    elif isabel_interaction < 300 and isabel_interaction > 200:
        draw_speech(window, 'Wait...', position_x+100, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 400 and isabel_interaction > 300:
        draw_speech(window, 'Are those... WINGS?', position_x+25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 500 and isabel_interaction > 400:
        draw_speech(window, 'How did a little kid like you get such a.. ', position_x+25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 600 and isabel_interaction > 500:
        draw_speech(window, 'Nevermind.  ', position_x+25, position_y+10, 25 ,(255,97,3))
    elif isabel_interaction < 700 and isabel_interaction > 600:
        draw_speech(window, ' Kid are you seriously gonna head past here?', position_x+25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 800 and isabel_interaction > 700:
        draw_speech(window, 'Into the Mist Forest?', position_x+25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 900 and isabel_interaction > 800:
        draw_speech(window, 'How are you gonna defend yourself?', position_x+25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 1000 and isabel_interaction > 900:
        draw_speech(window, 'Here take this atleast', position_x+25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 1100 and isabel_interaction > 1000:
        draw_speech(window, 'This weapon is a Ice blade staff', position_x+25, position_x+10, 25, (255,97,3))
    elif isabel_interaction < 1200 and isabel_interaction > 1100:
        draw_speech(window, 'It lets you shoot little magic ice daggers', position_x+25, position_y+10, 25, (255,97,3))
    elif isabel_interaction < 1300 and isabel_interaction > 1200:
        draw_speech(window, 'Press F to use it!', position_x+25, position_y+10, 25, (255,97,3))

def draw_screen(window, background, grass, character_x, side_1_x, side_1_right, side_1_right_rec, side_1, side_1_rec, character, character_rec, text):
    window.blit(background, (0,0))
    window.blit(grass, (0,800))
    if character_x > side_1_x:
        window.blit(side_1_right, side_1_right_rec)
    else:
        window.blit(side_1, side_1_rec)   
    window.blit(character, character_rec)
    window.blit(text, (800,0))
def draw_forest(window, character, character_rec, night_background, night_grass, tree1, 
enemy1, enemy1_rec):

    window.blit(night_background, (0,0))
    window.blit(night_grass, (0,800))
    window.blit(tree1,(660, 340))
    window.blit(character, character_rec)
    window.blit(enemy1, enemy1_rec)

def check_enemy1_range(character_x, stage_count):
    
    if character_x == 660 and stage_count == 1:
        # If character is in line with enemy1, shoot a projectile
        # at the character
        return True
    # Else do nothing
    return False
    
def draw_enemy1_proj(window, enemy1_projectile_left, enemy1_proj_rec, enemy1_projectile_x,
enemy1_projectile_speed):
    
    enemy1_proj_rec = enemy1_projectile_left.get_rect(topleft = (enemy1_projectile_x, 700))
    enemy1_projectile_x -= enemy1_projectile_speed
    if enemy1_projectile_x < -250:
        enemy1_projectile_x = 1200
    window.blit(enemy1_projectile_left, enemy1_proj_rec)
    
    return enemy1_projectile_x

def show_enemy_hp(window, enemy_health, high_hp, medium_hp, low_hp):
    if enemy_health == 3:
        window.blit(high_hp, (1200, 600)) 
    elif enemy_health == 2:
        window.blit(medium_hp, (1200, 600)) 
    elif enemy_health == 1:
        window.blit(low_hp, (1200, 600))
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
    character = pygame.image.load('characted_standing.png').convert_alpha()
    character_left = pygame.image.load('character_standing_left.png').convert_alpha()
    character_right = pygame.image.load('characted_standing.png').convert_alpha()
    
    player = Player(character, x_position, y_position)
    
    # Character Health
    character_healthfull_sprite = pygame.image.load('health_full.png')
    character_health2_hearts_sprite = pygame.image.load('health_2hearts.png')
    character_Health1_heart_sprite = pygame.image.load('health_1heart.png')
    
    # Flight sprites
    character_flying1_right = pygame.image.load('flying_frame_character.png').convert_alpha()
    character_flying1_left = pygame.image.load('flying_frame_character_left.png').convert_alpha()
    character_flying_right = [pygame.image.load('flying_frame_character.png').convert_alpha(), pygame.image.load('flying_frame2_right.png').convert_alpha()]
    character_flying_left = [pygame.image.load('flying_frame_character_left.png').convert_alpha(), pygame.image.load('flying_frame2_left.png').convert_alpha()]
    
    #Backgrounds
    grass = pygame.image.load('resize_background_2.png').convert()
    background = pygame.image.load('background_sky.png').convert()
    night_background = pygame.image.load('night_sky_starry.png').convert()
    night_grass = pygame.image.load('night_grass_updated.png').convert()
    tree1 = pygame.image.load('tree1.png').convert_alpha()
    
    # Array of walking right frames
    walking_right = [pygame.image.load('walk_frame1.png'), pygame.image.load('walking_frame2right.png')]
    walking_left = [pygame.image.load('walk_frame1_left.png'), pygame.image.load('walking_frame2left.png')]

    # Game fonts
    font = pygame.font.Font('slkscr.ttf', 50)
    text = font.render('Wing it!', False, 'White')
    
    #Side character_1
    side_1 = pygame.image.load('Isabel_Idle1.png').convert_alpha()
    side_1_rec = side_1.get_rect(topleft = (1100, 665))
    side_1_right = pygame.image.load('Isabel_Idle1_right.png').convert_alpha()
    side_1_right_rec = side_1_right.get_rect(topleft = (1050, 665))


    # Enemy 1
    enemy1 = Enemy1()
    enemy1.rect = enemy1.image.get_rect(topleft = (1100, 440))
    enemy1_projectile_x = 1100
    # Enemy 1's projectile
    enemy1_proj = Enemy1_proj(enemy1_projectile_x)
    
    enemy_full_hp = pygame.image.load('healthbar_full.png')
    enemy_high_hp = pygame.image.load('healthbar_high.png')
    enemy_medium_hp = pygame.image.load('healthbar_medium.png')
    enemy_low_hp = pygame.image.load('healthbar_low.png').convert_alpha()
    check_anim = True
    # False signifies that character is facing left, 
    # True signifies character is facing right
    check_position = False
    
    #weapon_particle
    weapon = pygame.image.load('particle_effect.png').convert_alpha()
    weapon_x = 0
    weapon_y = 0

    player_proj = Player_proj(weapon, weapon_x, weapon_y)
    

    run_program = True
    isabel_interaction = 0
    
    blit_weapon = False
    # Check if character has talked with Isabel
    # And recieved the staff.
    got_staff = False
    
   # Character movement speed 
    character_speed = 12
    walk_count = 0
    fly_count = 0
    
    stage_count = 0
    # Program game loop
    while run_program == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if player.rect.x > 1920 and stage_count == 0:
            stage_count += 1

            player.rect.x = -200
        elif player.rect.x < -300 and stage_count > 0:
            stage_count -= 1
            player.rect.x = 1900
    
        if stage_count == 0:
            draw_screen(window, background, grass, player.rect.x, side_1_rec.x, side_1_right,
                    side_1_right_rec, side_1, side_1_rec, player.character, player.rect,
                    text)
            
        elif stage_count == 1:
            draw_forest(window,player.character, player.rect, night_background, night_grass, tree1, enemy1.image, enemy1.rect)
            
            show_enemy_hp(window, enemy1.health, enemy_high_hp, enemy_medium_hp, enemy_low_hp)
            
        if player.health == 3:
            window.blit(character_healthfull_sprite, (-210,-170))
        elif player.health == 2:
            window.blit(character_health2_hearts_sprite, (-210, -170))
        elif player.health == 1:
            window.blit(character_Health1_heart_sprite, (-210, -170))
        
        key_list = pygame.key.get_pressed()
    
        if key_list[pygame.K_SPACE] == 1:
            player.gravity = -20
        # Check idle position of character
        if key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and check_position == True and player.rect.y == 660:
            player.character = character_right

        elif key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 and check_position == False and player.rect.y == 660:
            player.character = character_left
            #main_char.character = character_left
            
        # WEAPON MECHANICS
        # Shoot weapon
        if key_list[pygame.K_f] == 1:
            if check_position == False:
                player_proj.direction = False
            else:
                player_proj.direction = True
            blit_weapon = True
            weapon_x = player.rect.x
            weapon_y = player.rect.y
            if check_position == False:
                player_proj.image = pygame.image.load('particle_effect_left.png').convert_alpha()
            else:
                player_proj.image = pygame.image.load('particle_effect.png').convert_alpha()
                
            player_proj.rect = player_proj.image.get_rect(topleft = (weapon_x, weapon_y))
            player_proj.speed = 20

        player.rect.y += player.gravity
        
        # Check if character has clipped into ground
        if player.rect.y > 660:
       #if main_char
            player.rect.y = 660
            
            if check_position == False and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1 :
                player.character = character_left
            elif check_position == True and key_list[pygame.K_a] != 1 and key_list[pygame.K_d] != 1:
                player.character = character_right
            player.rect = player.character.get_rect(topleft = (player.rect.x, player.rect.y))
        
        # Jumping Mechanic
        if player.rect.y != 660:
            if check_anim == False:
                if key_list[pygame.K_SPACE] == 1 and check_position == True:
                    player.character = character_flying1_right
                    if (fly_count) > 1:
                        fly_count == 0

                    if fly_count < 2:
                        player.character = character_flying_right[math.floor(fly_count)]
                    else:
                        fly_count = 0
                    fly_count +=0.075
                elif key_list[pygame.K_SPACE] == 1 and check_position == False:
                    player.character = character_flying1_left
                    if (fly_count) > 1:
                        fly_count == 0
                    if fly_count < 2:
                        player.character = character_flying_left[math.floor(fly_count)]
                    else:
                        fly_count = 0
                    fly_count +=0.075
                elif check_position == False and key_list[pygame.K_SPACE] != 1:
                    player.character = character_flying1_left
                elif check_position == True and key_list[pygame.K_SPACE] != 1:
                    player.character = character_flying1_right
                player.rect = character.get_rect(topleft = (player.rect.x, player.rect.y))
            else:
                if check_position == False:
                    player.character = character_left
                else:
                    player.character = character_right
                player.rect = player.character.get_rect(topleft = (player.rect.x, player.rect.y))

                check_anim = False
            player.rect = player.character.get_rect(topleft = (player.rect.x, player.rect.y))
            player.gravity += 1

        # Movement Right
        if key_list[pygame.K_d] == 1:
            player.rect.left += character_speed

            if player.rect.y != 660 and key_list[pygame.K_SPACE] == 1:
                player.character = character_flying1_right
                if (fly_count) > 1:
                    fly_count == 0
                if fly_count < 2:
                    player.character = character_flying_right[math.floor(fly_count)]
                else:
                    fly_count = 0
                fly_count +=0.075
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
                walk_count +=0.1
                
                check_position = True

            player.rect = player.character.get_rect(topleft = (player.rect.x, player.rect.y))
        # Movement Left
        elif key_list[pygame.K_a] == 1:
            player.rect.left -= character_speed
            if player.rect.y != 660 and key_list[pygame.K_SPACE] == 1:
 
                player.character = character_flying1_left
                if (fly_count) > 1:
                    fly_count == 0
                if fly_count < 2:
                    player.character = character_flying_left[math.floor(fly_count)]
                else:
                    fly_count = 0
                fly_count +=0.075
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
                walk_count +=0.1
                
                check_position = False
            player.rect = player.character.get_rect(topleft = (player.rect.x,player.rect.y))
        
        isabel_proximity = calculate_isabel_proximity(player.rect.x, player.rect.y, 
        side_1_rec.x ,side_1_rec.y)
        
        if isabel_proximity == True and stage_count == 0:
            if key_list[pygame.K_RIGHT] == 1:
                isabel_interaction+= 100
            
            isabel_speech(window, isabel_interaction, side_1_rec.x, side_1_rec.y)
            if isabel_interaction < 1400 and isabel_interaction > 1300:
                draw_speech(window, 'I dont like the idea of a kid like you gettin hurt', side_1_rec.x+25, side_1_rec.y+10, 25, (255,97,3))
                character_got_item = pygame.image.load('obtained_staff.png').convert_alpha()
                # Character has gotten the staff
                # and can now use it
                got_staff = True
                player.character = character_got_item
                player.rect = player.character.get_rect(topleft = (player.rect.x, player.rect.y))
                
            elif isabel_interaction < 1500 and isabel_interaction > 1400:
                player.character = character_right 
                player.rect = character.get_rect(topleft = (player.rect.x, player.rect.y))
                draw_speech(window, 'Now get outta here!', side_1_rec.x+25, side_1_rec.y+10, 25, (255,97,3))
  
            isabel_interaction += 1
       
        # Projectile acceleration
        player_proj.speed = projectile_acceleration(player_proj.speed, 1.01)
        
        # Modify x_value of projectile 
        weapon_x = move_projectile(player_proj.direction, weapon_x, player_proj.speed)

        # Replay dialogue interaction
        if isabel_proximity == True and key_list[pygame.K_RETURN] == 1:
            isabel_interaction = 0
        
        # Shoot weapon
        if blit_weapon == True and got_staff == True:
            player_proj.rect = player_proj.image.get_rect(topleft = (weapon_x, weapon_y))
            window.blit(player_proj.image, player_proj.rect)
            offset = (enemy1.rect.x - player_proj.rect.x), (enemy1.rect.y - player_proj.rect.y)
            if player_proj.mask.overlap(enemy1.mask, (offset)) != None and stage_count == 1:
                
                if enemy1.was_hit == False:
                    enemy1.health -= 1
                    enemy1.was_hit = True
                
            else:
                enemy1.was_hit = False
                
        shoot_enemy_weap = check_enemy1_range(player.rect.y, stage_count)
        if shoot_enemy_weap == True:
            enemy1_proj.shoot = True
        # Shoot enemy weapon
        if enemy1_proj.shoot == True:
            enemy1_proj.rect = enemy1_proj.image.get_rect(topleft = (enemy1_projectile_x, 1000))

            #player.rect = player.character.get_rect(topleft = (player.rect.x, player.rect.y))
            
            x_offset = player.rect[0]- enemy1_proj.rect[0] 
            y_offset = player.rect.y - enemy1_proj.rect.y

            if player.mask.overlap(enemy1_proj.mask, (x_offset,0)) != None and player.rect.y == 660:
                if player.was_hit == False:
                    player.health -= 1
                    player.was_hit = True   
            else:
                player.was_hit = False      
            enemy1_projectile_x = draw_enemy1_proj(window, enemy1_proj.image, enemy1_proj.rect, enemy1_projectile_x, 
            enemy1_proj.speed)
            enemy1_proj.rect = enemy1_proj.image.get_rect(topleft = (enemy1_projectile_x, 1000))
            if enemy1_projectile_x < -250:
                enemy1_proj.shoot = False
                
            
        pygame.display.update()  
        clock.tick(60)
 
if __name__ == "__main__":
    main()
        

