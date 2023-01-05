import pygame, sys, math, copy
from pygame.locals import *

WIN_WIDTH = 400
WIN_HEIGHT = 400
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BG_COLOR = WHITE
LINE_COLOR = BLACK
X_COLOR = RED
O_COLOR = BLUE
SLEEP_TIME = 500

X = 'x' # moves first
O = 'o'
P1 = X # the piece player 1 has
P2 = O # the piece player 2 has
P2_CPU = True # is player 2 a computer player or not?
current_turn = P1 if P1 == X else P2 # who is currently playing

board = [['', '', ''], ['', '', ''], ['', '', '']] # 0-1-2, 3-4-5, 6-7-8
"""
1 | 2 | 3
=========
4 | 5 | 6
=========
7 | 8 | 9
"""

def main():
    global FPSCLOCK, DISPLAY, BASIC_FONT, board, current_turn

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Tic-Tac-Toe')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 20)

    waiting_for_input = True
    game_won = False

    # game loop
    while True:
        events = pygame.event.get()
        if is_board_full(board) or not game_won == 0: # end of game, stick here until we want to play again
            text = 'It\'s a tie!' if is_board_full(board) and game_won == 0 else ('Player ' + str(game_won) + ' has won!')
            draw_screen_data(board, text, False)
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            continue

        draw_screen_data(board, 'Player ' + ('1' if current_turn == P1 else '2') + ', it\'s your turn', True)

        if current_turn == P2 and P2_CPU:
            # computer move
            draw_screen_data(board, 'The CPU is making its turn...', False)

            # syntactic sugars for board
            X_COORD = 0
            Y_COORD = 1

            move = -1 # tile number

            # can I win on the next move, or
            # can the player win on the next move?
            for attempt in range(3):
                if attempt < 2:
                    for tile in range(9):
                        piece_here = board[tile_num_to_board_coords(tile)[X_COORD]][tile_num_to_board_coords(tile)[Y_COORD]]
                        opposite_turn = P2 if current_turn == P1 else P1
                        if piece_here == '':
                            board_copy = copy.deepcopy(board) # what would the board look like if I made this move?
                            board_copy[tile_num_to_board_coords(tile)[X_COORD]][tile_num_to_board_coords(tile)[Y_COORD]] = current_turn if attempt == 0 else opposite_turn
                            # prioritize me winning over the opponent
                            if is_board_winning(board_copy):
                                move = tile
                                break

            if move == -1: # still not found a move yet
                BEST_MOVES = [4,0,2,6,8,1,3,5,7] # if I must make a move arbitarily, this is the order from highest-lowest priority to choose from
                for tile in range(len(BEST_MOVES)):
                    piece_here = board[tile_num_to_board_coords(BEST_MOVES[tile])[X_COORD]][tile_num_to_board_coords(BEST_MOVES[tile])[Y_COORD]]
                    if piece_here == '':
                        move = BEST_MOVES[tile]
                        break

            board[tile_num_to_board_coords(move)[X_COORD]][tile_num_to_board_coords(move)[Y_COORD]] = current_turn
            # wrap up turn
            current_turn = P1
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.wait(SLEEP_TIME) # slack between turns
            game_won = is_board_winning(board)
            continue

        waiting_for_input = True
        clicked_button = None

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                clicked_button = get_button_clicked_from_mouse(mx, my)
            elif event.type == KEYDOWN:
                # keys 0-8 select a square
                key = event.key # 49-57 for keys 1-9
                if key >= 49 and key <= 57:
                    clicked_button = get_button_clicked_from_key(key - 49)

        if waiting_for_input:
            # waiting for player to select a square
            if clicked_button:
                # syntactic sugars
                X_COORD = 0
                Y_COORD = 1
                if board[clicked_button[X_COORD]][clicked_button[Y_COORD]] == '':
                    # make the move, advancing turn
                    board[clicked_button[X_COORD]][clicked_button[Y_COORD]] = current_turn # set the piece here to the current player's piece
                    current_turn = P2 if current_turn == P1 else P1
                    draw_screen_data(board, 'Advancing turns...', False)
                    waiting_for_input = False

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if not waiting_for_input:
            pygame.time.wait(SLEEP_TIME) # slack between turns
            game_won = is_board_winning(board)

def draw_board(board, highlights):
    """
    Draws an empty board firstly, then filling out spaces automatically based on board data
    Also draws box highlights for empty tiles if 'highlights' is True
    """
    # verticals
    pygame.draw.line(DISPLAY, BLACK, (150, 55), (150, WIN_HEIGHT - 55), 10)
    pygame.draw.line(DISPLAY, BLACK, (250, 55), (250, WIN_HEIGHT - 55), 10)

    # horizontals
    pygame.draw.line(DISPLAY, BLACK, (55, 150), (WIN_WIDTH - 55, 150), 10)
    pygame.draw.line(DISPLAY, BLACK, (55, 250), (WIN_WIDTH - 55, 250), 10)

    # draw board data
    for x in range(0, 3):
        for y in range(0, 3):
            if board[x][y]:
                draw_icon(board[x][y], x, y)
            elif highlights:
                highlight_space(x, y)

def draw_screen_data(board, text, highlights):
    """
    Draws the whole game layout from scratch, including text, board, and highlights (if enabled)
    """
    DISPLAY.fill(WHITE)
    turn_surf = BASIC_FONT.render(text, True, BLACK)
    turn_rect = turn_surf.get_rect()
    turn_rect.topleft = (5, WIN_HEIGHT - 25)
    DISPLAY.blit(turn_surf, turn_rect)
    draw_board(board, highlights)

def draw_icon(icon, x, y):
    """
    Draws 'icon' (x or o) on board coordinates x and y (each ranging from 0-2)
    """
    if board[x][y] != '' and board[x][y] != icon:
        print('ERROR in draw_icon: Can\'t replace icon with different icon')
        return

    if icon == O:
        pygame.draw.circle(DISPLAY, O_COLOR, (100 * (x + 1), 100 * (y + 1)), 25, 5)
    elif icon == X:
        pygame.draw.line(DISPLAY, X_COLOR, (75 + (100 * x), 75 + (100 * y)), (125 + (100 * x), 125 + (100 * y)), 5)
        pygame.draw.line(DISPLAY, X_COLOR, (125 + (100 * x), 75 + (100 * y)), (75 + (100 * x), 125 + (100 * y)), 5)

def highlight_space(x, y):
    """
    Highlight square at board coordinates x and y (0-2)
    """
    pygame.draw.rect(DISPLAY, BLUE, pygame.Rect((2 * x + 1) * 50 + 5, (2 * y + 1) * 50 + 5, 91, 91), 10)

def get_button_clicked_from_key(num):
    """
    Gets the button clicked based on tile num
    """
    if (num < 0 or num > 8):
        return None

    return tile_num_to_board_coords(num)

def get_button_clicked_from_mouse(x, y):
    """
    Converts window coordinates to board coordinates
    """
    if (x < 55 or x > WIN_HEIGHT - 55) or (y < 50 or y > WIN_HEIGHT - 50):
        return None

    board_x = math.floor((x - 55) / 100)
    board_y = math.floor((y - 50) / 100)
    return board_x, board_y

def tile_num_to_board_coords(num):
    """
    Converts a number from 0-8 to board coords
        i.e. 0 = (0, 0); 3 = (0, 1). See line 26 / declaration of 'board' global variable
    """
    return (num % 3, math.floor(num / 3))

def is_board_winning(board):
    """
    Determines if someone has won the game. Returns 1 or 2 if so depending on player, 0 otherwise
    (Does not look for ties, that is covered in 'is_board_full')
    """
    winning_combos = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
		[0, 3, 6],
		[1, 4, 7],
		[2, 5, 8],
		[0, 4, 8],
		[2, 4, 6]
    ]

    # syntactic sugars for board
    X_COORD = 0
    Y_COORD = 1

    for combo in range(len(winning_combos)):
        tile_0 = board[tile_num_to_board_coords(winning_combos[combo][0])[X_COORD]][tile_num_to_board_coords(winning_combos[combo][0])[Y_COORD]]
        tile_1 = board[tile_num_to_board_coords(winning_combos[combo][1])[X_COORD]][tile_num_to_board_coords(winning_combos[combo][1])[Y_COORD]]
        tile_2 = board[tile_num_to_board_coords(winning_combos[combo][2])[X_COORD]][tile_num_to_board_coords(winning_combos[combo][2])[Y_COORD]]
        
        if tile_0 and tile_0 == tile_1 and tile_1 == tile_2:
            return 1 if tile_0 == X else 2

    return 0

def is_board_full(board):
    """
    Returns true if board is full, False otherwise
    """
    for x in range(0, 3):
        for y in range(0, 3):
            if not board[x][y]:
                return False
    return True

main()