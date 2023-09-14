from tkinter import *

from database.game import Game
from database.gamesCountDatabase import CompetitiveGamesNames, GamesDB
from database.playerDatabase import PlayerDBCommands

class TicTacToe(Game):

    CURRENT_GAME = CompetitiveGamesNames.TicTacToe

    def __init__(self, root: Tk, controller=None, player1='Jogador 1', player2='Jogador 2'):
        super(TicTacToe, self).__init__(root, controller, 'Joguin da véia.')
        self.controller = controller
        self.player_one = player1
        self.player_two = player2
        self.startGame()

    def startGame(self):
        self.player_turn = True  # true se player1 ou false se player2
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.resizable(False, False)
        self.generateMenu()
        self.generateTable()
        self.winner = 0
        self.round = 0
        self.table = [['' for j in range(3)] for i in range(3)]

    def generateMenu(self):
        frame_menu = Frame(self.root, relief='solid', bd=3)
        title_font = 'Helvetica 18 bold'
        Label(frame_menu, 
                 text=self.player_one, 
                 font=title_font, 
                 bg='blue'
        ).grid(row=0, sticky=W)

        Label(frame_menu, 
                 text='VS', 
                 font=title_font, 
                 bg='brown'
        ).grid(row=0, column=1, sticky=NSEW)

        Label(frame_menu, 
                 text=self.player_two, 
                 font=title_font, 
                 bg='red'
        ).grid(row=0, column=2, sticky=E)

        frame_menu.grid_columnconfigure(0, weight=1)
        frame_menu.grid_columnconfigure(1, weight=3)
        frame_menu.grid_columnconfigure(2, weight=1)
        # frame_menu.grid_rowconfigure(0, weight=1)
        frame_menu.grid(row=0, columnspan=99, sticky=NSEW)

    def generateTable(self):
        self.font_labels = 'Helvetica 18 bold'
        self.area_height = 5
        self.area_width = 12
        self.frame_game = Frame(self.root) 
        for row in range(0, 9, 4):
            for column in range(0, 9, 4):
                lbl_tile = Label(self.frame_game, text='', width=self.area_width, height=self.area_height, font=self.font_labels)
                lbl_tile.grid(row=row, column=column, sticky=NSEW, columnspan=2, rowspan=2)
                lbl_tile.bind("<ButtonPress-1>", lambda play, row=row, column=column: self.jogar(row, column))
                if column != 8:
                    b1 = Label(self.frame_game, text='', bg='black', width=2, height=1)
                    b1.grid(row=row, column=(column+2), sticky=NSEW, columnspan=2, rowspan=2)
            if row != 8:
                b3 = Label(self.frame_game, text='', bg='black', width=2, height=1)
                b3.grid(row=(row+2), column=0, sticky=NSEW, columnspan=10, rowspan=2)
    
        self.frame_game.grid(row=1)

    def jogar(self, LinhaInicial, ColunaInicial):
        valores = [0, 4, 8]
        if self.player_turn:
            actual_label = Label(self.frame_game, text='X', width=self.area_width, height=self.area_height, font=self.font_labels)
        else:
            actual_label = Label(self.frame_game, text='O', width=self.area_width, height=self.area_height, font=self.font_labels)
        
        actual_label.grid(row=LinhaInicial, column=ColunaInicial, sticky=NSEW, columnspan=2, rowspan=2)
        linha = valores.index(LinhaInicial) 
        coluna = valores.index(ColunaInicial)
        self.table[linha][coluna] = 1 if self.player_turn else 2
        self.player_turn = False if self.player_turn else True
        self.round += 1
        self.verifyWin()
            
    def verifyWin(self):
        if self.table[0][0] and self.table[0][0] == self.table[0][1] and self.table[0][0] == self.table[0][2]:  # linha 1
            self.winner = self.table[0][0]
        elif self.table[1][0] and self.table[1][0] == self.table[1][1] and self.table[1][0] == self.table[1][2]:  # linha 2
            self.winner = self.table[1][0]
        elif self.table[2][0] and self.table[2][0] == self.table[2][1] and self.table[2][0] == self.table[2][2]: # linha 3
            self.winner = self.table[2][0]
        elif self.table[0][0] and self.table[0][0] == self.table[1][0] and self.table[0][0] == self.table[2][0]: # coluna 1
            self.winner = self.table[0][0]
        elif self.table[0][1] and self.table[0][1] == self.table[1][1] and self.table[0][1] == self.table[2][1]: # coluna 2
            self.winner = self.table[0][1]
        elif self.table[0][2] and self.table[0][2] == self.table[1][2] and self.table[0][2] == self.table[2][2]: # coluna 3
            self.winner = self.table[0][2]
        elif self.table[0][0] and self.table[0][0] == self.table[1][1] and self.table[0][0] == self.table[2][2]: # diagonal principal
            self.winner = self.table[0][0]
        elif self.table[0][2] and self.table[0][2] == self.table[1][1] and self.table[0][2] == self.table[2][0]: # diagonal secundária
            self.winner = self.table[0][2]
        elif self.round >= 9:
            self.winner = 3
        self.root.update()
        if self.winner != 0:
            self.endGame()  
        
    def endGame(self):
        topLevelWinner = Toplevel(self.root)
        topLevelWinner.resizable(False, False)
        topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
        if self.winner != 3:
            winner_player = self.player_one if self.winner == 1 else self.player_two
            loser_player = self.player_two if self.winner == 1 else self.player_one
            PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.TicTacToe, winner_player, won=True)
            PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.TicTacToe, loser_player)
            Label(topLevelWinner, text=f'Vitória de: {winner_player}.', font='Helvetica 14 bold').grid(columnspan=3)
        else:
            PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.TicTacToe, self.player_one)
            PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.TicTacToe, self.player_two)
            Label(topLevelWinner, text=f'Empate!', font='Helvetica 14 bold').grid(columnspan=3)
        Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=NSEW)
        Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=1, column=1, sticky=NSEW, columnspan=2)
        topLevelWinner.grab_set()
        

    def RestartGame(self, toplevel):
        toplevel.destroy()
        self.startGame()

if __name__ == '__main__':
    app = Tk()
    master = TicTacToe(app)
    app.mainloop()