from tkinter import *
from tkinter import messagebox
import random
import time

GAME_ROWS = 5
GAME_COLUMNS = 6
PLAYER_ONE_COLOR = 'lime'
PLAYER_TWO_COLOR = 'RED'
def showMat(mat):
    for i in range(GAME_ROWS):
        for j in range(GAME_COLUMNS):
            print(mat[i][j], ' ', end='')
        print()

class TileMatching:
    def __init__(self, master:Tk, controller=None):
        self.root = master
        self.root.resizable(False, False) 
        self.root.title('Tile Matching in tkinter')
        self.emojiList = [
            '💀', '👽', '👾', '🤖', '🎃', 
            '😺', '🎱', '🤑', '🤠', '😈', 
            '👹', '👺', '🤡', '💩', '👻', 
        ]
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.controller = controller
        if controller != None:
            self.changeCloseButtonFunction()
        self.startGame()

    def changeCloseButtonFunction(self):
        self.root.protocol('WM_DELETE_WINDOW', self.goBackFunction)

    def goBackFunction(self):
        self.controller.goingBack(self.root)
    
    def _slots(self, positions=False):
        if positions:
            return [[row, column] for column in range(GAME_COLUMNS) for row in range(GAME_ROWS)]
        # return [[None for column in range(GAME_COLUMNS)] for row in range(GAME_ROWS)]
        return [[None] * GAME_COLUMNS for row in range(GAME_ROWS)]
    
    def startGame(self):
        '''
        we are playing with 15 emojis as the items, 
        so the window game will have 5 rows and 6 
        columns what means it will have 30 slots.
        '''
        self.slots = self._slots()
        self.choiceOne, self.choiceTwo = None, None
        self.ButtonOne:None | Button = None
        self.ButtonTwo:None | Button = None
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
        freeSlots = self._slots(positions=True)
        for item in self.emojiList:
            slot1, slot2 = random.sample(freeSlots, k=2)
            freeSlots.pop(freeSlots.index(slot1))
            freeSlots.pop(freeSlots.index(slot2))
            self.slots[slot1[0]][slot1[1]] = item
            self.slots[slot2[0]][slot2[1]] = item

        # showMat(self.slots)

    def createHeader(self):
        self.frameHeader = Frame(self.root)
        titleFont = 'Helvetica 18 bold'
        subFont = 'Helvetica 14'

        framePlayerOne = Frame(self.frameHeader)
        Label(framePlayerOne, 
                 text='Jogador 1', 
                 font=titleFont, 
                 fg=PLAYER_ONE_COLOR
        ).grid()
        self.LabelPlayerOneCards = Label(
            framePlayerOne, 
            text=f'Cartas: {len(self.PlayerOneCards)}', 
            font=subFont,
            fg=PLAYER_ONE_COLOR
        )
        self.LabelPlayerOneCards.grid()
        
        frameTurn = Frame(self.frameHeader)
        Label(frameTurn, 
                 text='Vez do jogador:', 
                 font=titleFont
        ).grid()
        self.LabelTurn = Label(
            frameTurn, 
            text=1 if self.PlayerTurn else 2, 
            font=subFont
        )
        self.LabelTurn.grid()

        framePlayerTwo = Frame(self.frameHeader)
        Label(
            framePlayerTwo, 
            text='Jogador 2', 
            font=titleFont, 
            fg=PLAYER_TWO_COLOR
        ).grid()
        self.LabelPlayerTwoCards = Label(
            framePlayerTwo, 
            text=f'Cartas: {len(self.PlayerTwoCards)}', 
            font=subFont,
            fg=PLAYER_TWO_COLOR
        )
        self.LabelPlayerTwoCards.grid()

        framePlayerOne.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=NSEW)
        frameTurn.grid(row=0, column=2, rowspan=2, sticky=NSEW)
        framePlayerTwo.grid(row=0, column=4, rowspan=2, sticky=NSEW)
        self.frameHeader.grid_columnconfigure(1, weight=1)
        self.frameHeader.grid_columnconfigure(3, weight=1)
    
        self.frameHeader.grid(sticky=NSEW)

    def createButtons(self):
        '''
        cria os botões clicáveis com a função de mudar o texto
        '''
        self.frameButtons = Frame(self.root)
        for row in range(GAME_ROWS):
            for column in range(GAME_COLUMNS):
                btn = Button(self.frameButtons, text='', 
                        width=5, height=2, relief='solid', font='None 28 bold', 
                        # command=lambda position=(row, column):self.control(position))
                )
                btn.config(command= 
                         lambda 
                         button=btn,
                         position=(row, column)
                         :
                         self.control(button, position))
                btn.grid(row=row, column=column, sticky=NSEW, padx=1, pady=1)
        self.frameButtons.grid()

    def control(self, button, position):
        # verifica e valida se é o primeiro card aberto ou o segundo
        if not self.choiceOne:
            self.ButtonOne = button
            self.click1(button, position)
        elif not self.choiceTwo and button != self.ButtonOne:
            self.ButtonTwo = button
            self.click2(button, position)
            self.root.update()
            time.sleep(0.6)
            self.validate()

    def click1(self, button:Button, position):
        row, column = position
        self.choiceOne = self.slots[row][column]
        button.config(text=self.choiceOne)

    def click2(self, button:Button, position):
        row, column = position
        self.choiceTwo = self.slots[row][column]
        button.config(text=self.choiceTwo)   

    def validate(self):
        if self.choiceOne == self.choiceTwo:
            self.discoveredCards += 1
            self.ButtonOne.config(state='disabled')
            self.ButtonOne.config(bg=PLAYER_ONE_COLOR if self.PlayerTurn else PLAYER_TWO_COLOR)
            self.ButtonTwo.config(state='disabled')
            self.ButtonTwo.config(bg=PLAYER_ONE_COLOR if self.PlayerTurn else PLAYER_TWO_COLOR)
            
            (
                self.PlayerOneCards.append(self.choiceOne) if self.PlayerTurn 
                else self.PlayerTwoCards.append(self.choiceOne)
            )
            self.LabelPlayerOneCards.config(text=f'Cartas: {len(self.PlayerOneCards)}')
            self.LabelPlayerTwoCards.config(text=f'Cartas: {len(self.PlayerTwoCards)}')
            self.choiceOne, self.choiceTwo = None, None
            self.ButtonOne, self.ButtonTwo = None, None
            if self.discoveredCards == len(self.emojiList):
                messagebox.showinfo('ACABOU', 'FIM DE JOGO.')
                self.endGame()
        else:
            # messagebox.showinfo('Troca de jogadores', 'Cartas não iguais, troca de jogadores.')
            self.PlayerTurn = not self.PlayerTurn
            self.LabelTurn.config(text=1 if self.PlayerTurn else 2)
            self.ButtonOne.config(text='')
            self.ButtonTwo.config(text='')
            self.choiceOne, self.choiceTwo = None, None

    def endGame(self):
        topLevelWinner = Toplevel(self.root)
        topLevelWinner.grab_set()
        topLevelWinner.resizable(False, False)
        topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
        Label(topLevelWinner,
                    text=f'Vitória do jogador {1 if len(self.PlayerOneCards) > len(self.PlayerTwoCards) else 2}', 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=NSEW)
        Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=1, column=1, sticky=NSEW, columnspan=2)
        
    def close(self):
        if self.controller != None:
            self.controller.goingBack(self.root)
        else:
            self.root.destroy()

    def RestartGame(self, toplevel:Toplevel):
        toplevel.destroy()
        self.frameButtons.destroy()
        self.frameHeader.destroy()
        self.startGame()

if __name__ == '__main__':
    root = Tk()
    app = TileMatching(root)
    root.mainloop()
