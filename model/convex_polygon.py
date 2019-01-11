""" 一个basic凸多边形的model，每一个实例都是pymunk空间中的一个凸多边形实体，可以在直接调用draw方法来画自己
"""
import pygame
import pymunk
from pymunk import Vec2d
COLLTYPE_DEFAULT = 0


class Poly:
    def __init__(self, mass: int, centroid: tuple, poly_points: list, poly_fraction: int=0,
                 moment: int=None, is_static: bool=False):
        self.__mass = mass
        self.__centroid = centroid
        self.__poly_points: list = poly_points
        self.__poly_fraction = poly_fraction
        self.__moment = moment
        self.__is_static = is_static
        self.__body = None
        self.__shape = None

    def __create_poly_in_space(self):
        if self.__moment is None:
            self.__moment = pymunk.moment_for_poly(self.__mass, self.__poly_points)
        self.__body = pymunk.Body(self.__mass, self.__moment)
        self.__body.position = Vec2d(self.__centroid)
        self.__shape = pymunk.Poly(self.__body, self.__poly_points)
        self.__shape.friction = self.__poly_fraction
        self.__shape.collision_type = COLLTYPE_DEFAULT

    # 返回一个已经创建好body和shape的四边形
    @staticmethod
    def create_box_with_centroid(centroid: tuple, size: int, mass: int, moment: int=None, fraction: int=0):
        poly = Poly(mass, centroid, [(-size, -size), (-size, size), (size, size), (size, -size)], fraction, moment)
        poly.__create_poly_in_space()
        return poly

    def is_created(self):
        return self.__body is not None

    def draw_poly(self, screen, poly_color, width=0):  # width=0代表填充整个多边形区域
        points = self.__poly_points
        # todo pygame与pmunk的坐标转换

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
        return self.__centroid

    @property
    def poly_fraction(self):
        return self.__poly_fraction

    @property
    def moment(self):
        return self.moment