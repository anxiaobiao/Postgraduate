# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:25:58 2021

@author: Tom Wade
"""

from Force_create import Force_create as FC
from Circular_barrier_description import Circular_barrier_description as CBD
from Circle_APF import Circle_APF as CA
from Convex_polygon_barrier_description import Convex_polygon_barrier_description as CPBD

import numpy as np
import matplotlib.pyplot as plt

def main():
    # 路径
    path = np.array([])
    # 赋初值
    origin = np.array([0.0,0.0])
    destination = np.array([100.0,100.0]) 
    missile = origin.astype(float)
    range_of_action = 3
    
    barrier_con = np.array([[20.0,20.0], [20.0,30.0], [30.0,40.0], [40.0,30.0], [40.0,20.0]])
    
    barrier_cir_one = np.array([40.0,60.0])
    barrier_cir_one_rad = 10
    
    barrier_cir_two = np.array([60.0,30.0])
    barrier_cir_two_rad = 10
    
    time = 0
    # for i in range(200):
    while (missile - destination < np.array([0.0, 0.0])).any() :
        barrier_ciecle_1 = CBD(missile, barrier_cir_one, barrier_cir_one_rad).circular_barrier(missile, barrier_cir_one, barrier_cir_one_rad)
        
        barrier_convex = CPBD(missile, barrier_con).convex_polygon_barrier(missile, barrier_con)
        
        barrier_ciecle_2 = CBD(missile, barrier_cir_two, barrier_cir_two_rad).circular_barrier(missile, barrier_cir_two, barrier_cir_two_rad)

        obstacle = np.append(barrier_ciecle_1, barrier_ciecle_2)
        obstacle = np.append(obstacle, barrier_convex)
        obstacle_size = int(len(obstacle) / 2)
        obstacle = obstacle.reshape(obstacle_size,2)
        # 环流APF方法
        f = CA(origin, destination, missile, obstacle, range_of_action, obstacle_size)
        cir_APF = f.circle_APF(origin, destination, missile, obstacle, range_of_action, obstacle_size)
        # 传统APF方法
        # f = FC(origin, destination, missile, obstacle, range_of_action, obstacle_size)
        # cir_APF = f.join_force_field()
        
        join_forces = cir_APF / np.hypot(cir_APF[0], cir_APF[1])
        
        missile += join_forces
        
        path = np.append(path, missile)
        
        print(missile)
        # 防止死循环
        if time < 700:
            time += 1
        else:
            break

    path = path.reshape(int(len(path) / 2), 2)
    
    draw(path, origin, destination, barrier_con, barrier_cir_one, barrier_cir_one_rad, barrier_cir_two, barrier_cir_two_rad)
    

def draw(path, origin, destination, barrier_con, barrier_cir_one, barrier_cir_one_rad, barrier_cir_two, barrier_cir_two_rad):
    path_X = path[:, 0]
    path_Y = path[:, 1]
    
    barrier = np.append(barrier_con, barrier_con[0])
    barrier = barrier.reshape(int(len(barrier)/2), 2)
    barrier_X = barrier[:, 0]
    barrier_Y = barrier[:, 1]
    
    point_X = np.append(origin[0], destination[0])
    point_Y = np.append(origin[1], destination[1])
    
    circle_1_X, circle_1_Y = circle(barrier_cir_one, barrier_cir_one_rad)
    circle_2_X, circle_2_Y = circle(barrier_cir_two, barrier_cir_two_rad)
    
    plt.plot(circle_1_X, circle_1_Y, color='b')
    plt.plot(circle_1_X, 2 * barrier_cir_one[1] - circle_1_Y, color='b')
    plt.plot(circle_2_X, circle_2_Y, color='b')
    plt.plot(circle_2_X, 2 * barrier_cir_two[1] - circle_2_Y, color='b')
    
    plt.plot(barrier_X, barrier_Y, color='b')
    
    plt.plot(path_X, path_Y)

    plt.scatter(point_X, point_Y, color = 'r')
    
    plt.show()
    # 绘制圆
def circle(center, radius):
    X = np.arange(center[0] - radius, center[0] + radius, 0.01)
    Y = center[1] + np.sqrt(radius ** 2 - (X - center[0]) ** 2)
    
    return X, Y
     

    
main()   
    