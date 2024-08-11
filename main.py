import pygame
from os.path import join 
import random

#Sprite class is just a in built class with a image and a rect
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups) # call super constructor with group arg
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(bottomright = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.player_direction = pygame.math.Vector2()
        self.player_speed = 300
    
    def update(self, dt):
         self.keys = pygame.key.get_pressed()
         self.player_direction.x = int(self.keys[pygame.K_RIGHT]) - int(self.keys[pygame.K_LEFT])
         self.player_direction.y = int(self.keys[pygame.K_DOWN]) - int(self.keys[pygame.K_UP])
         self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
         self.rect.center += self.player_speed * self.player_direction * dt

         recent_keys = pygame.key.get_just_pressed()
         if recent_keys[pygame.K_SPACE]:
             print('fire laser')



# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()
pygame.display.set_caption('Space Shooter')
# run code forever so that the screen does not close immediatley

#plain surface 
surf = pygame.Surface((100, 200)) # must attach to display surface
surf.fill('orange')
x = 100

all_sprites = pygame.sprite.Group()
player = Player(all_sprites) #Pass in groups as a constructor to player class, its automatically added to the group



star_surf =  pygame.image.load(join('images', 'star.png')).convert_alpha()

meteor_surf =  pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf =  pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))


star_pos = [(random.randint(0, 1280), random.randint(0, 720)) for i in range(20)]
while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      

   
    all_sprites.update(dt)
    # draw the game
    display_surface.fill('darkgray')
    


    for pos in star_pos:
        display_surface.blit(star_surf,pos)

        #blit means put one surface ontop another surface
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    
    #Do not used blit for sprites, instead use a group
    #display_surface.blit(player.image, player.rect)

    all_sprites.draw(display_surface)

   

    pygame.display.update() #update is for entire screen, flip for parts of screen

pygame.quit() #Uninitialize everything to close properly