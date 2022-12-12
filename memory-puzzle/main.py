import random, pygame, sys, math, os
from pygame.locals import *

sys.argv = sys.argv[1:] # remove first arg, that's the file name
assert len(sys.argv) == 4, 'There must be exactly 4 args supplied'
# arguments from cmd
# 0 = difficulty (0-6)
# 1 = difficulty scaling (0 or 1)
# 2 = limited attempts (0 or 1)
# 3 = color palette (0-2)

sys.argv[0] = int(sys.argv[0])
sys.argv[1] = int(sys.argv[1])
sys.argv[2] = int(sys.argv[2])
sys.argv[3] = int(sys.argv[3])
assert sys.argv[3] >= 0 and sys.argv[3] <= 2, 'Color palette can only be 0 - 2'

# GUI constants
FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 550
REVEAL_SPEED = 4 # box reveal speed (in pixels per tick)
BOX_SIZE = 40 # px
GAP_SIZE = 10 # px
WRONG_GUESS_RATIO = 2

# dynamic game variables
board_width = 4 # columns number
board_height = 4 # rows number
attempts_left = 4

# crashes program is the condition below is false to prevent further issues
assert (board_width * board_height) % 2 == 0, 'There must be an even number of boxes on the board'

x_margin = int((WINDOW_WIDTH - (board_width * (BOX_SIZE + GAP_SIZE))) / 2)
y_margin = int((WINDOW_HEIGHT - (board_height * (BOX_SIZE + GAP_SIZE))) / 2)

# from cmd args
difficulty = sys.argv[0] # (4x4, 4x6, 6x6, 6x8, 8x8, 8x10, 10x10) (can be changed during a game if difficulty scaling is true)
DIFFICULTY_SCALING = False if sys.argv[1] == 0 else True
LIMITED_ATTEMPTS = False if sys.argv[2] == 0 else True

dir_path = os.path.dirname(os.path.realpath(__file__)) # the file currently being ran (mainmenu.py)

PALETTE_FILE = dir_path + '/data/palettes/default.txt'
if sys.argv[3] == 1:
    PALETTE_FILE = dir_path + '/data/palettes/warmcolors.txt'
elif sys.argv[3] == 2:
    PALETTE_FILE = dir_path + '/data/palettes/coldcolors.txt'

f = open(PALETTE_FILE, "r") # open colors file for reading only
lines = f.readlines()

# color consts; load palettes from files (below are all currently default) - these are also loaded from cmd args
DARKGRAY = (50, 50, 50)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
COLOR1   = (int(lines[0].split(' ')[0]), int(lines[0].split(' ')[1]), int(lines[0].split(' ')[2]))
COLOR2   = (int(lines[1].split(' ')[0]), int(lines[1].split(' ')[1]), int(lines[1].split(' ')[2]))
COLOR3   = (int(lines[2].split(' ')[0]), int(lines[2].split(' ')[1]), int(lines[2].split(' ')[2]))
COLOR4   = (int(lines[3].split(' ')[0]), int(lines[3].split(' ')[1]), int(lines[3].split(' ')[2]))
COLOR5   = (int(lines[4].split(' ')[0]), int(lines[4].split(' ')[1]), int(lines[4].split(' ')[2]))
COLOR6   = (int(lines[5].split(' ')[0]), int(lines[5].split(' ')[1]), int(lines[5].split(' ')[2]))
COLOR7   = (int(lines[6].split(' ')[0]), int(lines[6].split(' ')[1]), int(lines[6].split(' ')[2]))
assert difficulty >= 0 and difficulty <= 6, 'Difficulty must be from 0 - 6'
assert DIFFICULTY_SCALING == True or DIFFICULTY_SCALING == False, 'Difficulty scaling must be True or False'
assert LIMITED_ATTEMPTS == True or LIMITED_ATTEMPTS == False, 'Limited attempts must be True or False'

# other color stuff
BGCOLOR = DARKGRAY
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = COLOR3

# shape constants
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
HEXAGON = 'hexagon'
HOURGLASS = 'HOURGLASS'
SMILEY_FACE = 'smiley_face'

# tuples for all combinations of icons
ALLCOLORS = (COLOR1, COLOR2, COLOR3, COLOR4, COLOR5, COLOR6, COLOR7)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL, HEXAGON, HOURGLASS, SMILEY_FACE)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= board_width * board_height, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAY, board_width, board_height, difficulty, attempts_left
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.Font('freesansbold.ttf', 20)

    mouse_x = 0 # x coord of mousedown
    mouse_y = 0 # y coord of mousedown
    pygame.display.set_caption('Memory Puzzle')

    board_width, board_height = set_board_size(difficulty)
    attempts_left = int((board_width * board_height) / WRONG_GUESS_RATIO)

    main_board = get_randomized_board(board_width, board_height)
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None # (x, y) of first box clicked per turn

    DISPLAY.fill(BGCOLOR)
    start_game_animation(main_board)

    while True:
        mouse_clicked = False

        attempts_text_surf = font.render(f'You have {attempts_left} wrong guess' + ('es' if attempts_left > 1 else '') + ' left' if LIMITED_ATTEMPTS else '', True, (255,255,255), BGCOLOR)
        attempts_text_rect = attempts_text_surf.get_rect()
        attempts_text_rect.center = (155, 540)

        DISPLAY.fill(BGCOLOR) # draw the window
        DISPLAY.blit(attempts_text_surf, attempts_text_rect)
        draw_board(main_board, revealed_boxes)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

        box_x, box_y = get_box_at_pixel(mouse_x, mouse_y)
        if box_x != None and box_y != None:
            # mosue is over a box
            if not revealed_boxes[box_x][box_y]:
                if not mouse_clicked:
                    draw_highlight_box(box_x, box_y) # highlight box on mouse hover
                else:
                    reveal_boxes_animation(main_board, [(box_x, box_y)])
                    revealed_boxes[box_x][box_y] = True # set this box as revealed so it doesn't suddenly close
                    if first_selection == None: # first box clicked this turn
                        first_selection = (box_x, box_y)
                    else:
                        # check for match
                        icon1shape, icon1color = get_shape_and_color(main_board, first_selection[0], first_selection[1])
                        icon2shape, icon2color = get_shape_and_color(main_board, box_x, box_y)

                        if icon1shape != icon2shape or icon1color != icon2color:
                            # no match, cover both boxes
                            pygame.time.wait(1000)
                            cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (box_x, box_y)])
                            revealed_boxes[first_selection[0]][first_selection[1]] = False
                            revealed_boxes[box_x][box_y] = False

                            if LIMITED_ATTEMPTS:
                                attempts_left -= 1
                                if attempts_left == 0:
                                    # we're done
                                    attempts_text_surf = font.render(f'Game over...' if LIMITED_ATTEMPTS else '', True, (255,255,255), BGCOLOR)
                                    DISPLAY.fill(BGCOLOR) # draw the window
                                    DISPLAY.blit(attempts_text_surf, attempts_text_rect)
                                    draw_board(main_board, revealed_boxes)
                                    pygame.display.update()
                                    pygame.time.wait(2000)

                                    # reset board
                                    attempts_left = int((board_width * board_height) / WRONG_GUESS_RATIO)
                                    main_board = get_randomized_board(board_width, board_height)
                                    revealed_boxes = generate_revealed_boxes_data(False)

                                    # show fully unrevealed board
                                    attempts_text_surf = font.render(f'Re-randomizing...' if LIMITED_ATTEMPTS else '', True, (255,255,255), BGCOLOR)
                                    DISPLAY.fill(BGCOLOR) # draw the window
                                    DISPLAY.blit(attempts_text_surf, attempts_text_rect)
                                    draw_board(main_board, revealed_boxes)
                                    pygame.display.update()
                                    pygame.time.wait(1000)

                                    # replay start game animation
                                    start_game_animation(main_board)
                        elif has_won(revealed_boxes): # found all pairs?
                            game_won_animation(main_board)
                            pygame.time.wait(2000)

                            if DIFFICULTY_SCALING:
                                difficulty += 1
                                if difficulty > 6:
                                    difficulty = 6
                                board_width, board_height = set_board_size(difficulty)

                            # reset board
                            attempts_left = int((board_width * board_height) / WRONG_GUESS_RATIO)
                            main_board = get_randomized_board(board_width, board_height)
                            revealed_boxes = generate_revealed_boxes_data(False)

                            # show fully unrevealed board
                            draw_board(main_board, revealed_boxes)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            # replay start game animation
                            start_game_animation(main_board)
                        first_selection = None # reset first selection
        
        # redraw
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def set_board_size(difficulty):
    """
    Sets board size based on difficulty (0 - 6)
    """
    global board_width, board_height, x_margin, y_margin

    if difficulty == 0:
        board_height = 4
        board_width = 4
    elif difficulty == 1:
        board_height = 4
        board_width = 6
    elif difficulty == 2:
        board_height = 6
        board_width = 6
    elif difficulty == 3:
        board_height = 6
        board_width = 8
    elif difficulty == 4:
        board_height = 8
        board_width = 8
    elif difficulty == 5:
        board_height = 8
        board_width = 10
    elif difficulty == 6:
        board_height = 10
        board_width = 10
    assert (board_width * board_height) % 2 == 0, 'There must be an even number of boxes on the board'

    x_margin = int((WINDOW_WIDTH - (board_width * (BOX_SIZE + GAP_SIZE))) / 2)
    y_margin = int((WINDOW_HEIGHT - (board_height * (BOX_SIZE + GAP_SIZE))) / 2)

    return board_width, board_height
            

def generate_revealed_boxes_data(val):
    """
    Sets the revealed status of every box on the board to 'val'

    Params:
        val (bool): State to set every box to

    Returns:
        (list): The new array of booleans containing every box's revealed status
    """
    revealed_boxes = []
    for i in range(board_width):
        revealed_boxes.append([val] * board_height)
    return revealed_boxes

def get_randomized_board(board_width, board_height):
    """
    Generates a randomized board, consisting of two of each combination of shape/color possible

    Returns:
        (list): The board, consisting of an icon in each available spot. The number of icons used depends on the board dimension constants' values
    """
    # get every possible combination of shape & color
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    
    random.shuffle(icons) # order of icons we will use
    num_icons_used = int(board_width * board_height / 2)

    icons = icons[:num_icons_used] * 2 # make two of each icon being used
    random.shuffle(icons) # the actual order of icons on the board

    # add icons to board
    board = []
    for x in range(board_width):
        column = []
        for y in range(board_height):
            column.append(icons[0])
            del icons[0] # remove icons from list as we add them
        board.append(column)
    return board

def split_into_groups_of(group_size, arr):
    """
    Splits the given 'arr' into an array of subarrays, with each inner array being at most 'group_size' elements long.

    Params:
        group_size (int): Maximum number of items in each subarray
        arr (array): The array to split

    Returns:
        (arr[arr]): An array of subarrays of the original 'arr', with each subarray being at most 'group_size' items in length
    """
    result = []
    for i in range(0, len(arr), group_size):
        result.append(arr[i:i + group_size])
    return result

def left_top_coords_of_box(box_x, box_y):
    """
    Based on the box indices supplied, gets the x/y coordinates of the top-left corner of the box given. i.e. (1, 0) box indices will be the 2nd box in the 1st row

    Returns:
        (int, int): x/y coords of the top-left corner of the box
    """
    global x_margin, y_margin
    left = box_x * (BOX_SIZE + GAP_SIZE) + x_margin
    top = box_y * (BOX_SIZE + GAP_SIZE) + y_margin
    return (left, top)

def get_box_at_pixel(x, y):
    """
    Gets the box located at (x, y), if one exists

    Params:
        x (int): x coordinate
        y (int): y coordinate

    Returns:
        (int, int): box indices of the box at (x, y); will return (None, None) if a box does not exist
    """
    for box_x in range(board_width):
        for box_y in range(board_height):
            left, top = left_top_coords_of_box(box_x, box_y)
            box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if box_rect.collidepoint(x, y):
                return (box_x, box_y)
    return (None, None)

def draw_icon(shape, color, box_x, box_y):
    """
    Draw the specified icon and color within the specified box indices

    Params:
        shape (string): The type of shape to draw
        color (Color): The color to draw this shape in
        box_x (int): Box index (x)
        box_y (int): Box index (y)
    """
    tenth = int(BOX_SIZE * 0.1)
    quarter = int(BOX_SIZE * 0.25)
    half = int(BOX_SIZE * 0.5)

    left, top = left_top_coords_of_box(box_x, box_y) # get pixel coords from this box

    # draw shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAY, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAY, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(DISPLAY, color, (left, top + i), (left + i, top), 3)
            pygame.draw.line(DISPLAY, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i), 3)
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY, color, (left, top + quarter, BOX_SIZE, half))
    elif shape == HEXAGON:
        pygame.draw.polygon(DISPLAY, color, ((left + quarter, top + tenth), (left + BOX_SIZE - quarter, top + tenth), (left + BOX_SIZE - tenth, top + half), (left + BOX_SIZE - quarter, top + BOX_SIZE - tenth), (left + quarter, top + BOX_SIZE - tenth), (left + tenth, top + half)))
    elif shape == HOURGLASS:
        pygame.draw.polygon(DISPLAY, color, ((left + quarter, top + quarter), (left + 3*quarter, top + quarter), (left + quarter, top + 3*quarter), (left + 3*quarter, top + 3*quarter)))
    elif shape == SMILEY_FACE:
        pygame.draw.line(DISPLAY, color, (left + quarter, top + tenth), (left + quarter, top + half), 3)
        pygame.draw.line(DISPLAY, color, (left + 3*quarter, top + tenth), (left + 3*quarter, top + half), 3)
        pygame.draw.line(DISPLAY, color, (left + quarter, top + 3*quarter), (left + half, top + BOX_SIZE - tenth), 3)
        pygame.draw.line(DISPLAY, color, (left + 3*quarter, top + 3*quarter), (left + half, top + BOX_SIZE - tenth), 3)

def get_shape_and_color(board, box_x, box_y):
    """
    Gets the shape/color of the icon within the specified box indices

    Returns:
        The shape
        The color
    """
    return board[box_x][box_y][0], board[box_x][box_y][1]

def draw_box_covers(board, boxes, coverage):
    """
    Animates the boxes being covered and revealed.

    Params:
        board: The board containing all boxes
        boxes: A list of boxes to (un)cover
        coverage: Amount of coverage (in pixels) over the box to draw. 0 = box completely uncovered
    """
    for box in boxes:
        left, top = left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(DISPLAY, BGCOLOR, (left, top, BOX_SIZE, BOX_SIZE)) # paint over everything that already existed here; use BG color
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1]) # draw icon
        if coverage > 0:
            pygame.draw.rect(DISPLAY, BOXCOLOR, (left, top, coverage, BOX_SIZE)) # cover the icon to some extent
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def reveal_boxes_animation(board, reveal):
    """
    Perform reveal animation for all boxes in 'reveal'
    """
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED):
        draw_box_covers(board, reveal, coverage)

def cover_boxes_animation(board, cover):
    """
    Perform cover animation for all boxes in 'cover'
    """
    for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED):
        draw_box_covers(board, cover, coverage)

def draw_board(board, revealed):
    """
    Draws the full board and its boxes in each of their reveal states.
    """
    for box_x in range(board_width):
        for box_y in range(board_height):
            left, top = left_top_coords_of_box(box_x, box_y)
            if not revealed[box_x][box_y]:
                # covered
                pygame.draw.rect(DISPLAY, BOXCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                # revealed; draw icon
                shape, color = get_shape_and_color(board, box_x, box_y)
                draw_icon(shape, color, box_x, box_y)

def draw_highlight_box(box_x, box_y):
    """
    Draws a square highlight around this box, to be used in conjunction with mouse hover.
    """
    left, top = left_top_coords_of_box(box_x, box_y)
    pygame.draw.rect(DISPLAY, HIGHLIGHTCOLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)

def start_game_animation(board):
    """
    Draws the board on the screen and reveals 8 random boxes (maximum) at a time. Amount of boxes revealed at a time scales with board size.
    """
    pygame.event.pump() # prevents game from freezing when this is called after a game is won
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for x in range(board_width):
        for y in range(board_height):
            boxes.append((x, y))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(int(math.ceil((board_width * board_height) / 8)), boxes)

    draw_board(board, covered_boxes)
    for box_group in box_groups:
        reveal_boxes_animation(board, box_group)
        cover_boxes_animation(board, box_group)

def game_won_animation(board):
    """
    Flashes the background color.
    """
    covered_boxes = generate_revealed_boxes_data(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors

        # after filling screen, redraw board on top
        DISPLAY.fill(color1)
        draw_board(board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(200)

def has_won(revealed):
    """
    Returns true if all boxes revealed, otherwise false
    """
    for box in revealed:
        if False in box:
            return False
    return True

main()