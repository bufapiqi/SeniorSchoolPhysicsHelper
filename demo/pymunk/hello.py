import sys
import random
import pygame
from pygame.locals import *
from model.arc import Arc
from model.line import Line
import pymunk


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    print(screen.get_height())
    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()   # 创建一个对象来帮助跟踪时间

    space = pymunk.Space()  # 2  创建一个space， space是模拟的基本单位，可以在space上添加bodies,shapes,和joints
    space.gravity = (0.0, -900.0)  # 设置 space的重力

    a = Arc((0, 200), (200, 0))
    a.create_arc_in_space()
    temp_s = a.arc_shapes
    for i in temp_s:
        space.add(i)

    tl = Line((150, 150), (-10, 0), (100, 0), 5, is_static=True)
    tl.create_line_in_space()
    space.add(tl.line)

    # lines = add_static_L(space)
    lines = add_L(space)
    balls = []
    points = []
    ticks_to_next_ball = 10
    leftdown = False
    while True:
        screen.fill((255, 255, 255))  # 越后面添加上去的 越在画布的上面
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # leftdown = True
                x, y = event.pos
                ball_shape = add_ball(space, x, 600-y)
                balls.append(ball_shape)
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                # leftdown = False
                pass
            elif leftdown and event.type == MOUSEMOTION:
                pass
                # x, y = event.pos
                # points.append((x, y))

        # ticks_to_next_ball -= 1
        # if ticks_to_next_ball <= 0:
        #     ticks_to_next_ball = 25
        #     ball_shape = add_ball(space)
        #     balls.append(ball_shape)

        space.step(1/50.0)  # 3

        draw_lines(screen, lines)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 0:  # 1
                balls_to_remove.append(ball)  # 2

        for ball in balls_to_remove:
            space.remove(ball, ball.body)  # 删除一个pymunk中的object，要同时删掉其body和shape
            balls.remove(ball)  # 4

        for ball in balls:
            draw_ball(screen, ball)

        for i in range(len(points)-1):
            p1 = points[i]
            p2 = points[i+1]
            pygame.draw.lines(screen, (255, 0, 0), False, [p1, p2])

        x, y = pygame.mouse.get_pos()  # 获得鼠标的位置
        drawText(screen, "("+str(x)+","+str(y)+")", x, y)
        a.draw_arc(screen, (255, 0, 0))
        tl.draw_line(screen, (255, 0, 0))
        # print(pygame.font.get_fonts())
        pygame.display.flip()

        clock.tick(50)


def add_ball(space, x, y):
    mass = 1  # 设置质量
    radius = 14  # 设置圆的半径
    moment = pymunk.moment_for_circle(mass, 0, radius)  # 计算惯性矩：截面抵抗弯曲的性质（质量， 内半径， 外半径；实心圆的内径是0）
    body = pymunk.Body(mass, moment)  # 根据moment mass 创建一个body
    body.position = x, y  # 3
    shape = pymunk.Circle(body, radius)  # 设置碰撞的形状
    space.add(body, shape)  # 5
    return shape


def drawText(self, text, posx, posy, textHeight=24, fontColor=(0, 0, 0), backgroudColor=(255,255,255)):
    fontObj = pygame.font.SysFont('arial', textHeight)  # 通过字体文件获得字体对象
    textSurfaceObj = fontObj.render(text, True, fontColor, backgroudColor)  # 配置要显示的文字
    textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
    textRectObj.center = (posx, posy)  # 设置显示对象的坐标
    self.blit(textSurfaceObj, textRectObj)  # 绘制字


def draw_ball(screen, ball):
    p = int(ball.body.position.x), 600-int(ball.body.position.y)
    pygame.draw.circle(screen, (0, 0, 255), p, int(ball.radius), 2)


def draw_points(screen, points):
    pygame.draw.rect(screen, [255, 0, 0], [points[0], points[1], 1, 1], 1)


def add_static_L(space):  # 在pymunk的space空间里添加线
    body = pymunk.Body(body_type = pymunk.Body.STATIC)  # 添加一个静止的body
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255, 0), 5)  # 画两条线  先创建body，然后再在这个body上添加shape
    l2 = pymunk.Segment(body, (-150, 0), (-150, 50), 5)
    space.add(l1, l2)  # 3
    return [l1, l2]


def add_L(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # 创建一个静态的旋转中心
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC) # 1
    rotation_limit_body.position = (200, 300)

    body = pymunk.Body(10, 10000)  # 通过质量和惯性矩创建一个body
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (255.0, 0.0), 5.0)
    l2 = pymunk.Segment(body, (-150.0, 0), (-150.0, 50.0), 5.0)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))  # 3

    # 控制旋转的角度
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit)  # 2
    # 控制旋转的角度

    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    return [l1, l2]


def draw_lines(screen, lines):  # 通过pymunk空间里线 在pygame里划线
    for line in lines:
        body = line.body  # 拿到line的body
        pv1 = body.position + line.a.rotated(body.angle)  # 这里的角度是0
        pv2 = body.position + line.b.rotated(body.angle)  # line.b就是线的第二个断点的坐标
        p1 = to_pygame(pv1)  # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (255, 0, 0), False, [p1, p2])


def to_pygame(p):  # 从pymunk到pygame的坐标转换
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

if __name__ == '__main__':
    sys.exit(main())
