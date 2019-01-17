""" 画text的类
"""
import pygame


class Text:

    def __init__(self, text: str, posx: int, posy: int, text_height: int=10,
                 font_color: tuple=(0, 0, 0), background_color: tuple=(255, 255, 255)):
        self.__text = text
        self.__pos_x = posx
        self.__pos_y = posy
        self.__text_height = text_height
        self.__font_color = font_color
        self.__background = background_color

    def draw_text(self, screen):
        fontObj = pygame.font.SysFont('arial', self.__text_height)  # 通过字体文件获得字体对象
        textSurfaceObj = fontObj.render(self.__text, True, self.__font_color, self.__background)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        textRectObj.center = (self.__pos_x, self.__pos_y)  # 设置显示对象的坐标
        screen.blit(textSurfaceObj, textRectObj)  # 绘制字

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    @property
    def text_pos(self):
        return self.__pos_x, self.__pos_y

    @text_pos.setter
    def text_pos(self, new_pos: tuple):
        self.__pos_x = new_pos[0]
        self.__pos_y = new_pos[1]

    @property
    def text_height(self):
        return self.__text_height

    @text_height.setter
    def text_height(self, new_height: int):
        self.__text_height = new_height

    @property
    def font_color(self):
        return self.__font_color

    @font_color.setter
    def font_color(self, new_color: tuple):
        self.__font_color = new_color

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, new_background):
        self.__background = new_background
