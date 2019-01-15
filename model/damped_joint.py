""" 弹簧joint,是baseJoint的子类.暂时只支持 竖直方向和水平方向. 如果想加强，修改draw即可
"""
import pymunk
from SeniorSchoolPhysicsHelper.model.base_joint import BaseJoint
import math
from SeniorSchoolPhysicsHelper.util.Vector2D import Vec2d


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

    def draw_joint(self):
        # todo  实现画弹簧的逻辑
        # 第一个点的坐标
        anchor_a = self.__anchor_a
        # 第二个点的坐标
        anchor_b = self.__anchor_b
        # 计算ab之间的总长
        len_ab = math.sqrt((anchor_a[0] - anchor_b[0])**2 + (anchor_a[1] - anchor_b[1])**2)
        # 画出连接第一个点的直线 （长度固定）

        # 画出连接第二个点的直线 （长度固定）
        # 算出第一个点跟第二个点，减去直线长度之后的距离
        # 计算线的坐标
        # 画出弹簧的形状
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
