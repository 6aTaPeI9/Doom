import time
import math

from tkinter import Canvas, Tk, Frame, BOTH, YES, ALL, PhotoImage, Label, NW
from config import *
from tools import *
from map_static import MAP
from PIL import ImageTk, Image
from collections import deque

class CeillType:
    EMPTY = '.'
    WALL = '#'
    RED_WALL = '@'


class GameCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.bind("<KeyPress>", self.key_pressed)

        # Масштабированная размеры карты.
        self.scaled_width = len(MAP[0]) * SCALE
        self.scaled_height = len(MAP) * SCALE

        # Заполняем параметры при инициализации размеров окна
        self.on_resize(None)

        self.focus_set()
        self.map = MAP
        self.view_degree = START_VIEW_DEGREE
        self.view_range = DEFAULT_FOV

        # Стартовая позиция игрока
        self.center_x = 150
        self.center_y = 150


    def key_pressed(self, event):
        if event.char == 'a':
            self.view_degree -= VIEW_STEP
        elif event.char == 'd':
            self.view_degree += VIEW_STEP
        elif event.char == 's':
            self.step_straight(-STEP)
        elif event.char == 'w':
            self.step_straight(STEP)

        self.drawing_loop()


    def step_straight(self, step: int):
        step_x = calc_cos(self.view_degree) * step
        step_y = calc_sin(self.view_degree) * step

        if self.map[int(self.center_y + step_y) // SCALE][int(self.center_x + step_x) // SCALE] == CeillType.EMPTY:
            self.center_x += step_x
            self.center_y += step_y


    def draw_mini_map(self):
        # не масштабированные размеры карты
        map_height = len(self.map)
        map_width = len(self.map[0])

        # размеры мини-карты
        mini_map_widht = self.width * MINI_MAP_SCALE
        mini_map_height = self.height * MINI_MAP_SCALE

        # Размеры одной клетки мини-карты
        # ceil_width = mini_map_widht / map_width
        # ceil_height = mini_map_height / map_height
        ceil_width = SCALE
        ceil_height = SCALE

        # Точка от которой будет рисоваться миникарта
        start_y = self.height - mini_map_height
        start_x = 0

        # Смещение каждой клетки по ширине и высотке
        ceil_dx = ceil_width + start_x
        ceil_dy = ceil_height + start_y

        for idy, row in enumerate(self.map):
            ceil_y = idy * ceil_dy
            self.create_line(
                    start_x,
                    ceil_y,
                    0 + mini_map_widht,
                    ceil_y,
                    fill='green'
                )
            for idx, ceil in enumerate(row):
                ceil_x = idx * ceil_dx
                self.create_line(
                    ceil_x,
                    ceil_y,
                    ceil_x,
                    ceil_y + mini_map_height,
                    fill='green'
                )

                if ceil == CeillType.EMPTY:
                    continue
                elif ceil == CeillType.WALL:

                    # Верняя левая точка клетки
                    self.create_rectangle(
                        ceil_x,
                        ceil_y,
                        ceil_x + ceil_width,
                        ceil_y + ceil_height,
                        fill='white'
                    )

        # Рисуем границу мини-карты
        self.create_rectangle(
            start_x,
            start_y,
            start_x + mini_map_widht,
            start_y + mini_map_height
        )

        mini_map_pos_x = int(start_x + (self.center_x * self.scale_width_coeff * MINI_MAP_SCALE))
        mini_map_pos_y = int(start_y + (self.center_y * self.scale_height_coeff * MINI_MAP_SCALE))
        avg_degree = self.view_degree

        self.create_line(
            mini_map_pos_x,
            mini_map_pos_y,
            mini_map_pos_x + calc_cos(avg_degree) * (VIEW_RADIUS * self.scale_width_coeff * MINI_MAP_SCALE),
            mini_map_pos_y + calc_sin(avg_degree) * (VIEW_RADIUS * self.scale_width_coeff * MINI_MAP_SCALE),
            fill='white'
        )


    def redraw_evet(self):
        start_time = time.time()
        self.draw_mini_map()

        # sin - лево/право
        # cos - верх/низ

        curent_angel = self.view_degree - DEFAULT_FOV // 2
        ray_len = 50
        circl_radius = 2
        
        xm = (self.center_x // SCALE) * SCALE
        ym = (self.center_y // SCALE) * SCALE

        for ray in range(RAYS_COUNT):
            cos_a = calc_cos(curent_angel)
            sin_a = calc_sin(curent_angel)

            x = cos_a * ray_len
            y = sin_a * ray_len

            if cos_a > 0:
                x_dx = 1
                near_x = xm + SCALE
            else:
                x_dx = -1
                near_x = xm

            for i in range(3):
                vert_dist = abs(self.center_x - near_x)
                x_dy = self.center_y + vert_dist * calc_tan(curent_angel) * x_dx
                self.create_oval(
                    near_x - circl_radius,
                    x_dy - circl_radius,
                    near_x + circl_radius,
                    x_dy + circl_radius,
                    fill='white'
                )
                near_x += SCALE

            # horiz_dist = self.center_y - near_y

            # if sin_a > 0:
            #     y_dx = 1
            #     near_y = ym + SCALE
            # else:
            #     y_dx = -1
            #     near_y = ym

            # self.create_oval(
            #     self.center_x * self.scale_width_coeff - circl_radius,
            #     near_y * self.scale_height_coeff - circl_radius,
            #     self.center_x * self.scale_width_coeff + circl_radius,
            #     near_y * self.scale_height_coeff + circl_radius,
            #     fill='white'
            # )


            self.create_line(
                self.center_x,
                self.center_y,
                self.center_x + x,
                self.center_y + y,
                fill='red'
            )

            curent_angel += RAY_FREQ

        self.create_text(
            self.width - 25,
            5,
            text=str(int(1 / ((time.time() - start_time) or 0.0001))),
            fill='red'
        )

    def drawing_loop(self):
        self.delete(ALL)
        self.redraw_evet()
        # self.after(1, self.drawing_loop)


    def on_resize(self, event):
        """
            Метод обработки изменения размеров экрана
        """
        if event:
            self.width = event.width
            self.height = event.height
        else:
            self.height = self.winfo_reqheight()
            self.width = self.winfo_reqwidth()

        self.config(width=self.width, height=self.height)

        # Отношение масштабированного размера карты к размеру экрана
        self.scale_width_coeff = 1
        self.scale_height_coeff = 1


if __name__ == '__main__':
    root = Tk()
    myframe = Frame(root)
    myframe.pack(fill=BOTH, expand=YES)
    canvas = GameCanvas(
        myframe,
        width=MIN_SCREEN_WIDTH,
        height=MIN_SCREEN_HEIGHT,
        bg='black',
        highlightthickness=0
    )
    canvas.pack(fill=BOTH, expand=YES)
    canvas.after(500, canvas.drawing_loop)
    root.mainloop()