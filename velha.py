from tkinter import *

class TicTacToe:
    def __init__(self, master: Tk, controller=None):
        self.root = master
        self.root.title('Joguin da véia.')
        self.controller = controller
        if controller != None:
            self.changeCloseButtonFunction()
        self.startGame()

    def changeCloseButtonFunction(self):
        self.root.protocol('WM_DELETE_WINDOW', self.goBackFunction)

    def goBackFunction(self):
        self.controller.goingBack(self.root)

    def startGame(self):
        self.player1 = True  # true se player1 ou false se player2
        self.frame_jogo = Frame(self.root)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.resizable(False, False)
        self.gerar()
        self.frame_jogo.grid(row=0)
        self.winner = 0
        self.round = 0
        self.table = [['' for j in range(3)] for i in range(3)]

    def gerar(self):
        self.fontLabels = 'Helvetica 18 bold'
        self.altura_area = 5
        self.largura_area = 12
        a1 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a1.grid(row=0, column=0, sticky=NSEW, columnspan=2, rowspan=2)
        a1.bind("<ButtonPress-1>", lambda play: self.jogar(0, 0))
        b1 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b1.grid(row=0, column=2, sticky=NSEW, columnspan=2, rowspan=2)
        
        a2 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a2.grid(row=0, column=4, sticky=NSEW, columnspan=2, rowspan=2)
        a2.bind("<ButtonPress-1>", lambda play: self.jogar(0, 4))
        b2 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b2.grid(row=0, column=6, sticky=NSEW, columnspan=2, rowspan=2)

        a3 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a3.grid(row=0, column=8, sticky=NSEW, columnspan=2, rowspan=2)
        a3.bind("<ButtonPress-1>", lambda play: self.jogar(0, 8))
        b3 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b3.grid(row=2, column=0, sticky=NSEW, columnspan=10, rowspan=2)
        
        a4 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a4.grid(row=4, column=0, sticky=NSEW, columnspan=2, rowspan=2)
        a4.bind("<ButtonPress-1>", lambda play: self.jogar(4, 0))
        b4 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b4.grid(row=4, column=2, sticky=NSEW, columnspan=2, rowspan=2)
        
        a5 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a5.grid(row=4, column=4, sticky=NSEW, columnspan=2, rowspan=2)
        a5.bind("<ButtonPress-1>", lambda play: self.jogar(4, 4))
        b5 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b5.grid(row=4, column=6, sticky=NSEW, columnspan=2, rowspan=2)

        a6 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a6.grid(row=4, column=8, sticky=NSEW, columnspan=2, rowspan=2)
        a6.bind("<ButtonPress-1>", lambda play: self.jogar(4, 8))
        b6 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b6.grid(row=6, column=0, sticky=NSEW, columnspan=10, rowspan=2)
        
        a7 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a7.grid(row=8, column=0, sticky=NSEW, columnspan=2, rowspan=2)
        a7.bind("<ButtonPress-1>", lambda play: self.jogar(8, 0))
        b7 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b7.grid(row=8, column=2, sticky=NSEW, columnspan=2, rowspan=2)
        
        a8 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a8.grid(row=8, column=4, sticky=NSEW, columnspan=2, rowspan=2)
        a8.bind("<ButtonPress-1>", lambda play: self.jogar(8, 4))
        b8 = Label(self.frame_jogo, text='', bg='black', width=2, height=1)
        b8.grid(row=8, column=6, sticky=NSEW, columnspan=2, rowspan=2)

        a9 = Label(self.frame_jogo, text='', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        a9.grid(row=8, column=8, sticky=NSEW, columnspan=2, rowspan=2)
        a9.bind("<ButtonPress-1>", lambda play: self.jogar(8, 8))

    def jogar(self, LinhaInicial, ColunaInicial):
        valores = [0, 4, 8]
        if self.player1:
            actual_label = Label(self.frame_jogo, text='1', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        else:
            actual_label = Label(self.frame_jogo, text='2', width=self.largura_area, height=self.altura_area, font=self.fontLabels)
        
        actual_label.grid(row=LinhaInicial, column=ColunaInicial, sticky=NSEW, columnspan=2, rowspan=2)
        linha = valores.index(LinhaInicial) 
        coluna = valores.index(ColunaInicial)
        self.table[linha][coluna] = 1 if self.player1 else 2
        self.player1 = False if self.player1 else True
        self.round += 1
        self.verifyWin()
            
    def verifyWin(self):
        if self.table[0][0] and self.table[0][0] == self.table[0][1] and self.table[0][0] == self.table[0][2]:  # linha 1
            print(self.table[0][0])
            self.winner = self.table[0][0]
        elif self.table[1][0] and self.table[1][0] == self.table[1][1] and self.table[1][0] == self.table[1][2]:  # linha 2
            print(self.table[1][0])
            self.winner = self.table[1][0]
        elif self.table[2][0] and self.table[2][0] == self.table[2][1] and self.table[2][0] == self.table[2][2]: # linha 3
            print(self.table[2][0])
            self.winner = self.table[2][0]
        elif self.table[0][0] and self.table[0][0] == self.table[1][0] and self.table[0][0] == self.table[2][0]: # coluna 1
            print(self.table[0][0])
            self.winner = self.table[0][0]
        elif self.table[0][1] and self.table[0][1] == self.table[1][1] and self.table[0][1] == self.table[2][1]: # coluna 2
            print(self.table[0][1])
            self.winner = self.table[0][1]
        elif self.table[0][2] and self.table[0][2] == self.table[1][2] and self.table[0][2] == self.table[2][2]: # coluna 3
            print(self.table[0][2])
            self.winner = self.table[0][2]
        elif self.table[0][0] and self.table[0][0] == self.table[1][1] and self.table[0][0] == self.table[2][2]: # diagonal principal
            print(self.table[0][0])
            self.winner = self.table[0][0]
        elif self.table[0][2] and self.table[0][2] == self.table[1][1] and self.table[0][2] == self.table[2][0]: # diagonal secundária
            print(self.table[0][2])
            self.winner = self.table[0][2]
        elif self.round >= 9:
            self.winner = 3
        self.root.update()
        self.endGame()
    
    def disable_event(self):
        pass
        
    def endGame(self):
        if self.winner:
            topLevelWinner = Toplevel(self.root)
            topLevelWinner.resizable(False, False)
            topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
            if self.winner != 3:
                Label(topLevelWinner, text=f'Vitória do jogador {self.winner}.', font='Helvetica 14 bold').grid(columnspan=3)
            else:
                Label(topLevelWinner, text=f'Empate!', font='Helvetica 14 bold').grid(columnspan=3)
            Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                      command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=NSEW)
            Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                      command=self.close).grid(row=1, column=1, sticky=NSEW, columnspan=2)
            topLevelWinner.grab_set()

    def close(self):
        if self.controller != None:
            self.controller.goingBack(self.root)
        else:
            self.root.destroy()

    def RestartGame(self, toplevel):
        toplevel.destroy()
        self.startGame()

if __name__ == '__main__':
    app = Tk()
    master = TicTacToe(app)
    app.mainloop()