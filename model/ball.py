""" 一个basic圆的model，每一个实例都是pymunk空间中的一个圆实体，可以在直接调用draw方法来画自己
"""
import math

import pygame
import pymunk
from util.math_util import coordinates_transform


class Ball:
    def __init__(self, mass, in_radius: int, out_radius: int, position: tuple, moment: int = None,
                 is_static: bool = False):
        self.__mass = mass
        self.__in_radius = in_radius
        self.__out_radius = out_radius
        self.__position = position
        self.__moment = moment
        self.__is_static = is_static
        self.__body = None
        self.__shape = None

    def create_ball_in_space(self):
        if self.__moment is None:
            self.__moment = pymunk.moment_for_circle(self.__mass, self.__in_radius, self.__out_radius)
        if self.__is_static:
            self.__body = pymunk.Body(self.__mass, self.__moment, body_type=pymunk.Body.STATIC)
        else:
            self.__body = pymunk.Body(self.__mass, self.__moment)
        self.__body.position = coordinates_transform(self.__position)
        self.__shape = pymunk.Circle(self.__body, self.__out_radius)

    def draw_ball(self, screen, color, border_width):
        bx = int(self.__body.position.x)
        by = int(self.__body.position.y)
        pygame.draw.circle(screen, color, (bx, by), self.__out_radius, border_width)

    def is_created(self):
        return self.__body is not None

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, mass: int):
        self.__mass = mass

    @property
    def in_radius(self):
        return self.__in_radius

    @in_radius.setter
    def in_radius(self, in_radius: int):
        self.__in_radius = in_radius

    @property
    def out_radius(self):
        return self.__out_radius

    @out_radius.setter
    def out_radius(self, out_radius: int):
        self.__out_radius = out_radius

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position: tuple):
        self.__position = position

    @property
    def moment(self):
        return self.__moment

    @moment.setter
    def moment(self, moment: int):
        self.__moment = moment

    @property
    def body(self):
        return self.__body

    @property
    def shape(self):
        return self.__shape

    def body_clicked(self):
        if self.__event is None:
            return False
        else:
            point_x, point_y = self.__event.pos
        bx = int(self.__body.position.x)
        by = int(self.__body.position.y)
        if math.pow(point_x - bx, 2) + math.pow(point_y - by, 2) <= math.pow(self.out_radius, 2):
            return True
        else:
            return False
