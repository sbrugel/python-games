# Memory Puzzle

Originally done by Al Sweigart, this is a Pygame adaptation of the classic memory puzzle game.

The player is presented with a board of boxes covering different icons (shapes of different colors). The player must select pairs of matching icons until all icons on the board are revealed.

## Controls

`Left Click` - Open a box

## Changes from original

- [New] 7 board size presets ranging from 4x4 to 10x10
- [New] "Difficulty scaling" toggle: every time you win a game, the board size increases by one preset (based on the above)
- [New] Added three more shapes: hexagon, hourglass, smiley face
- [Change] FPS increased to 60 with animation speeds changed accordingly
- [Change] When boxes are revealed at start, number of boxes opened at a time scales with board size
- [Change] Window size slight increase
- [Fix] Window no longer freezes when revealing box contents after a game is won
- [Docs] Function documentation and additional comments added
