from pathlib import Path
from enum import Enum
import sqlite3
import typing

if __name__ == '__main__':
    from gamesCountDatabase import GamesCountDB, GamesDB, CompetitiveGamesNames
else:
    from database.gamesCountDatabase import GamesCountDB, GamesDB, CompetitiveGamesNames


GAMES_COUNT_TABLE = GamesDB.TABLE_NAME.value
TABLE_NAME = 'Players'

class PlayerDB(Enum):
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'players.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}'
        '('
        'player_id       INTEGER PRIMARY KEY, '
        'nick            TEXT UNIQUE, '
        'password        TEXT, '
        'games_count_id  INTEGER NOT NULL, '
        'FOREIGN KEY (games_count_id) references '
            f'"{GAMES_COUNT_TABLE}"("Player_id") ON DELETE CASCADE'
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


class PlayerDBCommands():

    @staticmethod
    def connectDataBase():
        connection = sqlite3.connect(PlayerDB.DB_FILE.value)
        cursor = connection.cursor()
        return connection, cursor
    
    @staticmethod
    def getDataBasePlayers():
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDB.LIST_PLAYERS.value)
        connection.commit()
        return cursor.fetchall()
    
    @staticmethod
    def getGamePlayerInfo(game_name):
        connection, cursor = PlayerDBCommands.connectDataBase()
        game_column = (
            f'game.{game_name}_won' 
                if game_name in CompetitiveGamesNames._member_names_ else 
            f'game.{game_name}_best_time'
        )
        game_order = 'DESC' if game_name in CompetitiveGamesNames._member_names_ else 'ASC'
        sql1 = (
            f'SELECT p.player_id, p.nick, {game_column} '  
            f'FROM {TABLE_NAME} p '
            f'INNER JOIN {GAMES_COUNT_TABLE} game '
            f'ON p.games_count_id = game.Player_id ' 
            f'WHERE {game_column} <> 0 '
            f'ORDER BY {game_column} {game_order}'  
        )
        cursor.execute(sql1)
        valued_players = cursor.fetchall()
        sql2 = (
            f'SELECT p.player_id, p.nick, {game_column} '  
            f'FROM {TABLE_NAME} p '
            f'INNER JOIN {GAMES_COUNT_TABLE} game '
            f'ON p.games_count_id = game.Player_id '
            f'WHERE {game_column} = 0 '
            f'ORDER BY p.player_id ASC'  
        )
        cursor.execute(sql2)
        non_valued_players = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return valued_players + non_valued_players

    @staticmethod
    def removePlayer(nick):
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDB.DELETE_ITEM.value, (nick, ))
        connection.commit()

    @staticmethod
    def getPlayerData(nick):
        PlayerDBCommands.createDataBase()
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDB.GET_SPECIFIC_PLAYER.value, (nick, ))
        player = cursor.fetchone()
        connection.commit()
    
    @staticmethod
    def createDataBase():
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDB.CREATE_TABLE.value)
        connection.commit()

    @staticmethod
    def getAllPlayers():
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDB.LIST_PLAYERS.value)
        print(cursor.fetchall())
        cursor.close()
        connection.close()

    @staticmethod
    def insertPlayer(nick, password, games_counter):
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDB.INSERIR_JOGADOR.value, (nick, password, games_counter))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def getGamesCountInfo(nick):
        connection, cursor = PlayerDBCommands.connectDataBase()
        cursor.execute(PlayerDB.GET_GAME_COUNT_ID.value, (nick, ))
        game_count_id = cursor.fetchone()
        # print('game_count_id ->', game_count_id)

        cursor.close()
        connection.close()
        return GamesCountDB.getSpecificPlayerData(game_count_id)
        
    @staticmethod
    # def setGamePlayed(game: typing.Union[CompetitiveGamesNames, TimedGamesNames], nick, won:bool = False):
    def setGamePlayed(game, nick, won:bool = False):
        connection, cursor = PlayerDBCommands.connectDataBase()
        player_info = PlayerDBCommands.getGamesCountInfo(nick)
        player_id = player_info[0]
        sql = (
            f'UPDATE {GAMES_COUNT_TABLE} SET {game.name}_played = {game.name}_played + 1 ' + 
            (f', {game.name}_won = {game.name}_won + 1' if won else '') + 
            ' WHERE Player_id=?'
        )
        cursor.execute(sql, (player_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        return
    
if __name__ == '__main__':
    PlayerDBCommands.createDataBase()
    PlayerDBCommands.getAllPlayers()
    aa = PlayerDBCommands.getGamesCountInfo("521")