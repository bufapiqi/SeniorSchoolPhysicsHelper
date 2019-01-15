""" 所有joint的父类
"""
import pymunk
from abc import ABCMeta, abstractmethod


class BaseJoint(metaclass=ABCMeta):
    def __init__(self, body_a: pymunk.Body, body_b: pymunk.Body):
        self._body_a = body_a
        self._body_b = body_b
        self._type = ""
        self._joint = None

    @abstractmethod
    def create_joint_in_space(self):
        pass

    @abstractmethod
    def draw_joint(self, screen, color: tuple):
        pass

    def is_created(self):
        if self._joint is None:
            return False
        return True

    @property
    def type(self):
        return self._type

    @property
    def body_a(self):
        return self._body_a

    @property
    def body_b(self):
        return self._body_b

    @property
    def joint(self):
        return self._joint
