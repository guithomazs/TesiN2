import tkinter as tk

# --- constants --- (UPPER_CASE_NAMES)

# title bar colors
TITLE_FOREGROUND = "white"
TITLE_BACKGROUND = "#2c2c2c"
TITLE_BACKGROUND_HOVER = "green"

BUTTON_FOREGROUND = "white"
BUTTON_BACKGROUND = TITLE_BACKGROUND
BUTTON_FOREGROUND_HOVER = BUTTON_FOREGROUND
BUTTON_BACKGROUND_HOVER = 'red'

# window colors
WINDOW_BACKGROUND = "white"
WINDOW_FOREGROUND = "black"

# --- classes --- (CamelCaseNames)

class MyButton(tk.Button):
    def __init__(self, master, text='x', command=None, **kwargs):
        super().__init__(master, bd=0, font="bold", padx=5, pady=2, 
                         fg=BUTTON_FOREGROUND, 
                         bg=BUTTON_BACKGROUND,
                         activebackground=BUTTON_BACKGROUND_HOVER,
                         activeforeground=BUTTON_FOREGROUND_HOVER, 
                         highlightthickness=0, 
                         text=text,
                         command=command)

        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self['bg'] = BUTTON_BACKGROUND_HOVER

    def on_leave(self, event):
        self['bg'] = BUTTON_BACKGROUND


# GAME HUB BUTTONS
GAME_SELECT_BUTTON_FOREGROUND = "black"
GAME_SELECT_BUTTON_BACKGROUND = "white"
GAME_SELECT_BUTTON_FOREGROUND_HOVER = "white"
GAME_SELECT_BUTTON_BACKGROUND_HOVER = "#2c2c2c"
GAME_SELECT_BUTTON_FONT = 'Georgia 22 bold'

class GameSelectButton(tk.Button):
    def __init__(self, master, text='X', command=None, relief='groove', bd=2, **kwargs):
        super().__init__(master, bd=bd, font=GAME_SELECT_BUTTON_FONT, padx=5, pady=2, 
                         fg=GAME_SELECT_BUTTON_FOREGROUND, 
                         bg=GAME_SELECT_BUTTON_BACKGROUND,
                         activebackground=GAME_SELECT_BUTTON_BACKGROUND_HOVER,
                         activeforeground=GAME_SELECT_BUTTON_FOREGROUND_HOVER, 
                         highlightthickness=0, 
                         text=text,
                         command=command,
                         relief=relief,
                        )

        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self['bg'] = GAME_SELECT_BUTTON_BACKGROUND_HOVER
        self['fg'] = GAME_SELECT_BUTTON_FOREGROUND_HOVER

    def on_leave(self, event):
        self['bg'] = GAME_SELECT_BUTTON_BACKGROUND
        self['fg'] = GAME_SELECT_BUTTON_FOREGROUND


# GAME HUB BUTTONS
PSEUDO_MENU_BUTTON_FOREGROUND = "black"
PSEUDO_MENU_BUTTON_BACKGROUND = "#2c2c2c"
PSEUDO_MENU_BUTTON_FOREGROUND_HOVER = "white"
PSEUDO_MENU_BUTTON_BACKGROUND_HOVER = "black"
PSEUDO_MENU_BUTTON_FONT = 'Georgia 14 bold'

class PseudoMenuButton(tk.Button):
    def __init__(self, master, text='', command=None, relief='groove', bd=2, **kwargs):
        super().__init__(master, bd=bd, font=PSEUDO_MENU_BUTTON_FONT, padx=5, pady=2, 
                         fg=PSEUDO_MENU_BUTTON_FOREGROUND, 
                         bg=PSEUDO_MENU_BUTTON_BACKGROUND,
                         activebackground=PSEUDO_MENU_BUTTON_BACKGROUND_HOVER,
                         activeforeground=PSEUDO_MENU_BUTTON_FOREGROUND_HOVER, 
                         highlightthickness=0, 
                         text=text,
                         command=command,
                         relief=relief,
                        )

        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self['bg'] = PSEUDO_MENU_BUTTON_BACKGROUND_HOVER
        self['fg'] = PSEUDO_MENU_BUTTON_FOREGROUND_HOVER

    def on_leave(self, event):
        self['bg'] = PSEUDO_MENU_BUTTON_BACKGROUND
        self['fg'] = PSEUDO_MENU_BUTTON_FOREGROUND



class MainTitleBar(tk.Frame):
    def __init__(self, master, by_its_own=True, *args, **kwargs):
        super().__init__(master, relief='raised', bd=1, 
                         bg=TITLE_BACKGROUND,
                         highlightcolor=TITLE_BACKGROUND, 
                         highlightthickness=0)
        

        self.title_label = tk.Label(self, 
                                    bg=TITLE_BACKGROUND, 
                                    fg=TITLE_FOREGROUND)
                                    
        self.title_label.bind("<ButtonPress-1>", self.on_press)
        self.title_label.bind("<B1-Motion>", self.on_move)
        
        self.set_title("Title Name")

        self.close_button = MyButton(self, text='x', command=master.destroy)
        self.minimize_button = MyButton(self, text='-', command=self.on_minimize)

        if by_its_own:
            self.elements_pack()
                         
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_move)

    def elements_pack(self):
        self.pack(expand=True, fill='x')
        self.title_label.pack(side='left')
        self.close_button.pack(side='right')
        self.minimize_button.pack(side='right')

    def set_title(self, title):
        self.title = title
        self.title_label['text'] = title
        
    def on_press(self, event):
        self.xwin = event.x
        self.ywin = event.y
        # self.set_title("Title Name - ... I'm moving! ...")
        # self['bg'] = 'green'
        # self.title_label['bg'] = TITLE_BACKGROUND_HOVER
        
    def on_move(self, event):
        x = event.x_root - self.xwin
        y = event.y_root - self.ywin
        self.master.geometry(f'+{x}+{y}')
        
    def on_minimize(self):
        print('TODO: minimize')


class InGameTitleBar(MainTitleBar):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, by_its_own=False, *args, **kwargs)
        go_back_button = MyButton(self, text='↩', command=master.destroy)
        go_back_button.pack(side='left')
        self.elements_pack()


class GridMainTitleBar(tk.Frame):
    def __init__(self, master, by_its_own=True, *args, **kwargs):
        super().__init__(master, relief='raised', bd=1, 
                         bg=TITLE_BACKGROUND,
                         highlightcolor=TITLE_BACKGROUND, 
                         highlightthickness=0)
        
        self.title_label = tk.Label(self, 
                                    bg=TITLE_BACKGROUND, 
                                    fg=TITLE_FOREGROUND)
                                    
        self.title_label.bind("<ButtonPress-1>", self.on_press)
        self.title_label.bind("<B1-Motion>", self.on_move)
        
        self.set_title("Title Name")

        self.close_button = MyButton(self, text='x', command=master.destroy)
        # self.minimize_button = MyButton(self, text='-', command=self.on_minimize)
        self.minimize_button = MyButton(self, text='-')
        self.minimize_button.bind("<ButtonPress-1>", self.on_minimize2)

        if by_its_own:
            self.elements_grid()
                         
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_move)

    def elements_grid(self):
        self.grid(sticky=tk.NSEW, columnspan=99)
        self.grid_columnconfigure(1, weight=1)
        self.title_label.grid(row=0, column=1)
        self.minimize_button.grid(row=0, column=2)
        self.close_button.grid(row=0, column=3)

    def set_title(self, title):
        self.title = title
        self.title_label['text'] = title
        
    def on_press(self, event):
        self.xwin = event.x
        self.ywin = event.y
        # self.set_title("Title Name - ... I'm moving! ...")
        # self['bg'] = 'green'
        # self.title_label['bg'] = TITLE_BACKGROUND_HOVER
        
    def on_move(self, event):
        x = event.x_root - self.xwin
        y = event.y_root - self.ywin
        self.master.geometry(f'+{x}+{y}')

    def on_minimize(self):
        self.winfo_parent()
        print('aqui -', self.winfo_parent())
        
    def on_minimize2(self, event):
        self.winfo_parent()
        grandparent = event.widget.master.master
        parent = event.widget.master
        print(grandparent, parent, grandparent == parent)
        # grandparent.state(newstate='iconic')
        # grandparent.wm_state('iconic')

class GridInGameTitleBar(GridMainTitleBar):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, by_its_own=False, *args, **kwargs)
        go_back_button = MyButton(self, text='↩', command=master.destroy)
        go_back_button.grid(row=0, column=0, sticky=tk.NSEW)
        self.elements_grid()

# --- main ---
if __name__ == '__main__':
    root = tk.Tk()
    # turns off title bar, geometry
    root.overrideredirect(True)

    # set new geometry
    root.geometry('400x100+200+200')

    # title_bar = MainTitleBar(root) 
    title_bar = InGameTitleBar(root) 
    #title_bar.pack()  # it is inside `TitleBar.__init__()`

    # a canvas for the main area of the window
    window = tk.Canvas(root, bg=WINDOW_BACKGROUND, highlightthickness=0)

    # pack the widgets
    window.pack(expand=True, fill='both')

    root.mainloop()