import random, time, pygame, os, sys
from pygame.locals import *

sys.argv = sys.argv[1:] # remove first arg, that's the file name
assert len(sys.argv) == 3, 'There must be exactly 3 args supplied'

# arguments from cmd
# 0 = show ghost pieces (0-1)
# 1 = board size (0-2), normal/small/smaller
# 2 = game speed (0-2), normal/fast/faster

FPS = 25
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOX_SIZE = 20
BOARD_WIDTH = 10

HIDE_GHOSTS = int(sys.argv[0])

if int(sys.argv[1]) == 0:
    BOARD_HEIGHT = 20
elif int(sys.argv[1]) == 1:
    BOARD_HEIGHT = 15
else:
    BOARD_HEIGHT = 10

if int(sys.argv[2]) == 0:
    BASE_FALL_FREQ = 0.02
elif int(sys.argv[2]) == 1:
    BASE_FALL_FREQ = 0.03
else:
    BASE_FALL_FREQ = 0.04

BLANK = '.'

# timeout for moving pieces manually
MOVE_SIDEWAYS_FREQ = 0.15
MOVE_DOWN_FREQ = 0.1

X_MARGIN = int((WINDOW_WIDTH - BOARD_WIDTH * BOX_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (BOARD_HEIGHT * BOX_SIZE) - 5

WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def main():
    global FPSCLOCK, DISPLAY, BASICFONT, BIGFONT
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris')

    show_text_screen('Tetromino')
    while True: # game loop
        dir_path = os.path.dirname(os.path.realpath(__file__)) # the file currently being ran (mainmenu.py)

        pygame.mixer.music.load(dir_path + '/assets/tetrisb.wav')
        pygame.mixer.music.play(-1, 0.0)
        run_game()
        pygame.mixer.music.stop()
        show_text_screen('Game Over')

def run_game():
    # starting varaiables
    board = get_blank_board()
    last_move_down_time = time.time()
    last_move_side_time = time.time()
    last_fall_time = time.time()

    moving_down = False
    moving_left = False
    moving_right = False

    score = 0
    level, fall_freq = calculate_level_and_fall_freq(score)

    falling_piece = get_new_piece()
    next_piece = get_new_piece()

    while True: # game loop
        if falling_piece == None:
            # start a new piece at top
            falling_piece = next_piece
            next_piece = get_new_piece()
            last_fall_time = time.time() # reset

            if not is_valid_position(board, falling_piece):
                return # can't fit on the board, so game over
        
        check_for_quit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_p:
                    # pause
                    DISPLAY.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    show_text_screen('Paused') # pause until key press

                    pygame.mixer.music.play(-1, 0.0)
                    last_move_down_time = time.time()
                    last_move_side_time = time.time()
                    last_fall_time = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    moving_left = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    moving_right = False
                elif (event.key == K_DOWN or event.key == K_s):
                    moving_down = False
            elif event.type == KEYDOWN:
                # move piece left/right
                if (event.key == K_LEFT or event.key == K_a) and is_valid_position(board, falling_piece, adj_x=-1):
                    falling_piece['x'] -= 1
                    moving_left = True
                    moving_right = False
                    last_move_side_time = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and is_valid_position(board, falling_piece, adj_x=1):
                    falling_piece['x'] += 1
                    moving_right = True
                    moving_left = False
                    last_move_side_time = time.time()

                # rotate piece
                elif (event.key == K_UP or event.key == K_w):
                    falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])

                elif (event.key == K_q):
                    falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])
                    if not is_valid_position(board, falling_piece):
                        falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])

                # make piece fall faster
                elif (event.key == K_DOWN or event.key == K_s):
                    moving_down = True
                    if is_valid_position(board, falling_piece, adj_y=1):
                        falling_piece['y'] += 1
                    last_move_down_time = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    moving_down = False
                    moving_left = False
                    moving_right = False
                    for i in range(1, BOARD_HEIGHT):
                        if not is_valid_position(board, falling_piece, adj_y=i):
                            break
                    falling_piece['y'] += i - 1

        # handle piece movement
        if (moving_left or moving_right) and time.time() - last_move_side_time > MOVE_SIDEWAYS_FREQ:
            if moving_left and is_valid_position(board, falling_piece, adj_x=-1):
                falling_piece['x'] -= 1
            elif moving_right and is_valid_position(board, falling_piece, adj_x=1):
                falling_piece['x'] += 1
            last_move_side_time = time.time()

        if moving_down and time.time() - last_move_down_time > MOVE_DOWN_FREQ and is_valid_position(board, falling_piece, adj_y=1):
            falling_piece['y'] += 1
            last_move_down_time = time.time()

        # let the piece fall if it is time to fall
        if time.time() - last_fall_time > fall_freq:
            # see if the piece has landed
            if not is_valid_position(board, falling_piece, adj_y=1):
                # falling piece has landed, set it on the board
                add_to_board(board, falling_piece)
                score += remove_complete_lines(board)
                level, fall_freq = calculate_level_and_fall_freq(score)
                falling_piece = None
            else:
                # piece did not land, just move the piece down
                falling_piece['y'] += 1
                last_fall_time = time.time()

        # drawing everything on the screen
        DISPLAY.fill(BGCOLOR)
        draw_board(board)
        draw_status(score, level)
        draw_next_piece(next_piece)
        if falling_piece != None:
            if not HIDE_GHOSTS:
                draw_piece(get_ghost_piece(board, falling_piece))
            draw_piece(falling_piece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def make_text_objs(text, font, color):
    """
    Based on provided text/color, returns the surface and rect of the text for easier creation
    """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def check_for_key_press():
    check_for_quit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def show_text_screen(text):
    """
    Displays large text on the screen until a key is pressed, in which the function returns
    """
    # draw text drop shadow
    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTSHADOWCOLOR)
    title_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    DISPLAY.blit(title_surf, title_rect)

    # draw text
    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3)
    DISPLAY.blit(title_surf, title_rect)

    # draw extra Press a key to play. text
    press_key_surf, press_key_rect = make_text_objs('Press a key to play...', BASICFONT, TEXTCOLOR)
    press_key_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
    DISPLAY.blit(press_key_surf, press_key_rect)

    while check_for_key_press() == None: # return from function when a key is pressed
        pygame.display.update()
        FPSCLOCK.tick()

def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) # put the other KEYUP event objects back

def calculate_level_and_fall_freq(score):
    """
    Based on current score, return the level the player is on, and how many seconds pass until a piece falls down one space
    """
    level = int(score / 5) + 1
    fall_freq = 0.27 - (level * BASE_FALL_FREQ)
    return level, fall_freq

def get_new_piece():
    """
    Return a random new piece in a random rotation and color. A dictionary is returned which has its shape, rotation, position and color.
    """
    shape = random.choice(list(PIECES.keys()))
    new_piece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARD_WIDTH / 2) - int(TEMPLATE_WIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    return new_piece

def get_ghost_piece(board, piece):
    """
    Get the "preview" of the current piece. That is, how far down the piece can go given its current x position. This makes it easier for the player to properly
    align their current piece
    """
    ghost_piece = {'shape': piece['shape'],
                    'rotation': piece['rotation'],
                    'x': piece['x'],
                    'y': piece['y'],
                    'color': GRAY}
    # find the lowest possible y value without colliding into other pieces or the ground
    while True:
        ghost_piece['y'] += 1
        if not is_valid_position(board, ghost_piece):
            ghost_piece['y'] -= 1
            break
    return ghost_piece

def add_to_board(board, piece):
    """
    Fill in the board based on piece's location, shape, and rotation
    """
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK: # aka, there is a '.' at this position
                board[x + piece['x']][y + piece['y']] = piece['color']

def get_blank_board():
    """
    Returns a blank board array
    """
    board = []
    for i in range(BOARD_WIDTH):
        board.append([BLANK] * BOARD_HEIGHT)
    return board

def is_on_board(x, y):
    """
    Returns a boolean indicating if the specified coordinates are within the playing board or outside of it
    """
    return x >= 0 and x < BOARD_WIDTH and y < BOARD_HEIGHT

def is_valid_position(board, piece, adj_x=0, adj_y=0):
    """
    Returns true if the piece is within a board and not colliding with anything
    """
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            is_above_board = y + piece['y'] + adj_y < 0
            if is_above_board or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK: # always valid if the part is above the board/there is a '.' here
                continue
            if not is_on_board(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
                return False
            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
                return False
    return True

def is_complete_line(board, y):
    """
    Returns true if the board at height y has no blank spaces
    """
    for x in range(BOARD_WIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def remove_complete_lines(board):
    """
    Removes any lines on the board that are "complete", move everything above them down one line. Returns the number of lines removed
    """
    num_removed = 0
    y = BOARD_HEIGHT - 1 # begin at bottom
    while y >= 0:
        if is_complete_line(board, y):
            # remove the line, pull boxes down by one line
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARD_WIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y-1]
            # set above line to blank
            for x in range(BOARD_WIDTH):
                board[x][0] = BLANK
            
            num_removed += 1
            # on the next run of this loop, y is the same, so that the line pulled down is checked
        else:
            y -= 1 # move on to check the next row
    return num_removed

def convert_to_pixel_coords(boxx, boxy):
    """
    Convert the given board coordinates to window x/y coordinates.
    """
    return (X_MARGIN + (boxx * BOX_SIZE)), (TOP_MARGIN + (boxy * BOX_SIZE))

def draw_box(boxx, boxy, color, pixelx=None, pixely=None):
    """
    Draw a box at the board coordinates specified. If the latter two args are specified, draw to pixel coordinates stored at those places. (Used for "next" piece)
    """
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_to_pixel_coords(boxx, boxy)
    
    if color != GRAY: # ordinary piece, where color is an index of the colors array
        pygame.draw.rect(DISPLAY, COLORS[color], (pixelx + 1, pixely + 1, BOX_SIZE - 1, BOX_SIZE - 1))
        pygame.draw.rect(DISPLAY, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOX_SIZE - 4, BOX_SIZE - 4))
    else: # ghost piece, color is explicitly passed in
        pygame.draw.rect(DISPLAY, color, (pixelx + 1, pixely + 1, BOX_SIZE - 1, BOX_SIZE - 1))

def draw_board(board):
    """
    Draw an empty board.
    """
    # draw border
    pygame.draw.rect(DISPLAY, BORDERCOLOR, (X_MARGIN - 3, TOP_MARGIN - 7, (BOARD_WIDTH * BOX_SIZE) + 8, (BOARD_HEIGHT * BOX_SIZE) + 8), 5)

    # fill background
    pygame.draw.rect(DISPLAY, BGCOLOR, (X_MARGIN, TOP_MARGIN, BOX_SIZE * BOARD_WIDTH, BOX_SIZE * BOARD_HEIGHT))

    # draw boxes on the board
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            draw_box(x, y, board[x][y])

def draw_status(score, level):
    """
    Draw the score and level.
    """
    # draw score text
    score_surf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 150, 20)
    DISPLAY.blit(score_surf, score_rect)

    # draw level text
    level_surf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOW_WIDTH - 150, 50)
    DISPLAY.blit(level_surf, level_rect)

def draw_piece(piece, pixelx=None, pixely=None):
    """
    Draw the specified piece based on the piece structure provided.
    If pixelx and pixely are provided, draw the piece there. Else, draw the piece at the coorindates specified in its structure.
    """
    shape_to_draw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely not been specified, use the location stored in the piece data structure
        pixelx, pixely = convert_to_pixel_coords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if shape_to_draw[y][x] != BLANK:
                draw_box(None, None, piece['color'], pixelx + (x * BOX_SIZE), pixely + (y * BOX_SIZE))

def draw_next_piece(piece):
    """
    Draw the text and piece for the next piece.
    """
    next_surf = BASICFONT.render('Next:', True, TEXTCOLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOW_WIDTH - 120, 80)
    DISPLAY.blit(next_surf, next_rect)

    draw_piece(piece, pixelx=WINDOW_WIDTH-120, pixely=100)

main()