from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database.playerDatabase import PlayerDBCommands
from configurePlayers import NewPlayer, RemovePlayer
from utils import *

LABEL_FRAME_FONT = 'Arial 24 bold'
BACKGROUND_COLOR = 'black'
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
        PseudoMenuButton(frame_buttons, 
                         text='Cadastrar novo jogador', 
                         command=self.createNewPlayer
        ).grid(row=0, column=0)
        PseudoMenuButton(frame_buttons, 
                         text='Excluir jogador',
                         command=self.RemoveSelectedPlayer
        ).grid(row=0, column=1)
        frame_buttons.grid()
        self.label_players = LabelFrame(self.root, text='Jogadores', font=LABEL_FRAME_FONT, background="grey")
        self.label_players.grid_columnconfigure(0, weight=1)
        self.label_players.grid(sticky=NSEW)
        self.createTreeview()

    def createNewPlayer(self):
        NewPlayer(self.root, self.players_treeview)

    def RemoveSelectedPlayer(self):
        player = self.players_treeview.selection()
        if len(player) > 1:
            messagebox.showwarning('Aviso.', 'Apenas exclua o seu jogador por favor.')
            return
        elif len(player) != 1:
            messagebox.showwarning('Aviso.', 'É necessário ao menos um jogador para excluir.')
            return
        nick_user = self.players_treeview.item(player, 'values')[0]
        # SQLCommands.getPlayerData(nick_user)
        RemovePlayer(self.root, nick=nick_user, root_players_treeview=self.players_treeview, excluding_player=player)

    def createTreeview(self):
        self.players_treeview = PlayersTreeView(self.label_players, show='tree', height=15)
        self.insertPlayers()
        self.players_treeview.grid(row=0, column=0, sticky=NSEW)

    def insertPlayers(self):
        players_list = self.getPlayersList()
        for player_nick, player_pwd in players_list:
            self.players_treeview.insert('', 'end', values=player_nick, text=player_nick)
    
    def getPlayersList(self):
        return PlayerDBCommands.getDataBasePlayers()

if __name__ == '__main__':
    app = Tk()
    screen = Players(app)
    app.mainloop()