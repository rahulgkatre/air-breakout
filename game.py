import numpy as np
import cv2
import time

def vision(pos, q):
    cap = cv2.VideoCapture(0)
    width =  cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    x_vals = []
    frame_rate = 30
    prev = 0

    while True:
        if len(x_vals) == 10:
            x_vals.clear()

        time_elapsed = time.time() - prev
        ret, frame = cap.read()

        if time_elapsed > 1./frame_rate:
            prev = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
            
            lower = np.array([20, 100, 100]) 
            upper = np.array([30, 255, 255]) 
        
            mask = cv2.inRange(hsv, lower, upper)
            contours = cv2.findContours(image = mask, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE)[0]
            cv2.drawContours(image = mask, contours = contours, contourIdx = -1, color = (0, 0, 255), thickness = 5)
            blob = cv2.flip(mask, 1)

            if cv2.findNonZero(blob) is not None:
                x_vals.append(cv2.findNonZero(blob)[0][0][0])
            x = np.array(x_vals)

            if not math.isnan(np.median(x)) and not math.isnan(np.median(y)):
                pos = int(np.median(x))
                q.put(pos)
            
            # cv2.imshow('mask', cv2.flip(mask, 1)) 
            # cv2.imshow('frame', cv2.flip(frame, 1)) 
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()

    cap.release()
    cv2.destroyAllWindows()

import math
import pygame
import os

x = int((1920 - 640)/2)
y = int((1080 - 480)/2)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
 
black = (0, 0, 0)
white = (255, 255, 255)

blockcount = 8
block_height = 20
block_width = (640 - 2 * blockcount) / blockcount

class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        
        self.image = pygame.Surface([block_width, block_height])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
 
class Ball(pygame.sprite.Sprite):
    speed = 5.0
    x = 0
    y = 240
 
    direction = 200
    width = 10
    height = 10
 
    def __init__(self):
        super().__init__()
 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
 
    def update(self):
        direction_radians = math.radians(self.direction)
 
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        self.rect.x = self.x
        self.rect.y = self.y
 
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
 
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
 
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
 
        if self.y > 480:
            return True
        else:
            return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 
        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))
 
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height
 
    def update(self, pos):        
        self.rect.x = pos
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                return True

def breakout(pos, q):
    win = False
    pygame.init()
    
    clock = pygame.time.Clock()
    game_over = False
    exit_program = False
    main_menu = True
    
    while not exit_program:
        screen = pygame.display.set_mode([640, 480])
        screen.fill(black)
        pygame.display.set_caption('Breakout')
        pygame.mouse.set_visible(0)
        font = pygame.font.Font(None, 36)
        background = pygame.Surface(screen.get_size())
        
        blocks = pygame.sprite.Group()
        balls = pygame.sprite.Group()
        allsprites = pygame.sprite.Group()
        
        player = Player()
        allsprites.add(player)
        
        ball = Ball()
        allsprites.add(ball)
        balls.add(ball)

        top = 20

        for row in range(4):
            for column in range(0, blockcount):
                block = Block(white, column * (block_width + 2), top)
                blocks.add(block)
                allsprites.add(block)
            top += block_height + 2

        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True

        replay = False
        if main_menu:
            text = font.render("Air Breaker", True, white)
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 240 - 18
            screen.blit(text, textpos)

            text = font.render("Press SPACE to continue or Q to quit", True, white)
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 240 + 18
            screen.blit(text, textpos)

            pygame.display.flip()        

            choice_made = False
            while not choice_made:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            exit()
                        if event.key == pygame.K_SPACE:
                            main_menu = False
                            choice_made = True
                            game_over = False
                            break

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program = True

            clock.tick(30)
            screen.fill(black)

            pos = q.get()
            player.update(pos)
            game_over = ball.update()

            if game_over:
                allsprites.empty()
                if win:
                    text = font.render("You win!", True, white)
                    textpos = text.get_rect(centerx=background.get_width()/2)
                    textpos.top = 240 - 18
                    screen.blit(text, textpos)
                else:
                    text = font.render("Game Over", True, white)
                    textpos = text.get_rect(centerx=background.get_width()/2)
                    textpos.top = 240 - 18
                    screen.blit(text, textpos)

                text = font.render("Press SPACE to continue or Q to quit", True, white)
                textpos = text.get_rect(centerx=background.get_width()/2)
                textpos.top = 240 + 18
                screen.blit(text, textpos)

            if pygame.sprite.spritecollide(player, balls, False):
                diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
                ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
                ball.bounce(diff)
        
            deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
        
            if len(deadblocks) > 0:
                ball.bounce(0)    
            if len(blocks) == 0:
                allsprites.empty()
                text = font.render("You win!", True, white)
                textpos = text.get_rect(centerx=background.get_width()/2)
                textpos.top = 240 - 18
                screen.blit(text, textpos)

                text = font.render("Press SPACE to continue or Q to quit", True, white)
                textpos = text.get_rect(centerx=background.get_width()/2)
                textpos.top = 240 + 18
                screen.blit(text, textpos)
                game_over = True        

            allsprites.draw(screen)    
            pygame.display.flip()

        choice_made = False
        while not choice_made:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit()
                    if event.key == pygame.K_SPACE:
                        main_menu = True
                        choice_made = True
                        replay = True
                        break
    pygame.quit()

import threading
import queue

if __name__ == '__main__':
    pos = 0
    q = queue.Queue()
    thread1 = threading.Thread(target=vision,args=(pos,q))
    thread2 = threading.Thread(target=breakout,args=(pos,q))
    thread1.start()
    thread2.start()
