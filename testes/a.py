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

competitive_games = [game.value for game in CompetitiveGamesNames]
timed_games = [game.value for game in TimedGamesNames]
games_values = ''
for game in competitive_games:
    games_values = games_values + f'{game}_played INTEGER NOT NULL DEFAULT 0,'
    games_values = games_values + f'{game}_won INTEGER NOT NULL DEFAULT 0,'

for game in timed_games:
    games_values = games_values + (
        f'{game}_best_time INTEGER NOT NULL DEFAULT 0,'
            if game != timed_games[-1]
            else 
        f'{game}_best_time INTEGER NOT NULL DEFAULT 0'
    )
print(games_values)
TABLE_NAME = 'games'
CREATE_TABLE = (
        f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} '
        '('
        'Player_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        + games_values +
        ')'    
    )
print(CREATE_TABLE)