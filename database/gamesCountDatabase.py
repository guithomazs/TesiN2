from pathlib import Path
from enum import Enum
import sqlite3

class GamesCountDB(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'games'
    SQL_CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} '
        '('
        'Player_id                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        'TicTacToe_played         INTEGER NOT NULL DEFAULT 0'
        'TicTacToe_won            INTEGER NOT NULL DEFAULT 0'
        'TileMatching_played      INTEGER NOT NULL DEFAULT 0'
        'TileMatching_won         INTEGER NOT NULL DEFAULT 0'
        'ClassicCheckers_played   INTEGER NOT NULL DEFAULT 0'
        'ClassicCheckers_won      INTEGER NOT NULL DEFAULT 0'
        'BrazilianCheckers_played INTEGER NOT NULL DEFAULT 0'
        'BrazilianCheckers_won    INTEGER NOT NULL DEFAULT 0'
        ')'    
    )

    SQL_LIST_PLAYERS = (
        f'SELECT * FROM {TABLE_NAME}'
    )

    SQL_DELETE_ALL = (
        f'DELETE FROM {TABLE_NAME}'
    )

    SQL_DELETE_ITEM = (
        f'DELETE FROM {TABLE_NAME} '
        'WHERE game_id = ?'
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
        cursor.execute(GamesCountDB.SQL_LIST_PLAYERS.value)
        connection.commit()
        return cursor.fetchall()
    
    @staticmethod
    def removePlayer(nick):
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.SQL_DELETE_ITEM.value, [nick])
        connection.commit()

    @staticmethod
    def createDataBase():
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesCountDB.SQL_CREATE_TABLE.value)
        connection.commit()

if __name__ == '__main__':
    GamesCountDB.createDataBase()
