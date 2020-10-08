"""
    Модуль содержит константные параметры
"""

import math

MIN_SCREEN_WIDTH = 600
MIN_SCREEN_HEIGHT = 400

# Угол обзора(в градусах)
DEFAULT_FOV = 60

# Стартовый угол под которым повернута камера(в градусах)
START_VIEW_DEGREE = 0

# Множитель стандартной координатной сетки.
# Используется только для обьектов отличных от игрока.
SCALE = 30

# Размер миникарты 1/5 от общего размера
MINI_MAP_SCALE = 1

# Длина видимости
VIEW_RADIUS = 300

# Частота бросания лучшей.
RAY_FREQ = 0.05

MAX_POINTS = VIEW_RADIUS // SCALE

# Кол-во бросаемых лучей в области видимости
RAYS_COUNT = int(DEFAULT_FOV // RAY_FREQ)

RAY_ANGLE = DEFAULT_FOV

# Шаг поворота камеры
VIEW_STEP = 4

# Длина шага вперед/назад
STEP = 10