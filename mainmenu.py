from tkinter import *

import json
import os
import systemcall

class Window():
    dir_path = os.path.dirname(os.path.realpath(__file__)) # the file currently being ran (mainmenu.py)
    metas = []
    games = {} # dictionary that maps game folders to button objects

    def __init__(self):
        self.root = Tk()

        # first get all games that can be run (find meta files)
        dir_list = []

        for root, dirs, files in os.walk(self.dir_path, topdown=False):
            for name in dirs:
                dir_list.append(os.path.join(root, name))

        for dir in dir_list:
            if 'meta.json' in os.listdir(dir):
                self.metas.append(dir + '\\meta.json')

        # read the json files / add buttons for games
        for meta in self.metas:
            f = open(meta)
            data = json.load(f)

            assert 'name' in data and 'colors' in data, 'The following meta file is missing a required property: ' + meta

            # we add a lambda (anon function) so it doesn't always run on start, only when clicked
            self.games.update({meta[:meta.find('meta.json')]: Button(self.root, text = data['name'], 
                command = lambda n = meta[:meta.find('meta.json')]: systemcall.SystemCall('python optionsmenu.py ' + n).start(), 
                bg = data['colors']['background'], 
                fg = data['colors']['foreground'])})
            f.close()

        # add components (title and buttons) to win
        Label(self.root, text = 'Python Games', font = ("Arial 20 bold")).place(x = 10, y = 10)

        # width and height get updated as games added (3 game buttons per row)
        width = 0
        height = 100
        
        i = 10 # current width to place button at

        games_loaded = 0
        for game in self.games:
            # place button down, get width after updating idletasks (which updates component sizes)
            self.games[game].place(x = i, y = height - 50)
            self.root.update_idletasks() 
            i += 10 + self.games[game].winfo_width()

            # if width exceeds max, change it
            if i > width:
                width = i + 20

            # start a new row of buttons after hititng 3 games on this row
            games_loaded += 1
            if games_loaded % 3 == 0 and not games_loaded == len(self.games):
                height += 30
                i = 10

        self.root.title('Python Games')
        self.root.geometry(str(width) + 'x' + str(height))
        self.root.mainloop()

win = Window()