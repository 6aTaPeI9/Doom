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
        self.image_links = []
        self.picture = Image.open(r'game_map/textures/wall3.png')
        self.texture_scale = 2
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

    @lru_cache(maxsize=2048)
    def crop_image(self, width):
        return self.picture.crop((
            width,
            0,
            width + self.win_scale,
            128
        ))


    # @lru_cache(maxsize=1024)
    def get_image(self, width, height: int):
        img = self.crop_image(width)
        img = img.resize((self.win_scale, height))
        img = ImageTk.PhotoImage(img, Image.ANTIALIAS)
        return img


    def get_line_lenght(self, x1, y1, x2, y2):
        """
            Метод возвращает длину отрезка по двум точкам
        """
        return math.sqrt(abs((x2 - x1) ** 2 + (y2 - y1) ** 2))


    def redraw_evet(self):
        start_time = time.time()

        curent_angel = self.player.angle - self.player.fov // 2
        ray_len = 50

        xm = (self.player.pos_x // self.map.scale) * self.map.scale
        ym = (self.player.pos_y // self.map.scale) * self.map.scale

        self.image_links = []
        drawed_walls = []

        self.draw_mini_map()

        for ray in range(self.player.rays_count):
            cos_a = calc_cos(curent_angel) or 0.000001
            sin_a = calc_sin(curent_angel) or 0.000001

            # cos = y. cos(90...0, 0...270) >= 0
            # dx - смещение по горизонтали. Смотрим всегда на 1 блок вперед.
            # x_h - ближайшая точка пересечения на вертикальной оси.
            if cos_a >= 0:
                # Луч направлен право.
                dx = 1
                x_h = xm + self.map.scale
            else:
                # Луч направлен влево
                dx = -1
                x_h = xm

            cnt = 0
            for _ in range(0, self.map.scaled_width, self.map.scale):
                cnt += 1
                # Вычисляем гипотенузу по углу и прилегающему катету.
                deepth_h = (x_h - self.player.pos_x) / cos_a

                # ближайшая точка пересечения на горизонтальной оси
                y_h = self.player.pos_y + deepth_h * sin_a

                texture = self.map.check_barrier((x_h + dx), y_h, True, True)

                # При выходе за границы, прерываем цикл
                if y_h < 0 or y_h > self.map.scaled_height:
                    break

                # self.canvas.create_rectangle(
                #         (x_h + dx) // self.map.scale * self.map.scale * self.map.mm_w_scale + 10,
                #         y_h // self.map.scale * self.map.scale * self.map.mm_h_scale + 10,
                #         ((x_h + dx) // self.map.scale * self.map.scale * self.map.mm_w_scale) + self.map.ceil_width - 10,
                #         (y_h // self.map.scale * self.map.scale * self.map.mm_h_scale) + self.map.ceil_height - 10,
                #         fill='blue'
                # )

                # self.canvas.create_oval(
                #         *circl_coords(
                #             (x_h + dx) * self.map.mm_w_scale,
                #             y_h * self.map.mm_h_scale,
                #             7
                #         ),
                #         fill='white',
                #         outline=''
                # )

                if texture:
                    break

                x_h += (self.map.scale * dx)

            print('cnt: ', cnt)


            # sin = x. sin(0...180) >= 0
            # dy - смещение по вертикали. Смотрим всегда на 1 блок вперед.
            # y_v - ближайшая точка пересечения на горизонтальной оси.
            if sin_a < 0:
                # луч направлен вниз
                dy = -1
                y_v = ym
            else:
                # луч направлен вверх
                dy = 1
                y_v = ym + self.map.scale


            for _ in range(0, self.map.scaled_height, self.map.scale):
                if sin_a > 0:
                    pass

                # Вычисляем гипотенузу по углу и прилегающему катету.
                deepth_v = (y_v - self.player.pos_y) / sin_a

                # ближайшая точка пересечения на вертикальной оси
                x_v = self.player.pos_x + deepth_v * cos_a

                texture = self.map.check_barrier(x_v, (y_v + dx), True, True)

                # При выходе за границы, прерываем цикл
                if x_v < 0 or x_v > self.map.scaled_width:
                    break

                # self.canvas.create_rectangle(
                #         x_v // self.map.scale * self.map.scale * self.map.mm_w_scale + 10,
                #         (y_v + dy) // self.map.scale * self.map.scale * self.map.mm_h_scale + 10,
                #         (x_v // self.map.scale * self.map.scale * self.map.mm_w_scale) + self.map.ceil_width - 10,
                #         ((y_v + dy) // self.map.scale * self.map.scale * self.map.mm_h_scale) + self.map.ceil_height - 10,
                #         fill='red'
                # )

                self.canvas.create_oval(
                        *circl_coords(
                            x_v * self.map.mm_w_scale,
                            (y_v + dy) * self.map.mm_h_scale, 7
                        ),
                        fill='orange',
                        outline=''
                )

                if texture:
                    break


                y_v += (self.map.scale * dy)

            offset = 0

            if deepth_h < deepth_v:
                deepth, x, y = deepth_h, x_h, y_h
                offset = y_h
                prev_x = x_h
                prev_y = y_h + self.map.scale
            else:
                deepth, x, y = deepth_v, x_v, y_v
                offset = x_v
                prev_x = x_v + self.map.scale
                prev_y = y_v

            scale_x, scale_y = self.map.rescale_coord(x, y)

            self.canvas.create_oval(
                *circl_coords(
                    self.map.mm_start_x + scale_x // self.map.scale * self.map.scale * self.map.mm_w_scale,
                    self.map.mm_start_y + scale_y // self.map.scale * self.map.scale * self.map.mm_h_scale,
                    7
                ),
                fill='red',
                outline=''
            )

            self.canvas.create_line(
                self.map.mm_start_x + self.player.pos_x * self.map.mm_w_scale,
                self.map.mm_start_y + self.player.pos_y * self.map.mm_h_scale,
                self.map.mm_start_x + scale_x * self.map.scale * self.map.mm_w_scale,
                self.map.mm_start_y + scale_y * self.map.scale * self.map.mm_h_scale,
                fill='red'
            )

            scale_x_next, scale_y_next = self.map.rescale_coord(prev_x, prev_y)
            self.canvas.create_oval(
                *circl_coords(
                    self.map.mm_start_x + scale_x_next * self.map.scale * self.map.mm_w_scale,
                    self.map.mm_start_y + scale_y_next * self.map.scale * self.map.mm_h_scale,
                    7
                ),
                fill='red',
                outline=''
            )

            self.canvas.create_line(
                self.map.mm_start_x + self.player.pos_x * self.map.mm_w_scale,
                self.map.mm_start_y + self.player.pos_y * self.map.mm_h_scale,
                self.map.mm_start_x + scale_x_next * self.map.scale * self.map.mm_w_scale,
                self.map.mm_start_y + scale_y_next * self.map.scale * self.map.mm_h_scale,
                fill='red'
            )

            self.canvas.create_line(
                self.map.mm_start_x + self.player.pos_x * self.map.mm_w_scale,
                self.map.mm_start_y + self.player.pos_y * self.map.mm_h_scale,
                self.map.mm_start_x + self.player.pos_x * self.map.mm_w_scale + cos_a * deepth * self.map.mm_w_scale,
                self.map.mm_start_y + self.player.pos_y * self.map.mm_h_scale + sin_a * deepth * self.map.mm_h_scale,
                fill='gray'
            )

            # ------------------ Прямоугольники -------------------------

            # if (scale_x, scale_y) not in drawed_walls:
            #     drawed_walls.append((scale_x, scale_y))

            #     # Вычисляем длину прямой до правого угла стены
            #     right_deepth = self.get_line_lenght(self.player.pos_x, self.player.pos_y, scale_x * self.map.scale, scale_y * self.map.scale)

            #     # Вычисляем длину прямой до левого угла стены
            #     left_deepth = self.get_line_lenght(self.player.pos_x, self.player.pos_y, scale_x_next * self.map.scale, scale_y_next * self.map.scale)

            #     # Вычисляем длину прямой между левым и правым углом стены
            #     among_deepth = self.get_line_lenght(scale_x * self.map.scale, scale_y * self.map.scale, scale_x_next * self.map.scale, scale_y_next * self.map.scale)

            #     # Вычисляем угол по
            #     wall_degree = abs(((right_deepth ** 2) + (left_deepth ** 2) - (among_deepth ** 2)) / (2 * right_deepth * left_deepth))
            #     rel_degree = math.degrees(math.acos(wall_degree))

            #     wall_width = rel_degree / (self.player.fov / self.player.rays_count)

            #     # right_deepth *= calc_cos(self.player.angle - curent_angel)
            #     # left_deepth *= calc_cos(self.player.angle - curent_angel)

            #     right_side_height = max((3 * self.player.proj_dist * self.map.scale) / right_deepth, 0.00001)
            #     left_side_height = max((3 * self.player.proj_dist * self.map.scale) / left_deepth, 0.00001)

            #     # x1 - нижний левый
            #     # x2 - верхний правый
            #     # x3 - верхний правый
            #     # x4 - нижний праый

            #     if cos_a >= 0:
            #         if sin_a >= 0:
            #             wall_polygon = (
            #             ray * self.win_scale,
            #             (self.map.win_height // 2) - left_side_height // 2,

            #             ray * self.win_scale,
            #             (self.map.win_height // 2) - left_side_height // 2 + left_side_height,

            #             ray * self.win_scale + wall_width * self.win_scale,
            #             (self.map.win_height // 2) - right_side_height // 2 + right_side_height,

            #             ray * self.win_scale + wall_width * self.win_scale,
            #             (self.map.win_height // 2) - right_side_height // 2,
            #         )
            #         else:
            #             wall_polygon = (
            #                 ray * self.win_scale,
            #                 (self.map.win_height // 2) - right_side_height // 2,

            #                 ray * self.win_scale,
            #                 (self.map.win_height // 2) - right_side_height // 2 + right_side_height,

            #                 ray * self.win_scale + wall_width * self.win_scale,
            #                 (self.map.win_height // 2) - left_side_height // 2 + left_side_height,

            #                 ray * self.win_scale + wall_width * self.win_scale,
            #                 (self.map.win_height // 2) - left_side_height // 2,
            #             )
            #     else:
            #         if sin_a < 0:
            #             wall_polygon = (
            #             ray * self.win_scale,
            #             (self.map.win_height // 2) - left_side_height // 2,

            #             ray * self.win_scale,
            #             (self.map.win_height // 2) - left_side_height // 2 + left_side_height,

            #             ray * self.win_scale + wall_width * self.win_scale,
            #             (self.map.win_height // 2) - right_side_height // 2 + right_side_height,

            #             ray * self.win_scale + wall_width * self.win_scale,
            #             (self.map.win_height // 2) - right_side_height // 2,
            #         )
            #         else:
            #             wall_polygon = (
            #                 ray * self.win_scale,
            #                 (self.map.win_height // 2) - right_side_height // 2,

            #                 ray * self.win_scale,
            #                 (self.map.win_height // 2) - right_side_height // 2 + right_side_height,

            #                 ray * self.win_scale + wall_width * self.win_scale,
            #                 (self.map.win_height // 2) - left_side_height // 2 + left_side_height,

            #                 ray * self.win_scale + wall_width * self.win_scale,
            #                 (self.map.win_height // 2) - left_side_height // 2,
            #             )

            #     if texture:
            #         self.canvas.create_polygon(
            #             wall_polygon,
            #             fill=texture.color if type(texture) == Wall else 'white',
            #             outline=''
            #         )

            if texture:
                deepth *= calc_cos(self.player.angle - curent_angel)
                proj_height = max((3 * self.player.proj_dist * self.map.scale) / deepth, 0.00001)
                self.canvas.create_rectangle(
                    ray * self.win_scale,
                    (self.map.win_height // 2) - proj_height // 2,
                    ray * self.win_scale + self.win_scale,
                    (self.map.win_height // 2) - proj_height // 2 + proj_height,
                    fill=texture.color if type(texture) == Wall else 'gray',
                    outline=''
                )

            # ------------------ Текстуры -------------------------
            # texture_width = int((int(offset) % self.map.scale) * self.texture_scale)
            # self.image_links.append(self.get_image(texture_width, int(proj_height)))

            # self.canvas.create_image(
            #     (ray * self.win_scale, (self.map.win_height // 2) - proj_height // 2), anchor=NW, image=self.image_links[ray]
            # )

            curent_angel += (self.player.fov / self.player.rays_count)

        self.canvas.create_text(
            self.map.win_width - 25,
            5,
            text=str(int(1 / ((time.time() - start_time) or 0.0001))),
            fill='red'
        )
