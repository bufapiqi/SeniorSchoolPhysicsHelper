""" pygame的渲染菜单选项的类，可以把该类添加到menu中，让menu进行集中渲染
"""
# todo 待完善
import pygame
from pygame import image
from util.Vector2D import Vec2d


class MenuItem:

    def __init__(self, up_image: image, down_image: image, relative_position: int):
        self.__up_image = up_image
        self.__down_image = down_image
        self.__relative_position = relative_position

    def draw_item(self, screen, menu_rect: tuple):
        # caculate_position_with_menu()
        # w, h = self.imageUp.get_size()
        # x, y = self.position
        #
        # if self.isOver():
        #     screen.blit(self.imageDown, (x-w/2,y-h/2))
        # else:
        #     screen.blit(self.imageUp, (x-w/2, y-h/2))
        pass

    def is_click(self, rect: tuple):
        point_x, point_y = pygame.mouse.get_pos()
        point_a, point_b = MenuItem.caculate_position_with_menu(rect)
        position = (Vec2d(point_b) - Vec2d(point_a)) / 2 + Vec2d(point_a)
        x, y = position.x, position.y
        w, h = self.__up_image.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    @staticmethod
    def caculate_position_with_menu(rect: tuple):
        # todo 从相对位置计算 在screen上的绝对位置
        return (0, 0), (0, 0)

    @property
    def up_image(self):
        return self.__up_image

    @property
    def down_image(self):
        return self.__down_image

    @property
    def relative_position(self):
        return self.__relative_position
