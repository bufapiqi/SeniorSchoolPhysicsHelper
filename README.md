# SeniorSchoolPhysicsHelper

模块：
1.algorithm --> 图形识别

2.pygame  -->  界面渲染，pygame目录下，不同的py文件应该代表不同的画布，
即通过切换不同的py来切换页面

3.physicsEngine  -->  基于pymunk的物理引擎

4.util -->  pygame，pymunk之间的坐标转换工具

5.main  -->  启动

todo:
1. menu类（pygame）
2. 完成img_model
3. menu里选项的一个通用model
4. 坐标转换的东西（通过配置文件读取）
5. 其他joint的model都要实现
6. 自定义形状的model，或者滚轮的那种model得讨论一下
7. 可能还包含body的中心点适配问题，要能自动判断坐标和修正坐标


question:
1.多边形如何确定质心？？（三角形、四边形）pymunk是先创建body，再通过body创建shape的
