from tkinter import *
from tkinter import ttk
from database.gameHistory import GamesHistoryCommands
from database.playerDatabase import PlayerDBCommands

class PlayerHistory(Toplevel):
    
    def __init__(self, master, player_id='2'):
        super().__init__(master)
        self.root = master
        self.player_id = player_id
        self.title('Histórico do jogador')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grab_set()
        self.createScreen()

    def createScreen(self):
        screen_frame = Frame(self)
        screen_frame.grid_rowconfigure(0, weight=1)
        screen_frame.grid_columnconfigure(0, weight=1)
        player_matches = GamesHistoryCommands.selectPlayerMatches(self.player_id)

        player_nick = PlayerDBCommands.getNickByID(self.player_id)
        label_player_nick = Label(screen_frame, text=player_nick, font='Helvetica 18 bold')
        label_player_nick.grid(row=0, column=0, sticky=NSEW)
        
        treeview_columns = ('player_one', 'game_match', 'player_two')
        
        matches_treeview = ttk.Treeview(screen_frame, columns=treeview_columns, show='tree', height=15)
        matches_treeview.heading('player_one', text='player_one')
        matches_treeview.heading('game_match', text='game_match')
        matches_treeview.heading('player_two', text='player_two')

        matches_treeview.column('#0', width=0)
        matches_treeview.column('player_one', minwidth=50, width=100, stretch=1, anchor=W)
        matches_treeview.column('game_match', minwidth=200, width=200, stretch=1, anchor=N)
        matches_treeview.column('player_two', minwidth=50, width=100, stretch=1, anchor=E)
        
        matches_treeview.tag_configure('won', background='green')
        matches_treeview.tag_configure('lost', background='red')
        matches_treeview.tag_configure('draw', background='gray')
        
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("Treeview", background="black", 
                fieldbackground="black", foreground="white",
                font='Helvetica 12 bold')

        for curr_player_id, match_game, other_player_id, winner_player_id in player_matches:
            player1_nick = PlayerDBCommands.getNickByID(curr_player_id)
            player2_nick = PlayerDBCommands.getNickByID(other_player_id)
            if winner_player_id == curr_player_id:
                curr_tag = 'won'
            elif winner_player_id is not None:
                curr_tag = 'lost'
            else:
                curr_tag = 'draw'
            matches_treeview.insert('', 'end', values=(player1_nick, match_game, player2_nick), tags=(curr_tag))
        matches_treeview.grid(sticky=NSEW)
        screen_frame.grid()   

    def getBackground(self, curr_player_id, winner_player):
        return (
            'green' if curr_player_id == winner_player 
            else 'red' if (winner_player not in [None, 'None']) 
                else 'grey'
        )


if __name__ == '__main__':
    app = Tk()
    PlayerHistory(app)
    app.mainloop()