import pygame
from os.path import join 
import random

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')
# run code forever so that the screen does not close immediatley

#plain surface 
surf = pygame.Surface((100, 200)) # must attach to display surface
surf.fill('orange')
x = 100


# importing an image 
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(bottomright = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))



star_surf =  pygame.image.load(join('images', 'star.png')).convert_alpha()

meteor_surf =  pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf =  pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (0,0))

star_pos = [(random.randint(0, 1280), random.randint(0, 720)) for i in range(20)]
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    display_surface.fill('darkgray')
    


    for pos in star_pos:
        display_surface.blit(star_surf,pos)

        #blit means put one surface ontop another surface
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(player_surf, player_rect)
    display_surface.blit(laser_surf, laser_rect)


    if player_rect.right < WINDOW_WIDTH:
     player_rect.left += 0.2
   

    pygame.display.update() #update is for entire screen, flip for parts of screen

pygame.quit() #Uninitialize everything to close properly