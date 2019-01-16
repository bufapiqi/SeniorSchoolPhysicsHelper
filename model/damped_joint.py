""" 弹簧joint,是baseJoint的子类.暂时只支持 竖直方向和水平方向. 如果想加强，修改draw即可
"""
import pymunk
import pygame
from model.base_joint import BaseJoint
from util.Vector2D import Vec2d


class DampedJoint(BaseJoint):

    def __init__(self, body_a: pymunk.Body, body_b: pymunk.Body, anchor_a: tuple, anchor_b: tuple,
                 rest_length: int, stiffness: int, damping: int):
        BaseJoint.__init__(self, body_a, body_b)
        self.__anchor_a = anchor_a
        self.__anchor_b = anchor_b
        self.__rest_length = rest_length
        self.__stiffness = stiffness
        self.__damping = damping
        self._type = "DampedSpring"

    def create_joint_in_space(self):
        self._joint = pymunk.DampedSpring(self._body_a, self._body_b, self.__anchor_a, self.__anchor_b,
                                          self.__rest_length, self.__stiffness, self.__damping)

    def draw_joint(self, screen, color: tuple):
        # todo  实现画弹簧的逻辑
        # 用第一个点得来的向量
        vector_a = Vec2d(self.__anchor_a)
        # 用第二个点得来的向量
        vector_b = Vec2d(self.__anchor_b)
        # 计算ab之间的总长
        len_ab = vector_a.get_distance(vector_b)
        # 画出连接第一个点的直线 （长度固定）
        line_a = ((vector_b - vector_a) / 10) + vector_a
        pygame.draw.line(screen, color, vector_a, line_a)
        # 画出连接第二个点的直线 （长度固定）
        line_b = ((vector_a - vector_b) / 10) + vector_b
        pygame.draw.line(screen, color, vector_b, line_b)
        # 画出弹簧
        step = len_ab / 20
        angle = vector_a.get_angle()
        for i in range(1, 16, 2):
            temp_middle = line_a + step * i
            # todo 徐海溦
            pass

    @property
    def anchor(self):
        return self.__anchor_b, self.__anchor_b

    @property
    def rest_length(self):
        return self.__rest_length

    @property
    def stiffness(self):
        return self.__stiffness

    @property
    def damping(self):
        return self.__damping
