""" pygame的渲染菜单的类，使用该类，可以渲染一个矩形区域的菜单
"""
import pygame
from pygameEngine.menu_item import MenuItem


class Menu:

    def __init__(self, rect_s: tuple, rect_e: tuple, menu_item: list):
        self.__rect_s = rect_s
        self.__rect_e = rect_e
        if menu_item is None:
            self.__menu_item = []
        else:
            self.__menu_item = menu_item

    def draw_menu(self):

        pass

    def add_item(self, item: MenuItem):
        self.__menu_item.append(item)

    @property
    def menu_item(self):
        return self.__menu_item
