""" pygame的渲染菜单的类，使用该类，可以渲染一个矩形区域的菜单
"""
import pygame
from pygameEngine.menu_item import MenuItem


class Menu:

    def __init__(self, rect_s: tuple, rect_e: tuple, menu_item: list=None, event=None, background=None):
        self.__rect_s = rect_s
        self.__rect_e = rect_e
        self.__background = background
        self.__event = event
        if menu_item is None:
            self.__menu_item = []
        else:
            self.__menu_item = menu_item

    def draw_menu(self, screen):
        if type(self.__background) == str or type(self.__background) == tuple:
            # 读图片
            # todo 图片的逻辑
            # 也可以读图片
            pass
        else:
            # 现在先画个边框
            pygame.draw.line(screen, (255, 0, 0), (self.__rect_s[0], self.__rect_s[1]),
                             (self.__rect_e[0], self.__rect_s[1]))  # 上边框
            pygame.draw.line(screen, (255, 0, 0), (self.__rect_e[0], self.__rect_s[1]),
                             (self.__rect_e[0], self.__rect_e[1]))  # 右边框
            pygame.draw.line(screen, (255, 0, 0), (self.__rect_e[0], self.__rect_e[1]-1),
                             (self.__rect_s[0], self.__rect_e[1]-1))  # 下边框
            pygame.draw.line(screen, (255, 0, 0), (self.__rect_s[0]+1, self.__rect_s[1]),
                             (self.__rect_s[0]+1, self.__rect_e[1]))  # 左边框
            # 现在先画个边框
            # raise RuntimeError("background should be image_path or rgb_tuple !!!")
        for i in self.__menu_item:
            i.draw_item(screen)

    def add_item(self, item: MenuItem):
        self.__menu_item.append(item)

    def is_click(self):
        point_x, point_y = self.__event.pos
        self.__event = None
        in_x = self.rect_s[0] < point_x < self.__rect_e[0]
        in_y = self.__rect_s[1] < point_y < self.__rect_e[1]
        return in_x and in_y

    @property
    def menu_item(self):
        return self.__menu_item

    @property
    def rect_s(self):
        return self.__rect_s

    @property
    def rect_e(self):
        return self.__rect_e

    @property
    def event(self):
        return self.__event

    @event.setter
    def event(self, event):
        self.__event = event
        if self.is_click():
            for item in self.__menu_item:
                item.event = self.__event
