import cocos as cos
from cocos.actions import *


class mouseDisplay(cos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(mouseDisplay, self).__init__()

        self.posx = 100
        self.posy = 240
        self.text = cos.text.Label('No mouse events yet', font_size=18, x=self.posx, y=self.posy)
        self.add(self.text)

    def update_text(self, x, y):
        text = 'Mouse @ %d,%d' % (x, y)
        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy

    def on_mouse_motion(self, x, y, dx, dy):
        """当鼠标移动到应用程序窗口上并且没有按鼠标按键时

        （x，y）是鼠标的物理坐标
        （dx，dy）是鼠标至上次调用后经过的的距离向量

        """
        self.update_text(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """此函数在鼠标在应用程序窗口上移动并按下鼠标按键时被调用

        （x，y）是鼠标的物理坐标
        （dx，dy）是鼠标至上次调用后经过的的距离向量

        'buttons' 是一个按位或pyglet.window.mouse常量-->LEFT，MIDDLE，RIGHT
        'modifiers' 是一个按位或pyglet.window.key修饰符常量
           (值如 'SHIFT', 'OPTION', 'ALT')
        """
        point = cos.draw.Circle
        self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        """此函数在按任何键时被调用

        （x，y）是鼠标的物理坐标
        'buttons' 是一个按位或pyglet.window.mouse常量-->LEFT，MIDDLE，RIGHT
        'modifiers' 是一个按位或pyglet.window.key修饰符常量
           (值如 'SHIFT', 'OPTION', 'ALT')
        """
        # self.posx, self.posy = cos.director.get_virtual_coordinates(x, y)
        self.posx, self.posy = x, y
        self.update_text(x, y)


if __name__ == "__main__":
    cos.director.director.init(resizable=True)  # 导演的初始化

    main_scene = cos.scene.Scene(mouseDisplay())  # 画布的初始化
    cos.director.director.run(main_scene)  # 上画布