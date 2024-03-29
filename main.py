from contextlib import redirect_stderr
import sys
import pygame
import random
from pygame.locals import *
from Button import Button

pygame.init()
vec = pygame.math.Vector2   #Two Demenstion 

screenWidth = 900
screenHeight = 600
ACC = 0.5
FRIC = -0.09
FPS = 60

win_sound = pygame.mixer.Sound("assets/fanfare.wav")

FramePerSecond = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
MBG = pygame.image.load("assets/mainmenu.jpg")
BG = pygame.image.load("assets/background.jpg")
window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("2D Game")
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png")
        self.surf = pygame.image.load("assets/player.png")
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        self.immunity_frames = 0

    def move(self):
        self.acc = vec(0,0.5)
 
        pressed_keys = pygame.key.get_pressed()
            
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC 

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
     
        self.rect.midbottom = self.pos
        
        self.jumping = False

    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False

        if hits:
            if self.pos.y < hits[0].rect.bottom and hits[0].color == 'w':
                win()

        if self.immunity_frames > 0:
            self.immunity_frames -= 1
            if self.immunity_frames % 2 == 0:
                self.surf.set_alpha(0)
            else: 
                self.surf.set_alpha(255)
        else:
            self.surf.set_alpha(255)

        if P1.vel.x > 0:
            self.image = pygame.image.load("assets/player.png")
            self.surf = pygame.image.load("assets/player.png")
        elif P1.vel.x < 0:
            self.image = pygame.image.load("assets/player2.png")
            self.surf = pygame.image.load("assets/player2.png")
                

class platform(pygame.sprite.Sprite):

    def __init__(self,x,y,posx,posy,color):
        w,h,Posx,PosY,c= x,y,posx,posy,color
        if c == 'r':
            c = (0,0,0)
        if c == 'g':
            c = (112,128,144)
        if c == 'b':
            c = (105,105,105)
        if c == 'w':
            c = (255,255,255)
            

        super().__init__()
        self.color = color
        self.surf = pygame.Surface((w, h))
        self.surf.fill(c)
        self.rect = self.surf.get_rect(center = ((Posx,PosY)))
        
        all_sprites.add(self)   
        platforms.add(self)
  
    def move(self):
        pass

class Trap(pygame.sprite.Sprite):
    '''
    Class that will create traps that will hurt the player (works similar to platform)
    '''
    def __init__(self,x,y,platform,c):
        color = c
        super().__init__()
        self.surf = pygame.Surface((x, y))
        self.surf.fill((255,255,0))
        self.color = color
        self.rect = self.surf.get_rect()
        self.platform = platform
        self.rect.midbottom = self.platform.rect.midtop
        
        all_sprites.add(self)   
        platforms.add(self)

    def move(self):
        pass

#Level 1 Generation*******************************************************
PT1 = platform(screenWidth , 20,0,screenHeight,'g') # base platform
PT2 = platform(200,200,200,500,'b')
PT3 = platform(200,300,400,465,'b')
PT4 = platform(300,400,600,400,'b')
PT5 = platform(500,400,1200,400,'b')
platform(100,200,1600,200,'b')
platform(100,200,1800,400,'b')
platform(100,200,2000,400,'b')
platform(500,30,2720,400,'b')
platform(475,30,3000,300,'b')
platform(475,30,3300,400,'b')
platform(500,40,4090,170,'w') # level 1 end goal
platform(200,40,4600,470,'b')
platform(200,40,4800,330,'b')
platform(40,40,4500,270,'b')
platform(600,1000,5100,470,'b')
#*************************************************
# Testing player, traps, and sprites, etc.
Players = pygame.sprite.Group()
traps = pygame.sprite.Group() 

P1 = Player()
all_sprites.add(P1)
platforms.add(PT1)

trap1 = Trap(25, 25, PT3,1)
trap2 = Trap(50, 50, PT4,1)
trap3 = Trap(20, 20, PT2,1)
trap4 = Trap(50, 50, PT5,1)

traps.add(trap1)
traps.add(trap2)
traps.add(trap3)
traps.add(trap4)

for trap in traps:
    all_sprites.add(trap)

def play():

    while True:

        window.fill("black")

        window.blit(BG, (0, 0))

        hits = pygame.sprite.spritecollide(P1, traps, False)
        for event in pygame.event.get():
            if event.type == QUIT:
             pygame.quit()
             sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    P1.jump()
        if hits and P1.immunity_frames == 0:
            P1.health -= 50
            P1.immunity_frames = 60

        P1.update()

        for entity in all_sprites:
             window.blit(entity.surf, entity.rect)
             entity.move()       


        health_text = font.render(f"Health: {P1.health}", True, (255, 255, 255))
        window.blit(health_text, (10,10))

        if P1.rect.right <= screenWidth / 5:
            P1.pos.x += abs(P1.vel.x)
            for plat in platforms:
                plat.rect.x += abs(P1.vel.x)
                PT1.surf = pygame.Surface((screenWidth, 20))
                PT1.surf.fill((112,128,144))
                PT1.rect = PT1.surf.get_rect(center = (screenWidth/2, screenHeight - 10))

        if P1.rect.left >= screenWidth / 3:
            P1.pos.x -= abs(P1.vel.x)
            for plat in platforms:
                plat.rect.x -= abs(P1.vel.x)
                PT1.surf = pygame.Surface((screenWidth, 20))
                PT1.surf.fill((112,128,144))
                PT1.rect = PT1.surf.get_rect(center = (screenWidth/2, screenHeight - 10))

        if P1.health <= 0:
            game_over_surf = pygame.Surface((screenWidth, screenHeight))
            game_over_surf.fill((0,0,0))
            game_over_text = font.render("GAME OVER", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(screenWidth/2, screenHeight/2))
            game_over_surf.blit(game_over_text, game_over_rect)
            window.blit(game_over_text, (screenWidth/2 - 70, screenHeight/2 - 20))
            window.blit(game_over_surf, (0,0))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        pygame.display.update()
        FramePerSecond.tick(FPS)

def main_menu():

    while True:   

        window.blit(MBG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Working Title", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(450, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(450, 450), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def win():
    game_over_surf = pygame.Surface((screenWidth, screenHeight))
    game_over_surf.fill((155,25,34))
    game_over_text = font.render("YOU WIN!", True, (255, 255, 255))
    pygame.mixer.Sound.play(win_sound)
    pygame.mixer.music.stop()
    game_over_rect = game_over_text.get_rect(center=(screenWidth/2, screenHeight/2))
    game_over_surf.blit(game_over_text, game_over_rect)
    window.blit(game_over_text, (screenWidth/2 - 70, screenHeight/2 - 20))
    window.blit(game_over_surf, (0,0))
    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()
main_menu()     