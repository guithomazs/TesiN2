from tkinter import *
from utils import MyButton
import sqlite3
from sqlite3 import Error
from pathlib import Path
from enum import Enum



ROOT_DIR = Path(__file__).parent
DB_NAME = 'players.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE_NAME = 'Players'
class SQLCommands(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'Players'
    SQL_CRIAR_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
        '('
        'nick TEXT PRIMARY KEY,'
        'password TEXT'
        ')'    
    )

    SQL_INSERIR_JOGADOR = (
        f'INSERT INTO {TABLE_NAME}'
        '(nick, password)'
        'VALUES '
        '(?, ?)'
    )

    SQL_LIST_PLAYERS = (
        f'SELECT * FROM {TABLE_NAME}'
    )

NEW_PLAYER_FONT = 'Helvetica 22 bold'
class NewPlayer(Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title('Novo Jogador')
        self.grid_rowconfigure(0, weight=1)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.grid_columnconfigure(0, weight=1)
        # self.grab_set()
        self.startConnection()
        self.createScreen()

    def startConnection(self):
        # self.connection = sqlite3.connect(SQLCommands.DB_FILE.value)
        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()
        self.cursor.execute(SQLCommands.SQL_CRIAR_TABLE)
        self.connection.commit()

    def createScreen(self):
        screen_frame = Frame(self)
        frame_data = Frame(screen_frame)

        lbl_nick = Label(frame_data, text='Nick:', font=NEW_PLAYER_FONT)
        self.ent_nick = Entry(frame_data, font=NEW_PLAYER_FONT)
        
        lbl_password = Label(frame_data, text='Password:', font=NEW_PLAYER_FONT)
        self.ent_password = Entry(frame_data, show='*', font=NEW_PLAYER_FONT)

        lbl_nick.grid(row=0, column=0, sticky=NSEW)
        self.ent_nick.grid(row=0, column=1, sticky=NSEW)
        
        lbl_password.grid(row=1, column=0, sticky=NSEW)
        self.ent_password.grid(row=1, column=1, sticky=NSEW)

        frame_data.grid(columnspan=2, sticky=NSEW)
        
        btn_save = MyButton(screen_frame, text='Cadastrar', command=self.register)
        btn_cancel = MyButton(screen_frame, text='Cancelar', command=self.close)

        btn_save.grid(row=2, column=0, sticky=NSEW)
        btn_cancel.grid(row=2, column=1, sticky=NSEW)

        screen_frame.grid(sticky=NSEW)

    def register(self):
        nick = self.ent_nick.get()
        pwd = self.ent_password.get()
        try:
            self.cursor.execute(SQLCommands.SQL_INSERIR_JOGADOR, (nick, pwd))
        except Exception as e:
            print(e)


    def close(self):
        self.cursor.close()
        self.connection.close()
        self.destroy()


if __name__ == '__main__':
    app = Tk()
    aa = NewPlayer(app)
    app.mainloop()