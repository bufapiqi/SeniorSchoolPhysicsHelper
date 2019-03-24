#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import math

import pygame
import sys

from model.arc import Arc
from model.line import Line


def get_distance(position1, position2):
    return math.pow(position1[0] - position2[0], 2) + math.pow(position1[1] - position2[1], 2)


def add_positions(positions: list):
    result = []
    position1 = positions[0]
    result.append(position1)
    threshold = 50

    for i in range(1, len(positions)):
        position2 = positions[i]
        if position2 == (0, 0):
            result.append((0, 0))
            if i == len(positions) - 1:
                return result
            else:
                position1 = positions[i + 1]
                continue
        dist = get_distance(position1, position2)
        times = int(math.sqrt(dist / threshold))
        for j in range(times):
            tmp_x = int(position1[0] * (times-1-j) / times + position2[0] * (j + 1) / times)
            tmp_y = int(position1[1] * (times-1-j) / times + position2[1] * (j + 1) / times)
            result.append((tmp_x, tmp_y))
        position1 = position2
    return result


if __name__ == '__main__':
    positions = [(1, 1), (56, 56), (0, 0)]
    print(add_positions(positions))


def recognize(positions: list, sign: int):
    return sign


# 初始化
pygame.init()

size = width, height = 1000, 600  # 设置屏幕尺寸
BLUE = 0, 0, 255
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0

screen = pygame.display.set_mode(size)  # 创建surface对象
pygame.display.set_caption('画圆及拖拽')  # 创建标题

COUNT = pygame.USEREVENT + 1
# 调整画图间隔时间
pygame.time.set_timer(COUNT, 500)

positions = []
polys = []
lines = []
arcs = []
clicked = []
tmp_sign = 0

moving = False
counts = 0
moving_count = 0

# 写入生成数据的文件
path = 'G:/temp.txt'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 获取点击鼠标事件
            if event.button == 1:  # 点击鼠标左键
                counts = 0
                moving_count = 0
                moving = True
        elif event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
            if event.button == 1:  # 松开鼠标左键
                moving = False
                if moving_count <= 2:
                    tmp = polys + lines + arcs
                    for entity in tmp:
                        if entity.body_clicked(event):
                            if entity in clicked:
                                clicked.remove(entity)
                            else:
                                clicked.append(entity)
                            break
                positions.append((0, 0))
        elif moving and event.type == COUNT:
            moving_count += 1
        # 这样操作就是停止操作的时间段内不得发生超过两次事件，发生时positions清0,即间隔市场大约为t~2t，此处为0.5到1s
        if len(positions) != 0 and not moving and event.type == COUNT:
            counts += 1
            if counts == 2:
                print(positions)
                positions = add_positions(positions)
                f = open(path, 'a')
                f.write(str(positions)+'\n')

                # if recognize(positions, 0) == 0:
                #     more = max(positions[-2][0] - positions[0][0], positions[-2][1] - positions[0][1])
                #     a = Arc(positions[0], (positions[0][0] + more, positions[0][1] + more))
                #     arcs.append(a)
                # elif recognize(positions, 1) == 1:
                #     l = Line()
                positions.clear()
    if moving:
        positions.append(pygame.mouse.get_pos())

    screen.fill(WHITE)  # 填充屏幕
    for i in range(len(positions) - 1):
        p1 = positions[i]
        p2 = positions[i + 1]
        # print(i) 发现一个很有意思的事情，我在这里i+3似乎没有意义，下一个i依旧只加了1
        # if p2 == (0, 0):
        #     i = i + 3
        if p1 != (0, 0) and p2 != (0, 0):
            pygame.draw.lines(screen, (255, 0, 0), False, [p1, p2])
    # 刷新屏幕
    pygame.display.flip()
