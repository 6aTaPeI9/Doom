"""
    Модуль содержит вспомогательные инструменты
"""

import math
from functools import lru_cache


def frange(start, stop=None, step=None):
    """
        Аналог встроенного метода <range>, но
        для вещественных чисел
    """
    start = float(start)
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0

    count = 0
    while True:
        temp = float(start + count * step)
        if step > 0 and temp >= stop:
            break
        elif step < 0 and temp <= stop:
            break
        yield temp
        count += 1


def circl_coords(x: int, y: int, diagonal: int) -> tuple:
    """
        Метод вовзвращает координаты круга с заданной
        начальной точкой и диагональю
    """
    half_diagonal = diagonal // 2
    return (x - half_diagonal, y - half_diagonal, x + half_diagonal, y + half_diagonal)


@lru_cache(maxsize=2048)
def calc_sin(degree):
    return math.sin(math.radians(degree))

@lru_cache(maxsize=2048)
def calc_cos(degree):
    return math.cos(math.radians(degree))

@lru_cache(maxsize=2048)
def calc_tan(degree):
    return math.tan(math.radians(degree))
