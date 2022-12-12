import pygame, sys, random
from pygame.locals import *

sys.argv = sys.argv[1:] # remove first arg, that's the file name
# assert len(sys.argv) == 6, 'There must be exactly 6 args supplied'

# arguments from cmd
# 0 = board size (0-2)
# 1 = difficulty (moves to make when shuffling) (0-5)
# 2 = difficulty scaling (0-1)
# 3 = show moves when shuffling (0-1)
# 4 = color of tiles
# 5 = color of background

# dimensions of the board
assert int(sys.argv[0]) >= 0 and int(sys.argv[0]) <= 2, 'Board size can only be 0 (3x3) to 2 (5x5)'
BOARD_WIDTH = int(sys.argv[0]) + 3 # boxes
BOARD_HEIGHT = int(sys.argv[0]) + 3 # boxes

# num times to make random moves
assert int(sys.argv[1]) >= 0 and int(sys.argv[1]) <= 5, 'Difficulty must be 0 - 5'
random_moves = (15 * (int(sys.argv[1]) + 1)) - 5

# difficulty scaling
DIFFICULTY_SCALING = False if int(sys.argv[2]) == 0 else True

# show sliding
SHOW_SLIDING = False if int(sys.argv[3]) == 0 else True

TILE_SIZE = 80
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 60
BLANK = None

BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

# constant colors
BGCOLOR = DARKTURQUOISE
BASIC_FONT_SIZE = 20
BUTTON_COLOR = WHITE
BUTTON_TEXT_COLOR = BLACK
MESSAGE_COLOR = WHITE

# potentially modifiable colors
TILE_COLOR = GREEN
TEXT_COLOR = WHITE
BORDER_COLOR = BRIGHTBLUE

X_MARGIN = int((WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAY, BASIC_FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, random_moves

    solve_button_clicked = False

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

    # get the button objects; not blitted in main
    RESET_SURF, RESET_RECT = make_text('Reset',    TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 90)
    NEW_SURF,   NEW_RECT   = make_text('New Game', TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = make_text('Solve',    TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 30)

    main_board, solution_seq = generate_new_puzzle(random_moves)
    SOLVED_BOARD = get_starting_board() # the solved board is just the starting board
    all_moves = [] # list of moves made from solved config

    while True:
        slide_to = None # direction, if any, a tile should slide
        msg = 'Click tile or press arrow keys to slide'
        if main_board == SOLVED_BOARD:
            msg = 'Solved!'
            if not solve_button_clicked and DIFFICULTY_SCALING: # increase difficulty if user solved on their own
                random_moves += 15
                solve_button_clicked = True # loop will return here indefinitely, don't make it do that

        # repeatedly draw the intiial board first
        draw_board(main_board, msg)

        check_for_quit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONDOWN:
                spot_x, spot_y = get_spot_clicked(main_board, event.pos[0], event.pos[1])

                if (spot_x, spot_y) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        reset_animation(main_board, all_moves) # clicked on Reset button
                        all_moves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        solve_button_clicked = False
                        main_board, solution_seq = generate_new_puzzle(random_moves) # clicked on New Game button
                        all_moves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        solve_button_clicked = True
                        reset_animation(main_board, solution_seq + all_moves) # clicked on Solve button
                        all_moves = []
                else:
                    # check if the clicked tile was next to the blank spot

                    blank_x, blank_y = get_blank_position(main_board)
                    if spot_x == blank_x + 1 and spot_y == blank_y:
                        slide_to = LEFT
                    elif spot_x == blank_x - 1 and spot_y == blank_y:
                        slide_to = RIGHT
                    elif spot_x == blank_x and spot_y == blank_y + 1:
                        slide_to = UP
                    elif spot_x == blank_x and spot_y == blank_y - 1:
                        slide_to = DOWN

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                # can use the 'in' operator to see if a value is one of multiple (subsitute for or keyword)
                if event.key in (K_LEFT, K_a) and is_valid_move(main_board, LEFT):
                    slide_to = LEFT
                elif event.key in (K_RIGHT, K_d) and is_valid_move(main_board, RIGHT):
                    slide_to = RIGHT
                elif event.key in (K_UP, K_w) and is_valid_move(main_board, UP):
                    slide_to = UP
                elif event.key in (K_DOWN, K_s) and is_valid_move(main_board, DOWN):
                    slide_to = DOWN

        if slide_to:
            slide_animation(main_board, slide_to, 'Click tile or press arrow keys to slide', 8) # show slide on screen
            make_move(main_board, slide_to)
            all_moves.append(slide_to) # record the slide

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

def get_starting_board():
    """
    Returns a board with all tiles in order / the solved state.
    i.e. 3x3 solved would be [[1,4,7],[2,5,8],[3,6,None]]
    
    And the board will look like this:\n
    1   2   3\n
    4   5   6\n
    7   8\n

    Returns:
        (int[][]): The board with all tiles in order ("solved")
    """
    counter = 1 # the value to add to this position of the board
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(counter)
            counter += BOARD_WIDTH
        board.append(column)
        counter -= BOARD_WIDTH * (BOARD_HEIGHT - 1) + BOARD_HEIGHT - 1

    board[BOARD_WIDTH - 1][BOARD_HEIGHT - 1] = None
    return board

def get_blank_position(board):
    """
    There is a single blank square on the board. This function returns the x and y board coordinates of that square.

    Params:
        board (int[][]): The game board

    Returns:
        (int, int): x/y board coords of the blank square
    """
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == None:
                return (x, y)

def make_move(board, move):
    """
    Moves the appropriate square adjacent to the blank square in the specified direction. i.e. Moving right: the square to the LEFT of the blank square moves right.

    This doesn't check if the move is valid.

    Params:
        board (int[][]): The board to make the move on
        move (string): The requested move direction
    """
    blank_x, blank_y = get_blank_position(board)

    # all of these swap the blank square with the appropriate adjacent square
    if move == UP:
        board[blank_x][blank_y], board[blank_x][blank_y + 1] = board[blank_x][blank_y + 1], board[blank_x][blank_y]
    elif move == DOWN:
        board[blank_x][blank_y], board[blank_x][blank_y - 1] = board[blank_x][blank_y - 1], board[blank_x][blank_y]
    elif move == LEFT:
        board[blank_x][blank_y], board[blank_x + 1][blank_y] = board[blank_x + 1][blank_y], board[blank_x][blank_y]
    elif move == RIGHT:
        board[blank_x][blank_y], board[blank_x - 1][blank_y] = board[blank_x - 1][blank_y], board[blank_x][blank_y]

def is_valid_move(board, move):
    """
    Determines if the requested move is valid.
    A move is valid if the box (adjacent to the blank space) to be moved can actually move to the blank space.

    Params:
        board (int[][]): The board to make the move on
        move (string): The requested move direction

    Returns:
        (bool): True if move valid
    """
    blank_x, blank_y = get_blank_position(board)

    # '\' states that while we are adding a new line, the line technically continues on
    return  (move == UP and blank_y != len(board[0]) - 1) or \
            (move == DOWN and blank_y != 0) or \
            (move == LEFT and blank_x != len(board) - 1) or \
            (move == RIGHT and blank_x != 0)

def get_random_move(board, last_move=None):
    """
    Get a random move to make on the board, excluding any moves that are invalid or if applicable, the move assigned to 'last_move'

    Params:
        board (int[][]): The board to make the move on
        last_move (string): Previous move - will not be made in this run of the function

    Returns:
        (string): A random move (UDLR) that is valid and not the same as the last move
    """
    valid_move = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list if we move in the opposite direction or if the move isn't valid
    if last_move == UP or not is_valid_move(board, DOWN):
        valid_move.remove(DOWN)
    if last_move == DOWN or not is_valid_move(board, UP):
        valid_move.remove(UP)
    if last_move == LEFT or not is_valid_move(board, RIGHT):
        valid_move.remove(RIGHT)
    if last_move == RIGHT or not is_valid_move(board, LEFT):
        valid_move.remove(LEFT)

    # return a random move from the list of available moves
    return random.choice(valid_move)

def get_left_top_of_tile(tile_x, tile_y):
    """
    Returns x and y window coordinates of the tile supplied

    Params:
        tile_x (int): Board coords (x)
        tile_y (int): Board coords (y)

    Returns:
        Window x and y coords
    """
    left = X_MARGIN + (tile_x * TILE_SIZE) + (tile_x - 1)
    top = Y_MARGIN + (tile_y * TILE_SIZE) + (tile_y - 1)
    return (left, top)

def get_spot_clicked(board, x, y):
    """
    Gets the box clicked, if one was clicked.

    Params:
        board (int[][]): The board
        x (int), y (int): The x and y window coords of the click

    Returns:
        (int, int): the box coords that were clicked if one exists, otherwise (None, None)
    """
    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            left, top = get_left_top_of_tile(tile_x, tile_y)
            tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
            if tile_rect.collidepoint(x, y):
                return (tile_x, tile_y)
    return (None, None)

def draw_tile(tile_x, tile_y, number, adj_x=0, adj_y=0):
    """
    Draws a tile at board coordinates (tile_x, tile_y), with an optional offset of (adj_x, adj_y) pixels.

    Params:
        tile_x (int), tile_y (int): The board coordinates to draw at
        number (int): The number to put on the box
        adj_x (int), adj_y (int): Pixel offset to draw on
    """
    left, top = get_left_top_of_tile(tile_x, tile_y)
    pygame.draw.rect(DISPLAY, TILE_COLOR, (left + adj_x, top + adj_y, TILE_SIZE, TILE_SIZE))
    text_surf = BASIC_FONT.render(str(number), True, TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(TILE_SIZE / 2) + adj_x, top + int(TILE_SIZE / 2) + adj_y
    DISPLAY.blit(text_surf, text_rect)

def make_text(text, color, bgcolor, top, left):
    """
    Creates text on the screen that is positioned on the topleft point of the location specified

    Params:
        text (string): The text to display
        color (ColorValue): The color of the font
        bgcolor (ColorValue): The background color
        top (int), left (int): Top-left x and y coords for this text

    Returns:
        (Surface, Rect): The surface and location of the text
    """
    text_surf = BASIC_FONT.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return (text_surf, text_rect)

def draw_board(board, message):
    """
    Draws all of the board, its tiles, and option buttons, as well as an optional message to display on the top-left (i.e. board status)

    Params:
        board (int[][]): The board to draw
        message (string): The message to draw on the top-left corner, optional
    """
    DISPLAY.fill(BGCOLOR)
    if message:
        text_surf, text_rect = make_text(message, MESSAGE_COLOR, BGCOLOR, 5, 5)
        DISPLAY.blit(text_surf, text_rect)

    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            if board[tile_x][tile_y]:
                draw_tile(tile_x, tile_y, board[tile_x][tile_y])

    left, top = get_left_top_of_tile(0, 0)
    width = BOARD_WIDTH * TILE_SIZE
    height = BOARD_HEIGHT * TILE_SIZE

    # draw the border, with a thickness of 4 px
    pygame.draw.rect(DISPLAY, BORDER_COLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAY.blit(RESET_SURF, RESET_RECT)
    DISPLAY.blit(NEW_SURF, NEW_RECT)
    DISPLAY.blit(SOLVE_SURF, SOLVE_RECT)

def slide_animation(board, direction, message, animation_speed):
    """
    Perform the slide animation based on the direction/speed specified.

    This does not check the validity of the move.

    Params:
        board (int[][]): The board
        direction (string): Direction of slide
        message (string): What to display on the top left of the board
        animation_speed (int): How fast to move the tile being slid (pixels per frame)
    """
    blank_x, blank_y = get_blank_position(board)
    if direction == UP:
        move_x = blank_x
        move_y = blank_y + 1
    elif direction == DOWN:
        move_x = blank_x
        move_y = blank_y - 1
    elif direction == LEFT:
        move_x = blank_x + 1
        move_y = blank_y
    elif direction == RIGHT:
        move_x = blank_x - 1
        move_y = blank_y

    # prepare base surface
    draw_board(board, message)
    base_surf = DISPLAY.copy() # copy the current board state and use it as a "background" for sliding animation

    # draw blank spcae over moving tile on base_surf surface; this prevents it from "sticking" when we perform the moving animation
    move_left, move_top = get_left_top_of_tile(move_x, move_y)
    pygame.draw.rect(base_surf, BGCOLOR, (move_left, move_top, TILE_SIZE, TILE_SIZE))

    for i in range(0, TILE_SIZE, animation_speed):
        # dtaw the tile that is sliding over
        check_for_quit()
        DISPLAY.blit(base_surf, (0, 0))
        if direction == UP:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, -i)
        if direction == DOWN:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, i)
        if direction == LEFT:
            draw_tile(move_x, move_y, board[move_x][move_y], -i, 0)
        if direction == RIGHT:
            draw_tile(move_x, move_y, board[move_x][move_y], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generate_new_puzzle(num_slides):
    """
    Takes the starting (solved) board configuration and make num_slides number of random moves, all animated.

    Params:
        num_slides (int): Number of moves to make

    Returns:
        (int[][], string[]): The new board, along with the number of sequences it took to get to that board
    """
    sequence = []
    board = get_starting_board()
    draw_board(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    last_move = None
    for i in range(num_slides):
        move = get_random_move(board, last_move)
        if SHOW_SLIDING:
            slide_animation(board, move, 'Generating a new puzzle', animation_speed=int(TILE_SIZE / 3))
        make_move(board, move)
        sequence.append(move)
        last_move = move

    return (board, sequence)

def reset_animation(board, all_moves):
    """
    Perform all moves in 'all_moves' in reverse order; this should bring the board back to its original solved state.

    Params:
        board (int[][]): The board
        all_moves (string[]): The moves taken from the solved to current board state
    """
    rev_all_moves = all_moves[:] # copies the list
    rev_all_moves.reverse()

    for move in rev_all_moves:
        if move == UP:
            opposite_move = DOWN
        elif move == DOWN:
            opposite_move = UP
        elif move == RIGHT:
            opposite_move = LEFT
        elif move == LEFT:
            opposite_move = RIGHT
        slide_animation(board, opposite_move, '', animation_speed=int(TILE_SIZE / 2))
        make_move(board, opposite_move)

main()