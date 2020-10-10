"""
    Модуль содрежит основной обьект для рендера
"""

import time

from PIL import ImageTk, Image
from tools import calc_cos, calc_sin
from game_map.walls import CeillType


class Camera:
    def __init__(self, game_obj):
        self.map = game_obj.map
        self.canvas = game_obj
        self.player = game_obj.player


    def draw_mini_map(self):
        """
            Метод отрисовывает миникарту
        """
        for idy, row in enumerate(self.map.map):
            ceil_y = self.map.mm_start_y + idy * self.map.ceil_height
            self.canvas.create_line(
                    self.map.mm_start_x,
                    ceil_y,
                    0 + self.map.mm_widht,
                    ceil_y,
                    fill='green'
                )
            for idx, ceil in enumerate(row):
                ceil_x = self.map.mm_start_x + idx * self.map.ceil_width
                self.canvas.create_line(
                    ceil_x,
                    ceil_y,
                    ceil_x,
                    ceil_y + self.map.mm_height,
                    fill='green'
                )

                if ceil == CeillType.EMPTY:
                    continue
                elif ceil == CeillType.WALL:
                    # Верняя левая точка клетки
                    self.canvas.create_rectangle(
                        ceil_x,
                        ceil_y,
                        ceil_x + self.map.ceil_width,
                        ceil_y + self.map.ceil_height,
                        fill='white'
                    )

        # Рисуем границу мини-карты
        self.canvas.create_rectangle(
            self.map.mm_start_x,
            self.map.mm_start_y,
            self.map.mm_start_x + self.map.mm_widht,
            self.map.mm_start_y + self.map.mm_height,
            # fill='red'
        )

        mini_map_pos_x = int(self.map.mm_start_x + (self.player.pos_x * self.map.mm_w_scale))
        mini_map_pos_y = int(self.map.mm_start_y + (self.player.pos_y * self.map.mm_h_scale))
        avg_degree = self.player.angle

        self.canvas.create_line(
            mini_map_pos_x,
            mini_map_pos_y,
            mini_map_pos_x + calc_cos(avg_degree) * (self.player.view_range * self.map.mm_w_scale),
            mini_map_pos_y + calc_sin(avg_degree) * (self.player.view_range * self.map.mm_h_scale),
            fill='red'
        )


    def redraw_evet(self):
        start_time = time.time()

        # # sin - лево/право
        # # cos - верх/низ

        # # curent_angel = self.view_degree - DEFAULT_FOV // 2
        # ray_len = 50
        # circl_radius = 2

        # xm = (self.center_x // SCALE) * SCALE
        # ym = (self.center_y // SCALE) * SCALE

        # ceils = []

        # for ray in range(RAYS_COUNT):
        #     cos_a = calc_cos(curent_angel) or 0.000001
        #     sin_a = calc_sin(curent_angel) or 0.000001


        #     x = cos_a * ray_len
        #     y = sin_a * ray_len

        #     if cos_a >= 0:
        #         # луч направлен вверх
        #         dx = 1
        #         # X по горизонтали
        #         x_h = xm + SCALE
        #     else:
        #         # луч направлен вниз
        #         dx = -1
        #         x_h = xm

        #     for i in range(0, self.scaled_width, SCALE):
        #         deepth_h = (x_h - self.center_x) / cos_a
        #         y_h = self.center_y + deepth_h * sin_a

        #         if ((x_h + dx) // SCALE, y_h // SCALE) in self.map_set:
        #             break

        #         # self.canvas.create_oval(
        #         #     x_h - circl_radius,
        #         #     y_h - circl_radius,
        #         #     x_h + circl_radius,
        #         #     y_h + circl_radius,
        #         #     fill='red'
        #         # )
        #         x_h += (SCALE * dx)


        #     if sin_a >= 0:
        #         # луч направлен вверх
        #         dy = 1
        #         # X по горизонтали
        #         y_v = ym + SCALE
        #     else:
        #         # луч направлен вниз
        #         dy = -1
        #         y_v = ym

        #     for i in range(0, self.scaled_height, SCALE):
        #         # Расстояние до ближайшей вертикальной стены и пересечение лучем вертикальной стены по y
        #         deepth_v = (y_v - self.center_y) / sin_a
        #         x_v = self.center_x + deepth_v * cos_a

        #         if (x_v // SCALE, (y_v + dy) // SCALE) in self.map_set:
        #             break

        #         # self.canvas.create_oval(
        #         #     x_v - circl_radius,
        #         #     y_v - circl_radius,
        #         #     x_v + circl_radius,
        #         #     y_v + circl_radius,
        #         #     fill='red'
        #         # )

        #         y_v += (SCALE * dy)

        #     deepth = deepth_h if deepth_h < deepth_v else deepth_v

        #     self.canvas.create_line(
        #         self.center_x,
        #         self.center_y,
        #         self.center_x + deepth * cos_a,
        #         self.center_y + deepth * sin_a,
        #         fill='red'
        #     )

        #     curent_angel += RAY_FREQ

        self.draw_mini_map()

        self.canvas.create_text(
            self.map.win_width - 25,
            5,
            text=str(int(1 / ((time.time() - start_time) or 0.0001))),
            fill='red'
        )