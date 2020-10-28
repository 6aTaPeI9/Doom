"""
    Модуль содержит реализацию класса игрока
"""

from tools import calc_cos, calc_sin, calc_tan
from player.direction import Step, Rotate

class Player:
    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        speed: int,
        rotation_speed: int,
        view_range: int,
        fov: int,
        angle: int
    ):
        """
            Инциализация нового игрока
        """
        self.speed = speed
        self.angle = angle
        self.fov = fov
        self.view_range = fov
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rotation_speed = rotation_speed
        self.rays_count = 20 # TODO Вынести куда нибудь
        self.proj_dist = self.rays_count / (2 * calc_tan(self.fov / 2)) # TODO Вынести куда нибудь


    def get_position(self):
        """
            Кортеж с позицией игрока на карте
        """
        return (self.pos_x, self.pos_y)


    def make_step(self, direction):
        """
            Метод для просчета следующей позиции персонажа
        """
        if direction == Step.STRAIGHT:
            step = self.speed
        elif direction == Step.BACK:
            step = self.speed * -1
        # else:
        #     raise NotImplementedError(f'Движение в сторону {direction} невозможно.')

        step_x = calc_cos(self.angle) * step
        step_y = calc_sin(self.angle) * step

        return (self.pos_x + step_x, self.pos_y + step_y)

    
    def confirm_step(self, step_x, step_y):
        """
            Метод для подтверждения шага и изменения координат
        """
        self.pos_x = step_x
        self.pos_y = step_y

    def rotate(self, rotate_side: Rotate):
        """
            Метод для поворота взгляда
        """
        if rotate_side == Rotate.LEFT:
            self.angle -= self.rotation_speed
        elif rotate_side == Rotate.RIGHT:
            self.angle += self.rotation_speed
        # else:
        #     raise NotImplementedError(f'Изменение направления взгляда в сторону {rotate_side} невозможно.')

    def resize(self):
        pass
