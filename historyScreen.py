from tkinter import *
from tkinter import ttk
from database.gameHistory import GamesHistoryCommands
from database.playerDatabase import PlayerDBCommands
from utils import GridScrollableFrame

class PlayerHistory(Toplevel):
    def __init__(self, master, player_id='3'):
        super().__init__(master)
        self.root = master
        self.player_id = player_id
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.grab_set()
        self.createScreen()

    def createScreen(self):
        screen_frame = Frame(self)
        screen_frame.grid_rowconfigure(0, weight=1)
        screen_frame.grid_columnconfigure(0, weight=1)
        my_frame = GridScrollableFrame(screen_frame)
        player_matches = GamesHistoryCommands.selectPlayerMatches(self.player_id)
        actual_row = 0
        for curr_player_id, match_game, other_player_id, winner_player_id in player_matches:
            curr_frm = Frame(my_frame.scrollable_frame)
            curr_player_nick = PlayerDBCommands.getNickByID(curr_player_id)
            other_player_nick = PlayerDBCommands.getNickByID(other_player_id)
            label_p1 = Label(curr_frm, 
                             text=curr_player_nick, 
                             bg=self.getBackground(curr_player_id, winner_player_id)
            )
            game_match = Label(curr_frm, 
                             text=match_game, 
                             bg=self.getBackground(curr_player_id, winner_player_id)
            )
            label_p2 = Label(curr_frm, 
                             text=other_player_nick, 
                             bg=self.getBackground(curr_player_id, winner_player_id)
            )
            label_p1.grid(row=actual_row, column=0, sticky=NSEW)
            game_match.grid(row=actual_row, column=1, sticky=NSEW)
            label_p2.grid(row=actual_row, column=2, sticky=NSEW)
        my_frame.scrollable_frame.grid(sticky=NSEW)
        my_frame.grid(sticky=NSEW)

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