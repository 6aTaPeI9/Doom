from tkinter import Canvas, Tk, Frame, BOTH, YES, ALL
from config import *

from camera.camera import Camera

from player.player import Player
from player.direction import Step, Rotate
from player import player_config

from game_map import map_config
from game_map.game_field import GameField
from game_map.map_static import MAP

class Game(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.bind("<KeyPress>", self.key_pressed)

        self.focus_set()

        # Создаем карту
        self.map = GameField(MAP, map_config.SCALE, map_config.MINI_MAP_SCALE)

        # Заполняем параметры при инициализации размеров окна
        self.on_resize(None)

        self.player = Player(
            101,
            125,
            player_config.SPEED,
            player_config.ROTATION_SPEED,
            player_config.VIEW_RANGE,
            player_config.FOV,
            player_config.ANGLE
        )

        # Создаем камеру
        self.camera = Camera(self)


    def key_pressed(self, event):
        """
            Обработчик клавиш.
        """
        if event.char == 'a':
            self.player.rotate(Rotate.LEFT)

        elif event.char == 'd':
            self.player.rotate(Rotate.RIGHT)

        elif event.char == 's':
            self.map.player_step(self.player, Step.BACK)

        elif event.char == 'w':
            self.map.player_step(self.player, Step.STRAIGHT)


    def drawing_loop(self):
        self.delete(ALL)
        self.camera.redraw_evet()
        self.after(1, self.drawing_loop)


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

        # Пересчитываем все параметры карты зависящие от размеров окна
        self.map.resize(self.width, self.height)


if __name__ == '__main__':
    root = Tk()
    myframe = Frame(root)
    myframe.pack(fill=BOTH, expand=YES)
    canvas = Game(
        myframe,
        width=MIN_SCREEN_WIDTH,
        height=MIN_SCREEN_HEIGHT,
        bg='black',
        highlightthickness=0
    )
    canvas.pack(fill=BOTH, expand=YES)
    canvas.after(500, canvas.drawing_loop)
    root.mainloop()