import math
import sys

import pygame

import pymunk
from pygame.constants import KEYDOWN, QUIT, K_ESCAPE, K_s

from model.arc import Arc
from model.ball import Ball
from model.convex_polygon import Poly
from model.line import Line
from pygameEngine.menu import Menu
from pygameEngine.menu_item import MenuItem


def drawText(self, text, posx, posy, textHeight=24, fontColor=(0, 0, 0), backgroudColor=(255, 255, 255)):
    fontObj = pygame.font.SysFont('arial', textHeight)  # 通过字体文件获得字体对象
    textSurfaceObj = fontObj.render(text, True, fontColor, backgroudColor)  # 配置要显示的文字
    textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
    textRectObj.center = (posx, posy)  # 设置显示对象的坐标
    self.blit(textSurfaceObj, textRectObj)  # 绘制字


def add_arrow(screen, start: tuple, end: tuple):
    width = max(math.fabs(start[0] - end[0]), math.fabs(start[1] - end[1]))
    right = 1 if end[0] > start[0] else -1
    up = 1 if end[1] > start[1] else -1
    tmp_x = start[0] + right * width
    tmp_y = start[1] + up * width
    point1 = (tmp_x, (tmp_y * 2 / 3 + start[1] / 3))
    point2 = (tmp_x * 2 / 3 + start[0] / 3, tmp_y)
    # 箭头主干
    pygame.draw.line(screen, (255, 0, 0), start, (tmp_x, tmp_y))
    # 箭头两侧
    pygame.draw.line(screen, (255, 0, 0), end, point1)
    pygame.draw.line(screen, (255, 0, 0), end, point2)
    clip = screen.get_clip()
    screen.set_clip(clip.clip(min(tmp_x, tmp_x+right*60), min(tmp_y, tmp_y + up*30), 60, 30))


def main():
    pygame.init()

    size = width, height = 600, 600  # 设置屏幕尺寸
    BLUE = 0, 0, 255
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = (255, 0, 0)
    GREEN = 0, 255, 0

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('尝试完整作图')  # 创建标题

    space = pymunk.Space()  # 2  创建一个space， space是模拟的基本单位，可以在space上添加bodies,shapes,和joints
    space.gravity = (0.0, -10.0)  # 设置 space的重力

    COUNT = pygame.USEREVENT + 1
    # 调整画图间隔时间
    pygame.time.set_timer(COUNT, 500)

    polys = []
    lines = []
    arcs = []
    clicked = None

    # 标志在空间中创建实体只创建一次
    running_sign = 0

    # moving:当前鼠标是否处于按下状态，
    # stop_count:鼠标松开后计数（判断本次操作是否结束），
    # moving_count:鼠标按下后计数（判断是点击还是长按）
    moving = False
    stop_count = 0
    moving_count = 0

    # 此处提前创建，在实际运行时还得根据用户作图的首尾节点和半径参数确定，不过不难就是了
    a = Arc((200, 200), (300, 300))
    a.create_arc_in_space()
    arcs.append(a)

    poly1 = Poly.create_box_with_centroid((210, 190), 8, 8, 100, None, 0.3)
    poly1.create_poly_in_space()
    polys.append(poly1)

    poly2 = Poly.create_box_with_centroid((350, 325), 49, 24, 10, None, 0.6)
    poly2.create_poly_in_space()
    polys.append(poly2)

    l = Line((300, 350), (-300, 0), (300, 0), 2, 0.1, is_static=True)
    l.create_line_in_space()
    lines.append(l)

    stop_image = pygame.image.load("../../resources/stop.png")
    continue_image = pygame.image.load("../../resources/continue.png")
    restart_image = pygame.image.load("../../resources/restart.png")
    restart2_image = pygame.image.load("../../resources/restart2.png")
    delete_image = pygame.image.load("../../resources/delete.png")

    # menu = Menu((screen.get_width() / 3, 0), (screen.get_width(), screen.get_height() / 10))
    menu1 = Menu((380, 10), (580, 70))
    item = MenuItem(stop_image, continue_image, (menu1.rect_s[0], menu1.rect_s[1],
                                           menu1.rect_e[0], menu1.rect_e[1]), 1, 3)
    item1 = MenuItem(restart_image, restart_image, (menu1.rect_s[0], menu1.rect_s[1],
                                              menu1.rect_e[0], menu1.rect_e[1]), 2, 3)
    item2 = MenuItem(delete_image, delete_image, (menu1.rect_s[0], menu1.rect_s[1],
                                           menu1.rect_e[0], menu1.rect_e[1]), 3, 3)
    menu1.add_item(item)
    menu1.add_item(item1)
    menu1.add_item(item2)

    running = False
    stop_sign = True
    paint_arrow = False

    # 临时保存用户输入
    positions = []
    clip_before = screen.get_clip()

    start_count = 0

    while True:
        screen.fill(WHITE)  # 越后面添加上去的 越在画布的上面
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_s:
                paint_arrow = not paint_arrow
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 获取点击鼠标事件
                if event.button == 1:  # 点击鼠标左键
                    stop_count = 0
                    moving_count = 0
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if event.button == 1:  # 松开鼠标左键
                    if item.is_clicked(event):
                        print(running)
                        if running:
                            print('stop clicked!')
                            clip_before = screen.get_clip()
                            screen.set_clip(clip_before.clip(1, 1, 1, 1))
                        else:
                            print('continue clicked!')
                            screen.set_clip(clip_before)
                            running = True
                        stop_sign = not stop_sign
                        moving_count = 3
                        # continue防止与其它点击操作冲突
                        continue
                    elif item1.is_clicked(event):
                        print('restart clicked')
                        # 初始化方块的位置和量，并置运行时为作图时,需要恢复作图和space两方面
                        if running:
                            for arc in arcs:
                                temp_s = arc.arc_shapes
                                for i in temp_s:
                                    space.remove(i)
                            for poly in polys:
                                space.remove(poly.body, poly.shape)
                            for line in lines:
                                space.remove(line.body, line.line)

                        for poly in polys:
                            poly.create_poly_in_space()
                        running = False
                        running_sign = 0
                        continue
                    elif item2.is_clicked(event):
                        print('delete clicked')
                        if running:
                            pass
                        elif clicked is None:
                            print('No entity chosen!')
                        else:
                            if isinstance(clicked, Arc):
                                # temp_s = clicked.arc_shapes
                                # for i in temp_s:
                                #     space.remove(i)
                                #     print(i)
                                arcs.remove(clicked)
                            elif isinstance(clicked, Line):
                                # space.remove(clicked.body, clicked.line)
                                lines.remove(clicked)
                            elif isinstance(clicked, Poly):
                                # space.remove(clicked.body, clicked.shape)
                                polys.remove(clicked)
                            else:
                                print("Sth could not be recognized clicked!")

                    moving = False
                    if moving_count <= 2:  # 按住鼠标小于1s，判断为点击
                        tmp = polys + lines + arcs
                        for entity in tmp:
                            if entity.body_clicked(event):
                                if entity == clicked:
                                    clicked = None
                                else:
                                    clicked = entity
                                break
                        print('state changed: True')
                        # running = True
            if len(positions) != 0 and not moving and event.type == COUNT:
                stop_count += 1
                if stop_count == 2:
                    # f = open(path, 'a')
                    # f.write(str(positions)+'\n')
                    # todo 将postions交给识别部分，根据识别部分的返回绘制具体实体，暂时先用上面的直接创建的实体
                    # if recognize(positions, 0) == 0:
                    #     more = max(positions[-2][0] - positions[0][0], positions[-2][1] - positions[0][1])
                    #     a = Arc(positions[0], (positions[0][0] + more, positions[0][1] + more))
                    #     arcs.append(a)
                    # elif recognize(positions, 1) == 1:
                    #     l = Line()
                    positions.clear()
        # 判断是否长按绘图
        if moving:
            positions.append(pygame.mouse.get_pos())

        # 前端显示坐标，辅助debug
        x, y = pygame.mouse.get_pos()  # 获得鼠标的位置
        drawText(screen, "(" + str(x) + "," + str(y) + ")", x, y)

        # polys_to_remove = []
        # for poly in polys:
        #     if poly.body.position.x > screen.get_width() or poly.body.position.y > screen.get_height():
        #         polys_to_remove.append(poly)
        #
        # for poly in polys_to_remove:
        #     polys.remove(poly)

        # 运行时，其中arcs和lines其实可以不用运行时加入space，但是从扩展性的角度，还是放进去，拿出来的话或许性能会好些
        # 其实区别运行时和作图时用space.step就可以，但是为避免删除实体导致频繁改变space中实体，还是
        if running_sign == 0 and running:
            start_count += 1
            print(start_count)
            running_sign = 1
            for arc in arcs:
                temp_s = arc.arc_shapes
                for i in temp_s:
                    print(i)
                    space.add(i)
            for poly in polys:
                space.add(poly.body, poly.shape)
            for line in lines:
                space.add(line.body, line.line)

        for arc in arcs:
            if arc != clicked:
                arc.draw_arc(screen, RED)
            else:
                arc.draw_arc(screen, GREEN)
        for poly in polys:
            if poly != clicked:
                poly.draw_poly(screen, RED, 2)
            else:
                poly.draw_poly(screen, GREEN, 2)
        for line in lines:
            if line != clicked:
                line.draw_line(screen, RED)
            else:
                line.draw_line(screen, GREEN)

        screen.set_clip(None)
        if paint_arrow:
            add_arrow(screen, (300, 300), (400, 200))

        menu1.draw_menu(screen)

        # 此处不可以使用区分作图时和运行时的running，而应该使用区分运行和暂停的stop_sign
        if not stop_sign:
            space.step(1 / 50.0)  # 3
        pygame.display.flip()


if __name__ == '__main__':
    main()
