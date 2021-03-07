"""
    Модуль содрежит основной обьект для рендера
"""

import time
import math

from functools import lru_cache
from tkinter import NW
from PIL import ImageTk, Image
from tools import calc_cos, calc_sin, circl_coords
from game_map.walls import CeillType, Wall


class Camera:
    def __init__(self, game_obj):
        self.map = game_obj.map
        self.canvas = game_obj
        self.player = game_obj.player
        self.win_scale = int(self.map.win_width / self.player.rays_count)


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
                elif str(ceil) == CeillType.WALL:
                    # Верняя левая точка клетки
                    self.canvas.create_rectangle(
                        ceil_x,
                        ceil_y,
                        ceil_x + self.map.ceil_width,
                        ceil_y + self.map.ceil_height,
                        fill=ceil.color if type(ceil) == Wall else 'white',
                        outline=''
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


    def get_line_lenght(self, x1, y1, x2, y2):
        """
            Метод возвращает длину отрезка по двум точкам
        """
        return math.sqrt(abs((x2 - x1) ** 2 + (y2 - y1) ** 2))


    def redraw_evet(self):
        start_time = time.time()

        self.canvas.create_rectangle(0, 0, self.map.win_width, self.map.win_height // 2, fill='green')
        self.canvas.create_rectangle(0, self.map.win_height // 2, self.map.win_width, self.map.win_height, fill='gray')

        curent_angel = self.player.angle - self.player.fov // 2
        ray_len = 50

        xm = (self.player.pos_x // self.map.scale) * self.map.scale
        ym = (self.player.pos_y // self.map.scale) * self.map.scale

        self.image_links = []
        drawed_walls = []


        for ray in range(self.player.rays_count):
            cos_a = calc_cos(curent_angel) or 0.000001
            sin_a = calc_sin(curent_angel) or 0.000001

            x = cos_a * ray_len
            y = sin_a * ray_len

            if cos_a >= 0:
                # луч направлен влево
                dx = 1
                # X по горизонтали
                x_h = xm + self.map.scale
            else:
                # луч направлен вправо
                dx = -1
                x_h = xm

            for i in range(0, self.map.scaled_width, self.map.scale):
                # Вычисляем расстояние луча до ближайшего пересечения
                deepth_h = (x_h - self.player.pos_x) / cos_a
                y_h = self.player.pos_y + deepth_h * sin_a

                if self.map.check_barrier((x_h + dx), y_h, True):
                    break

                x_h += (self.map.scale * dx)


            if sin_a >= 0:
                # луч направлен вверх
                dy = 1
                # X по горизонтали
                y_v = ym + self.map.scale
            else:
                # луч направлен вниз
                dy = -1
                y_v = ym

            for i in range(0, self.map.scaled_height, self.map.scale):
                # Расстояние до ближайшей вертикальной стены и пересечение лучем вертикальной стены по y
                deepth_v = (y_v - self.player.pos_y) / sin_a
                x_v = self.player.pos_x + deepth_v * cos_a

                if self.map.check_barrier(x_v, (y_v + dy), True):
                    break

                y_v += (self.map.scale * dy)

            deepth = deepth_h if deepth_h < deepth_v else deepth_v
            deepth *= calc_cos(self.player.angle - curent_angel)
            proj_height = max((3 * self.player.proj_dist * self.map.scale) / deepth, 0.00001)

            win_scale = self.map.win_width / self.player.rays_count

            color = int(255 // (1 + deepth * deepth * 0.0001))

            self.canvas.create_rectangle(
                ray * win_scale,
                (self.map.win_height // 2) - proj_height // 2,
                ray * win_scale + win_scale,
                (self.map.win_height // 2) - proj_height // 2 + proj_height,
                fill="#%02x%02x%02x" % (color, color, color),
                outline=''
            )

            curent_angel += self.player.fov / self.player.rays_count
        self.draw_mini_map()

        self.canvas.create_text(
            self.map.win_width - 25,
            5,
            text=str(int(1 / ((time.time() - start_time) or 0.0001))),
            fill='red'
        )


