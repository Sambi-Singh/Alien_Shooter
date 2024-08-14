import pygame
from os.path import join 
from random import randint, uniform

#Sprite class is just a in built class with a image and a rect
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups) # call super constructor with group arg

        self.image= pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(bottomright = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.player_direction = pygame.math.Vector2()
        self.player_speed = 300

        # cool down
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        self.rotation = 0
        #transform test
        #self.image = pygame.transform.scale2x(self.image) # transforming too much reduces image quality
        # mask
        # self.mask = pygame.mask.from_surface(self.image)
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            print(current_time)
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    def update(self, dt):
         self.keys = pygame.key.get_pressed()
         self.player_direction.x = int(self.keys[pygame.K_RIGHT]) - int(self.keys[pygame.K_LEFT])
         self.player_direction.y = int(self.keys[pygame.K_DOWN]) - int(self.keys[pygame.K_UP])
         self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
         self.rect.center += self.player_speed * self.player_direction * dt

         recent_keys = pygame.key.get_just_pressed()
         if recent_keys[pygame.K_SPACE] and self.can_shoot:
             Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
             laser_sound.play()
             self.can_shoot = False
             self.laser_shoot_time = pygame.time.get_ticks()
        
         self.laser_timer()

        #  #continuous rotation
        #  self.rotation += 20* dt
        #  self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
    
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
        
        
        

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf,pos, groups):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image
        self.rect = self.image.get_frect(center = pos)
        self.speed = randint(400, 500)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation_speed = randint(40, 80)
        self.rotation_angle = 0

    
    def update(self, dt):
        
        self.rect.center += self.direction * self.speed * dt
        self.rotation_angle += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation_angle, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frames_index += 20 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()
def collisions():
    global running 

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)

        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()


def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)

    #Now draw the box around the text rect 
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20,10).move(0,-8), width = 5, 
                     border_radius= 10)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()
pygame.display.set_caption('Space Shooter')
# run code forever so that the screen does not close immediatley

#plain surface 

all_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites) #Pass in groups as a constructor to player class, its automatically added to the group

meteor_surf =  pygame.image.load(join('images', 'meteor.png')).convert_alpha()

laser_surf =  pygame.image.load(join('images', 'laser.png')).convert_alpha()

font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
text_surf = font.render('text', True, (240, 240, 240))

explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range (21)]

#sounds 
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.3)
game_music.play(loops = -1)  # -1 plays music indefinetly


# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf,(x, y), (all_sprites, meteor_sprites))
      

    all_sprites.update(dt)
    #collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    # destroy_asteroids = pygame.sprite.groupcollide(laser_sprites, meteor_sprites, True, True)
    
    # if collision_sprites:
    #     print(collision_sprites[0])
    
    
    collisions()
    #Determine if laser hit asteroid, if it does then kill both laser and asteroid 
    
    # draw the game
    display_surface.fill('#3a2e3f')
    


    

        #blit means put one surface ontop another surface    
    #Do not used blit for sprites, instead use a group
    #display_surface.blit(player.image, player.rect)
    all_sprites.draw(display_surface)
    

    display_score()


    pygame.display.update() #update is for entire screen, flip for parts of screen

pygame.quit() #Uninitialize everything to close properly