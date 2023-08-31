from tkinter import *
from utils import GameSelectButton

LABEL_FRAME_FONT = 'Arial 24 bold'
class Players:
    def __init__(self, master: Tk, controller=None) -> None:
        self.root = master
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.title('Player List')
        if controller != None:
            controller.createMenu(self.root)
        else:
            from gamesHub import GamesHubScreen
            GamesHubScreen.createMenu(self.root)
        label_players = LabelFrame(self.root, text='Jogadores', font=LABEL_FRAME_FONT)
        Button(self.root, text='Tela de Player List').grid()

if __name__ == '__main__':
    app = Tk()
    screen = Players(app)
    app.mainloop()