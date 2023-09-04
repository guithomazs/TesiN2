from tkinter import *
from utils import MyButton
import sqlite3
from database.playerDatabase import PlayerDBCommands
from sqlite3 import Error
from pathlib import Path
from enum import Enum

WINDOW_BG = 'white'
NEW_PLAYER_FONT = 'Helvetica 22 bold'
class NewPlayer(Toplevel):
    def __init__(self, master, root_players_treeview=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = master
        self.root_players_treeview = root_players_treeview
        self.resizable(False, False)
        self.title('Novo Jogador')
        self.config(bg=WINDOW_BG)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grab_set()
        self.startConnection()
        self.createScreen()

    def startConnection(self):
        self.connection = sqlite3.connect(PlayerDBCommands.DB_FILE.value)
        self.cursor = self.connection.cursor()
        self.cursor.execute(PlayerDBCommands.SQL_CREATE_TABLE.value)
        self.connection.commit()

    def createScreen(self):
        screen_frame = Frame(self, bg=WINDOW_BG)
        self.frame_data = Frame(screen_frame, bg=WINDOW_BG)

        self.lbl_nick = Label(self.frame_data, text='Nick:', font=NEW_PLAYER_FONT, bg=WINDOW_BG)
        self.ent_nick = Entry(self.frame_data, font=NEW_PLAYER_FONT)
        
        self.lbl_password = Label(self.frame_data, text='Password:', font=NEW_PLAYER_FONT, bg=WINDOW_BG)
        self.ent_password = Entry(self.frame_data, show='*', font=NEW_PLAYER_FONT)

        self.lbl_nick.grid(row=0, column=0, sticky=NSEW)
        self.ent_nick.grid(row=0, column=1, sticky=NSEW)
        
        self.lbl_password.grid(row=1, column=0, sticky=NSEW)
        self.ent_password.grid(row=1, column=1, sticky=NSEW)

        self.frame_data.grid(columnspan=2, sticky=NSEW)
        
        btn_save = MyButton(screen_frame, text='Cadastrar', command=self.register)
        btn_cancel = MyButton(screen_frame, text='Cancelar', command=self.close)

        btn_save.grid(row=2, column=0, sticky=NSEW)
        btn_cancel.grid(row=2, column=1, sticky=NSEW)

        screen_frame.grid(sticky=NSEW)

    def createErrorLabel(self, text):
        Label(self.frame_data, 
                text=text, 
                font=NEW_PLAYER_FONT, 
                bg=WINDOW_BG
        ).grid(row=3, columnspan=2, sticky=NSEW)
    def register(self):
        nick = self.ent_nick.get()
        pwd = self.ent_password.get()
        self.lbl_nick.config(fg='red' if nick == '' else 'black')
        self.lbl_password.config(fg='red' if pwd == '' else 'black')
        if nick != '' and pwd != '':
            try:
                self.cursor.execute(PlayerDBCommands.SQL_INSERIR_JOGADOR.value, (nick, pwd))
                if self.root_players_treeview != None:
                    self.root_players_treeview.insert('', 'end', values=nick, text=nick)
                self.connection.commit()
                self.close()
            except Exception as e:
                if type(e) == sqlite3.IntegrityError:
                    self.lbl_nick.config(fg='red')
                    self.createErrorLabel(text='Nick já em uso')
        else:
            self.createErrorLabel(text='Preencha todos os campos')

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.destroy()


REMOVE_PLAYER_FONT = 'Helvetica 22 bold'
REMOVE_PLAYER_TEXT_FONT = 'Helvetica 16 bold'
class RemovePlayer(Toplevel):
    def __init__(self, master, nick='MyNickName', root_players_treeview=None, excluding_player=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = master
        self.root_players_treeview = root_players_treeview
        self.excluding_player = excluding_player
        self.nickname = nick
        self.resizable(False, False)
        self.title('Excluir Jogador')
        self.config(bg=WINDOW_BG)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grab_set()
        self.startConnection()
        self.createScreen()

    def startConnection(self):
        self.connection = sqlite3.connect(PlayerDBCommands.DB_FILE.value)
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def createScreen(self):
        screen_frame = Frame(self, bg=WINDOW_BG)
        self.frame_data = Frame(screen_frame, bg=WINDOW_BG)

        self.lbl_nick = Label(self.frame_data, text=self.nickname, font=REMOVE_PLAYER_FONT, bg=WINDOW_BG)
        self.lbl_text = Label(self.frame_data, text='Entre com a senha para confirmar a exclusão', font=REMOVE_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        
        self.lbl_password = Label(self.frame_data, text='Password:', font=REMOVE_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        self.ent_password = Entry(self.frame_data, show='*', font=REMOVE_PLAYER_TEXT_FONT)

        self.lbl_nick.grid(row=0, column=0, columnspan=2,sticky=NSEW)
        self.lbl_text.grid(row=1, column=0, columnspan=2,sticky=NSEW)
        
        self.lbl_password.grid(row=3, column=0, sticky=NSEW)
        self.ent_password.grid(row=3, column=1, sticky=NSEW)

        btn_remove = MyButton(screen_frame, text='Cadastrar', command=self.removePlayer)
        btn_cancel = MyButton(screen_frame, text='Cancelar', command=self.close)

        self.frame_data.grid(sticky=NSEW, columnspan=2)
        screen_frame.grid(sticky=NSEW)
        btn_remove.grid(row=2, column=0, sticky=NSEW)
        btn_cancel.grid(row=2, column=1, sticky=NSEW)
        
    def removePlayer(self):
        insert_password = self.ent_password.get()
        self.cursor.execute(PlayerDBCommands.SQL_GET_SPECIFIC_PLAYER.value, [self.nickname])
        nickname, player_password = self.cursor.fetchone()
        if player_password == insert_password:
            PlayerDBCommands.removePlayer(nickname)
            self.root_players_treeview.delete(self.excluding_player)
            self.close()
        else:
            self.createErrorLabel('Senha incorreta')

    def createErrorLabel(self, text):
        Label(self.frame_data, 
                text=text, 
                font=REMOVE_PLAYER_FONT, 
                bg=WINDOW_BG,
                fg='red'
        ).grid(row=2, columnspan=2, sticky=NSEW)

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.destroy()




def lista_players():
    connection, cursor = PlayerDBCommands.connectDataBase()
    cursor.execute(PlayerDBCommands.SQL_CREATE_TABLE.value)
    connection.commit()
    cursor.execute(PlayerDBCommands.SQL_DELETE_ALL.value)
    # cursor.execute(SQLCommands.SQL_LIST_PLAYERS.value)
    connection.commit()
    print(cursor.fetchall())

if __name__ == '__main__':
    app = Tk()
    Button(app, text='sdasd', font=NEW_PLAYER_FONT, command=lista_players).grid()
    # aa = NewPlayer(app)
    aa = RemovePlayer(app)
    app.mainloop()