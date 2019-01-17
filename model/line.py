""" 一个basic线的model，每一个实例都是pymunk空间中的一个线实体，可以在直接调用draw方法来画自己
"""
import pygame
import pymunk
from util.math_util import coordinates_transform


class Line:
    def __init__(self, center_point: tuple, a_point: tuple, b_point: tuple, line_width: int,
                 fraction: int=0, is_static: bool=False):
        self.__center_point = center_point
        self.__a_point = a_point
        self.__b_point = b_point
        self.__line_width = line_width
        self.__fraction = fraction
        self.__is_static = is_static
        self.__body = None
        self.__line = None

    def create_line_in_space(self):
        if self.__is_static:
            self.__body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            self.__body = pymunk.Body()
        self.__body.position = coordinates_transform(self.__center_point)
        self.__line = pymunk.Segment(self.__body, self.__a_point,
                                     self.__b_point, self.__line_width)
        self.__line.friction = self.__fraction

    def is_created(self):
        return self.__body is not None

    def draw_line(self, screen, color):
        # pv1 = self.__body.position + self.__line.a.rotated(self.__body.angle)
        # pv2 = self.__body.position + self.__line.b.rotated(self.__body.angle)
        pv1 = self.__center_point[0] + self.__a_point[0], self.__center_point[1] + self.__a_point[1]
        pv2 = self.__center_point[0] + self.__b_point[0], self.__center_point[1] + self.__b_point[1]
        pygame.draw.line(screen, color, pv1, pv2, self.__line_width)

    @property
    def body(self):
        return self.__body

    @property
    def line(self):
        return self.__line

    @property
    def fraction(self):
        return self.__fraction

    @fraction.setter
    def fraction(self, fraction: int):
        self.__fraction = fraction

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
