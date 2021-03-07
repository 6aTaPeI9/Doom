"""
    Модуль содержащий статическое описание карты.
"""
from game_map.walls import Wall


MAP_TMPL = [
    'wwwwwwwwwwww',
    'w..w....w..w',
    'w..w.......w',
    'w..w.......w',
    'w..w....w..w',
    'w..w.......w',
    'w.....w....w',
    'w..........w',
    'w..w....w..w',
    'w..........w',
    'wwwwwwwwwwww',
]

MAP = []

for row in MAP_TMPL:
    wall_line = []
    for ceil in list(row):
        if ceil == 'w':
            wall_line.append(Wall('white'))
        else:
            wall_line.append('.')

    MAP.append(wall_line)
