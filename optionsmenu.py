from tkinter import *
from tkinter import ttk, colorchooser, messagebox

import json, sys, systemcall

class Window():
    game_folder = sys.argv[1]
    controls = []
    ctypes = []

    def print_controls(self, controls):
        args = []

        for i in range (len(self.controls)):
            if self.ctypes[i] == 'dropdown':
                args.append(str(controls[i].current()))
            elif self.ctypes[i] == 'toggle':
                args.append('1' if 'selected' in controls[i].state() else '0')
            elif self.ctypes[i] == 'color':
                args.append(controls[i].cget("bg"))
            
        systemcall.SystemCall('python ' + self.game_folder + '\\main.py ' + " ".join(args)).start()

    def __init__(self):
        self.root = Tk()

        meta = self.game_folder + 'meta.json'

        f = open(meta)
        data = json.load(f)
        f.close()

        width = 350
        height = 100
        last_option_height = 0

        if 'options' in data:
            # add all options to the screen
            for i in range(1, len(data['options']) + 1):
                opt = data['options']['opt' + str(i)]
                
                assert 'name' in opt and 'type' in opt, 'An option in this meta file is missing a required field'
                assert opt['type'] == 'dropdown' or opt['type'] == 'toggle' or opt['type'] == 'color', 'Invalid option type in this meta file > ' + opt['type']

                Label(self.root, text = opt['name'], font = ("Arial 12"), fg = data['colors']['foreground'], bg = data['colors']['background']).place(x = 10, y = 20 + i * 30)

                if opt['type'] == 'dropdown':
                    cbox = ttk.Combobox(self.root, width = 20, values = opt['options'])
                    cbox.place(x = 200, y = 20 + i * 30)
                    self.controls.append(cbox)
                    self.controls[i - 1].set(opt['options'][opt['defindex'] if 'defindex' in opt else 0])
                elif opt['type'] == 'toggle':
                    style = ttk.Style()
                    style.configure("TCheckbutton", background = data['colors']['background'])
                    cbox = ttk.Checkbutton(self.root, style="TCheckbutton")
                    cbox.place(x = 200, y = 20 + i * 30)
                    self.controls.append(cbox)
                elif opt['type'] == 'color':
                    cbox = Button(self.root, text = 'Pick', command = lambda j = (i - 1): self.controls[j].configure(bg = colorchooser.askcolor()[1]))
                    cbox.place(x = 200, y = 20 + i * 30)
                    if opt['default']:
                        cbox.configure(bg = opt['default'])
                    self.controls.append(cbox)

                self.ctypes.append(opt['type'])
                last_option_height = 20 + i * 30

            height = last_option_height + 30

        Label(self.root, text = data['name'], font = ("Arial 20 bold"), fg = data['colors']['foreground'], bg = data['colors']['background']).place(x = 10, y = 10)
        height += 40
        if last_option_height == 0:
            last_option_height = 40
        Button(self.root, text = 'Go', command = lambda: self.print_controls(self.controls)).place(x = 15, y = last_option_height + 30)
        
        self.root.title(data['name'] + ' Options')
        self.root.configure(bg = data['colors']['background'])
        self.root.geometry(str(width) + 'x' + str(height))
        self.root.mainloop()

win = Window()