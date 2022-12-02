import random, pygame, sys, math
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
WINDOWWIDTH = 640
WINDOWHEIGHT = 550
REVEALSPEED = 4 # box reveal speed (in pixels per tick)
BOXSIZE = 40 # px
GAPSIZE = 10 # px
WRONG_GUESS_RATIO = 2

# dynamic game variables
boardwidth = 4 # columns number
boardheight = 4 # rows number
attemptsleft = 4

# crashes program is the condition below is false to prevent further issues
assert (boardwidth * boardheight) % 2 == 0, 'There must be an even number of boxes on the board'

xmargin = int((WINDOWWIDTH - (boardwidth * (BOXSIZE + GAPSIZE))) / 2)
ymargin = int((WINDOWHEIGHT - (boardheight * (BOXSIZE + GAPSIZE))) / 2)

# from cmd args
difficulty = sys.argv[0] # (4x4, 4x6, 6x6, 6x8, 8x8, 8x10, 10x10) (can be changed during a game if difficulty scaling is true)
DIFFICULTY_SCALING = False if sys.argv[1] == 0 else True
LIMITED_ATTEMPTS = False if sys.argv[2] == 0 else True
PALETTE_FILE = 'data/palettes/default.txt'
if sys.argv[3] == 1:
    PALETTE_FILE = 'data/palettes/warmcolors.txt'
elif sys.argv[3] == 2:
    PALETTE_FILE = 'data/palettes/coldcolors.txt'

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
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= boardwidth * boardheight, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAY, boardwidth, boardheight, difficulty, attemptsleft
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    font = pygame.font.Font('freesansbold.ttf', 20)

    mousex = 0 # x coord of mousedown
    mousey = 0 # y coord of mousedown
    pygame.display.set_caption('Memory Puzzle')

    boardwidth, boardheight = setBoardSize(difficulty)
    attemptsleft = int((boardwidth * boardheight) / WRONG_GUESS_RATIO)

    mainBoard = getRandomizedBoard(boardwidth, boardheight)
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # (x, y) of first box clicked per turn

    DISPLAY.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        attempts_text_surf = font.render(f'You have {attemptsleft} wrong guess' + ('es' if attemptsleft > 1 else '') + ' left' if LIMITED_ATTEMPTS else '', True, (255,255,255), BGCOLOR)
        attempts_text_rect = attempts_text_surf.get_rect()
        attempts_text_rect.center = (155, 540)

        DISPLAY.fill(BGCOLOR) # draw the window
        DISPLAY.blit(attempts_text_surf, attempts_text_rect)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # mosue is over a box
            if not revealedBoxes[boxx][boxy]:
                if not mouseClicked:
                    drawHighlightBox(boxx, boxy) # highlight box on mouse hover
                else:
                    revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                    revealedBoxes[boxx][boxy] = True # set this box as revealed so it doesn't suddenly close
                    if firstSelection == None: # first box clicked this turn
                        firstSelection = (boxx, boxy)
                    else:
                        # check for match
                        icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                        if icon1shape != icon2shape or icon1color != icon2color:
                            # no match, cover both boxes
                            pygame.time.wait(1000)
                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False

                            if LIMITED_ATTEMPTS:
                                attemptsleft -= 1
                                if attemptsleft == 0:
                                    # we're done
                                    attempts_text_surf = font.render(f'Game over...' if LIMITED_ATTEMPTS else '', True, (255,255,255), BGCOLOR)
                                    DISPLAY.fill(BGCOLOR) # draw the window
                                    DISPLAY.blit(attempts_text_surf, attempts_text_rect)
                                    drawBoard(mainBoard, revealedBoxes)
                                    pygame.display.update()
                                    pygame.time.wait(2000)

                                    # reset board
                                    attemptsleft = int((boardwidth * boardheight) / WRONG_GUESS_RATIO)
                                    mainBoard = getRandomizedBoard(boardwidth, boardheight)
                                    revealedBoxes = generateRevealedBoxesData(False)

                                    # show fully unrevealed board
                                    attempts_text_surf = font.render(f'Re-randomizing...' if LIMITED_ATTEMPTS else '', True, (255,255,255), BGCOLOR)
                                    DISPLAY.fill(BGCOLOR) # draw the window
                                    DISPLAY.blit(attempts_text_surf, attempts_text_rect)
                                    drawBoard(mainBoard, revealedBoxes)
                                    pygame.display.update()
                                    pygame.time.wait(1000)

                                    # replay start game animation
                                    startGameAnimation(mainBoard)
                        elif hasWon(revealedBoxes): # found all pairs?
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)

                            if DIFFICULTY_SCALING:
                                difficulty += 1
                                if difficulty > 6:
                                    difficulty = 6
                                boardwidth, boardheight = setBoardSize(difficulty)

                            # reset board
                            attemptsleft = int((boardwidth * boardheight) / WRONG_GUESS_RATIO)
                            mainBoard = getRandomizedBoard(boardwidth, boardheight)
                            revealedBoxes = generateRevealedBoxesData(False)

                            # show fully unrevealed board
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            # replay start game animation
                            startGameAnimation(mainBoard)
                        firstSelection = None # reset first selection
        
        # redraw
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def setBoardSize(difficulty):
    """
    Sets board size based on difficulty (0 - 6)
    """
    global boardwidth, boardheight, xmargin, ymargin

    if difficulty == 0:
        boardheight = 4
        boardwidth = 4
    elif difficulty == 1:
        boardheight = 4
        boardwidth = 6
    elif difficulty == 2:
        boardheight = 6
        boardwidth = 6
    elif difficulty == 3:
        boardheight = 6
        boardwidth = 8
    elif difficulty == 4:
        boardheight = 8
        boardwidth = 8
    elif difficulty == 5:
        boardheight = 8
        boardwidth = 10
    elif difficulty == 6:
        boardheight = 10
        boardwidth = 10
    assert (boardwidth * boardheight) % 2 == 0, 'There must be an even number of boxes on the board'

    xmargin = int((WINDOWWIDTH - (boardwidth * (BOXSIZE + GAPSIZE))) / 2)
    ymargin = int((WINDOWHEIGHT - (boardheight * (BOXSIZE + GAPSIZE))) / 2)

    return boardwidth, boardheight
            

def generateRevealedBoxesData(val):
    """
    Sets the revealed status of every box on the board to 'val'

    Params:
        val (bool): State to set every box to

    Returns:
        (list): The new array of booleans containing every box's revealed status
    """
    revealedBoxes = []
    for i in range(boardwidth):
        revealedBoxes.append([val] * boardheight)
    return revealedBoxes

def getRandomizedBoard(boardwidth, boardheight):
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
    numIconsUsed = int(boardwidth * boardheight / 2)

    icons = icons[:numIconsUsed] * 2 # make two of each icon being used
    random.shuffle(icons) # the actual order of icons on the board

    # add icons to board
    board = []
    for x in range(boardwidth):
        column = []
        for y in range(boardheight):
            column.append(icons[0])
            del icons[0] # remove icons from list as we add them
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, arr):
    """
    Splits the given 'arr' into an array of subarrays, with each inner array being at most 'groupSize' elements long.

    Params:
        groupSize (int): Maximum number of items in each subarray
        arr (array): The array to split

    Returns:
        (arr[arr]): An array of subarrays of the original 'arr', with each subarray being at most 'groupSize' items in length
    """
    result = []
    for i in range(0, len(arr), groupSize):
        result.append(arr[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    """
    Based on the box indices supplied, gets the x/y coordinates of the top-left corner of the box given. i.e. (1, 0) box indices will be the 2nd box in the 1st row

    Returns:
        (int, int): x/y coords of the top-left corner of the box
    """
    global xmargin, ymargin
    left = boxx * (BOXSIZE + GAPSIZE) + xmargin
    top = boxy * (BOXSIZE + GAPSIZE) + ymargin
    return (left, top)

def getBoxAtPixel(x, y):
    """
    Gets the box located at (x, y), if one exists

    Params:
        x (int): x coordinate
        y (int): y coordinate

    Returns:
        (int, int): box indices of the box at (x, y); will return (None, None) if a box does not exist
    """
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    """
    Draw the specified icon and color within the specified box indices

    Params:
        shape (string): The type of shape to draw
        color (Color): The color to draw this shape in
        boxx (int): Box index (x)
        boxy (int): Box index (y)
    """
    tenth = int(BOXSIZE * 0.1)
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from this box

    # draw shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAY, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAY, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAY, color, (left, top + i), (left + i, top), 3)
            pygame.draw.line(DISPLAY, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i), 3)
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY, color, (left, top + quarter, BOXSIZE, half))
    elif shape == HEXAGON:
        pygame.draw.polygon(DISPLAY, color, ((left + quarter, top + tenth), (left + BOXSIZE - quarter, top + tenth), (left + BOXSIZE - tenth, top + half), (left + BOXSIZE - quarter, top + BOXSIZE - tenth), (left + quarter, top + BOXSIZE - tenth), (left + tenth, top + half)))
    elif shape == HOURGLASS:
        pygame.draw.polygon(DISPLAY, color, ((left + quarter, top + quarter), (left + 3*quarter, top + quarter), (left + quarter, top + 3*quarter), (left + 3*quarter, top + 3*quarter)))
    elif shape == SMILEY_FACE:
        pygame.draw.line(DISPLAY, color, (left + quarter, top + tenth), (left + quarter, top + half), 3)
        pygame.draw.line(DISPLAY, color, (left + 3*quarter, top + tenth), (left + 3*quarter, top + half), 3)
        pygame.draw.line(DISPLAY, color, (left + quarter, top + 3*quarter), (left + half, top + BOXSIZE - tenth), 3)
        pygame.draw.line(DISPLAY, color, (left + 3*quarter, top + 3*quarter), (left + half, top + BOXSIZE - tenth), 3)

def getShapeAndColor(board, boxx, boxy):
    """
    Gets the shape/color of the icon within the specified box indices

    Returns:
        The shape
        The color
    """
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    """
    Animates the boxes being covered and revealed.

    Params:
        board: The board containing all boxes
        boxes: A list of boxes to (un)cover
        coverage: Amount of coverage (in pixels) over the box to draw. 0 = box completely uncovered
    """
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAY, BGCOLOR, (left, top, BOXSIZE, BOXSIZE)) # paint over everything that already existed here; use BG color
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1]) # draw icon
        if coverage > 0:
            pygame.draw.rect(DISPLAY, BOXCOLOR, (left, top, coverage, BOXSIZE)) # cover the icon to some extent
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, reveal):
    """
    Perform reveal animation for all boxes in 'reveal'
    """
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, reveal, coverage)

def coverBoxesAnimation(board, cover):
    """
    Perform cover animation for all boxes in 'cover'
    """
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, cover, coverage)

def drawBoard(board, revealed):
    """
    Draws the full board and its boxes in each of their reveal states.
    """
    for boxx in range(boardwidth):
        for boxy in range(boardheight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # covered
                pygame.draw.rect(DISPLAY, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # revealed; draw icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    """
    Draws a square highlight around this box, to be used in conjunction with mouse hover.
    """
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAY, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def startGameAnimation(board):
    """
    Draws the board on the screen and reveals 8 random boxes (maximum) at a time. Amount of boxes revealed at a time scales with board size.
    """
    pygame.event.pump() # prevents game from freezing when this is called after a game is won
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(boardwidth):
        for y in range(boardheight):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(int(math.ceil((boardwidth * boardheight) / 8)), boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    """
    Flashes the background color.
    """
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors

        # after filling screen, redraw board on top
        DISPLAY.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(200)

def hasWon(revealed):
    """
    Returns true if all boxes revealed, otherwise false
    """
    for box in revealed:
        if False in box:
            return False
    return True

main()