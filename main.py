# content from kids can code: http://kidscancode.org/blog/
# source: Mr. Cozort (the Goat)
# import libraries and modules
# from platform import platform
import pygame as pg
from pygame.sprite import Sprite
import random
from random import choice 
from random import randint
from hashlib import new
from itertools import count
from secrets import choice
from pygame.sprite import Sprite
import random
from random import randint, randrange
import os
from math import *
from time import *
from pathlib import Path


vec = pg.math.Vector2
# game settings, defines the width and the height of the game window
WIDTH = 900
HEIGHT = 506
FPS = 30
x= WIDTH
y= HEIGHT 

# setup asset folders here - images for game
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# player settings for the game
PLAYER_FRIC = -0.2
PLAYER_GRAV = .98
POINTS = 0

# define colors for the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 211, 67)
ORANGE = (255, 162, 0)

#draws the text for the points and prints them on the screen
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial') #prints the arial font on the screen
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# sprites...
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # this is how you use an image with a sprite....
        self.image = pg.image.load(os.path.join(img_folder, 'spongebob.png')).convert() #image for the player
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2, HEIGHT) #drops the player at the bottom of the screen
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        self.inbounds = True 
    def controls(self):
        keys = pg.key.get_pressed() #when keys gets pressed, updates onto the computer
        if keys[pg.K_a]:#moves player left
            self.acc.x = -5 #negative 5 speed because of coordinate on graph
        if keys[pg.K_d]: #when d is pressed, player moves right
            self.acc.x = 5 #player moves positivly into the coordiant
       
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        # friction for the player 
        self.acc += self.vel * PLAYER_FRIC
        # self.acc.x += self.vel.x * PLAYER_FRIC
        # self.acc.y += self.vel.y * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.midbottom = self.pos   
        
            
# here's the mobs
class Mob(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'jellyfish.png')).convert() #displays the image for sprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5 #speed of the mob
        self.initialized = False

    def update(self):
        #this caused the mob to move
        self.rect.x += self.speed*floor(randint(1,2)) #keeps mobs inbounds 
        self.rect.y += self.speed*floor(randint(1,2))
        #this is how sprites stay in bounds
        if self.rect.x > WIDTH or self.rect.x < 0: #allows mob to bounce of walls
                self.speed*=-1
        if self.rect.y > HEIGHT or self.rect.y < 0:
                self.speed*=-1
    
    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH: #makes mobs bounce of walls
            self.speed *=-1
        if not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.speed *= -1
    


# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Can Spongebob Collect All of the Jelly Fish??")
clock = pg.time.Clock()
bg_image = pg.image.load(os.path.join(img_folder, 'jellyfishfield.png')).convert()

# create a group for all sprites
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes
#creates the player class
player = Player()


# add instances to groups
all_sprites.add(player)


for i in range(8):
    #displays 8 mobs on the screen 
    # instantiate mob class repeatedly
    m = Mob(randint(0, WIDTH), randint(0,HEIGHT)) #width and height of mob
    all_sprites.add(m)
    mobs.add(m)
print(mobs)



############################ Game loop #################################
running = True
while running:
    # keep the loop running using clock
    dt = clock.tick(FPS)
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False #helps keep the game running
      
############################## Update ####################################
    # update all sprites
    all_sprites.update()
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        #prints in terminal 
        print("ive struck a mob")
        POINTS += 1
        print(POINTS)
        print("i've collided...with a mob")
        player.health -= 1
    if len(mobs) == 0:
        #when you get all of the mobs, prints "you win" in terminal 
        print("YOU WIN")
    for event in pg.event.get():
        # checks for closed window
        if event.type == pg.QUIT:
            running = False
   
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    
################################# Draw ########################################
    # draw the background screen
    screen.blit(bg_image, (0,0)) 
    # draw all sprites
    all_sprites.draw(screen)
    # draw text on screen...
    draw_text("POINTS: " + str(POINTS), 22, WHITE, WIDTH / 2, HEIGHT / 24) #draws the points onto the screen
    if POINTS>=7:
        draw_text("YOU WIN", 100, RED, WIDTH/2, HEIGHT/4)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()