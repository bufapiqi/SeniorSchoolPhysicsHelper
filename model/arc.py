""" 一个弧线的model，每一个实例都是pymunk空间中的一个弧线实体，可以在直接调用draw方法来画自己
"""
import sys

import pygame
import pymunk
import math
import pymunk.autogeometry
from pygame.constants import QUIT

from model.game_model import GameModel
from util.math_util import one_dot_round, coordinates_transform


class Arc(GameModel):
    def __init__(self, start_point: tuple, end_point: tuple, fraction: int = 0, is_up: bool = True,
                 is_right: bool = True):
        # is_position --> True 弧线朝向向右，反之向左
        self.__start_point = start_point
        self.__end_point = end_point
        self.__fraction = fraction
        self.__is_up = is_up
        self.__is_right = is_right
        self.__points = []
        self.__shapes = []

    def create_arc_in_space(self):
        centroid_x, centroid_y = Arc.__get_centroid(self.__start_point, self.__end_point, self.__is_up, self.__is_right)
        radius = abs(self.__start_point[0] - self.__end_point[0])
        line_set = pymunk.autogeometry.PolylineSet()
        self.__points = Arc.__caculate_coordinates(self.__points, 1, radius, (centroid_x, centroid_y))
        # 通过sin，cos计算弧线的坐标，第二个参数为步长
        for i in range(len(self.__points) - 1):
            v0 = self.__points[i]
            v1 = self.__points[i + 1]
            line_set.collect_segment(v0, v1)
        for line in line_set:
            line = Arc.round_point(pymunk.autogeometry.simplify_curves(line, .7))  # 平滑曲线上
            pygame_coordinate = []
            for i in line:
                py_x, py_y = coordinates_transform(i)  # 把pymunk的坐标转换成pygame的坐标系
                pygame_coordinate.append((py_x, py_y))
            self.__points = line
            for i in range(len(pygame_coordinate) - 1):
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                shape = pymunk.Segment(body, pygame_coordinate[i], pygame_coordinate[i + 1], 1)
                shape.friction = self.__fraction
                self.__shapes.append(shape)

    @staticmethod
    def round_point(points: list):
        temp_list = []
        for i in points:
            temp_list.append((one_dot_round(i[0]), one_dot_round(i[1])))
        return temp_list

    @staticmethod
    def __caculate_coordinates(points: list, step: float, radius: int, centroid: tuple):
        if step <= 0 and step > 90:
            raise RuntimeError("step have to 0 < x <= 90")
        start = 0
        while start <= 91:
            y = radius * math.cos(math.radians(start))
            x = radius * math.sin(math.radians(start))
            points.append((centroid[0] - x, y))  # todo 需要根据不同方向的弧线，转换不同的坐标
            start = start + step
        return points

    def draw_arc(self, screen, color: tuple):
        pygame.draw.aalines(screen, color, False, self.__points)

    @staticmethod
    def __get_centroid(start_point: tuple, end_point: tuple, is_up: bool, is_right: bool):
        if is_up:
            if start_point[1] - end_point[1] > 0:
                y = start_point[1]
            else:
                y = end_point[1]
        else:
            if start_point[1] - end_point[1] > 0:
                y = end_point[1]
            else:
                y = start_point[1]
        if is_right:
            if start_point[0] - end_point[0] < 0:
                x = end_point[0]
            else:
                x = start_point[0]
        else:
            if start_point[0] - end_point[0] < 0:
                x = start_point[0]
            else:
                x = end_point[0]
        return x, y

    @property
    def arc_shapes(self):
        return self.__shapes

    @property
    def arc_points(self):
        return self.__points

    @property
    def start_point(self):
        return self.__start_point

    @property
    def end_point(self):
        return self.__end_point

    @property
    def fraction(self):
        return self.__fraction

    @property
    def is_up(self):
        return self.__is_up

    @property
    def is_right(self):
        return self.__is_right

    def body_clicked(self, event) -> bool:
        if event is None:
            return False
        else:
            point_x, point_y = event.pos

        min_dist = 50
        for point in self.__points:
            if math.pow(point_x - point[0], 2)+math.pow(point_y - point[1], 2) < min_dist:
                return True
        return False


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()  # 创建一个对象来帮助跟踪时间
    space = pymunk.Space()  # 2  创建一个space， space是模拟的基本单位，可以在space上添加bodies,shapes,和joints
    space.gravity = (0.0, -900.0)  # 设置 space的重力
    COUNT = pygame.USEREVENT + 1
    # 调整画图间隔时间
    pygame.time.set_timer(COUNT, 500)

    counts = 0
    moving = False
    clicked = []

    a = Arc((0, 100), (100, 0))
    a.create_arc_in_space()
    temp_s = a.arc_shapes
    for i in temp_s:
        space.add(i)
    while True:
        screen.fill((255, 255, 255))
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
                        if a.body_clicked(event):
                            if a in clicked:
                                clicked.remove(a)
                            else:
                                clicked.append(a)

            if moving and event.type == COUNT:
                counts += 1
        if a in clicked:
            a.draw_arc(screen, (255, 255, 0))
        else:
            a.draw_arc(screen, (255, 0, 0))
        space.step(1 / 50.0)  # 3
        pygame.display.flip()
        clock.tick(50)
