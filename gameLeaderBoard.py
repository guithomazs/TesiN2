from tkinter import *
from database.playerDatabase import PlayerDBCommands
from ticTacToe import TicTacToe
from utils import LeaderboardsTreeView


LABEL_FRAME_FONT = 'Arial 24 bold'
BACKGROUND_COLOR = 'black'
class GameLeaderBoard:
    def __init__(self, master: Tk, game=TicTacToe) -> None:
        self.root = master
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.title('Game Leaderboards')
        
        self.game = game
        game.isCompetitiveGame(game)
        self.label_frame_players = LabelFrame(self.root, 
                                        text=self.game.__name__, 
                                        font=LABEL_FRAME_FONT, 
                                        background="grey",
                                        labelanchor=N
        )
        self.label_frame_players.grid_columnconfigure(0, weight=1)
        self.label_frame_players.grid(sticky=NSEW)
        self.createTreeview()

        
    def createTreeview(self):
        colunas = ('id', 'nick', 'vitorias')
        self.players_treeview = LeaderboardsTreeView(
            self.label_frame_players, 
            columns = colunas,
            show='headings', 
            height=15
        )
        self.players_treeview.heading('id', text='id')
        self.players_treeview.column('id', minwidth=50, width=50, stretch=0)

        self.players_treeview.heading('nick', text='Nick')
        self.players_treeview.column('nick', minwidth=200, width=200, stretch=1)

        self.players_treeview.heading('vitorias', text='Vitórias')
        self.players_treeview.column('vitorias', minwidth=50, width=50, stretch=0)

        self.players_treeview.grid(row=0, column=0, sticky=NSEW)
        self.insertPlayers()

    def insertPlayers(self):
        players_list = self.getPlayersList()
        for player_id, player_nick, game_won in players_list:
            self.players_treeview.insert('', 'end', 
                                         values=[player_id, player_nick, game_won], 
                                    )
    
    def getPlayersList(self):
        return PlayerDBCommands.getGamePlayerInfo(self.game.__name__)
    
if __name__ == '__main__':
    app = Tk()
    GameLeaderBoard(app)
    app.mainloop()
