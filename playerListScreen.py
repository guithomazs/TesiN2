from tkinter import *
from tkinter import ttk
from utils import *

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
        frame_buttons = Frame(self.root)
        PseudoMenuButton(frame_buttons, text='Cadastrar novo jogador').grid(row=0, column=0)
        PseudoMenuButton(frame_buttons, text='Excluir jogador').grid(row=0, column=1)
        frame_buttons.grid()
        self.label_players = LabelFrame(self.root, text='Jogadores', font=LABEL_FRAME_FONT, background="grey")
        self.label_players.grid_columnconfigure(0, weight=1)
        self.label_players.grid(sticky=NSEW)
        self.createTreeview()
        

    def createTreeview(self):
        self.players_treeview = PlayersTreeView(self.label_players, show='tree', height=15)
        self.insertPlayers()
        self.players_treeview.grid(row=0, column=0, sticky=NSEW)

    def insertPlayers(self):
        players_list = self.getPlayersList()
        for player in players_list:
            self.players_treeview.insert('', 'end', values=player, text=player)

    
    def getPlayersList(self):
        return [f'player{i}' for i in range(20)]

if __name__ == '__main__':
    app = Tk()
    screen = Players(app)
    app.mainloop()