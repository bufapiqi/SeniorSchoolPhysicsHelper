""" 用来启动主程序  也可在这里面进行一些测试
"""
import sys
import pygame
from pygame.locals import *
from model.arc import Arc
from model.line import Line
from model.ball import Ball
from model.convex_polygon import Poly
from pygameEngine.menu_item import MenuItem
from pygameEngine.menu import Menu
from pygameEngine.text import Text
import math
# todo 徐琪  resources里面需要一些，一致的图标，比如 开始/暂停/继续，保存、计时，这些图标都需要画风一致，可以自己复制
# todo main文件，在画布里画出来看看


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600), 0, 32)
    pygame.display.set_caption("现在用来测试")
    clock = pygame.time.Clock()   # 创建一个对象来帮助跟踪时间

    line = Line((150, 150), (100, 100), (200, 200), 2, is_static=True)
    line.create_line_in_space()

    ball = Ball(1, 2, 2, (350, 350), is_static=True)
    ball.create_ball_in_space()

    poly = Poly.create_box_with_centroid((200, 200), 10, 1, is_static=True)

    a = Arc((0, 200), (200, 0))
    a.create_arc_in_space()

    print(sys.argv[0])
    up_image = pygame.image.load("../resources/pause.png")
    down_image = pygame.image.load("../resources/play1.png")
    save_image = pygame.image.load("../resources/save.png")
    time_image = pygame.image.load("../resources/time1.png")
    print("length:"+str(up_image.get_width()) + "  height:"+str(up_image.get_height()))
    menu = Menu((300, 300), (400, 400))
    menu1 = Menu((500, 10), (560, 100))
    item = MenuItem(up_image, down_image, (menu1.rect_s[0], menu1.rect_s[1],
                                           menu1.rect_e[0], menu1.rect_e[1]), 1, 4)
    item1 = MenuItem(save_image, save_image, (menu1.rect_s[0], menu1.rect_s[1],
                                              menu1.rect_e[0], menu1.rect_e[1]), 2, 4)
    item2 = MenuItem(time_image, time_image, (menu1.rect_s[0], menu1.rect_s[1],
                                              menu1.rect_e[0], menu1.rect_e[1]), 3, 4)
    menu1.add_item(item)
    menu1.add_item(item1)
    menu1.add_item(item2)
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

            a.draw_arc(screen, (255, 0, 0))
            # poly.draw_poly(screen, (0, 0, 255))
            # pygame.draw.arc(screen, (0, 0, 0), ((200, 200), (100, 100)), 0, math.pi/2, 1)
            # pygame.draw.line(screen, (0, 255, 0), (100, 100), (200, 200), 10)
            line.draw_line(screen, (0, 255, 0))
            # ball.draw_ball(screen, (0, 0, 255), 1)
            menu1.draw_menu(screen)
            text.draw_text(screen)
            pygame.display.flip()

            clock.tick(50)


if __name__ == '__main__':
    sys.exit(main())
