from pathlib import Path
from enum import Enum
import sqlite3

class GamesCountDB(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'games'
    CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} '
        '('
        'Player_id                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        'TicTacToe_played         INTEGER NOT NULL DEFAULT 0,'
        'TicTacToe_won            INTEGER NOT NULL DEFAULT 0,'
        'TileMatching_played      INTEGER NOT NULL DEFAULT 0,'
        'TileMatching_won         INTEGER NOT NULL DEFAULT 0,'
        'ClassicCheckers_played   INTEGER NOT NULL DEFAULT 0,'
        'ClassicCheckers_won      INTEGER NOT NULL DEFAULT 0,'
        'BrazilianCheckers_played INTEGER NOT NULL DEFAULT 0,'
        'BrazilianCheckers_won    INTEGER NOT NULL DEFAULT 0'
        ')'    
    )

    INSERT_PLAYER = (
        f'INSERT INTO {TABLE_NAME} ('
            'Player_id,'
            'TicTacToe_played,'
            'TicTacToe_won,'
            'TileMatching_played,'
            'TileMatching_won,'
            'ClassicCheckers_played,'
            'ClassicCheckers_won,'
            'BrazilianCheckers_played,'
            'BrazilianCheckers_won'
        ') VALUES ('
                'NULL, 0, 0, 0, 0, 0, 0, 0, 0'
            ')'
    )

    SPECIFIC_PLAYER_DATA = (
        f'SELECT * FROM {TABLE_NAME} '
        'WHERE Player_id = ?'
    )

    LIST_PLAYERS = (
        f'SELECT * FROM {TABLE_NAME}'
    )

    DELETE_ALL = (
        f'DELETE FROM {TABLE_NAME}'
    )

    DELETE_ITEM = (
        f'DELETE FROM {TABLE_NAME} '
        'WHERE Player_id = ?'
    )

    GET_LAST = (
        f'SELECT * FROM {TABLE_NAME}'
    )

    @staticmethod
    def connectDataBase():
        connection = sqlite3.connect(GamesCountDB.DB_FILE.value)
        cursor = connection.cursor()
        return connection, cursor
    
    @staticmethod
    def getDataBasePlayers():
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.LIST_PLAYERS.value)
        connection.commit()
        cursor.close()
        connection.close()
        return cursor.fetchall()
    
    @staticmethod
    def removePlayer(nick):
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.DELETE_ITEM.value, [nick])
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def createDataBase():
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.CREATE_TABLE.value)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def createNewPlayer():
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.CREATE_TABLE.value)
        connection.commit()
        cursor.execute(GamesCountDB.INSERT_PLAYER.value)
        connection.commit()
        cursor.close()
        connection.close()
    
    @staticmethod
    def getLastPlayer():
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.GET_LAST.value)
        
        row = cursor.fetchall()
        last_player = row[-1]

        cursor.close()
        connection.close()
        return last_player
    
    @staticmethod
    def printAllPlayers():
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.GET_LAST.value)
        print(cursor.fetchall())
        cursor.close()
        connection.close()

    @staticmethod
    def getSpecificPlayerData(player_id):
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.SPECIFIC_PLAYER_DATA.value, (player_id))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()
        return user_data
    

if __name__ == '__main__':
    GamesCountDB.createDataBase()
    # GamesCountDB.createNewPlayer()
    GamesCountDB.getLastPlayer()
    GamesCountDB.getSpecificPlayerData("1")
    GamesCountDB.printAllPlayers()