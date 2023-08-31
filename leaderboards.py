from tkinter import *

LABEL_FRAME_FONT = 'Arial 24 bold'
class Leaderboards:
    def __init__(self, master: Tk, controller=None) -> None:
        self.root = master
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.title('Leaderboard')
        if controller != None:
            controller.createMenu(self.root)
        else:
            from gamesHub import GamesHubScreen
            GamesHubScreen.createMenu(self.root)

if __name__ == '__main__':
    app = Tk()
    tela = Leaderboards(app)
    app.mainloop()