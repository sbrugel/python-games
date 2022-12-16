# Python Games

A few games I made/re-created in Python, using PyGame (primarily).

Some of these games were originally created by Al Sweigart from his _Making Games with Python & Pygame_ book, but were modified by myself in one or more ways to add new features or change existing ones. The code for those games is distributed/modified under the [CC BY-NC-SA 3.0 US](https://creativecommons.org/licenses/by-nc-sa/3.0/us/) license.

More info for each game in the READMEs of each folder.

## Dynamic Menus

One core feature about this project is the dynamic main menu to pick games to play - a GUI made in Tkinter, game buttons are automatically added to the window based on the prescence of `meta.json` files in each game folder. That way, I don't have to manually modify the main menu code to add each game.

Another, arguably bigger, feature is a dynamic options menu. You may have noticed in the root of this repo, there is a file called `optionsmenu.py`. This is a dynamic Tkinter GUI that displays the options of the game you select from the main menu, based on what is stored in that game's `meta.json` file. It supports several different input types, including dropdowns, checkboxes, and color pickers. This makes it so I don't have to make an options menu for every individual game, all I need to do is put the game options in the game's meta file. Talk about spending a bit too much time on automation :) See below for a couple examples.

![img](https://i.imgur.com/mjEo5gn.png)

![img](https://i.imgur.com/e3aUNmq.png)

## List of Games
### Original
TBA

### Recreated / Remixed
- [Memory Puzzle](https://github.com/sbrugel/python-games/tree/master/memory-puzzle): The player is presented with a 4x4 to 10x10 board of boxes covering icons of different shapes and colors. The player must match all pairs of icons to win.
- [Slide Puzzle](https://github.com/sbrugel/python-games/tree/master/slide-puzzle): On a square board that has number boxes in all spaces except one, the player must slide tiles around until the boxes are in numerical order.
- [Simon](https://github.com/sbrugel/python-games/tree/master/simon): The player must mimic a pattern given to them by clicking colored buttons in order. Each time the pattern is correctly simulated, the pattern length increases. The goal is to keep this pattern going for as long as possible.
- [Snake](https://github.com/sbrugel/python-games/tree/master/snake): The player controls the direction of a snake on a board, aiming for fruits to increase their score and the snake's length. The goal of the game is to go as long as possible before the snake either runs into itself or into an edge.
- [Tetris](https://github.com/sbrugel/python-games/tree/master/tetris): The player must guide falling blocks down to form rows filled with boxes, void of any gaps. When a complete row is formed, it is cleared and each row above moves down one row. The goal is to complete as many of these lines as possible until the screen fills up.

### Misc
- [Pygame Template](https://github.com/sbrugel/python-games/tree/master/template): A very basic app that demonstrates the fundamental aspects of Pygame.

## Meta File Notes

Meta files are used to hold game data to be displayed in the main menu and options menus. This includes the name of the game, the colors used for the button and options background, and the game's options.

For example, here is the `meta.json` file for Simon:
```json
{
    "name": "Simon",
    "options": {
        "opt1": {
            "name": "Memorization Difficulty",
            "type": "dropdown",
            "options": ["Easy", "Medium", "Hard"]
        },
        "opt2": {
            "name": "Squares on Board",
            "type": "dropdown",
            "options": ["4", "6"]
        },
        "opt3": {
            "name": "Timeout",
            "type": "dropdown",
            "options": ["1 sec", "2 sec", "3 sec", "4 sec"],
            "defindex": 3
        }
    },
    "colors": {
        "foreground": "#ff0000",
        "background": "#000000"
    }
}
```

- The first `name` key holds the name of the game. This is displayed on the game's button on the main menu, as well as the option menu's title.
- The last `colors` key holds the foreground and background colors of both the game's main menu button and the option menu's colors.
- The `options` key is more complex, and holds multiple embedded keys with unique names, each representing an option for the game.

### Options Keys

Each option must be its own unique key.

The `name` field is the name of the option to be displayed on the menu.

The `type` field is the type of input this option has. Can be `dropdown` (combo box), `toggle` (checkbutton), or `color` (color picker).
- If `dropdown` is selected, an additional `options` key MUST be supplied, which contains the combo box's values. The index of the selected value is passed into the game's main file. Optionally, a `defindex` key can be supplied, which sets the default selected index to the int supplied. Otherwise, it defaults to the combo box's first value.
- If `toggle` is selected, either a 0 (unchecked) or 1 (checked) is passed into the game's main file.
- If `color` is selected, a string containing the selected hex value is passed into the game's main file. A `default` field must be supplied which sets the default selected color. Below is an example of a color picker option from Slide Puzzle:

```json
"opt6": {
    "name": "Background Color",
    "type": "color",
    "default": "#033649"
}
```