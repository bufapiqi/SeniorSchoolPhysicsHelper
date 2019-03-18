""" 一个basic线的model，每一个实例都是pymunk空间中的一个线实体，可以在直接调用draw方法来画自己
"""
import sys

import pygame
import pymunk
from pygame.constants import QUIT

from model.ball import Ball
from model.game_model import GameModel
from util.math_util import coordinates_transform
from util.Vector2D import Vec2d


class Line(GameModel):
    def __init__(self, center_point: tuple, a_point: tuple, b_point: tuple, line_width: int,
                 friction: int = 0, is_static: bool = False, event=None):
        self.__center_point = center_point
        # a_point和b_point均为center_point的相对位置
        self.__a_point = a_point
        self.__b_point = b_point
        self.__line_width = line_width
        self.__friction = friction
        self.__is_static = is_static
        self.__body = None
        self.__line = None
        self.__event = None

    def create_line_in_space(self):
        if self.__is_static:
            self.__body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            self.__body = pymunk.Body()
        self.__body.position = coordinates_transform(self.__center_point)
        self.__line = pymunk.Segment(self.__body, self.__a_point,
                                     self.__b_point, self.__line_width)
        self.__line.friction = self.__friction

    def is_created(self):
        return self.__body is not None

    def draw_line(self, screen, color):
        # pv1 = self.__body.position + self.__line.a.rotated(self.__body.angle)
        # pv2 = self.__body.position + self.__line.b.rotated(self.__body.angle)
        lx = int(self.__body.position.x)
        ly = screen.get_height()-int(self.__body.position.y)
        pv1 = lx + self.__a_point[0], ly + self.__a_point[1]
        pv2 = lx + self.__b_point[0], ly + self.__b_point[1]
        pygame.draw.line(screen, color, pv1, pv2, self.__line_width)

    @property
    def body(self):
        return self.__body

    @property
    def line(self):
        return self.__line

    @property
    def friction(self):
        return self.__fraction

    @friction.setter
    def friction(self, friction: int):
        self.__friction = friction

    @property
    def center_point(self):
        return self.__center_point

    @center_point.setter
    def center_point(self, p: tuple):
        self.__center_point = p

    @property
    def a_point(self):
        return self.__a_point

    @a_point.setter
    def a_point(self, p: tuple):
        self.__a_point = p

    @property
    def b_point(self):
        return self.__b_point

    @b_point.setter
    def b_point(self, p: tuple):
        self.__b_point = p


    def body_clicked(self, event) -> bool:
        if event is None:
            return False
        else:
            point_x, point_y = event.pos
        lx, ly = self.center_point
        start = lx + self.__a_point[0], ly + self.__a_point[1]
        end = lx + self.__b_point[0], ly + self.__b_point[1]
        # 首先判断是否被点选
        if start[0] == end[0]:
            in_x = start[0] - 2 < point_x < start[0] + 2
            in_y = start[1] < point_y < end[1] if start[1] < end[1] else end[1] < point_y < start[1]
        else:
            k = (start[1] - end[1]) / (start[0] - end[0])
            b = (start[0] * end[1] - start[1] * end[0]) / (start[0] - end[0])
            in_x = start[0] < point_x < end[0] if start[0] < end[0] else end[0] < point_x < start[0]
            in_y = k * point_x + b - 2 < point_y < k * point_x + b + 2
        return in_x and in_y


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()  # 创建一个对象来帮助跟踪时间
    space = pymunk.Space()  # 2  创建一个space， space是模拟的基本单位，可以在space上添加bodies,shapes,和joints
    space.gravity = (0.0, -900.0)  # 设置 space的重力

    line = Line((5, 5), (1, 1), (9, 9), 2)
    line.create_line_in_space()
    space.add(line.body, line.line)
    ball = Ball(1, 3, 50, (100, 100))
    ball.create_ball_in_space()
    space.add(ball.body, ball.shape)
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        ball.draw_ball(screen, (255, 0, 0), 1)
        line.draw_line(screen, (255, 0, 0))
        space.step(1 / 50.0)  # 3
        pygame.display.flip()
        clock.tick(50)
