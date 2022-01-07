import pygame,sys
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1920, 1080))
window.fill((0,0,0))

pygame.display.set_caption('Wing It!')
surface = pygame.Surface((100, 200))
background = pygame.image.load('Pygame_background.png')
character = pygame.image.load('character_outlined.png')
grass = pygame.image.load('Background_Grass.png')

font = pygame.font.Font('slkscr.ttf', 50)
text = font.render('Wing it!', False, 'White')


def main():
    x_position = 100
    y_position = 700
    run_program = True
    while run_program == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        window.blit(grass, (0,820))
        window.blit(character, (x_position,y_position))
        window.blit(text, (720,0))
        x_position += 1
        
        
        pygame.display.update()  
        pygame.display.flip()
        clock.tick(60)
 
        
        

    
if __name__ == "__main__":
    main()
        

