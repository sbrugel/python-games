# Python Games

A few games I made/re-created in Python, using PyGame (primarily).

Some of these games were originally created by Al Sweigart from his _Making Games with Python & Pygame_ book, but were modified by myself in one or more ways (features-wise). The code for those games is distributed/modified under the [CC BY-NC-SA 3.0 US](https://creativecommons.org/licenses/by-nc-sa/3.0/us/) license.

More info for each game in the READMEs of each folder.

## Dynamic Main Menu

A main menu is included, where one can launch any of the completed games in this repostiory. This main menu looks for all the `meta.json` files in all game folders (if one is present, it signifies that a game is in that folder - it holds things including the game title and available customization options), and dynamically adds buttons that launches the customization options window for that game. From there, the player can set their preferences and run the game they picked!

## List of Games

- [Pygame Template](https://github.com/sbrugel/python-games/tree/master/template): A very basic app that demonstrates the fundamental aspects of Pygame.
- [Memory Puzzle](https://github.com/sbrugel/python-games/tree/master/memory-puzzle): The player is presented with a 4x4 to 10x10 board of boxes covering icons of different shapes and colors. The player must match all pairs of icons to win. Different difficulty modes, color palettes for icons, and a toggle for limited attempts are available.
- [Slide Puzzle](https://github.com/sbrugel/python-games/tree/master/slide-puzzle): On a square board that has number boxes in all spaces except one, the player must slide tiles around until the boxes are in numerical order.