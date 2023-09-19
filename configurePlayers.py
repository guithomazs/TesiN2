from tkinter import *
from utils import MyButton, OnlyDigitsEntry
import sqlite3
from database.playerDatabase import PlayerDBCommands, PlayerDB
from database.gamesCountDatabase import GamesCountDB
from historyScreen import PlayerHistory

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
        self.connection, self.cursor = PlayerDBCommands.connectDataBase()
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
                GamesCountDB.createNewPlayer()
                game_count_id = GamesCountDB.getLastPlayer()[0]
                self.cursor.execute(PlayerDB.INSERIR_JOGADOR.value, (nick, pwd, game_count_id))
                if self.root_players_treeview != None:
                    self.root_players_treeview.insert('', 'end', values=nick, text=nick)
                self.connection.commit()
                self.close()
            except Exception as e:
                print(e)
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
        self.connection, self.cursor = PlayerDBCommands.connectDataBase()

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

        btn_remove = MyButton(screen_frame, text='Remover', command=self.removePlayer)
        btn_cancel = MyButton(screen_frame, text='Cancelar', command=self.close)

        self.frame_data.grid(sticky=NSEW, columnspan=2)
        screen_frame.grid(sticky=NSEW)
        btn_remove.grid(row=2, column=0, sticky=NSEW)
        btn_cancel.grid(row=2, column=1, sticky=NSEW)
        
    def removePlayer(self):
        insert_password = self.ent_password.get()
        self.cursor.execute(PlayerDB.GET_SPECIFIC_PLAYER.value, [self.nickname])
        _, nickname, player_password, *_ = self.cursor.fetchone()
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


PLAYER_INFO_FONT = 'Helvetica 22 bold'
PLAYER_INFO_TEXT_FONT = 'Helvetica 16 bold'
class PlayerInfo(Toplevel):
    def __init__(self, master, nick='521', root_players_treeview=None, chosen_player=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = master
        self.nickname = nick
        self.admin_password = 'aaa'
        self.curr_password = ''
        self.curr_ind = 0
        self.root_treeview = root_players_treeview
        self.chosen_player = chosen_player
        self.resizable(False, False)
        self.title('Informações do Jogador')
        self.config(bg=WINDOW_BG)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grab_set()
        self.user_data = self.getUserGamesData()
        self.bind('<KeyRelease>', self.pressedKey)
        self.admin_entries = []
        self.mylbls = []
        self.active = False
        self.createScreen()

    def pressedKey(self, event):
        new_char = event.char
        if event.char != event.keysym and len(event.char) != 1:
            return
        if new_char == self.admin_password[self.curr_ind]:
            self.curr_password += new_char
            self.curr_ind += 1
        else:
            self.curr_password = ''
            self.curr_ind = 0
        if self.curr_password == self.admin_password:
            self.curr_password = ''
            self.curr_ind = 0
            self.changeAdminScreen()

    def changeAdminScreen(self):
        qnt_rows = len(self.texts)
        if not self.active:
            for i in range(1, qnt_rows):
                ent = OnlyDigitsEntry(self.frame_data, font=PLAYER_INFO_FONT, width=5)
                # ent.insert(0, self.user_data[i])
                ent.grid(row=i+1, column=2, padx=5)
                self.admin_entries.append(ent)
            btn_update = MyButton(self.screen_frame, bg='#55aa55', text='Atualizar Dados', command=self.updateData)
            btn_update.grid(row=1, column=0, columnspan=2, sticky=NSEW, pady=2)
        else:
            for i in self.admin_entries:
                i.grid_forget()
        self.active = not self.active
                
    def updateData(self):
        actual_value = 1
        for i in self.admin_entries:
            if i.get() != '':
                PlayerDBCommands.setColumnValue(self.lbl_nick.cget("text"), self.texts[actual_value], i.get())
                self.mylbls[actual_value].config(text=i.get())
            actual_value += 1
        self.changeAdminScreen()
        
    def getUserGamesData(self):
        return PlayerDBCommands.getGamesCountInfo(self.nickname)

    def createScreen(self):
        self.screen_frame = Frame(self, bg=WINDOW_BG)
        self.frame_data = Frame(self.screen_frame, bg=WINDOW_BG)

        self.lbl_nick = Label(self.frame_data, text=self.nickname, font=PLAYER_INFO_FONT, bg=WINDOW_BG)
        
        self.lbl_nick.grid(row=0, column=0, columnspan=2,sticky=NSEW)
        
        self.texts = ['Player_id', 
                 'TicTacToe_played', 
                 'TicTacToe_won', 
                 'TileMatching_played', 
                 'TileMatching_won', 
                 'ClassicCheckers_played', 
                 'ClassicCheckers_won', 
                 'BrazilianCheckers_played', 
                 'BrazilianCheckers_won'
        ]
        for element_row in range(len(self.texts)):
            Label(self.frame_data, 
                  text=self.texts[element_row],
                  font=PLAYER_INFO_TEXT_FONT,
                  bg=WINDOW_BG
            ).grid(row=element_row+1, column=0, sticky=W)
            values_label = Label(self.frame_data, 
                  text=self.user_data[element_row],
                  font=PLAYER_INFO_TEXT_FONT,
                  bg=WINDOW_BG
            )
            self.mylbls.append(values_label)
            values_label.grid(row=element_row+1, column=1, sticky=NSEW)

        btn_edit_nick = MyButton(self.screen_frame, text='Editar nick do usuário', command=lambda : self.editUser('nick'))
        btn_edit_pwd = MyButton(self.screen_frame, text='Editar senha do usuário', command=lambda : self.editUser('password'))
        btn_history = MyButton(self.screen_frame, text='Histórico do jogador', command=self.showHistory)
        btn_close = MyButton(self.screen_frame, text='Fechar', command=self.close)

        self.frame_data.grid(sticky=NSEW, columnspan=2)
        self.screen_frame.grid(sticky=NSEW)
        btn_edit_nick.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=2)
        btn_edit_pwd.grid(row=3, column=0, columnspan=2, sticky=NSEW, pady=2)
        btn_history.grid(row=4, column=0, columnspan=2, sticky=NSEW, pady=2)
        btn_close.grid(row=5, column=0, columnspan=2, sticky=NSEW)
    
    def showHistory(self):
        player_id = PlayerDBCommands.getIDByNick(self.lbl_nick.cget("text"))
        PlayerHistory(self.root, player_id=player_id)

    def editUser(self, edit_type):
        EditPlayer(self.root, 
                   nick=self.lbl_nick.cget("text"), 
                   root_players_treeview=self.root_treeview,
                   edition_player=self.chosen_player,
                   edition_type=edit_type, 
                   edition_label=self.lbl_nick
        )

    def close(self):
        self.destroy()

EDIT_PLAYER_FONT = 'Helvetica 22 bold'
EDIT_PLAYER_TEXT_FONT = 'Helvetica 16 bold'
class EditPlayer(Toplevel):
    def __init__(self, master, nick='521', root_players_treeview=None, edition_player=None, edition_type=None, edition_label=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root = master
        self.root_players_treeview = root_players_treeview
        self.edition_player = edition_player
        self.edition_label = edition_label
        self.player_nick = nick
        self.resizable(False, False)
        self.title('Editar Jogador')
        self.config(bg=WINDOW_BG)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grab_set()
        self.startConnection()
        if edition_type == 'nick':
            self.updateNickNameScreen()
        else:
            self.updatePasswordScreen()

    def startConnection(self):
        self.connection, self.cursor = PlayerDBCommands.connectDataBase()

    def updateNickNameScreen(self):
        screen_frame = Frame(self, bg=WINDOW_BG)
        self.frame_data = Frame(screen_frame, bg=WINDOW_BG)

        self.lbl_nick = Label(self.frame_data, text=self.player_nick, font=EDIT_PLAYER_FONT, bg=WINDOW_BG)
        self.lbl_text = Label(self.frame_data, text='Entre com a senha para confirmar a edição', font=EDIT_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        
        self.lbl_new_nick = Label(self.frame_data, text='Novo nick:', font=EDIT_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        self.ent_new_nick = Entry(self.frame_data, font=EDIT_PLAYER_TEXT_FONT)

        self.lbl_password = Label(self.frame_data, text='Senha:', font=EDIT_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        self.ent_password = Entry(self.frame_data, show='*', font=EDIT_PLAYER_TEXT_FONT)

        self.lbl_nick.grid(row=0, column=0, columnspan=2,sticky=NSEW)
        self.lbl_text.grid(row=1, column=0, columnspan=2,sticky=NSEW)
        
        self.lbl_new_nick.grid(row=3, column=0, sticky=NSEW)
        self.ent_new_nick.grid(row=3, column=1, sticky=NSEW)

        self.lbl_password.grid(row=4, column=0, sticky=NSEW)
        self.ent_password.grid(row=4, column=1, sticky=NSEW)

        btn_remove = MyButton(screen_frame, text='Atualizar', command=self.updatePlayerNick)
        btn_cancel = MyButton(screen_frame, text='Cancelar', command=self.close)

        self.frame_data.grid(sticky=NSEW, columnspan=2)
        screen_frame.grid(sticky=NSEW)
        btn_remove.grid(row=2, column=0, sticky=NSEW)
        btn_cancel.grid(row=2, column=1, sticky=NSEW)

    def updatePlayerNick(self):
        insert_password = self.ent_password.get()
        self.cursor.execute(PlayerDB.GET_SPECIFIC_PLAYER.value, [self.player_nick])
        _, nickname, player_password, *_ = self.cursor.fetchone()
        if player_password == insert_password:
            new_nickname = self.ent_new_nick.get()
            if(new_nickname,) in PlayerDBCommands.getAllPlayersNicks():
                self.createErrorLabel('Nickname já em uso') 
                return   
            PlayerDBCommands.updateNickname(nickname, new_nickname)
            self.edition_label.config(text=new_nickname)
            if self.root_players_treeview: 
                self.root_players_treeview.item(self.edition_player, text=new_nickname)
            self.close()
        else:
            self.createErrorLabel('Senha incorreta')
        
    def updatePasswordScreen(self):
        screen_frame = Frame(self, bg=WINDOW_BG)
        self.frame_data = Frame(screen_frame, bg=WINDOW_BG)

        self.lbl_nick = Label(self.frame_data, text=self.player_nick, font=EDIT_PLAYER_FONT, bg=WINDOW_BG)
        self.lbl_text = Label(self.frame_data, text='Entre com a senha para confirmar a edição', font=EDIT_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        
        self.lbl_password = Label(self.frame_data, text='Senha Atual:', font=EDIT_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        self.ent_password = Entry(self.frame_data, show='*', font=EDIT_PLAYER_TEXT_FONT)

        self.lbl_new_password = Label(self.frame_data, text='Nova senha:', font=EDIT_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        self.ent_new_password = Entry(self.frame_data, show='*', font=EDIT_PLAYER_TEXT_FONT)

        self.lbl_confirm_new_password = Label(self.frame_data, text='Confirmar senha:', font=EDIT_PLAYER_TEXT_FONT, bg=WINDOW_BG)
        self.ent_confirm_new_password = Entry(self.frame_data, show='*', font=EDIT_PLAYER_TEXT_FONT)

        self.lbl_nick.grid(row=0, column=0, columnspan=2,sticky=NSEW)
        self.lbl_text.grid(row=1, column=0, columnspan=2,sticky=NSEW)
        
        self.lbl_password.grid(row=3, column=0, sticky=NSEW)
        self.ent_password.grid(row=3, column=1, sticky=NSEW)

        self.lbl_new_password.grid(row=4, column=0, sticky=NSEW)
        self.ent_new_password.grid(row=4, column=1, sticky=NSEW)

        self.lbl_confirm_new_password.grid(row=5, column=0, sticky=NSEW)
        self.ent_confirm_new_password.grid(row=5, column=1, sticky=NSEW)

        btn_remove = MyButton(screen_frame, text='Atualizar', command=self.updatePlayerPassword)
        btn_cancel = MyButton(screen_frame, text='Cancelar', command=self.close)

        self.frame_data.grid(sticky=NSEW, columnspan=2)
        screen_frame.grid(sticky=NSEW)
        btn_remove.grid(row=2, column=0, sticky=NSEW)
        btn_cancel.grid(row=2, column=1, sticky=NSEW)
        
    def updatePlayerPassword(self):
        insert_password = self.ent_password.get()
        new_password = self.ent_new_password.get()
        confirmation_new_password = self.ent_confirm_new_password.get()
        self.cursor.execute(PlayerDB.GET_SPECIFIC_PLAYER.value, [self.player_nick])
        _, nickname, player_password, *_ = self.cursor.fetchone()
        if player_password == insert_password:
            if new_password != confirmation_new_password:
                self.createErrorLabel("As novas senhas não conferem.")
                return
            PlayerDBCommands.updatePassword(nickname, new_password)
            self.close()
        else:
            self.createErrorLabel('Senha incorreta')

    def createErrorLabel(self, text):
        Label(self.frame_data, 
                text=text, 
                font=EDIT_PLAYER_FONT, 
                bg=WINDOW_BG,
                fg='red'
        ).grid(row=2, columnspan=2, sticky=NSEW)

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.destroy()


def lista_players():
    connection, cursor = PlayerDBCommands.connectDataBase()
    cursor.execute(PlayerDB.CREATE_TABLE.value)
    connection.commit()
    cursor.execute(PlayerDB.LIST_PLAYERS.value)
    connection.commit()
    print(cursor.fetchall())

if __name__ == '__main__':
    app = Tk()
    Button(app, text='sdasd', font=NEW_PLAYER_FONT, command=lista_players).grid()
    # aa = NewPlayer(app)
    aa = PlayerInfo(app)
    app.mainloop()