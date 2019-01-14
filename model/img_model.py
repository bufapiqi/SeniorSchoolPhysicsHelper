""" 一个image的model，每一个实例都是pymunk空间中的一个image实体，可以在直接调用draw方法来画自己
"""
import pygame
import pymunk
import pymunk.autogeometry
import pymunk.pygame_util
# todo 要查看一下 如何使用autogeometry这个来创建shape


class ImgModel:
    def __init__(self, image, centroid: tuple, is_static: bool=False):
        self.__image = image
        self.__centroid = centroid
        self.__is_static = is_static
        self.__line_set = pymunk.autogeometry.PolylineSet()

    def create_model(self):
        img_bb = pymunk.BB(0, 0, self.__image.get_width(), self.__image.get_height())
        self.__image.lock()
        # pymunk.autogeometry.march_soft(
        #     img_bb,
        #     self.__image.get_width(), self.__image.get_height(),
        #     99,
        #     segment_func,
        #     sample_func=sample_func)
        # logo_img.unlock()

    def sample_func(self, point):
        try:
            p = pymunk.pygame_util.to_pygame(point, self.__image)
            color = self.__image.get_at(p)
            return color.a
        except:
            return 0

    def __segment_func(self, v0, v1):
        self.__line_set.collect_segment(v0, v1)



### Generate geometry from pymunk logo image
# logo_img = pygame.image.load("pymunk_logo_sphinx.png")
# logo_bb = pymunk.BB(0, 0, logo_img.get_width(), logo_img.get_height())
#
# def sample_func(point):
#     try:
#         p = pymunk.pygame_util.to_pygame(point, logo_img)
#         color = logo_img.get_at(p)
#
#         return color.a
#         return color.hsla[2]
#     except:
#         return 0
#
# line_set = pymunk.autogeometry.PolylineSet()
# def segment_func(v0, v1):
#     line_set.collect_segment(v0, v1)
#
# logo_img.lock()
# pymunk.autogeometry.march_soft(
#     logo_bb,
#     logo_img.get_width(), logo_img.get_height(),
#     99,
#     segment_func,
#     sample_func)
# logo_img.unlock()
# r = 10
#
# letter_group = 0
# for line in line_set:
#     line = pymunk.autogeometry.simplify_curves(line, .7)
#
#     max_x = 0
#     min_x = 1000
#     max_y = 0
#     min_y = 1000
#     for l in line:
#         max_x = max(max_x, l.x)
#         min_x = min(min_x, l.x)
#         max_y = max(max_y, l.y)
#         min_y = min(min_y, l.y)
#     w,h = max_x - min_x, max_y - min_y
#
#     # we skip the line which has less than 35 height, since its the "hole" in
#     # the p in pymunk, and we dont need it.
#     if h < 35:
#         continue
#
#     center = Vec2d(min_x + w/2., min_y + h/2.)
#     t = pymunk.Transform(a=1.0, d=1.0, tx=-center.x, ty=-center.y)
#
#     r += 30
#     if r > 255:
#         r = 0
#
#     if True:
#         for i in range(len(line)-1):
#             shape = pymunk.Segment(space.static_body, line[i], line[i+1], 1)
#             shape.friction = 0.5
#             shape.color = (255,255,255)
#             space.add(shape)
