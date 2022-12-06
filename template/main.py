# https://inventwithpython.com/pygame/chapter2.html
# modified to include extra event listener demonstration

import pygame, sys, time
from pygame.locals import *

# set up display & essentials
pygame.init()
DISPLAY = pygame.display.set_mode((500, 400)) # convert_alpha() allows transparent colors to be drawn
pygame.display.set_caption('Insert witty title here')

FPS = 60
fpsClock = pygame.time.Clock()

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

catImg = pygame.image.load('assets/cat.png')
fontObj = pygame.font.Font('freesansbold.ttf', 32)
soundObj = pygame.mixer.Sound('assets/tetrisb.wav') # only .wav supported, it seems

# game vars
# setup cat
catx = 10
caty = 10
direction = 'r'

# setup text (text, bool for anti-alias, color and background)
text_surfaceObj = fontObj.render('I\'m just some text', True, GREEN, BLUE)
text_rectObj = text_surfaceObj.get_rect()
text_rectObj.center = (200, 150)

# setup audio
soundObj.play()

# drawing stuff
DISPLAY.fill(WHITE)

# https://www.pygame.org/docs/ref/draw.html
pygame.draw.polygon(DISPLAY, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.line(DISPLAY, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(DISPLAY, BLUE, (120, 120), (120, 60))
pygame.draw.circle(DISPLAY, BLUE, (300, 50), 20, 0)
pygame.draw.ellipse(DISPLAY, RED, (300, 250, 40, 80), 1)
pygame.draw.rect(DISPLAY, RED, (200, 150, 100, 50))

# the game loop (handles events, updates game state, draws state)
while True:
    # NOTE: the cat will "clone" itself on the display, to prevent this we must 
    # keep making the background a solid color, however this will cause all shapes we
    # drew already to disappear unless we also redraw them.

    # DISPLAY.fill(WHITE) # uncomment/comment this line and see what happens

    # moving the cat and blitting it on display
    if direction == 'r':
        catx += 5
        if catx == 280:
            direction = 'd'
    elif direction == 'd':
        caty += 5
        if caty == 220:
            direction = 'l'
    elif direction == 'l':
        catx -= 5
        if catx == 10:
            direction = 'u'
    elif direction == 'u':
        caty -= 5
        if caty == 10:
            direction = 'r'

    DISPLAY.blit(catImg, (catx, caty))
    DISPLAY.blit(text_surfaceObj, text_rectObj) # later lines get layered above other objects

    # https://www.pygame.org/docs/ref/event.html
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pygame.display.set_caption('you clicked at ' + str(event.pos))
        elif event.type == KEYDOWN:
            pygame.display.set_caption('you pressed ' + str(event.key) + ' (' + str(event.unicode) + ')')

    pygame.display.update() # only updates the surface returned from set_mode() appear
    fpsClock.tick(FPS)