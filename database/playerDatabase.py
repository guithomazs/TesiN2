from pathlib import Path
from enum import Enum
import gamesCountDatabase
import sqlite3

class PlayerDBCommands(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'Players'
    SQL_CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
        '('
        'nick            TEXT PRIMARY KEY,'
        'password        TEXT,'
        'games_count_id  INT NOT NULL'
        'FOREIGN KEY (games_count_id) references '
            f'"{gamesCountDatabase.GamesCountDB.TABLE_NAME}"("Player_id")'
        ')'    
    )

    SQL_INSERIR_JOGADOR = (
        f'INSERT INTO {TABLE_NAME}'
        '(nick, password, games_count_id)'
        'VALUES '
        '(?, ?, ?)'
    )

    SQL_LIST_PLAYERS = (
        f'SELECT * FROM {TABLE_NAME}'
    )

    SQL_DELETE_ALL = (
        f'DELETE FROM {TABLE_NAME}'
    )

    SQL_DELETE_ITEM = (
        f'DELETE FROM {TABLE_NAME} '
        'WHERE nick = ?'
    )

    SQL_GET_SPECIFIC_PLAYER = (
        f'SELECT * FROM {TABLE_NAME} '
        'WHERE nick = ?'
    )

    @staticmethod
    def connectDataBase():
        connection = sqlite3.connect(PlayerDBCommands.DB_FILE.value)
        cursor = connection.cursor()
        return connection, cursor
    
    @staticmethod
    def getDataBasePlayers():
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.SQL_LIST_PLAYERS.value)
        connection.commit()
        return cursor.fetchall()
    
    @staticmethod
    def removePlayer(nick):
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.SQL_DELETE_ITEM.value, [nick])
        connection.commit()

    @staticmethod
    def getPlayerData(nick):
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.SQL_GET_SPECIFIC_PLAYER.value, [nick])
        player = cursor.fetchone()
        print(player)
        connection.commit()
    
    @staticmethod
    def createDataBase():
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.SQL_CREATE_TABLE.value)
        connection.commit()

if __name__ == '__main__':
    PlayerDBCommands.createDataBase()
