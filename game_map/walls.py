"""
    Модуль содержит описание статических обьектов на карте
"""

class CeillType:
    EMPTY = '.'
    WALL = '#'
    RED_WALL = '@'


class Wall:
    TEXT_VIEW = CeillType.WALL

    def __init__(self, color: str):
        self.color = color

    def __str__(self):
        return self.TEXT_VIEW

    def __repr(self):
        return self.TEXT_VIEW
