import random, pygame, sys
from pygame.locals import *

sys.argv = sys.argv[1:] # remove first arg, that's the file name
assert len(sys.argv) == 5, 'There must be exactly 5 args supplied'

# arguments from cmd
# 0 = length increase for each fruit (0-2)
# 1 = game speed (0-1), 0 for normal, 1 for fast
# 2 = disappearing food (0-1)
# 3 = snake color (hex)
# 4 = fruit color (hex)

LENGTH_INCREASE = int(sys.argv[0]) # + 1 = snake bits added per fruit
DEFAULT_LIFE = 45 if int(sys.argv[2]) == 1 else -1

FPS = 25 if int(sys.argv[1]) == 1 else 15
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size"
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size"
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE          = (255, 255, 255)
BLACK          = (  0,   0,   0)
DARKGRAY       = ( 40,  40,  40)
BGCOLOR        = BLACK
FRUITCOLOR     = sys.argv[4]
SNAKECOLOR     = sys.argv[3]

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
    start_x = random.randint(5, CELL_WIDTH - 1)
    start_y = random.randint(5, CELL_HEIGHT - 1)
    direction = RIGHT if start_x < CELL_WIDTH / 2 else LEFT
    if direction == RIGHT:
        snake_coords = [{'x': start_x, 'y': start_y}, {'x': start_x - 1, 'y': start_y}, {'x': start_x - 2, 'y': start_y}]
    else:
        snake_coords = [{'x': start_x -2 , 'y': start_y}, {'x': start_x - 1, 'y': start_y}, {'x': start_x, 'y': start_y}]
    score = 0

    # if fruit disappearing is turned on:
    fruit_life = DEFAULT_LIFE # how long each fruit stays on the board, measured in frames
    fruits_left = 3 if fruit_life != -1 else -1 # how many fruits can be missed

    # tracks number of snake pieces to add
    outstanding_parts = 0

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
            # do not remove snake tail segment, possibly even add one or two extra depending on settings
            apple = get_random_location()
            outstanding_parts = LENGTH_INCREASE
            if fruit_life != -1:
                fruit_life = DEFAULT_LIFE
            score += 1
        else:
            if outstanding_parts == 0:
                del snake_coords[-1] # remove a tail segment; if we don't do this the end will simply stick and snake will extend by one piece
            else:
                outstanding_parts -= 1 # don't remove if we still need to add segments!

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

        fruit_life -= 1

        if fruit_life == 0: # fruit disappearing (if enabled), move it elsewhere and subtract a life
            fruits_left -= 1
            fruit_life = DEFAULT_LIFE
            apple = get_random_location()

        if fruits_left == 0:
            return # game over, all lives gone!

        # draw things in this order
        DISPLAY.fill(BGCOLOR)
        draw_grid()
        draw_snake(snake_coords)
        draw_apple(apple, fruit_life)
        draw_score(score, fruits_left)
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
    title_surf_1 = title_font.render('Snake', True, WHITE)
    title_surf_2 = title_font.render('Snake', True, SNAKECOLOR)
    
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

def draw_score(score, fruits_left):
    """
    Displays the score on the top right of the screen

    Params:
        score (int): The score
    """
    score_surf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY.blit(score_surf, score_rect)

    if fruits_left != -1:
        fruits_surf = BASICFONT.render('Lives: %s' % (fruits_left), True, WHITE)
        fruits_rect = fruits_surf.get_rect()
        fruits_rect.topleft = (WINDOW_WIDTH - 120, 30)
        DISPLAY.blit(fruits_surf, fruits_rect)

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
        pygame.draw.rect(DISPLAY, SNAKECOLOR, snake_segment_rect)

def draw_apple(coord, life):
    """
    Draws the apple on the board

    Params:
        snake_coords (dict): A dictionary containing two values, one for the x and y coordinates each
    """
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY, FRUITCOLOR if life > 15 or life < 1 else WHITE, apple_rect)

def draw_grid():
    """
    Draws vertical/horizontal grid lines on the board
    """
    for x in range(0, WINDOW_WIDTH, CELL_SIZE): # verticals
        pygame.draw.line(DISPLAY, DARKGRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_WIDTH, CELL_SIZE): # horizontals
        pygame.draw.line(DISPLAY, DARKGRAY, (0, y), (WINDOW_WIDTH, y))

main()