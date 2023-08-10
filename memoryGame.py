import tkinter as tk
from tkinter import messagebox
import random

GAME_ROWS = 5
GAME_COLUMNS = 6
def showMat(mat):
    for i in range(GAME_ROWS):
        for j in range(GAME_COLUMNS):
            print(mat[i][j], ' ', end='')
        print()

class MemoryGame:
    def __init__(self, master:tk.Tk):
        self.root = master
        self.root.resizable(False, False) 
        self.root.title('Memory Game in tkinter')
        self.emojiList = [
            '😀', '😄', '😁', '😆', '😅', 
            '😂', '🤣', '🤑', '🤠', '😈', 
            '👹', '👺', '🤡', '💩', '👻', 
        ]
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.startGame()

    def startGame(self):
        '''
        we are playing with 15 emojis as the items, 
        so the window game will have 5 rows and 6 
        columns what means it will have 30 slots.
        '''
        self.slots = [[None for column in range(GAME_COLUMNS)] for row in range(GAME_ROWS)]
        print(self.slots)
        self.choiceOne, self.choiceTwo = None, None
        self.ButtonOne:None | tk.Button = None
        self.ButtonTwo:None | tk.Button = None
        self.PlayerTurn = True # True para jogador 1 ou False para jogador 2, definindo o jogador da vez
        self.PlayerOneCards = []
        self.PlayerTwoCards = []
        self.discoveredCards = 0
        self.fillSlots()
        self.createHeader()
        self.createButtons()

    def fillSlots(self):
        '''
        cria as opções de slots vazios (posições da tabela de acordo com seu tamanho)
        e as preenche de acordo com os emojis da lista de emoji, definindo posições aleatórias
        para os pares de emoji. (itens do jogo da memória)
        '''
        freeSlots = [[row, column] for column in range(GAME_COLUMNS) for row in range(GAME_ROWS)]
        print(freeSlots)
        for item in self.emojiList:
            slot1, slot2 = random.sample(freeSlots, k=2)
            freeSlots.pop(freeSlots.index(slot1))
            freeSlots.pop(freeSlots.index(slot2))
            self.slots[slot1[0]][slot1[1]] = item
            self.slots[slot2[0]][slot2[1]] = item

        showMat(self.slots)

    def createHeader(self):
        self.frameHeader = tk.Frame(self.root)
        titleFont = 'Helvetica 18 bold'
        subFont = 'Helvetica 14'

        framePlayerOne = tk.Frame(self.frameHeader)
        tk.Label(framePlayerOne, text='Jogador 1', font=titleFont).grid()
        self.LabelPlayerOneCards = tk.Label(framePlayerOne, 
                                            text=f'Cartas: {len(self.PlayerOneCards)}', 
                                            font=subFont)
        self.LabelPlayerOneCards.grid()
        
        frameTurn = tk.Frame(self.frameHeader)
        tk.Label(frameTurn, text='Vez do jogador:', font=titleFont).grid()
        self.LabelTurn = tk.Label(frameTurn, text=1 if self.PlayerTurn else 2, font=subFont)
        self.LabelTurn.grid()

        framePlayerTwo = tk.Frame(self.frameHeader)
        tk.Label(framePlayerTwo, text='Jogador 2', font=titleFont).grid()
        self.LabelPlayerTwoCards = tk.Label(framePlayerTwo, 
                                            text=f'Cartas: {len(self.PlayerTwoCards)}', 
                                            font=subFont)
        self.LabelPlayerTwoCards.grid()

        framePlayerOne.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=tk.NSEW)
        frameTurn.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW)
        framePlayerTwo.grid(row=0, column=4, rowspan=2, sticky=tk.NSEW)
        self.frameHeader.grid_columnconfigure(1, weight=1)
        self.frameHeader.grid_columnconfigure(3, weight=1)
    
        self.frameHeader.grid(sticky=tk.NSEW)

    def createButtons(self):
        '''
        cria os botões clicáveis com a função de mudar o texto
        '''
        self.frameButtons = tk.Frame(self.root)
        self.buttonsList = []
        for row in range(GAME_ROWS):
            for column in range(GAME_COLUMNS):
                btn = tk.Button(self.frameButtons, text='', \
                        width=5, height=2, relief='solid', font='None 28 bold', \
                        # command=lambda position=(row, column):self.control(position))
                )
                self.buttonsList.append(btn)
                btn.config(command= 
                         lambda 
                         button=self.buttonsList[-1],
                         position=(row, column)
                         :
                         self.control(button, position))
                btn.grid(row=row, column=column, sticky=tk.NSEW, padx=1, pady=1)
        self.frameButtons.grid()

    def control(self, button, position):
        # verifica e valida se é o primeiro card aberto ou o segundo
        if not self.choiceOne:
            self.ButtonOne = button
            self.click1(button, position)
        elif not self.choiceTwo:
            self.ButtonTwo = button
            self.click2(button, position)

    def click1(self, button:tk.Button, position):
        row, column = position
        self.choiceOne = self.slots[row][column]
        button.config(text=self.choiceOne)

    def click2(self, button:tk.Button, position):
        row, column = position
        self.choiceTwo = self.slots[row][column]
        # print(self.choiceOne, self.choiceTwo)
        button.config(text=self.choiceTwo)
        self.validate()

    def validate(self):
        if self.choiceOne == self.choiceTwo:
            self.discoveredCards += 1
            self.ButtonOne.config(state='disabled')
            self.ButtonTwo.config(state='disabled')
            
            self.PlayerOneCards.append(self.choiceOne) if self.PlayerTurn \
                else self.PlayerTwoCards.append(self.choiceOne)
            self.LabelPlayerOneCards.config(text=f'Cartas: {len(self.PlayerOneCards)}')
            self.LabelPlayerTwoCards.config(text=f'Cartas: {len(self.PlayerTwoCards)}')
            self.choiceOne, self.choiceTwo = None, None
            self.ButtonOne, self.ButtonTwo = None, None
            if self.discoveredCards == len(self.emojiList):
                messagebox.showinfo('ACABOU', 'FIM DE JOGO.')
                print(len(self.PlayerOneCards), len(self.PlayerTwoCards))
                self.endGame()
        else:
            messagebox.showinfo('Troca de jogadores', 'Cartas não iguais, troca de jogadores.')
            self.PlayerTurn = not self.PlayerTurn
            self.LabelTurn.config(text=1 if self.PlayerTurn else 2)
            self.ButtonOne.config(text='')
            self.ButtonTwo.config(text='')
            self.choiceOne, self.choiceTwo = None, None

    def endGame(self):
        topLevelWinner = tk.Toplevel(self.root)
        topLevelWinner.grab_set()
        topLevelWinner.resizable(False, False)
        topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
        tk.Label(topLevelWinner,
                    text=f'Vitória do jogador {1 if len(self.PlayerOneCards) > len(self.PlayerTwoCards) else 2}', 
                    font='Helvetica 14 bold').grid(columnspan=3)
        tk.Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=tk.NSEW)
        tk.Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=1, column=1, sticky=tk.NSEW, columnspan=2)
        
    def close(self):
        self.root.destroy()

    def RestartGame(self, toplevel:tk.Toplevel):
        toplevel.destroy()
        self.frameButtons.destroy()
        self.frameHeader.destroy()
        self.startGame()


root = tk.Tk()
app = MemoryGame(root)
root.mainloop()
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = MemoryGame(root)
#     root.mainloop()