import tkinter as tk
from tkinter import ttk

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

MY_BUTTON_FONT = 'Georgia 12 bold'
class MyButton(tk.Button):
    def __init__(self, master, text='x', command=None, **kwargs):
        super().__init__(master, bd=0, padx=5, pady=2, 
                         fg=BUTTON_FOREGROUND, 
                         bg=BUTTON_BACKGROUND,
                         activebackground=BUTTON_BACKGROUND_HOVER,
                         activeforeground=BUTTON_FOREGROUND_HOVER, 
                         font=MY_BUTTON_FONT,
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


# MENU BUTTONS
# PSEUDO_MENU_BUTTON_FOREGROUND = "#502bc2"
PSEUDO_MENU_BUTTON_FOREGROUND = "lime"
PSEUDO_MENU_BUTTON_BACKGROUND = "black"
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

WIFI_FOREGROUND_COLORS = [PSEUDO_MENU_BUTTON_FOREGROUND, PSEUDO_MENU_BUTTON_FOREGROUND_HOVER]
class WifiButton(PseudoMenuButton):
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
        self.button_status = True
        
        self.bind('<ButtonPress-1>', self.on_press)
        self.bind('<Enter>', lambda event: self.on_enter(PSEUDO_MENU_BUTTON_BACKGROUND_HOVER, 
                                                   PSEUDO_MENU_BUTTON_FOREGROUND_HOVER))
        self.bind('<Leave>', lambda event: self.on_leave(PSEUDO_MENU_BUTTON_BACKGROUND, 
                                                   PSEUDO_MENU_BUTTON_FOREGROUND))

    def on_press(self, event):
        self.button_status = not self.button_status
        if self.button_status:
            self['bg'] = PSEUDO_MENU_BUTTON_BACKGROUND_HOVER
            self['fg'] = PSEUDO_MENU_BUTTON_FOREGROUND_HOVER
            self.bind('<Enter>', lambda event: self.on_enter(PSEUDO_MENU_BUTTON_BACKGROUND, 
                                            PSEUDO_MENU_BUTTON_FOREGROUND))
            self.bind('<Leave>', lambda event: self.on_leave(PSEUDO_MENU_BUTTON_BACKGROUND_HOVER, 
                                            PSEUDO_MENU_BUTTON_FOREGROUND_HOVER))
        else:
            self.bind('<Enter>', lambda event: self.on_enter(PSEUDO_MENU_BUTTON_BACKGROUND_HOVER, 
                                            PSEUDO_MENU_BUTTON_FOREGROUND_HOVER))
            self.bind('<Leave>', lambda event: self.on_enter(PSEUDO_MENU_BUTTON_BACKGROUND, 
                                            PSEUDO_MENU_BUTTON_FOREGROUND))

    def on_enter(self, background_hover, foreground_hover):
        self['bg'] = background_hover
        self['fg'] = foreground_hover

    def on_leave(self, background_hover, foreground_hover):
        self['bg'] = background_hover
        self['fg'] = foreground_hover

# PLAYER LIST BUTTONS
PLAYER_LIST_BUTTON_FOREGROUND = "lime"
PLAYER_LIST_BUTTON_BACKGROUND = "black"
PLAYER_LIST_BUTTON_FOREGROUND_HOVER = "white"
PLAYER_LIST_BUTTON_BACKGROUND_HOVER = "black"
PLAYER_LIST_BUTTON_FONT = 'Georgia 14 bold'

class PlayerListButton(tk.Button):
    def __init__(self, master, text='', command=None, relief='groove', bd=2, **kwargs):
        super().__init__(master, bd=bd, font=PLAYER_LIST_BUTTON_FONT, padx=5, pady=2, 
                         fg=PLAYER_LIST_BUTTON_FOREGROUND, 
                         bg=PLAYER_LIST_BUTTON_BACKGROUND,
                         activebackground=PLAYER_LIST_BUTTON_BACKGROUND_HOVER,
                         activeforeground=PLAYER_LIST_BUTTON_FOREGROUND_HOVER, 
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

class GridScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.canvas.config(background='black')
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(sticky=tk.NSEW, row=0, column=0)
        scrollbar.grid(sticky=tk.NSEW, row=0, column=1)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


TREEVIEW_INTERN_FONT = 'Helvetica 12 bold'
class PlayersTreeView(ttk.Treeview):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        treeview_scrollbar = tk.Scrollbar(master, 
                                       orient=tk.VERTICAL, 
                                       command=self.yview
        )
        treeview_scrollbar.grid(row=0, column=1, sticky='ns')
        self.config(yscrollcommand=treeview_scrollbar.set)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background='black', 
                        fieldbackground='black',
                        foreground='lime',
                        font=TREEVIEW_INTERN_FONT,
        )
        style.theme_use("clam")
        style.map("Treeview", background=[('selected', 'green')])