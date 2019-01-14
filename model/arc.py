""" 一个弧线的model，每一个实例都是pymunk空间中的一个弧线实体，可以在直接调用draw方法来画自己
"""

import pygame
import pymunk
import math


class Arc:
    def __init__(self, start_point: tuple, end_point: tuple, fraction: int=0, is_up: bool=True, is_right: bool=False):
        # is_position --> True 弧线朝向向右，反之向左
        self.__start_point = start_point
        self.__end_point = end_point
        self.__fraction = fraction
        self.__is_up = is_up
        self.__is_right = is_right
        self.__points = []

    def create_arc_in_space(self):
        centroid_x, centroid_y = Arc.__get_centroid(self.__start_point, self.__end_point, self.__is_up, self.__is_right)
        radius = abs(self.__start_point[0] - self.__end_point[0])
        print(radius)
        print(math.sin())
        for i in range(1, 90):  # 按照每一度计算坐标从一度到89度
            y = radius * math.cos(i)
            x = radius * math.sin(i)
            # todo 这里还要根据中心点转换坐标
            self.__points.append((int(x), int(y)))
        print(self.__points)

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


if __name__ == "__main__":
    a = Arc((0, 100), (100, 0))
    a.create_arc_in_space()


