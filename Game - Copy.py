import pygame
from pygame.locals import *
import sys
from os.path import *
import random
import time
from tkinter import filedialog
from tkinter import *


pygame.init() 
pygame.font.init()
# Begin pygame
 
# Declaring variables to be used through th e program
# ACC and FRIC are for acceleration and friction respectively, which we’ll use while creating the physics for our game.
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60 
# FPS:In simpler words it defines how many times the game loop will run in a single second.
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
#collision 
hit_cooldown = pygame.USEREVENT + 1
#######################
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game-of-Champion")

'''
up line creates the display for our pygame 
video using the height and width we defined earlier. 
The second line just changes the title of the window 
from it’s default
'''
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255) 

#a font
headingfont = pygame.font.SysFont("Verdana", 40)
regularfont = pygame.font.SysFont('Corbel',25)
smallerfont = pygame.font.SysFont('Corbel',16) 
text = regularfont.render('LOAD' , True , color_light)

# Run animation RIGHT
run_ani_R = [pygame.image.load('Player_Sprite_R.png'), pygame.image.load('Player_Sprite2_R.png'),
             pygame.image.load('Player_Sprite3_R.png'),pygame.image.load('Player_Sprite4_R.png'),
             pygame.image.load('Player_Sprite5_R.png'),pygame.image.load('Player_Sprite6_R.png'),
             pygame.image.load('Player_Sprite_R.png')]

# Run animation LEFT
run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
             pygame.image.load("Player_Sprite3_L.png"),pygame.image.load("Player_Sprite4_L.png"),
             pygame.image.load("Player_Sprite5_L.png"),pygame.image.load("Player_Sprite6_L.png"),
             pygame.image.load("Player_Sprite_L.png")]

# Attack RIGHT
attack_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Attack_R.png"),
                pygame.image.load("Player_Attack2_R.png"),pygame.image.load("Player_Attack2_R.png"),
                pygame.image.load("Player_Attack3_R.png"),pygame.image.load("Player_Attack3_R.png"),
                pygame.image.load("Player_Attack4_R.png"),pygame.image.load("Player_Attack4_R.png"),
                pygame.image.load("Player_Attack5_R.png"),pygame.image.load("Player_Attack5_R.png"),
                pygame.image.load("Player_Sprite_R.png")]
 
# Attack LEFT
attack_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Attack_L.png"),
                pygame.image.load("Player_Attack2_L.png"),pygame.image.load("Player_Attack2_L.png"),
                pygame.image.load("Player_Attack3_L.png"),pygame.image.load("Player_Attack3_L.png"),
                pygame.image.load("Player_Attack4_L.png"),pygame.image.load("Player_Attack4_L.png"),
                pygame.image.load("Player_Attack5_L.png"),pygame.image.load("Player_Attack5_L.png"),
                pygame.image.load("Player_Sprite_L.png")]

  

# Background 
# PART 1 
class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            #bgimage : tres important c'est a partir d'ici que tu charges l'image
            self.bgimage = pygame.image.load('114.png')        
            self.bgY = 0 
            #Le self.bgYet self.bgXstockent la position X et Y de l'arrière-plan.
            self.bgX = 0
            #render()qui est utilisée pour afficher l'image d'arrierePlan dans la fenêtre pygame
      def render(self):
            displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


#Creating the Ground
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect = self.image.get_rect(center = (350, 350))
 
    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y)) 
        #Using self.rect.x and self.rect.y we can return the X and Y positions of the rectangle object to the blit() method.
      
        
#class player######
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()
         #self.direction is used to store the current direction of the Player. By default we have kept the player facing right

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))  #self.pos is for the position of the player.
        self.vel = vec(0,0) #self.vel is for the velocity of the player
        self.acc = vec(0,0)  #self.acc is for the acceleration of the player. 
        self.direction = "RIGHT"
       
        # Movement 
        self.jumping = False
        self.running = False
        self.move_frame = 0

        # Combat
        self.attacking = False
        self.cooldown = False 
        self.attack_frame = 0


    def move(self):
          # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
          self.acc = vec(0,0.5)

          if abs(self.vel.x) > 0.3:
                self.running = True
          else:
                self.running = False

          # Returns the current key presses
          pressed_keys = pygame.key.get_pressed()

          
          if pressed_keys[K_LEFT]:
                self.acc.x = -ACC
          if pressed_keys[K_RIGHT]:
                self.acc.x = ACC 

          
          self.acc.x += self.vel.x * FRIC
          self.vel += self.acc
          self.pos += self.vel + 0.5 * self.acc  

          
          if self.pos.x > WIDTH:
                self.pos.x = 0
          if self.pos.x < 0:
                self.pos.x = WIDTH
          
          self.rect.midbottom = self.pos              

    def gravity_check(self):
          hits = pygame.sprite.spritecollide(player ,ground_group, False)
          if self.vel.y > 0:
              if hits:
                  lowest = hits[0]
                  if self.pos.y < lowest.rect.bottom:
                      self.pos.y = lowest.rect.top + 1
                      self.vel.y = 0
                      self.jumping = False

                  
    def update(self):
          
          if self.move_frame > 6:
                self.move_frame = 0
                return

         
          if self.jumping == False and self.running == True:  
                if self.vel.x > 0:
                      self.image = run_ani_R[self.move_frame]
                      self.direction = "RIGHT"
                else:
                      self.image = run_ani_L[self.move_frame]
                      self.direction = "LEFT"
                self.move_frame += 1

         
          if abs(self.vel.x) < 0.2 and self.move_frame != 0:
                self.move_frame = 0
                if self.direction == "RIGHT":
                      self.image = run_ani_R[self.move_frame]
                elif self.direction == "LEFT":
                      self.image = run_ani_L[self.move_frame]

    def attack(self):
         if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
 
   
         if self.direction == "RIGHT":
                  self.image = attack_ani_R[self.attack_frame]
         elif self.direction == "LEFT":
                  self.correction()
                  self.image = attack_ani_L[self.attack_frame] 
      
          
         self.attack_frame += 1


    def jump(self):
        self.rect.x += 1

        
        hits = pygame.sprite.spritecollide(self, ground_group, False) # help Check to see if payer is in contact with the ground
        
        self.rect.x -= 1

        
        if hits and not self.jumping:
           self.jumping = True 
           self.vel.y = -12

    def correction(self):
      # Function is used to correct an error
      # with character position on left attack frames
         if self.attack_frame == 1:
            self.pos.x -= 20
         if self.attack_frame == 10:
            self.pos.x += 20

#CLASS ENEMY
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("Enemy.png")
            self.rect = self.image.get_rect()     
            self.pos = vec(0,0)
            self.vel = vec(0,0)

            self.direction = random.randint(0,1) # 0 for Right, 1 for Left
            self.vel.x = random.randint(2,6) / 2 
            
            if self.direction == 0:
                  self.pos.x = 0
                  self.pos.y = 235
            if self.direction == 1:
                  self.pos.x = 700
                  self.pos.y = 235
            
      

      def move(self):
            if self.pos.x >= (WIDTH-20):  # Causes the enemy to change directions    
                  self.direction = 1
            elif self.pos.x <= 0:
                  self.direction = 0
                
            if self.direction == 0:
                  self.pos.x += self.vel.x
            if self.direction == 1:
                  self.pos.x -= self.vel.x
            
            self.rect.center = self.pos # Updates rect    
        
      def render(self):
            displaysurface.blit(self.image,(self.pos.x,self.pos.y))
      
      def player_hit(self):
            if self.cooldown == False:    
                  self.cooldown = True
                  pygame.time.set_timer(hit_cooldown, 1000) 
                  
                  print("hit")
                  pygame.display.update()

      def update(self):
      
            hits = pygame.sprite.spritecollide(self, Playergroup, False)
 
      
            if hits and player.attacking == True:
                  self.kill()
                  #print("Enemy killed")
      
                     
            elif hits and player.attacking == False:
                  self.player_hit()



###### VERY IMPORTANT FOR THIS PROGRAMM #####           
background = Background()
ground = Ground()

enemy = Enemy()
player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

ground_group = pygame.sprite.Group()
ground_group.add(ground)






##### END #####

while True:
    player.gravity_check() 
      
    for event in pygame.event.get():
        # Will run when the close window button is clicked    
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
            
        # For events that occur upon clicking the mouse (left click) 
        if event.type == pygame.MOUSEBUTTONDOWN:
              pass


        # Event handling for a range of different key presses    
        if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                    player.jump()
              if event.key == pygame.K_RETURN:
                  if player.attacking == False:
                        player.attack()
                        player.attacking = True 
                        
        if event.type == hit_cooldown:
              player.cooldown = FALSE
              pygame.time.set_timer(hit_cooldown, 0)
                    
    player.update()   
    if player.attacking==True:
          player.attack()       
    player.move()
    background.render()
    ground.render()
    
    displaysurface.blit(player.image, player.rect)

    enemy.update()
    enemy.move()
    enemy.render()

    pygame.display.update()      
    FPS_CLOCK.tick(FPS)

