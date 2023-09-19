from pathlib import Path
import sqlite3
from enum import Enum


class GamesHistoryDB(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'gamesHistory'
    CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} '
        '('
        'match_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        'match_game TEXT NOT NULL, '
        'player_one_id INTEGER NOT NULL, '
        'player_two_id INTEGER NOT NULL,'
        'winner_player_id INTEGER, '
        'FOREIGN KEY (player_one_id) references '
            f'"Players"("player_id"), '
        'FOREIGN KEY (player_two_id) references '
            f'"Players"("player_id"), '    
        'FOREIGN KEY (winner_player_id) references '
            f'"Players"("player_id")'
        ')'    
    )

    INSERT_NEW_MATCH = (
        f'INSERT INTO {TABLE_NAME} '
        '(match_game, player_one_id, player_two_id, winner_player_id) '
        'VALUES '
        '(?, ?, ?, ?)'
    )

    INSERT_NEW_DRAW = (
        f'INSERT INTO {TABLE_NAME} '
        '(match_game, player_one_id, player_two_id) '
        'VALUES '
        '(?, ?, ?)'
    )

    PLAYER_MATCHES = (
        f'SELECT player_one_id, match_game, player_two_id, winner_player_id FROM {TABLE_NAME}'
        ' WHERE player_one_id = ? OR player_two_id = ? ORDER BY match_id DESC'
    )

class GamesHistoryCommands():

    @staticmethod
    def createDataBase():
        connection, cursor = GamesHistoryCommands.connectDataBase()
        cursor.execute(GamesHistoryDB.CREATE_TABLE.value)
        connection.commit()
        connection.close()
    
    @staticmethod
    def connectDataBase():
        connection = sqlite3.connect(GamesHistoryDB.DB_FILE.value)
        cursor = connection.cursor()
        return connection, cursor
    
    @staticmethod
    def insertNewMatch(*args):
        connection, cursor = GamesHistoryCommands.connectDataBase()
        if len(args) == 4:
            cursor.execute(GamesHistoryDB.INSERT_NEW_MATCH.value, (args))
        else:
            cursor.execute(GamesHistoryDB.INSERT_NEW_DRAW.value, (args))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def dropTable():
        connection, cursor = GamesHistoryCommands.connectDataBase()
        sql = f'DROP TABLE IF EXISTS {GamesHistoryDB.TABLE_NAME.value}'
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def selectAll():
        connection, cursor = GamesHistoryCommands.connectDataBase()
        sql = f'SELECT * FROM {GamesHistoryDB.TABLE_NAME.value}'
        cursor.execute(sql)
        allHistory = cursor.fetchall()
        print(allHistory)
        connection.commit()
        cursor.close()
        connection.close()
        return allHistory
    
    @staticmethod
    def selectPlayerMatches(player_id):
        connection, cursor = GamesHistoryCommands.connectDataBase()
        cursor.execute(GamesHistoryDB.PLAYER_MATCHES.value, [player_id, player_id])
        player_history = cursor.fetchall()
        # print(player_history)
        connection.commit()
        cursor.close()
        connection.close()
        return player_history
    
if __name__ == '__main__':
    # GamesCountDB.clearDataBase()
    # GamesHistoryCommands.createDataBase()
    # GamesHistoryCommands.dropTable()
    GamesHistoryCommands.selectAll()