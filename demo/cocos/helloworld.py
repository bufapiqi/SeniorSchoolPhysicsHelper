import math
import sys

import pygame

import pymunk
from pygame.constants import KEYDOWN, QUIT, K_ESCAPE, K_s
from pygame.event import Event

from model.arc import Arc
from model.ball import Ball
from model.convex_polygon import Poly
from model.line import Line
from pygameEngine.menu import Menu
from pygameEngine.menu_item import MenuItem


BLUE = 0, 0, 255
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = (255, 0, 0)
GREEN = 0, 255, 0
    

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


def get_width(positions):
    right = 0
    left = 600
    for position in positions:
        if position[0] != 0:
            left = min(position[0], left)
            right = max(position[0], right)
    return right - left


def border_painter(screen, start, width, height):
    left_up = start
    left_down = (start[0], start[1] + height)
    right_up = (start[0]+width, start[1])
    right_down = (start[0]+width, start[1] + height)
    pygame.draw.line(screen, RED, left_up, left_down)
    pygame.draw.line(screen, RED, left_up, right_up)
    pygame.draw.line(screen, RED, left_down, right_down)
    pygame.draw.line(screen, RED, right_up, right_down)


# 显示速度和移动轨迹
# 作图时调用该方法，直接使用sub(screen)即可，运行时传入clicked的速度列表和坐标（默认时间间隔见COUNT）
def subwindow(screen, list1 = None, list2 = None):
    print(list1)
    print(list2)
    size = width, height = 270, 270
    start1 = (615, 15)
    start2 = (615, 315)
    border_painter(screen, start1, width, height)
    border_painter(screen, start2, width, height)
    drawText(screen, 'v/t', 600, 10)
    drawText(screen, 'poly', 600, 310)

    if list1 is not None and len(list1) != 0:
        print(len(list1))
        if len(list1) > 30:
            list1 = list1[-30:]
        points = []
        max_rate = max(list1)
        min_rate = min(list1)
        dist = max_rate - min_rate
        if dist == 0:
            dist = 1
        for index, rate in enumerate(list1):
            points.append((start1[0] + 9 * index, start1[1] + height - height*((rate-min_rate)/dist)))
        if len(points) == 1:
            pygame.draw.line(screen, RED, points[0], points[0])
        else:
            for i in range(len(points)-1):
                pygame.draw.line(screen, RED, points[i], points[i+1])

    if list2 is not None and len(list2) != 0:
        print(len(list2))
        points2 = []
        for point in list2:
            points2.append((start2[0] + point[0]*0.45, start2[1] + height - point[1]*0.45))
        if len(points2) == 1:
            pygame.draw.line(screen, RED, points2[0], points2[0])
        else:
            for i in range(len(points2)-1):
                pygame.draw.line(screen, RED, points2[i], points2[i+1])


def main():
    pygame.init()

    size = width, height = 900, 600  # 设置屏幕尺寸
    # BLUE = 0, 0, 255
    # WHITE = 255, 255, 255
    # BLACK = 0, 0, 0
    # RED = (255, 0, 0)
    # GREEN = 0, 255, 0

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('尝试完整作图')  # 创建标题

    space = pymunk.Space()  # 2  创建一个space， space是模拟的基本单位，可以在space上添加bodies,shapes,和joints
    space.gravity = (0.0, -10.0)  # 设置 space的重力

    COUNT = pygame.USEREVENT + 1
    COUNT_TIME = 500
    # 调整画图间隔时间
    pygame.time.set_timer(COUNT, COUNT_TIME)

    polys = []
    lines = []
    arcs = []
    clicked = None

    # 看起来识别是来不及了，那么加上index表示
    index = 0
    # 作图辅助,依次为arc的上端，arc下端和线条高度
    index1 = (0, 0)
    index2 = (0, 0)
    height = 0

    # 标志在空间中创建实体只创建一次
    running_sign = 0

    # moving:当前鼠标是否处于按下状态，
    # stop_count:鼠标松开后计数（判断本次操作是否结束），
    # moving_count:鼠标按下后计数（判断是点击还是长按）
    # running == True时，moving一律为False
    moving = False
    stop_count = 0
    moving_count = 0

    # 此处提前创建，在实际运行时还得根据用户作图的首尾节点和半径参数确定，不过不难就是了
    # a = Arc((200, 200), (300, 300))
    # a.create_arc_in_space()
    # arcs.append(a)
    #
    # poly1 = Poly.create_box_with_centroid((210, 190), 8, 8, 100, None, 0.3)
    # poly1.create_poly_in_space()
    # polys.append(poly1)
    #
    # poly2 = Poly.create_box_with_centroid((350, 325), 49, 24, 10, None, 0.6)
    # poly2.create_poly_in_space()
    # polys.append(poly2)
    #
    # l = Line((300, 350), (-300, 0), (300, 0), 2, 0.1, is_static=True)
    # l.create_line_in_space()
    # lines.append(l)

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

    # 保存选中滑块的速率列表和坐标
    clicked_rates = []
    clicked_pos = []
    last_one = None

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
                    moving_count = 0
                    if not running:
                        moving = True
            elif event.type == pygame.MOUSEBUTTONUP:  # 获取松开鼠标事件
                if event.button == 1:  # 松开鼠标左键
                    stop_count = 0
                    moving = False
                    if item.is_clicked(event):
                        stop_sign = not stop_sign
                        print(running)
                        positions.clear()
                        if running:
                            print('stop clicked!')
                            clip_before = screen.get_clip()
                            screen.set_clip(clip_before.clip(1, 1, 1, 1))
                        else:
                            print('continue clicked!')
                            screen.set_clip(clip_before)
                            running = True
                        # moving_count = 3
                        # continue防止与其它点击操作冲突
                        continue

                    elif item1.is_clicked(event):
                        print('restart clicked')
                        print(moving)
                        # 初始化方块的位置和量，并置运行时为作图时,需要恢复作图和space两方面
                        # 初始化进行操作：全图状态置作图时，清空space中实体并全部重新创建位置
                        # 置running_sign即可添加空间为初始
                        if not stop_sign:
                            stop_sign = not stop_sign
                            faker = Event(pygame.USEREVENT, {'pos': (410, 40)})
                            item.is_clicked(faker)

                        if running:
                            for arc in arcs:
                                temp_s = arc.arc_shapes
                                for i in temp_s:
                                    space.remove(i)
                            for poly in polys:
                                space.remove(poly.body, poly.shape)
                            for line in lines:
                                space.remove(line.body, line.line)
                            running_sign = 0
                            running = False
                            for poly in polys:
                                poly.create_poly_in_space()
                        clicked_pos.clear()
                        clicked_rates.clear()
                        last_one = None
                        positions.clear()

                    elif item2.is_clicked(event):
                        print('delete clicked')
                        if running:
                            pass
                        elif clicked is None:
                            print('No entity chosen!')
                        else:
                            index -= 1
                            if isinstance(clicked, Arc):
                                # temp_s = clicked.arc_shapes
                                # for i in temp_s:
                                #     space.remove(i)
                                #     print(i)
                                arcs.remove(clicked)
                                clicked = None
                            elif isinstance(clicked, Line):
                                # space.remove(clicked.body, clicked.line)
                                lines.remove(clicked)
                                clicked = None
                            elif isinstance(clicked, Poly):
                                # space.remove(clicked.body, clicked.shape)
                                polys.remove(clicked)
                                clicked = None
                            else:
                                print("Sth could not be recognized clicked!")
                        positions.clear()
                        print(index)

                    elif moving_count <= 2:  # 按住鼠标小于1s，判断为点击
                        print("less than 1s")
                        positions.clear()
                        if not running:
                            tmp = polys + lines + arcs
                            for entity in tmp:
                                if entity.body_clicked(event):
                                    if entity == clicked:
                                        clicked = None
                                        print('entity clicked!: False')
                                    else:
                                        clicked = entity
                                        print('entity clicked!: True')
                                    break
                        # running = True

                    elif not running:
                        # if moving_count <= 2:
                        #     tmp = polys + lines + arcs
                        #     for entity in tmp:
                        #         if entity.body_clicked(event):
                        #             if entity in clicked:
                        #                 clicked.remove(entity)
                        #             else:
                        #                 clicked.append(entity)
                        #             break
                        positions.append((0, 0))
                        moving = False
                        print(positions)

            elif event.type == COUNT:
                if running and isinstance(clicked, Poly):
                    if last_one is None:
                        last_one = clicked.body.position
                    else:
                        now = clicked.body.position
                        print(str(now)+'123')
                        if now.x < 600 and now.y > 0:
                            distance = int(math.sqrt(math.pow(now[0] - last_one[0], 2)+math.pow(now[1] - last_one[1], 2)))
                            clicked_rates.append(distance * 2)
                            last_one = now

                if len(positions) != 0 and not moving:
                    print('paint over')
                    print(positions)
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
                        if len(positions) <= 3:
                            pass
                        elif index == 0:
                            start = positions[0]
                            end = positions[-2]
                            arc_width = max(math.fabs(start[0]-end[0]), math.fabs(start[1] - end[1]))
                            real = (start[0]+arc_width, start[1]+arc_width)
                            index1 = start
                            index2 = real
                            a = Arc(start, real)
                            a.create_arc_in_space()
                            print('arc created!')
                            arcs.append(a)
                            index += 1
                        elif index == 1:
                            x_sum = 0
                            y_sum = 0
                            for position in positions:
                                if position[0] != 0:
                                    x_sum += position[0]
                                    y_sum += position[1]
                            centroid = (x_sum/len(positions), y_sum/len(positions))
                            height = centroid[1]
                            width = math.fabs(centroid[0] - positions[0][0])
                            l = Line(centroid, (-width, 0), (width, 0), 2, 0.1, is_static=True)
                            l.create_line_in_space()
                            print('line created!')
                            lines.append(l)
                            index += 1
                        elif index == 2:
                            poly1 = Poly.create_box_with_centroid((index1[0]+10, index1[1]-10), 9, 9, 100, None, 0.5)
                            poly1.create_poly_in_space()
                            print('poly1 created')
                            polys.append(poly1)
                            index += 1
                        elif index == 3:
                            poly_width = int(get_width(positions)/2)
                            poly_height = index2[1] - height if index2[1] > height else height - index2[1]
                            print((index2[0]+poly_width, int((height+index2[1])/2)))
                            poly2 = Poly.create_box_with_centroid((index2[0]+poly_width, int((height+index2[1])/2)),
                                                                  poly_width, int(poly_height/2),
                                                                  10, None, 0.5)
                            poly2.create_poly_in_space()
                            print('poly2 created')
                            polys.append(poly2)
                            index += 1
                        positions.clear()
                elif moving:
                    moving_count += 1
        # 判断是否长按绘图
        if moving:
            positions.append(pygame.mouse.get_pos())

        if running and isinstance(clicked, Poly):
            pos = clicked.body.position
            if pos.x < 600 and pos.y > 0:
                clicked_pos.append(clicked.body.position)

        # 前端显示坐标，辅助debug
        x, y = pygame.mouse.get_pos()  # 获得鼠标的位置
        drawText(screen, "(" + str(x) + "," + str(y) + ")", x, y)

        for i in range(len(positions) - 1):
            p1 = positions[i]
            p2 = positions[i + 1]
            # print(i) 发现一个很有意思的事情，我在这里i+3似乎没有意义，下一个i依旧只加了1,应该是因为对于range函数里面是迭代器
            # if p2 == (0, 0):
            #     i = i + 3
            if p1 != (0, 0) and p2 != (0, 0):
                pygame.draw.lines(screen, (255, 0, 0), False, [p1, p2])

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
                    space.add(i)
            for poly in polys:
                print(poly.centroid)
                print(poly.poly_points)
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

        subwindow(screen, clicked_rates, clicked_pos)

        menu1.draw_menu(screen)

        # 此处不可以使用区分作图时和运行时的running，而应该使用区分运行和暂停的stop_sign
        if not stop_sign:
            space.step(1 / 50.0)  # 3
        pygame.display.flip()


if __name__ == '__main__':
    main()
