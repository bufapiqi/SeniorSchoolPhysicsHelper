""" 用来启动主程序  也可在这里面进行一些测试
"""
# todo 写成一个类
import sys
import pygame
from pygame.locals import *
from model.arc import Arc
from pygameEngine.menu_item import MenuItem
from pygameEngine.menu import Menu
from pygameEngine.text import Text
import math


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600), 0, 32)
    pygame.display.set_caption("现在用来测试")
    clock = pygame.time.Clock()   # 创建一个对象来帮助跟踪时间
    a = Arc((0, 200), (200, 0))
    a.create_arc_in_space()

    print(sys.argv[0])
    up_image = pygame.image.load("../resources/pause.jpg")
    down_image = pygame.image.load("../resources/play.jpg")
    print("length:"+str(up_image.get_width()) + "  height:"+str(up_image.get_height()))
    menu = Menu((300, 300), (400, 400))
    item = MenuItem(up_image, down_image, (menu.rect_s[0], menu.rect_s[1],
                                           menu.rect_e[0], menu.rect_e[1]), 1, 1)
    menu.add_item(item)
    text = Text("A", 500, 500)



    while True:
            screen.fill((255, 255, 255))  # 越后面添加上去的 越在画布的上面
            for event in pygame.event.get():
                # print(event)
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    menu.event = event
                    # item.event = event

            # print(pygame.font.get_fonts())
            a.draw_arc(screen, (255, 0, 0))
            pygame.draw.arc(screen, (0, 0, 0), ((200, 200), (100, 100)), 0, math.pi/2, 1)
            # item.draw_item(screen)
            menu.draw_menu(screen)
            text.draw_text(screen)
            pygame.display.flip()

            clock.tick(50)


if __name__ == '__main__':
    sys.exit(main())
