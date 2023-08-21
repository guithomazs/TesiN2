import random
import tkinter as tk

class Tela:
    def __init__(self, master: tk.Tk, n_bombs=15, ordem=20):
        self.janela = master
        self.janela.title('É o Minas é.')
        self.num_bombas = n_bombs
        self.ordem=ordem
        self.start()
    
    def start(self):
        self.labelTimer = tk.Label(self.janela, text='0', font='Helvetica 18 bold')
        self.labelTimer.grid(row=0,columnspan=self.ordem, sticky=tk.NSEW)
        self.frameBombs = tk.Frame(self.janela)
        self.frameBombs.grid(row=1, columnspan=self.ordem)
        self.on_game = 0
        self.timer = 0
        self.table = [['n' for j in range(self.ordem)] for i in range(self.ordem)]
        self.createButtons()
    
    def createButtons(self):
        for linha in range(len(self.table)):
            for coluna in range(len(self.table)):
                btn = tk.Button(self.frameBombs, text='', \
                        width=2, height=1, \
                        command=lambda position=(linha, coluna):self.control(position))
                btn.bind("<ButtonPress-3>", lambda event, position=(linha, coluna):self.changeButton(event, position))
                btn.grid(row=linha, column=coluna, sticky=tk.NSEW, padx=1, pady=1)
    
    def button_GoBackNormal(self, event, position):
        linha, coluna = position[0], position[1]
        btn = tk.Button(self.frameBombs, text='', \
                        width=2, height=1, \
                        command=lambda position=(linha, coluna):self.control(position))
        btn.bind("<ButtonPress-3>", lambda event, position=(linha, coluna):self.changeButton(event, position))
        btn.grid(row=linha, column=coluna, sticky=tk.NSEW, padx=1, pady=1)

    def changeButton(self, event, position):
        linha, coluna = position[0], position[1]
        if self.on_game:
            flagButton = tk.Button(self.frameBombs, text="\U0001F3F4", fg='red')
            flagButton.bind("<ButtonPress-3>", lambda event, position=(linha, coluna):self.button_GoBackNormal(event, position))
            flagButton.grid(row=linha, column=coluna, sticky=tk.NSEW, padx=1, pady=1)

    def create_protected(self, pos):
        linha, coluna = pos[0], pos[1]
        protected_area = [[linha, coluna]]
        if linha == 0 and coluna == 0:
            protected_area.append([0,1])
            protected_area.append([1,0])
            protected_area.append([1,1])
        elif linha == 0 and coluna == len(self.table[linha]) - 1:
            protected_area.append([0, coluna-1])
            protected_area.append([1, coluna-1]) 
            protected_area.append([1, coluna])
        elif linha == 0:
            protected_area.append([0, coluna-1])
            protected_area.append([0, coluna+1])
            protected_area.append([1, coluna-1])
            protected_area.append([1, coluna])
            protected_area.append([1, coluna+1])
        elif linha == len(self.table) - 1 and coluna == 0:
            protected_area.append([linha, 1])
            protected_area.append([linha-1, 0])
            protected_area.append([linha-1, 1])
        elif linha == len(self.table) - 1 and coluna == len(self.table[linha]) - 1:
            protected_area.append([linha, coluna-1])
            protected_area.append([linha-1, coluna-1]) 
            protected_area.append([linha-1, coluna])
        elif linha == len(self.table) - 1:
            protected_area.append([linha, coluna-1])
            protected_area.append([linha, coluna+1])
            protected_area.append([linha-1, coluna-1]) 
            protected_area.append([linha-1, coluna])
            protected_area.append([linha-1, coluna+1])
        else:
            protected_area.append([linha, coluna-1])
            protected_area.append([linha, coluna+1])
            protected_area.append([linha-1, coluna-1]) 
            protected_area.append([linha-1, coluna])
            protected_area.append([linha-1, coluna+1])
            protected_area.append([linha+1, coluna-1]) 
            protected_area.append([linha+1, coluna])
            protected_area.append([linha+1, coluna+1])
        return protected_area
    
    def updateClock(self):
        if self.on_game:
            self.timer += 1
            self.labelTimer.config(text=self.timer)
            self.labelTimer.after(1000, self.updateClock)
    
    def control(self, pos):
        linha, coluna = pos[0], pos[1]
        if not self.on_game:
            self.gera_bombas(self.num_bombas, self.create_protected(pos))
            self.conta_bombas()
            self.on_game = 1
            self.updateClock()
        
        already_done = []
        open_list = [[linha, coluna]]
        while len(open_list):
            linha = open_list[0][0]
            coluna = open_list[0][1]
            if self.table[open_list[0][0]][open_list[0][1]] == 0:
                if linha == 0 and coluna == 0:
                    if [linha, coluna+1] not in already_done: open_list.append([linha, coluna+1])
                    if [linha+1, coluna] not in already_done: open_list.append([linha+1, coluna])
                    if [linha+1, coluna+1] not in already_done: open_list.append([linha+1, coluna+1])
                elif linha == 0 and coluna == len(self.table[linha]) - 1:
                    if [linha, coluna-1] not in already_done: open_list.append([linha, coluna-1])
                    if [linha+1, coluna-1] not in already_done: open_list.append([linha+1, coluna-1]) 
                    if [linha+1, coluna] not in already_done: open_list.append([linha+1, coluna])
                elif linha == 0:
                    if [linha, coluna-1] not in already_done: open_list.append([linha, coluna-1])
                    if [linha, coluna+1] not in already_done: open_list.append([linha, coluna+1])
                    if [linha+1, coluna-1] not in already_done: open_list.append([linha+1, coluna-1])
                    if [linha+1, coluna] not in already_done: open_list.append([linha+1, coluna])
                    if [linha+1, coluna+1] not in already_done: open_list.append([linha+1, coluna+1])
                elif linha == len(self.table) - 1 and coluna == 0:  # canto inferior esquerdo
                    if [linha, coluna+1] not in already_done: open_list.append([linha, coluna+1])
                    if [linha-1, coluna] not in already_done: open_list.append([linha-1, coluna])
                    if [linha-1, coluna+1] not in already_done: open_list.append([linha-1, coluna+1])
                elif linha == len(self.table) - 1 and coluna == len(self.table[linha]) - 1:  # canto inferior direito
                    if [linha, coluna-1] not in already_done: open_list.append([linha, coluna-1])
                    if [linha-1, coluna-1] not in already_done: open_list.append([linha-1, coluna-1]) 
                    if [linha-1, coluna] not in already_done: open_list.append([linha-1, coluna])
                elif linha == len(self.table) - 1:
                    if [linha, coluna-1] not in already_done: open_list.append([linha, coluna-1])
                    if [linha, coluna+1] not in already_done: open_list.append([linha, coluna+1])
                    if [linha-1, coluna-1] not in already_done: open_list.append([linha-1, coluna-1]) 
                    if [linha-1, coluna] not in already_done: open_list.append([linha-1, coluna])
                    if [linha-1, coluna+1] not in already_done: open_list.append([linha-1, coluna+1])
                elif coluna == 0:
                    if [linha-1, coluna] not in already_done: open_list.append([linha-1, coluna])
                    if [linha-1, coluna+1] not in already_done: open_list.append([linha-1, coluna+1])
                    if [linha, coluna+1] not in already_done: open_list.append([linha, coluna+1])
                    if [linha+1, coluna] not in already_done: open_list.append([linha+1, coluna])
                    if [linha+1, coluna+1] not in already_done: open_list.append([linha+1, coluna+1])
                elif coluna == len(self.table[linha]) - 1:
                    if [linha-1, coluna] not in already_done: open_list.append([linha-1, coluna])
                    if [linha-1, coluna-1] not in already_done: open_list.append([linha-1, coluna-1])
                    if [linha, coluna-1] not in already_done: open_list.append([linha, coluna-1])
                    if [linha+1, coluna-1] not in already_done: open_list.append([linha+1, coluna])
                    if [linha+1, coluna-1] not in already_done: open_list.append([linha+1, coluna-1])
                else:
                    if [linha, coluna-1] not in already_done: open_list.append([linha, coluna-1])
                    if [linha, coluna+1] not in already_done: open_list.append([linha, coluna+1])
                    if [linha-1, coluna-1] not in already_done: open_list.append([linha-1, coluna-1]) 
                    if [linha-1, coluna] not in already_done: open_list.append([linha-1, coluna])
                    if [linha-1, coluna+1] not in already_done: open_list.append([linha-1, coluna+1])
                    if [linha+1, coluna-1] not in already_done: open_list.append([linha+1, coluna-1]) 
                    if [linha+1, coluna] not in already_done: open_list.append([linha+1, coluna])
                    if [linha+1, coluna+1] not in already_done: open_list.append([linha+1, coluna+1])
            if open_list[0] not in already_done:
                self.change_text(open_list[0])
                already_done.append(open_list[0])
            open_list.pop(0)

    def change_text(self, pos):
        linha, coluna = pos[0], pos[1]
        if self.table[linha][coluna] == 'x':
            tk.Label(self.frameBombs, text='\U0001F4A3', \
                        borderwidth=3, relief='groove', fg='red') \
                .grid(row=linha, column=coluna, \
                        sticky=tk.NSEW, padx=1, pady=1)
            self.Restart()
        else:
            tk.Label(self.frameBombs, text=self.table[linha][coluna], \
                        borderwidth=3, relief='groove', fg='blue') \
                .grid(row=linha, column=coluna, \
                        sticky=tk.NSEW, padx=1, pady=1)
    
    def disable_event(self):
        pass

    def Restart(self):
        # self.janela.withdraw()
        self.on_game = 0
        self.restartTopLevel = tk.Toplevel()
        self.restartTopLevel.grab_set()
        self.restartTopLevel.resizable(False, False)
        self.restartTopLevel.protocol("WM_DELETE_WINDOW", self.disable_event)
        # self.restartTopLevel.bind("<Destroy>", self.reopen)
        fontBtns = 'Helvetica 12 bold'
        restartButton = tk.Button(self.restartTopLevel, text='Jogar novamente', font=fontBtns, command=self.RestartGame)
        restartButton.grid()
        quitButton = tk.Button(self.restartTopLevel, text='Sair', font=fontBtns, command=self.sair)
        quitButton.grid(row=0, column=1)
    
    def reopen(self, e):
        self.janela.deiconify()

    def RestartGame(self):
        self.restartTopLevel.destroy()
        self.start()

    def sair(self):
        self.janela.destroy()
        
    def gera_bombas(self, num_bombs, protected_area=None):
        opcoes = []
        for i in range(self.ordem):
            for j in range(self.ordem):
                if [i, j] not in protected_area: opcoes.append([i, j])
        escolhidos = random.choices(opcoes, k=num_bombs)
        for linha, coluna in escolhidos:
            self.table[linha][coluna] = 'x'

    def conta_bombas(self):
        for linha in range(len(self.table)):
            for coluna in range(len(self.table)):
                contador = 0
                
                if self.table[linha][coluna] == 'x':
                    continue

                if linha == 0:
                    if coluna == 0:
                        if self.table[linha][coluna+1] == 'x': contador += 1
                        if self.table[linha+1][coluna] == 'x': contador += 1
                        if self.table[linha+1][coluna+1] == 'x': contador += 1
                    elif coluna == len(self.table) - 1:
                        if self.table[linha][coluna-1] == 'x': contador += 1
                        if self.table[linha+1][coluna] == 'x': contador += 1
                        if self.table[linha+1][coluna-1] == 'x': contador += 1
                    else:
                        if self.table[linha][coluna+1] == 'x': contador += 1
                        if self.table[linha][coluna-1] == 'x': contador += 1
                        if self.table[linha+1][coluna] == 'x': contador += 1
                        if self.table[linha+1][coluna+1] == 'x': contador += 1
                        if self.table[linha+1][coluna-1] == 'x': contador += 1
                elif linha == len(self.table) - 1:
                    if coluna == 0:
                        if self.table[linha][coluna+1] == 'x': contador += 1
                        if self.table[linha-1][coluna] == 'x': contador += 1
                        if self.table[linha-1][coluna+1] == 'x': contador += 1
                    elif coluna == len(self.table) - 1:
                        if self.table[linha][coluna-1] == 'x': contador += 1
                        if self.table[linha-1][coluna] == 'x': contador += 1
                        if self.table[linha-1][coluna-1] == 'x': contador += 1
                    else:
                        if self.table[linha][coluna+1] == 'x': contador += 1
                        if self.table[linha][coluna-1] == 'x': contador += 1
                        if self.table[linha-1][coluna] == 'x': contador += 1
                        if self.table[linha-1][coluna+1] == 'x': contador += 1
                        if self.table[linha-1][coluna-1] == 'x': contador += 1
                elif coluna == 0:
                    if self.table[linha][coluna+1] == 'x': contador += 1
                    if self.table[linha-1][coluna] == 'x': contador += 1
                    if self.table[linha-1][coluna+1] == 'x': contador += 1
                    if self.table[linha+1][coluna] == 'x': contador += 1
                    if self.table[linha+1][coluna+1] == 'x': contador += 1
                elif coluna == len(self.table) - 1:
                    if self.table[linha][coluna-1] == 'x': contador += 1
                    if self.table[linha-1][coluna] == 'x': contador += 1
                    if self.table[linha-1][coluna-1] == 'x': contador += 1
                    if self.table[linha+1][coluna] == 'x': contador += 1
                    if self.table[linha+1][coluna-1] == 'x': contador += 1
                else:
                    if self.table[linha][coluna+1] == 'x': contador += 1
                    if self.table[linha][coluna-1] == 'x': contador += 1
                    if self.table[linha-1][coluna] == 'x': contador += 1
                    if self.table[linha-1][coluna-1] == 'x': contador += 1
                    if self.table[linha-1][coluna+1] == 'x': contador += 1
                    if self.table[linha+1][coluna] == 'x': contador += 1
                    if self.table[linha+1][coluna-1] == 'x': contador += 1
                    if self.table[linha+1][coluna+1] == 'x': contador += 1
                
                self.table[linha][coluna] = contador

if __name__ == '__main__':
    app = tk.Tk()
    master = Tela(app)
    app.mainloop()
