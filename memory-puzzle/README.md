# Memory Puzzle

Originally done by Al Sweigart, this is a Pygame adaptation of the classic memory puzzle game.

The player is presented with a board of boxes covering different icons (shapes of different colors). The player must select pairs of matching icons until all icons on the board are revealed.

## Controls

`Left Click` - Open a box

## Customizability

- Starting difficulty can be set to one of 7 presets
- Difficulty scaling between rounds can be toggled; if you win a game, the board size increases in the next round
- Limited attempts can be enabled; you only have a certain number of mistakes you can make before you lose the round and must start over
- The color palette of the icons can be set to one of 3 presets

## Changes from original

- [New] 7 board size presets ranging from 4x4 to 10x10
- [New] "Difficulty scaling" toggle: every time you win a game, the board size increases by one preset (based on the above)
- [New] Added three more shapes: hexagon, hourglass, smiley face
- [New] Two new color palettes for icon colors added, can be set per game using command line arguments. The colors for the icons are read from a file with 7 lines, one for each.
- [Change] FPS increased to 60 with animation speeds changed accordingly
- [Change] When boxes are revealed at start, number of boxes opened at a time scales with board size
- [Change] Window size slight increase
- [Fix] Window no longer freezes when revealing box contents after a game is won
- [Docs] Function documentation and additional comments added

![image](https://i.imgur.com/W6Qyb7J.gif)