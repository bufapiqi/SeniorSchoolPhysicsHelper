""" 弹簧joint,是baseJoint的子类
"""
import pymunk
from SeniorSchoolPhysicsHelper.model.base_joint import BaseJoint


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
        # todo  实现画图的逻辑
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
