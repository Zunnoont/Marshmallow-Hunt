import pygame,sys
pygame.init()
clock = pygame.time.Clock()

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
   
# Main function of Wing It!
def main():
    # Pygame Window
    x_position = 100
    y_position = 660
    window = pygame.display.set_mode((1920, 1080))
    window.fill(('White'))

    # Game name
    pygame.display.set_caption('Wing It!')
    
    #Basic surface
    surface = pygame.Surface((100, 200))
    
    # Character Sprites
    character = pygame.image.load('characted_standing.png').convert_alpha()
    character_left = pygame.image.load('character_standing_left.png').convert_alpha()
    character_right = pygame.image.load('characted_standing.png').convert_alpha()
    character_get_beginner_weap = pygame.image.load('got_weapon.png').convert_alpha()
    
    # Flight sprites
    character_flying1_right = pygame.image.load('flying_frame_character.png')
    character_flying1_left = pygame.image.load('flying_frame_character_left.png')
    
    #Character rectangle
    character_rec = character.get_rect(topleft = (x_position,y_position))
    
    #Backgrounds
    grass = pygame.image.load('resize_background_2.png').convert()
    background = pygame.image.load('background_sky.png').convert()
    tree1 = pygame.image.load('tree1.png').convert()
    
    # Array of walking right frames
    walking_right = [pygame.image.load('frame1_walking_right.png'), pygame.image.load('frame2_walking_right.png')]

    # Game fonts
    font = pygame.font.Font('slkscr.ttf', 50)
    text = font.render('Wing it!', False, 'White')
    
    #Side character_1
    side_1 = pygame.image.load('Isabel_Idle1.png').convert_alpha()
    side_1_rec = side_1.get_rect(topleft = (1100, 665))
    side_1_right = pygame.image.load('Isabel_Idle1_right.png').convert_alpha()
    side_1_right_rec = side_1_right.get_rect(topleft = (1050, 665))


    check_anim = True
    
    # False signifies that character is facing left, 
    # True signifies character is facing right
    check_position = False
    
    #weapon_particle
    weapon = pygame.image.load('particle_effect.png').convert_alpha()
    weapon_x = 0
    weapon_y = 0
    weapon_rec = weapon.get_rect(topleft = (0,0))
    projectile_speed = 20
    weapon_direc = False
    
    player_gravity = 0
    run_program = True
    isabel_interaction = 0
    
    blit_weapon = False
    # Check if character has talked with Isabel
    # And recieved the staff.
    got_staff = False
    
   # Character movement speed 
    character_speed = 12

    while run_program == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        window.blit(background, (0,0))
        window.blit(grass, (0,800))
        if character_rec.x > side_1_rec.x:
            window.blit(side_1_right, side_1_right_rec)
        else:
            window.blit(side_1, side_1_rec)
            
        window.blit(character, character_rec)
        window.blit(text, (800,0))

        key_list = pygame.key.get_pressed()
        
         
        if key_list[pygame.K_SPACE] == 1:
            player_gravity = -20

        # WEAPON MECHANICS
        # Shoot ice weapon
        if key_list[pygame.K_f] == 1:
            if check_position == False:
                weapon_direc = False
            else:
                weapon_direc = True
            blit_weapon = True
            weapon_y = character_rec.y
            weapon_x = character_rec.x
            if check_position == False:
                weapon = pygame.image.load('particle_effect_left.png')
            else:
                weapon = pygame.image.load('particle_effect.png').convert_alpha()
                
            weapon_rec = weapon.get_rect(topleft = (weapon_x, weapon_y))
            projectile_speed = 15

        character_rec.y += player_gravity
        
        # Check if character has clipped into ground
        if character_rec.y > 660:
            character_rec.y = 660
            if check_position == False:
                character = character_left
            elif check_position == True:
                character = character_right
            character_rec = character.get_rect(topleft = (character_rec.x,character_rec.y))
        
        # Jumping Mechanic
        if character_rec.y != 660:
            if check_anim == False:
                if check_position == False:
                    character = character_flying1_left
                else:
                    character = character_flying1_right
                character_rec = character.get_rect(topleft = (character_rec.x,character_rec.y))
                check_anim == True
            else:
                if check_position == False:
                    character = character_left
                else:
                    character = character_right
                character_rec = character.get_rect(topleft = (character_rec.x,character_rec.y))

                check_anim = False
                
            character_rec = character.get_rect(topleft = (character_rec.x,character_rec.y))
            player_gravity += 1

        # Movement
        if key_list[pygame.K_d] == 1:
            character_rec.left += character_speed

            if character_rec.y != 660:
                character = character_flying1_right
                check_position = True

            else:
                character = character_right
                check_position = True

            character_rec = character.get_rect(topleft = (character_rec.x,character_rec.y))
        elif key_list[pygame.K_a] == 1:
            character_rec.left -= character_speed
            if character_rec.y != 660:
 
                character = character_flying1_left
                check_position = False
            else:
                character = character_left
                check_position = False
            character_rec = character.get_rect(topleft = (character_rec.x,character_rec.y))
        
        isabel_proximity = calculate_isabel_proximity(character_rec.x, character_rec.y, 
        side_1_rec.x ,side_1_rec.y)
        if isabel_proximity == True:
            if key_list[pygame.K_RIGHT] == 1:
                isabel_interaction+= 100
            
            isabel_speech(window, isabel_interaction, side_1_rec.x, side_1_rec.y)
            if isabel_interaction < 1400 and isabel_interaction > 1300:
                draw_speech(window, 'I dont like the idea of a kid like you gettin hurt', side_1_rec.x+25, side_1_rec.y+10, 25, (255,97,3))
                character_got_item = pygame.image.load('got_weapon.png').convert_alpha()
                # Character has gotten the staff
                # and can now use it
                got_staff = True
                got_item_x = character_rec.x
                got_item_y = character_rec.y
                character = character_got_item
                character_rec = character.get_rect(topleft = (got_item_x,got_item_y))
                
                #draw_speech(window, 'You got the Apprentice Ice Rod!', 500, 200, 50)
            elif isabel_interaction < 1500 and isabel_interaction > 1400:
                character = character_right 
                character_rec = character.get_rect(topleft = (character_rec.x, character_rec.y))

                draw_speech(window, 'Now get outta here!', side_1_rec.x+25, side_1_rec.y+10, 25, (255,97,3))
                   
                
            isabel_interaction += 1
            
        # Projectile acceleration
        projectile_speed = projectile_speed * 1.01
        # Modify x_value of projectile 
        if weapon_direc == False:
            weapon_x -= projectile_speed
        elif weapon_direc == True:
            weapon_x += projectile_speed
            
                
        if isabel_proximity == True and key_list[pygame.K_RETURN] == 1:
            isabel_interaction = 0
            
        if blit_weapon == True and got_staff == True:
            
            weapon_rec = weapon.get_rect(topleft = (weapon_x, weapon_y))
            window.blit(weapon, weapon_rec)
                
            
            
        pygame.display.update()  
        clock.tick(60)
 
        
if __name__ == "__main__":
    main()
        


        
        

    


