# 向sys模块借一个exit函数用来退出程序
from sys import exit
from time import time, sleep

import pygame
# 导入pygame库
# 导入一些常用的函数和常量
from pygame.locals import *
from pygame.math import Vector2
from math import sin, cos, pi

from Area.area import Area
from Layout.layout import Layout
from Level.level import Level
from SimulationController.simulation_controller import SimulationController
from Traffic.vehicle import Vehicle

pygame.init()
# 初始化pygame,为使用硬件做准备
x = 1920
y = 30
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

screen = pygame.display.set_mode((900, 1410), 0, 32)
# 创建了一个窗口
pygame.display.set_caption("Hello, World!")
# 设置窗口标题


if __name__ == '__main__':
    print('***[Simulation]***[Simulation]***[Simulation]***[Simulation]***[Simulation]***[Simulation]***')
    # 初始化层
    my_level = Level(height=0, name='L1')
    # 初始化布局，设定可视化参数
    main_layout = Layout(screen=screen, record=False)
    main_layout.level_register(my_level)
    # 仿真控制器
    SimulationController.simulation_tick = 1
    simulation_controller = SimulationController(layout=main_layout)

    # 生成任务点
    # task = [Vector2(100 * sin(i) + 100, 100 * cos(i) + 100) for i in range(0, 3600)]
    task = [Vector2(100, 100), Vector2(100, 600), Vector2(600, 600), Vector2(600, 100), Vector2(100, 100)]

    Area(level=my_level, point_list=task)

    # 生成车
    my_car = Vehicle(x=100, y=100, width=20, length=40, level=my_level, task=task)
    simulation_controller.register(my_car)

    while True:  # 主循环

        for event in pygame.event.get():
            if event.type == QUIT:
                # 接收到退出事件后退出程序
                print('正在保存输出文件......')
                main_layout.submit()
                print('完成！')
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    simulation_controller.display_cmd(cmd='position', values=Vector2(0, 10))
                elif event.key == K_UP:
                    simulation_controller.display_cmd(cmd='position', values=Vector2(0, -10))
                elif event.key == K_RIGHT:
                    simulation_controller.display_cmd(cmd='position', values=Vector2(10, 0))
                elif event.key == K_LEFT:
                    simulation_controller.display_cmd(cmd='position', values=Vector2(-10, 0))
                elif event.key == K_KP_PLUS:
                    simulation_controller.display_cmd(cmd='scale', values=1.1)
                elif event.key == K_KP_MINUS:
                    simulation_controller.display_cmd(cmd='scale', values=0.9)

        # 画面更新
        main_layout.draw()
        pygame.display.update()
        sleep(0.1)

        # 仿真更新
        t = time()
        simulation_controller.update()
        print("======[更新用时]：[" + '{:.6f}'.format(time() - t) + "s]======")
