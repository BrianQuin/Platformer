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
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,screenWidth-10), random.randint(0, screenHeight-30)))


    def move(self):
        pass

PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

for x in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)

   
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