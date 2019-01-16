""" pygame的渲染菜单的类，使用该类，可以渲染一个矩形区域的菜单
"""
import pygame
from pygameEngine.menu_item import MenuItem


class Menu:

    def __init__(self, rect_s: tuple, rect_e: tuple, menu_item: list, background=None):
        self.__rect_s = rect_s
        self.__rect_e = rect_e
        self.__background = background
        if menu_item is None:
            self.__menu_item = []
        else:
            self.__menu_item = menu_item

    def draw_menu(self, screen):
        screen.set_clip(self.__rect_s, self.__rect_e)
        if type(self.__background) == str or type(self.__background) == tuple:
            # 读图片
            pass
        else:
            raise RuntimeError("background should be image_path or rgb_tuple !!!")
        for i in self.__menu_item:
            i.draw_item()  # todo 待完善

    def add_item(self, item: MenuItem):
        self.__menu_item.append(item)

    @property
    def menu_item(self):
        return self.__menu_item

    @property
    def rect_s(self):
        return self.__rect_s

    @property
    def rect_e(self):
        return self.__rect_e
