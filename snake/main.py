import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size"
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size"
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # the index of the head of the snake (always 0; this is just easier to read)

def main():
    global FPSCLOCK, DISPLAY, BASICFONT

    # usual starter code
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()

def run_game():
    """
    Consists of the main game loop.
    """
    # starting variables
    # set random starter point - 6 pixels from edges to give player time to actually move around
    start_x = random.randint(5, CELL_WIDTH - 6)
    start_y = random.randint(5, CELL_HEIGHT - 6)
    snake_coords = [{'x': start_x, 'y': start_y}, {'x': start_x - 1, 'y': start_y}, {'x': start_x - 2, 'y': start_y}]
    direction = RIGHT

    # put apple in random place
    apple = get_random_location() # 'apple' var is the LOCATION of the apple

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_a) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_a) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_a) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if snake has hit itself
        if snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == CELL_WIDTH or snake_coords[HEAD]['y'] == -1 or snake_coords[HEAD]['y'] == CELL_HEIGHT:
            return # game over; exit this loop and the function.

        # check if snake has hit an edge
        for snake_part in snake_coords[1:]:
            if snake_part['x'] == snake_coords[HEAD]['x'] and snake_part['y'] == snake_coords[HEAD]['y']:
                return

        # eaten a fruit?
        if apple['x'] == snake_coords[HEAD]['x'] and apple['y'] == snake_coords[HEAD]['y']:
            # do not remove snake tail segment
            apple = get_random_location()
        else:
            del snake_coords[-1] # remove a tail segment; if we don't do this the end will simply stick and snake will extend by one piece

        # "move" snake by adding segment in direction of movement
        if direction == UP:
            new_head = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] - 1}
        elif direction == DOWN:
            new_head = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
        elif direction == LEFT:
            new_head = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
        elif direction == RIGHT:
            new_head = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}

        snake_coords.insert(0, new_head)

        # draw things in this order
        DISPLAY.fill(BGCOLOR)
        draw_grid()
        draw_snake(snake_coords)
        draw_apple(apple)
        draw_score(len(snake_coords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)       

def draw_press_key_msg():
    """
    Displays the "Press a key to play..." message on the bottom right of the screen
    """
    press_key_surf = BASICFONT.render('Press a key to play...', True, DARKGRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DISPLAY.blit(press_key_surf, press_key_rect)

def check_for_key_press():
    """
    An event listener for keydown events, returns the key pressed if one was pressed. (If Esc, exits the program)
    """
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_down_events = pygame.event.get(KEYDOWN)
    if len(key_down_events) == 0:
        return None
    if key_down_events[0].key == K_ESCAPE:
        terminate()
    return key_down_events[0].key

def show_start_screen():
    """
    Indefinitely shows the start screen until a key is pressed, in which case either the game starts or closes (Esc)
    """
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surf_1 = title_font.render('Snake', True, WHITE, DARKGREEN)
    title_surf_2 = title_font.render('Snake', True, GREEN)
    
    degrees1 = 0 # angle of 1st surf
    degrees2 = 0
    while True: # keep redrawing the screen
        # background first
        DISPLAY.fill(BGCOLOR)

        # then text
        rotated_surf_1 = pygame.transform.rotate(title_surf_1, degrees1)
        rotated_rect_1 = rotated_surf_1.get_rect()
        rotated_rect_1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY.blit(rotated_surf_1, rotated_rect_1)

        rotated_surf_2 = pygame.transform.rotate(title_surf_2, degrees2)
        rotated_rect_2 = rotated_surf_2.get_rect()
        rotated_rect_2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY.blit(rotated_surf_2, rotated_rect_2)

        draw_press_key_msg()

        if check_for_key_press():
            pygame.event.get()
            return
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        degrees1 += 3
        degrees2 += 7

def terminate():
    pygame.quit()
    sys.exit()

def get_random_location():
    """
    Gets the coordinates of a random cell on the board
    """
    return {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}

def show_game_over_screen():
    """
    Displays the game over screen indefinitely until a key is pressed, in which the game either starts or closes (Esc)
    """
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surf = game_over_font.render('Game', True, WHITE)
    over_surf = game_over_font.render('Over', True, WHITE)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, 10)
    over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

    DISPLAY.blit(game_surf, game_rect)
    DISPLAY.blit(over_surf, over_rect)

    draw_press_key_msg()
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press() # clear out any key presses in event queue

    while True:
        if check_for_key_press():
            pygame.event.get() # clear event queue
            return

def draw_score(score):
    """
    Displays the score on the top right of the screen

    Params:
        score (int): The score
    """
    score_surf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY.blit(score_surf, score_rect)

def draw_snake(snake_coords):
    """
    Draws the snake on the board

    Params:
        snake_coords (dict[]): A array of dictionary each containing two values, one for the x and y coordinates each
    """
    for coord in snake_coords:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        snake_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY, DARKGREEN, snake_segment_rect)
        snake_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(DISPLAY, GREEN, snake_inner_segment_rect)

def draw_apple(coord):
    """
    Draws the apple on the board

    Params:
        snake_coords (dict): A dictionary containing two values, one for the x and y coordinates each
    """
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY, RED, apple_rect)

def draw_grid():
    """
    Draws vertical/horizontal grid lines on the board
    """
    for x in range(0, WINDOW_WIDTH, CELL_SIZE): # verticals
        pygame.draw.line(DISPLAY, DARKGRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_WIDTH, CELL_SIZE): # horizontals
        pygame.draw.line(DISPLAY, DARKGRAY, (0, y), (WINDOW_WIDTH, y))

main()