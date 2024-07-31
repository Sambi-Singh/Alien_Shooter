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
star_surf =  pygame.image.load(join('images', 'star.png')).convert_alpha()

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    display_surface.fill('darkgray')
    x+=0.1

    #blit means put one surface ontop another surface
    display_surface.blit(player_surf, (x, 40))

    for star in range(20):
        display_surface.blit(star_surf,(random.randint(0, 1280), random.randint(0, 720)))
    pygame.display.update() #update is for entire screen, flip for parts of screen

pygame.quit() #Uninitialize everything to close properly