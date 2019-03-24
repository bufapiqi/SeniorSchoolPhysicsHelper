""" 一个basic凸多边形的model，每一个实例都是pymunk空间中的一个凸多边形实体，可以在直接调用draw方法来画自己
"""
import sys

import pygame
import pymunk
from pygame.constants import QUIT
from pymunk import Vec2d

from model.game_model import GameModel
from util.math_util import coordinates_transform
COLLTYPE_DEFAULT = 0


class Poly(GameModel):
    def __init__(self, mass: int, centroid: tuple, poly_points: list, poly_fraction: float=0,
                 moment: int=None, is_static: bool=False):
        self.__mass = mass
        self.__centroid = centroid
        self.__poly_points: list = poly_points
        self.__poly_fraction = poly_fraction
        self.__moment = moment
        self.__is_static = is_static
        self.__body = None
        self.__shape = None
        self.create_poly_in_space()

    def create_poly_in_space(self):
        if self.__moment is None:
            self.__moment = pymunk.moment_for_poly(self.__mass, self.__poly_points)
        self.__body = pymunk.Body(self.__mass, self.__moment, body_type=self.__is_static)
        # transfer_list = []
        # for i in self.__poly_points:
        #     transfer_list.append(coordinates_transform(i))
        #  todo poly 都是根据centroid来确定的 shape 的吗？？ 找时间确定一下
        self.__body.position = Vec2d(coordinates_transform(self.__centroid))
        self.__shape = pymunk.Poly(self.__body, self.__poly_points)
        self.__shape.friction = self.__poly_fraction
        self.__shape.collision_type = COLLTYPE_DEFAULT

    # 返回一个已经创建好body和shape的四边形
    @staticmethod
    def create_box_with_centroid(centroid: tuple, width: int, height: int, mass: int, moment: int=None,
                                 fraction: float=0, is_static: bool=False):
        poly = Poly(mass, centroid, [(-width, -height), (-width, height), (width, height), (width, -height)],
                    fraction, moment, is_static=is_static)
        return poly

    def is_created(self):
        return self.__body is not None

    def draw_poly(self, screen, poly_color, width=0):  # width=0代表填充整个多边形区域
        points = []
        for i in self.__poly_points:
            temp_x = self.__body.position.x + i[0]
            temp_y = screen.get_height() - self.__body.position.y + i[1]
            points.append((temp_x, temp_y))
        pygame.draw.polygon(screen, poly_color, points, width)

    @property
    def body(self):
        return self.__body

    @property
    def shape(self):
        return self.__shape

    @property
    def mass(self):
        return self.__mass

    @property
    def centroid(self):
        return self.__centroid

    @property
    def poly_points(self):
        return self.__poly_points

    @property
    def poly_fraction(self):
        return self.__poly_fraction

    @property
    def moment(self):
        return self.moment

    def body_clicked(self, event) -> bool:
        # 均为实际长宽的一半
        print(self.poly_points)
        print("polygon is clicked!")
        width, height = self.poly_points[2]
        position = self.__body.position
        center_x, center_y = position.x, 600 - position.y
        pos_x, pos_y = event.pos
        in_x = (center_x-width) < pos_x < (center_x+width)
        in_y = (center_y-height) < pos_y < (center_y+height)
        return in_x and in_y


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()  # 创建一个对象来帮助跟踪时间
    space = pymunk.Space()  # 2  创建一个space， space是模拟的基本单位，可以在space上添加bodies,shapes,和joints
    space.gravity = (0.0, -900.0)  # 设置 space的重力
    COUNT = pygame.USEREVENT + 1
    # 调整画图间隔时间
    pygame.time.set_timer(COUNT, 500)

    poly = Poly.create_box_with_centroid((150, 150), 20, 10, 10, None, 0)
    space.add(poly.body, poly.shape)

    counts = 0
    moving = False
    clicked = []

    while True:
        screen.fill((255, 255, 255))  # 越后面添加上去的 越在画布的上面
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:  # 获取点击鼠标事件
                if event.button == 1:  # 点击鼠标左键
                    counts = 0
                    moving = True
            if event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if event.button == 1:  # 松开鼠标左键
                    moving = False
                    print(counts)
                    if counts <= 2:
                        if poly.body_clicked(event):
                            if poly in clicked:
                                clicked.remove(poly)
                            else:
                                if len(clicked) > 0:
                                    clicked.clear()
                                    clicked.append(poly)

            if moving and event.type == COUNT:
                counts += 1
        if poly in clicked:
            poly.draw_poly(screen, (255, 255, 0), 2)
        else:
            poly.draw_poly(screen, (255, 0, 0), 2)
        space.step(1 / 50.0)  # 3
        pygame.display.flip()
        clock.tick(50)

