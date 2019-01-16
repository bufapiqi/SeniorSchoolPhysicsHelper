""" pygame的渲染菜单选项的类，可以把该类添加到menu中，让menu进行集中渲染
"""
# todo 待完善
import pygame
from pygame import image
from util.Vector2D import Vec2d
from util.math_util import caculate_position_with_menu


class MenuItem:

    def __init__(self, up_image: image, down_image: image, menu_rect: tuple, relative_position: int, num_items: int):
        point_a, point_b = caculate_position_with_menu(menu_rect, relative_position, num_items)
        upimage = up_image.convert_alpha()
        downimage = down_image.convert_alpha()
        self.__up_image = pygame.transform.scale(upimage, (abs(point_b[0] - point_a[0]), abs(point_b[1] - point_a[1])))
        self.__down_image = pygame.transform.scale(downimage, (abs(point_b[0] - point_a[0]), abs(point_b[1] - point_a[1])))
        self.__relative_position = relative_position
        self.__start_point = point_a
        self.__end_point = point_b
        self.__menu_rect = menu_rect
        self.__num_items = num_items

    def draw_item(self, screen):
        if self.is_click():
            screen.blit(self.__up_image, self.__start_point)
        else:
            screen.blit(self.__down_image, self.__start_point)

    def is_click(self):
        point_x, point_y = pygame.mouse.get_pos()
        position = (Vec2d(self.__end_point) - Vec2d(self.__start_point)) / 2 + Vec2d(self.__start_point)
        x, y = position.x, position.y
        w, h = self.__up_image.get_size()
        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    @property
    def up_image(self):
        return self.__up_image

    @property
    def down_image(self):
        return self.__down_image

    @property
    def relative_position(self):
        return self.__relative_position

    @property
    def start_point(self):
        return self.__start_point

    @property
    def end_point(self):
        return self.__end_point
