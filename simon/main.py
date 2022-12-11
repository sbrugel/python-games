import random, sys, time, pygame
import os
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 580
FLASH_SPEED = 500 # ms
FLASH_DELAY = 200 # ms
BUTTON_SIZE = 200
BUTTON_GAP_SIZE = 20
TIMEOUT = 4 # seconds before game over, if no button pushed

WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bg_color = BLACK

X_MARGIN = int((WINDOW_WIDTH - (2 * BUTTON_SIZE) - BUTTON_GAP_SIZE) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (2 * BUTTON_SIZE) - BUTTON_GAP_SIZE) / 2)

# button rectangles (collison regions for clicking events)
YELLOW_RECT = pygame.Rect(X_MARGIN, Y_MARGIN, BUTTON_SIZE, BUTTON_SIZE)
BLUE_RECT = pygame.Rect(X_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, Y_MARGIN, BUTTON_SIZE, BUTTON_SIZE)
RED_RECT = pygame.Rect(X_MARGIN, Y_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, BUTTON_SIZE, BUTTON_SIZE)
GREEN_RECT = pygame.Rect(X_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, Y_MARGIN + BUTTON_SIZE + BUTTON_GAP_SIZE, BUTTON_SIZE, BUTTON_SIZE)

def main():
    global FPSCLOCK, DISPLAY, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Simon')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    info_surf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    info_rect = info_surf.get_rect()
    info_rect.topleft = (10, WINDOW_HEIGHT - 25)

    dir_path = os.path.dirname(os.path.realpath(__file__)) # the file currently being ran (mainmenu.py)

    # load the sound files
    BEEP1 = pygame.mixer.Sound(dir_path + '/assets/beep1.wav')
    BEEP2 = pygame.mixer.Sound(dir_path + '/assets/beep2.wav')
    BEEP3 = pygame.mixer.Sound(dir_path + '/assets/beep3.wav')
    BEEP4 = pygame.mixer.Sound(dir_path + '/assets/beep4.wav')

    # variables for a new round
    pattern = [] # the current pattern of colors
    current_step = 0 # the color the player must press next
    last_click_time = 0 # timestamp of player's last button push
    score = 0
    
    # when false. pattern is playing, otherwise waiting for player input
    waiting_for_input = False

    while True: # game loop
        clicked_button = None
        DISPLAY.fill(bg_color)
        draw_buttons()

        score_surf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (WINDOW_WIDTH - 100, 10)
        DISPLAY.blit(score_surf, score_rect)

        DISPLAY.blit(info_surf, info_rect)

        check_for_quit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_button = get_button_clicked(mouse_x, mouse_y)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clicked_button = YELLOW
                elif event.key == K_w:
                    clicked_button = BLUE
                elif event.key == K_a:
                    clicked_button = RED
                elif event.key == K_s:
                    clicked_button = GREEN

        if not waiting_for_input:
            # play pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flash_button_animation(button)
                pygame.time.wait(FLASH_DELAY)
            waiting_for_input = True
        else:
            # wait for player to enter buttons
            if clicked_button and clicked_button == pattern[current_step]:
                # pushed correct button
                flash_button_animation(clicked_button)
                current_step += 1
                last_click_time = time.time()

                if current_step == len(pattern):
                    # pushed last button in pattern
                    change_background_animation()
                    score += 1
                    waiting_for_input = False
                    current_step = 0
            elif (clicked_button and clicked_button != pattern[current_step]) or (current_step != 0 and time.time() - TIMEOUT > last_click_time):
                # pushed wrong button / ran out of time
                game_over_animation()

                # reset game
                pattern = []
                current_step = 0
                waiting_for_input = False
                score = 0
                pygame.time.wait(1000)
                change_background_animation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    """
    Simply quits the program
    """
    pygame.quit()
    sys.exit()

def check_for_quit():
    """
    Quits the game if we click the top-right 'X' or press ESC
    """
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def flash_button_animation(color, animation_speed=50):
    """
    Flashes the specified button.

    Params:
        color (string): The color of the button to flash
        animation_speed (int): How fast to flash the button
    """
    if color == YELLOW:
        sound = BEEP1
        flash_color = BRIGHTYELLOW
        rectangle = YELLOW_RECT
    elif color == BLUE:
        sound = BEEP2
        flash_color = BRIGHTBLUE
        rectangle = BLUE_RECT
    elif color == RED:
        sound = BEEP3
        flash_color = BRIGHTRED
        rectangle = RED_RECT
    elif color == GREEN:
        sound = BEEP4
        flash_color = BRIGHTGREEN
        rectangle = GREEN_RECT

    orig_surf = DISPLAY.copy()
    flash_surf = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
    flash_surf = flash_surf.convert_alpha() # allows alpha part of RGBA to be used on this surface only
    r, g, b = flash_color
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animation_speed * step):
            check_for_quit()
            DISPLAY.blit(orig_surf, (0, 0))
            flash_surf.fill((r, g, b, alpha))
            DISPLAY.blit(flash_surf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAY.blit(orig_surf, (0, 0))

def draw_buttons():
    """
    Draws the four colored buttons on the screen, as defined above main()
    """
    pygame.draw.rect(DISPLAY, YELLOW, YELLOW_RECT)
    pygame.draw.rect(DISPLAY, BLUE,   BLUE_RECT)
    pygame.draw.rect(DISPLAY, RED,    RED_RECT)
    pygame.draw.rect(DISPLAY, GREEN,  GREEN_RECT)

def change_background_animation(animation_speed=40):
    """
    Gradually changes the window's background color to a random choice

    Params:
        animation_speed (int): How fast to change
    """
    global bg_color
    new_bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    new_bg_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    new_bg_surf = new_bg_surf.convert_alpha()
    r, g, b = new_bg_color
    for alpha in range(0, 255, animation_speed): # animation loop
        check_for_quit()
        DISPLAY.fill(bg_color)

        new_bg_surf.fill((r, g, b, alpha))
        DISPLAY.blit(new_bg_surf, (0, 0))

        draw_buttons() # keep the buttons on top of the transitioning background

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bg_color = new_bg_color

def game_over_animation(color=WHITE, animation_speed=50):
    """
    Plays every beep sound simultaneously and flashes the background.

    Params:
        color (string): The color to flash the background to
        animation_speed (int): How fast to flash the background
    """
    orig_surf = DISPLAY.copy()
    flash_surf = pygame.Surface(DISPLAY.get_size())
    flash_surf = flash_surf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # first iteration in loop goes from 0-255, then 255-0
            for alpha in range(start, end, animation_speed * step):
                # alpha is transparency, so 255 is opaque and 0 is invisible
                check_for_quit()
                flash_surf.fill((r, g, b, alpha))
                DISPLAY.blit(orig_surf, (0, 0))
                DISPLAY.blit(flash_surf, (0, 0))
                draw_buttons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def get_button_clicked(x, y):
    """
    Gets the color button clicked, if applicable.

    Params:
        x (int), y (int): x and y window coordinates of the mouse click event

    Returns:
        (string): The box clicked if any, otherwise returns None
    """
    if YELLOW_RECT.collidepoint((x, y)):
        return YELLOW
    elif BLUE_RECT.collidepoint((x, y)):
        return BLUE
    elif RED_RECT.collidepoint((x, y)):
        return RED
    elif GREEN_RECT.collidepoint((x, y)):
        return GREEN
    return None

main()