""" 用来启动主程序  也可在这里面进行一些测试
"""
# todo 写成一个类
import sys
import pygame
from pygame.locals import *
from SeniorSchoolPhysicsHelper.ymodel.arc import Arc
import math


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("现在用来测试")
    clock = pygame.time.Clock()   # 创建一个对象来帮助跟踪时间
    a = Arc((0, 200), (200, 0))
    a.create_arc_in_space()


    while True:
            screen.fill((255, 255, 255))  # 越后面添加上去的 越在画布的上面
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit(0)

            # print(pygame.font.get_fonts())
            a.draw_arc(screen, (255, 0, 0))
            pygame.draw.arc(screen, (0, 0, 0), ((200, 200), (100, 100)), 0, math.pi/2, 1)
            pygame.display.flip()

            clock.tick(50)


if __name__ == '__main__':
    sys.exit(main())
