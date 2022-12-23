import pygame, sys
from pygame.locals import * 
from random import randint
from math import floor

from vector2 import Vector2

SCREEN_SIZE = (640,480)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.rect = pygame.Rect(0,0,80,10)
        self.rect.midbottom = screen.get_rect().midbottom

    def update(self, time):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed * time
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_SIZE[0]:
            self.rect.x += self.speed * time
        

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = Vector2(0.25,-0.25)
        self.lives = 3
        self.movement = False
        self.rect = pygame.Rect(0,0,10,10)
        self.rect.midbottom = player.rect.midtop

    def update(self, time):
        if self.movement:
            self.rect.x += self.speed.x * time
            self.rect.y += self.speed.y * time
        else:
            self.rect.midbottom = player.rect.midtop
        self.bounce()
        self.end_game()

    def bounce(self):
        collide = pygame.sprite.spritecollide(player, balls, False, False)
        if self.rect.x < 0 or self.rect.right > SCREEN_SIZE[0]:
            self.speed.x *= -1
        if self.rect.y < 0:
            self.speed.y *= -1
        # if self.rect.bottom > player.rect.top and self.rect.left > player.rect.left and self.rect.right < player.rect.right:
        #     self.speed.y *= -1
        if collide:
            self.speed.y *= -1
        if self.rect.bottom >= SCREEN_SIZE[1]:
            self.lives -= 1
            # print('hit')
            self.movement = False
            self.rect.midbottom = player.rect.midtop
            self.speed = Vector2(0.25,-0.25)

    def end_game(self):
        if self.lives <= 0:
            sys.exit()
            

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(block_size.x * x, block_size.y * y ,block_size.x, block_size.y)
        self.health = 1

    def update(self):
        collide = pygame.sprite.groupcollide(blocks, balls, True, False)
        if collide:
            ball.speed.y *= -1


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('dash ball')

player = Player()
balls = pygame.sprite.Group()
ball = Ball()
balls.add(ball)
blocks = pygame.sprite.Group()

clock = pygame.time.Clock()

block_size = Vector2(50,10)
no_of_blocks = Vector2(floor(SCREEN_SIZE[0]/block_size.x), floor((SCREEN_SIZE[1]-200)/block_size.y))

x = 0
while x < no_of_blocks.x:
    for y in range(int(no_of_blocks.y)):
        block = Block(x,y)
        if randint(1,5) != 1:
            blocks.add(block)
    x += 1


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_q:
                sys.exit()
            if event.key == K_SPACE:
                ball.movement = True

    time_passed = clock.tick(240)


    screen.fill((20,20,20))
    pygame.draw.rect(screen,(100,100,100),player.rect)
    pygame.draw.ellipse(screen, (200,200,200), ball.rect)
    for block in blocks:
        pygame.draw.rect(screen,(170,169,173), block.rect)
    for live in range(1,ball.lives+1):
        pygame.draw.circle(screen,(200,200,200),(SCREEN_SIZE[0]-20*live, 20),5)

    player.update(time_passed)
    balls.update(time_passed)
    blocks.update()

    pygame.display.update()