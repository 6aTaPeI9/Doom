"""
    Модуль содержит обьект игрового поля
"""

from game_map.walls import CeillType
from player.player import Player

class GameField:
    def __init__(self, map: list, scale: int, mini_map_scale: int):
        """
            Инициализация игрового поля
        """
        self.map = map
        self.map_set = set()
        self.scale = scale

        # Масштабированная размеры карты
        self.scaled_width = len(self.map[0]) * self.scale
        self.scaled_height = len(self.map) * self.scale

        self.rel_width = len(self.map[0])
        self.rel_height = len(self.map)

        self.mm_scale = mini_map_scale
        self._generate_map_set()


    def _generate_map_set(self) -> None:
        """
            Метод генерирует сет из всех стен карты
        """
        for row_id, row in enumerate(self.map):
            for ceil_id, ceil in enumerate(row):
                if not str(ceil) == CeillType.WALL:
                    continue

                self.map_set.add((ceil_id, row_id))

        return


    def player_step(self, player: Player, direct):
        """
            Валидация перемещения игрока
        """
        next_pos = player.make_step(direct)
        br = self.check_barrier(*next_pos)

        if not br:
            player.confirm_step(*next_pos)

        return


    def rescale_coord(self, x, y):
        """
            Приведение переданных координат к реальным размерам карты
        """
        return (int(x // self.scale), int(y // self.scale))


    def check_barrier(self, x, y, scale: bool = True, with_val: bool = False):
        """
            Проверка координат на наличие препятствия
        """
        if scale:
            x, y = self.rescale_coord(x, y)

        if (x, y) == (4, 1):
            pass

        val = (x, y) in self.map_set

        if with_val and val:
            return self.map[y][x]
        else:
            return bool(val)


    def resize(self, win_width, win_height):
        """
            Метод пересчитывает параметры зависящие от размера окна
        """
        self.win_width = win_width
        self.win_height = win_height

        self.mm_widht = self.win_width * self.mm_scale
        self.mm_height = self.win_height * self.mm_scale

        self.ceil_width = self.mm_widht / self.rel_width
        self.ceil_height = self.mm_height / self.rel_height

        # Точка от которой будет рисоваться миникарта
        self.mm_start_y = self.win_height - self.mm_height
        self.mm_start_x = 0

        self.mm_w_scale = (self.win_width / self.scaled_width) * self.mm_scale
        self.mm_h_scale = (self.win_height / self.scaled_height) * self.mm_scale
