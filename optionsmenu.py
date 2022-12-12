from tkinter import *
from tkinter import ttk

import json
import sys
import systemcall

class Window():
    game_folder = sys.argv[1]
    controls = []

    def print_controls(self, controls):
        args = []
        error = False
        for control in controls:
            if hasattr(control, 'current'):
                # dropdown
                if control.current() == -1:
                    error = True
                    break
                args.append(str(control.current()))
            else:
                # checkbutton
                print('checkbox is ' + ('enabled' if 'selected' in control.state() else 'disabled'))
                args.append('1' if 'selected' in control.state() else '0')

        if error:
            print('An error occured. (will handle later)')
            return
            
        systemcall.SystemCall('python ' + self.game_folder + '\\main.py ' + " ".join(args)).start()

    def __init__(self):
        self.root = Tk()

        meta = self.game_folder + 'meta.json'

        f = open(meta)
        data = json.load(f)
        f.close()

        width = 350
        height = 100
        if 'options' in data:
            # add all options to the screen
            for i in range(1, len(data['options']) + 1):
                opt = data['options']['opt' + str(i)]
                
                assert 'name' in opt and 'type' in opt, 'An option in this meta file is missing a required field'
                assert opt['type'] == 'dropdown' or opt['type'] == 'toggle', 'Invalid option type in this meta file > ' + opt['type']

                Label(self.root, text = opt['name'], font = ("Arial 12"), fg = data['colors']['foreground'], bg = data['colors']['background']).place(x = 10, y = 20 + i * 30)
                if opt['type'] == 'dropdown':
                    cbox = ttk.Combobox(self.root, width = 20, values = opt['options'])
                    cbox.place(x = 200, y = 20 + i * 30)
                    
                    self.controls.append(cbox)
                elif opt['type'] == 'toggle':
                    style = ttk.Style()
                    style.configure("TCheckbutton", background = data['colors']['background'])

                    cbox = ttk.Checkbutton(self.root, style="TCheckbutton")
                    cbox.place(x = 200, y = 20 + i * 30)
                    self.controls.append(cbox)

            height = (len(data['options']) + 1) * 42

        Label(self.root, text = data['name'], font = ("Arial 20 bold"), fg = data['colors']['foreground'], bg = data['colors']['background']).place(x = 10, y = 10)
        Button(self.root, text = 'Go', command = lambda: self.print_controls(self.controls)).place(x = 15, y = height - 40)
        
        self.root.title(data['name'] + ' Options')
        self.root.configure(bg = data['colors']['background'])
        self.root.geometry(str(width) + 'x' + str(height))
        self.root.mainloop()

win = Window()