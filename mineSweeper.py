import random
import tkinter as tk

from database.game import Game
from database.gamesCountDatabase import TimedGamesNames

class MineSweeper(Game):
    
    CURRENT_GAME = TimedGamesNames.MineSweeper

    def __init__(self, root: tk.Tk, controller=None, player1=None, n_bombs=1, rows=15, columns=15):
        super(MineSweeper, self).__init__(root, controller, 'É o Minas é.')
        self.num_bombas = n_bombs
        self.rows = rows
        self.player = player1
        self.columns = columns
        self.to_be_discovered = (rows * columns) - n_bombs
        self.startGame()
    
    def startGame(self):
        self.label_timer = tk.Label(self.root, text='0', font='Helvetica 18 bold')
        self.label_timer.grid(row=0,columnspan=self.columns, sticky=tk.NSEW)
        self.frame_bombs = tk.Frame(self.root)
        self.frame_bombs.grid(row=1, columnspan=self.columns)
        self.already_done = []
        self.abertas = 0
        self.on_game = 0
        self.timer = 0
        self.table = [['n' for j in range(self.columns)] for i in range(self.rows)]

        for row in range(self.rows):
            for column in range(self.columns):
                btn = tk.Button(self.frame_bombs, text='', \
                        width=2, height=1, \
                        command=lambda position=(row, column):self.control(position))
                btn.bind("<ButtonPress-3>", lambda event, position=(row, column):self.changeButton(event, position))
                btn.grid(row=row, column=column, sticky=tk.NSEW, padx=1, pady=1)
    
    def button_GoBackNormal(self, event, position):
        row, column = position[0], position[1]
        btn = tk.Button(self.frame_bombs, text='', \
                        width=2, height=1, \
                        command=lambda position=(row, column):self.control(position))
        btn.bind("<ButtonPress-3>", lambda event, position=(row, column):self.changeButton(event, position))
        btn.grid(row=row, column=column, sticky=tk.NSEW, padx=1, pady=1)

    def changeButton(self, event, position):
        row, column = position[0], position[1]
        if self.on_game:
            flagButton = tk.Button(self.frame_bombs, text="\U0001F3F4", fg='red')
            flagButton.bind("<ButtonPress-3>", lambda event, position=(row, column):self.button_GoBackNormal(event, position))
            flagButton.grid(row=row, column=column, sticky=tk.NSEW, padx=1, pady=1)
        
    def isValidTile(self, tile):
        if (
            (tile[0] < 0 or tile[1] < 0) 
            or 
            (tile[0] >= self.rows or tile[1] >= self.columns)
        ):
            return False
        return True
    
    def getAroundTiles(self, row, column):
        return [
            [row-1, column-1],
            [row-1, column  ],
            [row-1, column+1],
            [row  , column-1],
            [row  , column+1],
            [row+1, column-1],
            [row+1, column  ],
            [row+1, column+1]
        ]

    def create_protected(self, pos):
        row, column = pos[0], pos[1]
        protected_area = [[row, column]]
        around_tiles = self.getAroundTiles(row, column)
        for tile in around_tiles:
            if self.isValidTile(tile):
                protected_area.append(tile)
        return protected_area
    
    def updateClock(self):
        if self.on_game:
            self.timer += 1
            self.label_timer.config(text=self.timer)
            self.label_timer.after(1000, self.updateClock)
    
    def control(self, pos):
        row, column = pos[0], pos[1]
        if not self.on_game:
            self.gera_bombas(self.num_bombas, self.create_protected(pos))
            self.conta_bombas()
            self.on_game = 1
            self.updateClock()
        
        open_list = [[row, column]]
        while len(open_list):
            row = open_list[0][0]
            column = open_list[0][1]
            around_tiles = self.getAroundTiles(row, column)
            if self.table[open_list[0][0]][open_list[0][1]] == 0:       
                for tile in around_tiles:
                    if self.isValidTile(tile):
                        if tile not in self.already_done and tile not in open_list: open_list.append(tile)
            if open_list[0] not in self.already_done:
                self.changeText(open_list[0])
                self.already_done.append(open_list[0])
            open_list.pop(0)

    def changeText(self, pos):
        row, column = pos[0], pos[1]
        if self.table[row][column] == 'x':
            tk.Label(self.frame_bombs,  
                    text='\U0001F4A3',
                    borderwidth=3, 
                    relief='groove', 
                    fg='red'
            ).grid(
                    row=row, 
                    column=column,
                    sticky=tk.NSEW, 
                    padx=1, 
                    pady=1
                )
            self.endGame()
            return
        
        self.abertas += 1
        tk.Label(self.frame_bombs, 
                text=self.table[row][column],
                borderwidth=3, 
                relief='groove', 
                fg='blue'
        ).grid(
                row=row, 
                column=column,
                sticky=tk.NSEW, 
                padx=1, 
                pady=1
            )
        if self.abertas == self.to_be_discovered:
            self.endGame(lost=False)

    def endGame(self, lost=True):
        self.on_game = 0
        text_victory = f'Meus parabéns, você conseguiu.' if not lost else "Que pena, você perdeu."
        text_end =  f'Deseja jogar novamente?'
        title = 'Fim de jogo!!!'
        
        top_level_winner = tk.Toplevel(self.root)
        top_level_winner.grab_set()
        top_level_winner.resizable(False, False)
        top_level_winner.protocol("WM_DELETE_WINDOW", self.close)
        top_level_winner.title(title)
        
        frame_texts = tk.Frame(top_level_winner)
        tk.Label(frame_texts,
                    text=text_victory, 
                    font='Georgia 18 bold'
        ).grid(columnspan=3)
        tk.Label(frame_texts,
                    text=text_end, 
                    font='Helvetica 14 bold'
        ).grid(columnspan=3)
        
        frame_texts.grid(sticky=tk.NSEW, columnspan=2)

        tk.Button(top_level_winner, 
                    text='Jogar Novamente', 
                    font='Helvetica 12 bold',
                    command=
                        lambda wm=top_level_winner: self.RestartGame(wm)
        ).grid(sticky=tk.NSEW)
        tk.Button(top_level_winner, 
                text='Sair', 
                font='Helvetica 12 bold',
                command=self.close
        ).grid(
            row=1, 
            column=1, 
            sticky=tk.NSEW, 
            columnspan=2
            )
        
    def RestartGame(self, toplevel:tk.Toplevel):
        toplevel.destroy()
        self.startGame()
        
    def gera_bombas(self, num_bombs, protected_area=None):
        options = []
        for i in range(self.rows):
            for j in range(self.columns):
                if [i, j] not in protected_area: options.append([i, j])
        bomb_positions = random.sample(options, k=num_bombs)
        for row, column in bomb_positions:
            self.table[row][column] = 'x'

    def conta_bombas(self):
        for row in range(self.rows):
            for column in range(self.columns):
                around_tiles = self.getAroundTiles(row, column)
                contador = 0
                
                if self.table[row][column] == 'x':
                    continue

                for around_tile in around_tiles:
                    if self.isValidTile(around_tile):
                        if self.table[around_tile[0]][around_tile[1]] == 'x': 
                            contador += 1
                
                self.table[row][column] = contador

if __name__ == '__main__':
    app = tk.Tk()
    master = MineSweeper(app)
    app.mainloop()
