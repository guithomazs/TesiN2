import tkinter as tk
import typing

from database.gamesCountDatabase import CompetitiveGamesNames, TimedGamesNames
from database.playerDatabase import PlayerDBCommands

class Players:
    name: str
    won: bool
    increase: int

class Game:

    CURRENT_GAME : typing.Union[CompetitiveGamesNames, TimedGamesNames]

    def __init__(self, root: tk.Tk, controller=None, title_text='No Title'):
        self.root = root
        self.root.resizable(False, False)
        self.root.title(title_text)
        self.controller = controller
        if controller != None:
            self.changeCloseButtonFunction()

    def changeCloseButtonFunction(self):
        self.root.protocol('WM_DELETE_WINDOW', self.goBackFunction)

    def goBackFunction(self):
        self.controller.goingBack(self.root)

    def close(self):
        if self.controller != None:
            self.controller.goingBack(self.root)
        else:
            self.root.destroy()

    def endGame(self, players: typing.List[Players]):
        for player in players:
            PlayerDBCommands.setGamePlayed(self.CURRENT_GAME, player.name, player.won)
        
    @staticmethod
    def isCompetitiveGame(game):
        if game.__name__ in CompetitiveGamesNames._member_names_:
            return True
        return False
    
    def getGameName(self):
        return self.__class__.__name__
    
