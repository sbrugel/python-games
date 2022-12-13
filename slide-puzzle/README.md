# Slide Puzzle

Originally done by Al Sweigart, this is a Pygame adaptation of the classic slide puzzle game.

The board is a square grid with number tiles filling all parts of the board except one spot (which is blank). The tiles start out in random positions, and the player must slide tiles around until the tiles are back in their original order.

![image](https://i.imgur.com/lisUCjJ.gif)

## Controls

`Arrow keys` - Move tiles around

## Customizability

- Board size can be 3x3, 4x4, or 5x5
- The difficulty, determined by number of moves done when shuffling, can be set to one of 5 different presets
- Difficulty scaling toggle (number of shuffle moves increases with each win). Only applies if the player solved the puzzle entirely on their own, WITHOUT clicking the "Solve" button.
- Toggle showing moves when shuffling to make the game easier or harder.
- Can set custom colors for the tiles and background

## Other changes from original

- [Change] FPS increased to 60 with animation speeds changed accordingly
- [Docs] Function documentation and additional comments added
