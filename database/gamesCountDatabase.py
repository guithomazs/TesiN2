from pathlib import Path
from enum import Enum
import sqlite3

class CompetitiveGamesNames(Enum):
    TicTacToe = 'TicTacToe'
    TileMatching = 'TileMatching'
    ClassicCheckers = 'ClassicCheckers'
    BrazilianCheckers = 'BrazilianCheckers'

class TimedGamesNames(Enum):
    MineSweeper = 'MineSweeper'

def get_games_sql_values():
    competitive_games = [game.value for game in CompetitiveGamesNames]
    timed_games = [game.value for game in TimedGamesNames]
    games_values = ''
    for game in competitive_games:
        games_values = games_values + f'{game}_played INTEGER NOT NULL DEFAULT 0,'
        games_values = games_values + f' {game}_won INTEGER NOT NULL DEFAULT 0, '

    for game in timed_games:
        games_values = games_values + (
            f'{game}_best_time INTEGER NOT NULL DEFAULT 0, '
                if game != timed_games[-1]
                else 
            f'{game}_best_time INTEGER NOT NULL DEFAULT 0'
        )
    return games_values

class GamesDB(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'games'
    CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} '
        '('
        'Player_id                INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        + get_games_sql_values() +
        ')'    
    )

    INSERT_PLAYER = (
        f'INSERT INTO {TABLE_NAME} DEFAULT VALUES'
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


class GamesCountDB():
    
    @staticmethod
    def connectDataBase():
        connection = sqlite3.connect(GamesDB.DB_FILE.value)
        cursor = connection.cursor()
        return connection, cursor
    
    @staticmethod
    def getDataBasePlayers():
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesDB.LIST_PLAYERS.value)
        connection.commit()
        cursor.close()
        connection.close()
        return cursor.fetchall()
    
    @staticmethod
    def removePlayer(nick):
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesDB.DELETE_ITEM.value, [nick])
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def createDataBase():
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesDB.CREATE_TABLE.value)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def createNewPlayer():
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesDB.CREATE_TABLE.value)
        connection.commit()
        cursor.execute(GamesDB.INSERT_PLAYER.value)
        connection.commit()
        cursor.close()
        connection.close()
    
    @staticmethod
    def getLastPlayer():
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesDB.GET_LAST.value)
        
        row = cursor.fetchall()
        last_player = row[-1]

        cursor.close()
        connection.close()
        return last_player
    
    @staticmethod
    def printAllPlayers():
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        cursor.execute(GamesDB.GET_LAST.value)
        print(cursor.fetchall())
        cursor.close()
        connection.close()

    @staticmethod
    def getSpecificPlayerData(player_id):
        GamesCountDB.createDataBase()
        connection, cursor = GamesCountDB.connectDataBase()
        print(player_id)
        cursor.execute(GamesDB.SPECIFIC_PLAYER_DATA.value, (player_id))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()
        return user_data
    

if __name__ == '__main__':
    GamesCountDB.createDataBase()
    GamesCountDB.createNewPlayer()
    GamesCountDB.getLastPlayer()
    GamesCountDB.getSpecificPlayerData("1")
    GamesCountDB.printAllPlayers()
    get_games_sql_values()