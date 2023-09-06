from pathlib import Path
from enum import Enum
import sqlite3
if __name__ == '__main__':
    from gamesCountDatabase import GamesCountDB
else:
    from database.gamesCountDatabase import GamesCountDB


GAMES_COUNT_TABLE = GamesCountDB.TABLE_NAME
class PlayerDBCommands(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'Players'
    CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
        '('
        'player_id       INTEGER PRIMARY KEY, '
        'nick            TEXT, '
        'password        TEXT, '
        'games_count_id  INTEGER NOT NULL, '
        'FOREIGN KEY (games_count_id) references '
            f'"{GAMES_COUNT_TABLE}"("Player_id")'
        ')'    
    )

    INSERIR_JOGADOR = (
        f'INSERT INTO {TABLE_NAME}'
        '(nick, password, games_count_id)'
        'VALUES '
        '(?, ?, ?)'
    )

    LIST_PLAYERS = (
        f'SELECT * FROM {TABLE_NAME}'
    )

    DELETE_ALL = (
        f'DELETE FROM {TABLE_NAME}'
    )

    DELETE_ITEM = (
        f'DELETE FROM {TABLE_NAME} '
        'WHERE nick = ?'
    )

    GET_SPECIFIC_PLAYER = (
        f'SELECT * FROM {TABLE_NAME} '
        'WHERE nick = ?'
    )

    GET_GAME_COUNT_ID = (
        f'SELECT games_count_id FROM {TABLE_NAME} '
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
        cursor.execute(PlayerDBCommands.LIST_PLAYERS.value)
        connection.commit()
        return cursor.fetchall()
    
    @staticmethod
    def removePlayer(nick):
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.DELETE_ITEM.value, (nick, ))
        connection.commit()

    @staticmethod
    def getPlayerData(nick):
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.GET_SPECIFIC_PLAYER.value, (nick, ))
        player = cursor.fetchone()
        print(player)
        connection.commit()
    
    @staticmethod
    def createDataBase():
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.CREATE_TABLE.value)
        connection.commit()

    @staticmethod
    def getAllPlayers():
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.LIST_PLAYERS.value)
        print(cursor.fetchall())
        cursor.close()
        connection.close()

    @staticmethod
    def insertPlayer(nick, password, games_counter):
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.INSERIR_JOGADOR.value, (nick, password, games_counter))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def getGamesCountInfo(nick):
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDBCommands.GET_GAME_COUNT_ID.value, (nick, ))
        game_count_id = cursor.fetchone()
        cursor.close()
        connection.close()
        return GamesCountDB.getSpecificPlayerData(game_count_id)
        
        

if __name__ == '__main__':
    PlayerDBCommands.createDataBase()
    PlayerDBCommands.getAllPlayers()
    aa = PlayerDBCommands.getGamesCountInfo("521")