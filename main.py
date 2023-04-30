import sys
import pygame
from pygame.locals import *

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

        if self.pos.x > screenWidth:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screenWidth
     
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

    def move(self):
        pass

PT1 = platform(screenWidth , 20,0,screenHeight)
P1 = Player()

PT2 = platform(200,20,200,400)

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
all_sprites.add(PT2)

platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)
while True:
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