import pygame, sys, os, math
from ball import Ball
from paddle import Paddle
from pygame.locals import *

sys.argv = sys.argv[1:] # remove first arg, that's the file name
assert len(sys.argv) == 3, 'There must be exactly 3 args supplied'

# arguments from cmd
# 0 = paddle size (0-2)
# 1 = ball speedup (0-1)
# 2 = object colors (hex)

dir_path = os.path.dirname(os.path.realpath(__file__))

WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)

BG_COLOR = BLACK
OBJECT_COLOR = sys.argv[2]
SLEEP_TIME = 1000

PADDLE_HEIGHT = 75
if int(sys.argv[0]) == 0:
    PADDLE_HEIGHT = 25
elif int(sys.argv[0]) == 0:
    PADDLE_HEIGHT = 125
BALL_SPEEDUP = False if int(sys.argv[1]) == 0 else True
BALL_RADIUS = 10
BALL_VEL = 5
PADDLE_VEL = 10

p1_score = p2_score = 0

def main():
    global FPSCLOCK, DISPLAY, BASIC_FONT, p1_score, p2_score, BALL_VEL

    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pong')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 30)

    HIT_SOUND = pygame.mixer.Sound(dir_path + '/assets/hit.wav')
    BOUNCE_SOUND = pygame.mixer.Sound(dir_path + '/assets/bounce.wav')
    ROUND_OVER_SOUND = pygame.mixer.Sound(dir_path + '/assets/roundover.wav')
    HIT_SOUND.set_volume(0.1)
    BOUNCE_SOUND.set_volume(0.1)
    ROUND_OVER_SOUND.set_volume(0.1)

    ball = Ball(WIN_WIDTH / 2, WIN_HEIGHT / 2, BALL_VEL, BALL_VEL, pygame.Rect((WIN_WIDTH / 2) - BALL_RADIUS, (WIN_HEIGHT / 2) - BALL_RADIUS, BALL_RADIUS * 2 + 5, BALL_RADIUS * 2 + 5))
    p1_paddle = Paddle(50, (WIN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), 0, pygame.Rect(50, (WIN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), 5, PADDLE_HEIGHT))
    p2_paddle = Paddle(WIN_WIDTH - 50, (WIN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), 0, pygame.Rect(WIN_WIDTH - 50, (WIN_HEIGHT / 2) - (PADDLE_HEIGHT / 2), 5, PADDLE_HEIGHT))

    # game loop
    while True:
        DISPLAY.fill(BG_COLOR)

        draw_text(str(p1_score), 150, 75)
        draw_text(str(p2_score), WIN_WIDTH - 150, 75)
        draw_ball(ball)
        draw_paddle(p1_paddle)
        draw_paddle(p2_paddle)

        # ball hits side - score
        if ball.x >= WIN_WIDTH - 5 or ball.x <= 5:
            ROUND_OVER_SOUND.play()
            if ball.x >= WIN_WIDTH - 5:
                p1_score += 1
            else:
                p2_score += 1
            draw_text(str(p1_score), 150, 75)
            draw_text(str(p2_score), WIN_WIDTH - 150, 75)

            # if speedup on, reset velocity
            BALL_VEL = 5
            if ball.xvel < 0:
                ball.xvel = -5
            else:
                ball.xvel = 5

            if ball.yvel < 0:
                ball.yvel = -5
            else:
                ball.yvel = 5  
                
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.wait(SLEEP_TIME)
            ball.x = WIN_WIDTH / 2
            ball.y = WIN_HEIGHT / 2
            continue

        # ball hits top or bottom - bounce
        if ball.y >= WIN_HEIGHT - 5 or ball.y <= 5:
            BOUNCE_SOUND.play()
            ball.yvel *= -1

        # ball bouncing off a paddle
        if ball.rect.colliderect(p1_paddle.rect) or ball.rect.colliderect(p2_paddle.rect):
            HIT_SOUND.play()
            if BALL_SPEEDUP:
                BALL_VEL += 0.5
            ball.xvel *= -1
            delta = 0
            if ball.rect.colliderect(p1_paddle.rect):
                delta = p1_paddle.y - ball.y
            elif ball.rect.colliderect(p2_paddle.rect):
                delta = p2_paddle.y - ball.y

            # I hate math so much (except Discrete, that class was fun)
            angle = -1.2 * math.fabs(delta) + 135
            new_xvel = BALL_VEL * math.sin(angle * math.pi / 180)
            
            # I hate math so much x2
            if (ball.xvel > 0 and new_xvel < 0) or (ball.xvel < 0 and new_xvel > 0):
                new_xvel *= -1

            # I hate math so much x3
            ball.xvel = new_xvel
            ball.yvel = math.sqrt(math.pow(BALL_VEL, 2) - math.pow(ball.xvel, 2))
            if angle > 90:
                ball.yvel *= -1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key
                if key == 1073741906: # up
                    p2_paddle.yvel = -PADDLE_VEL
                elif key == 1073741905: # down
                    p2_paddle.yvel = PADDLE_VEL
                elif key == 119: # w
                    p1_paddle.yvel = -PADDLE_VEL
                elif key == 115: # s
                    p1_paddle.yvel = PADDLE_VEL
            elif event.type == KEYUP:
                key = event.key
                if key == 1073741906 or key == 1073741905:
                    p2_paddle.yvel = 0
                elif key == 119 or key == 115: # s
                    p1_paddle.yvel = 0

        if p1_paddle.y + PADDLE_HEIGHT > WIN_HEIGHT:
            p1_paddle.y = WIN_HEIGHT - PADDLE_HEIGHT
        elif p1_paddle.y < 0:
            p1_paddle.y = 0

        if p2_paddle.y + PADDLE_HEIGHT > WIN_HEIGHT:
            p2_paddle.y = WIN_HEIGHT - PADDLE_HEIGHT
        elif p2_paddle.y < 0:
            p2_paddle.y = 0

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def draw_ball(ball: Ball):
    """
    Draws the ball with the x/y position given in the Ball object provided. Modifies position accordingly given its xvel/yvel properties
    """
    ball.x += ball.xvel
    ball.y += ball.yvel
    ball.rect = pygame.Rect(ball.x - BALL_RADIUS, ball.y - BALL_RADIUS, BALL_RADIUS * 2 + 5, BALL_RADIUS * 2 + 5)
    pygame.draw.circle(DISPLAY, OBJECT_COLOR, (ball.x, ball.y), BALL_RADIUS)

def draw_paddle(paddle: Paddle):
    """
    Draws a paddle with the x/y position given in the Paddle object provided. Modifies position accordingly given its yvel property, UNLESS it is touching an edge of the screen
    NOTE: x and y are the TOP-LEFT coordinates of the paddle
    """
    paddle.y += paddle.yvel
    paddle.rect = pygame.Rect(paddle.x, paddle.y, 5, PADDLE_HEIGHT)
    pygame.draw.rect(DISPLAY, OBJECT_COLOR, pygame.Rect(paddle.x, paddle.y, 5, PADDLE_HEIGHT))

def draw_text(text: str, x: int, y: int):
    """
    Draws text at the specified coordinates
    """
    text_surf = BASIC_FONT.render(text, True, GRAY, BG_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (x, y)
    DISPLAY.blit(text_surf, text_rect)

main()