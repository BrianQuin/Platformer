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
FRIC = -0.12
FPS = 60

FramePerSecond = pygame.time.Clock()

window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("2D Game")
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

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
    
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
                

class platform(pygame.sprite.Sprite):
    def __init__(self,x,y,posx,posy):
        w,h,Posx,PosY = x,y,posx,posy
        super().__init__()
        self.surf = pygame.Surface((w, h))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = ((Posx,PosY)))
        
        all_sprites.add(self)   
        platforms.add(self)
    def move(self):
        pass

#Level 1 Generation*******************************************************
PT1 = platform(screenWidth , 20,0,screenHeight) # base platform
platform(200,20,200,400)
platform(400,20,400,300)
platform(300,400,600,400)
platform(500,400,1200,400)
platform(100,200,1600,200)
platform(100,200,1800,400)
platform(100,200,2000,400)
platform(500,30,2720,400)
#*************************************************

P1 = Player()
all_sprites.add(P1)
platforms.add(PT1)

   
def play():

    while True:

        window.fill("black")

        for event in pygame.event.get():
            if event.type == QUIT:
             pygame.quit()
             sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    P1.jump()

        window.fill((0,0,0))
        P1.update()

        for entity in all_sprites:
             window.blit(entity.surf, entity.rect)
             entity.move()       

        if P1.rect.right <= screenWidth / 5:
            P1.pos.x += abs(P1.vel.x)
            for plat in platforms:
                plat.rect.x += abs(P1.vel.x)
                PT1.surf = pygame.Surface((screenWidth, 20))
                PT1.surf.fill((255,0,0))
                PT1.rect = PT1.surf.get_rect(center = (screenWidth/2, screenHeight - 10))

        if P1.rect.left >= screenWidth / 3:
            P1.pos.x -= abs(P1.vel.x)
            for plat in platforms:
                plat.rect.x -= abs(P1.vel.x)
                PT1.surf = pygame.Surface((screenWidth, 20))
                PT1.surf.fill((255,0,0))
                PT1.rect = PT1.surf.get_rect(center = (screenWidth/2, screenHeight - 10))

        pygame.display.update()
        FramePerSecond.tick(FPS)

def main_menu():

    while True:   

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
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
main_menu()     