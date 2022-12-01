import random, pygame, sys, math
from pygame.locals import *

# GUI constants
FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 4 # box reveal speed (in pixels per tick)
BOXSIZE = 40 # px
GAPSIZE = 10 # px

# dynamic game variables
boardwidth = 4 # columns number
boardheight = 4 # rows number

# crashes program is the condition below is false to prevent further issues
assert (boardwidth * boardheight) % 2 == 0, 'There must be an even number of boxes on the board'

XMARGIN = int((WINDOWWIDTH - (boardwidth * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (boardheight * (BOXSIZE + GAPSIZE))) / 2)

# color constants (RGB)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

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
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL, HEXAGON, HOURGLASS, SMILEY_FACE)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= boardwidth * boardheight, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAY
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # x coord of mousedown
    mousey = 0 # y coord of mousedown
    pygame.display.set_caption('Memory Puzzle')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # (x, y) of first box clicked per turn

    DISPLAY.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        DISPLAY.fill(BGCOLOR) # draw the window
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
                        elif hasWon(revealedBoxes): # found all pairs?
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)

                            # reset board
                            mainBoard = getRandomizedBoard()
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

def getRandomizedBoard():
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
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
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
            pygame.draw.line(DISPLAY, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAY, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY, color, (left, top + quarter, BOXSIZE, half))
    elif shape == HEXAGON:
        pygame.draw.polygon(DISPLAY, color, ((left + quarter, top + tenth), (left + BOXSIZE - quarter, top + tenth), (left + BOXSIZE - tenth, top + half), (left + BOXSIZE - quarter, top + BOXSIZE - tenth), (left + quarter, top + BOXSIZE - tenth), (left + tenth, top + half)))
    elif shape == HOURGLASS:
        pygame.draw.polygon(DISPLAY, color, ((left + quarter, top + quarter), (left + 3*quarter, top + quarter), (left + quarter, top + 3*quarter), (left + 3*quarter, top + 3*quarter)))
    elif shape == SMILEY_FACE:
        pygame.draw.line(DISPLAY, color, (left + quarter, top + tenth), (left + quarter, top + half))
        pygame.draw.line(DISPLAY, color, (left + 3*quarter, top + tenth), (left + 3*quarter, top + half))
        pygame.draw.line(DISPLAY, color, (left + quarter, top + 3*quarter), (left + half, top + BOXSIZE - tenth))
        pygame.draw.line(DISPLAY, color, (left + 3*quarter, top + 3*quarter), (left + half, top + BOXSIZE - tenth))

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