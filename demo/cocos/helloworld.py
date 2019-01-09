import cocos as cos
from cocos.actions import *


class HelloWorld(cos.layer.ColorLayer):
    def __init__(self):
        # blueish color
        super(HelloWorld, self).__init__(64, 64, 224, 255)

        label = cos.text.Label('Hello, World!', font_name='Times New Roman', font_size=32,
                               anchor_x='center', anchor_y='center')

        label.position = 320, 240  # label

        sprite = cos.sprite.Sprite('xuniji1.png')   # 创建一个sprite
        sprite.position = 320, 240
        sprite.scale = 3

        self.add(label)
        self.add(sprite, z=1)

        scale = ScaleBy(3, duration=2)
        label.do(Repeat(scale + Reverse(scale)))
        sprite.do(Repeat(Reverse(scale) + scale))



if __name__ == "__main__":
    cos.director.director.init()  # 导演的初始化
    hello_layer = HelloWorld()  # 层的初始化
    hello_layer.do(RotateBy(360, duration=10) )

    main_scene = cos.scene.Scene(hello_layer)  # 画布的初始化
    cos.director.director.run(main_scene)  # 上画布

