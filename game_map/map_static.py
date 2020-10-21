"""
    Модуль содержащий статическое описание карты.
"""
from game_map.walls import Wall

MAP = [
    [Wall('red'), Wall('blue'), Wall('orange'), Wall('yellow'), Wall('green')],
    [Wall('pink'), '.', '.', '.', Wall('purple')],
    [Wall('pink1'), '.', '.', '.', Wall('purple1')],
    [Wall('red'), Wall('blue'), Wall('orange'), Wall('yellow'), Wall('green')]
]
