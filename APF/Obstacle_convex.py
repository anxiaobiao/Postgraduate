# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 16:40:49 2021

@author: Tom Wade
"""

import numpy as np
import math

class obstacle_convex(object):
    def __init__(self, obstacle):
        self.obstacle = obstacle                #障碍物位置

    def initial_convexity(self, obstacle):
        min_obstacle = obstacle[0, 0]
        H_relative_dirction = np.array([0.0] * len(obstacle)) 
        min_lable = 0
        
        for i in range(len(obstacle)):      # 坐标最小值
            if min_obstacle < obstacle[i, 0]:
                min_lable = i
                min_obstacle = np.hypot(obstacle[i, 0], obstacle[i, 1])
                
        vector_obstacle = np.array([0, 1])
        
       
        while True:
            obstacle_temp = np.delete(obstacle, min_lable, 0)
            temp = obstacle_temp[0] - obstacle[min_lable]
            H_max = np.dot(temp / np.hypot(temp[0], temp[1]), vector_obstacle)
            H_lable = np.array([0])
            
            for i in range(len(obstacle)):
                vector = obstacle_temp[i] - obstacle[min_lable]
                H_relative_dirction[i] = np.dot(vector / np.hypot(vector[0], vector[1]), vector_obstacle)
                if H_max < H_relative_dirction:
                    H_max = H_relative_dirction
                    H_lable = i
            
            vector_temp = obstacle_temp[H_lable] - obstacle[min_lable]
            vector_obstacle = vector_temp / np.hypot(vector_temp[0], vector_temp[1])
            
            if vector_obstacle[H_lable] == obstacle[min_lable]:
                break
            else:
                np.append(obstacle, [obstacle_temp[H_lable]], axis=0)   
            
        return obstacle
    
    def barriers_intersect(obstacle_A, obstacle_B):
        for i in range(len(obstacle_A)):
            for j in range(len(obstacle_B)):
                side_A = obstacle_A[i + 1] - obstacle_A[i]
                side_B = obstacle_B[j + 1] - obstacle_B[j]
                
                matrix_1 = np.array([np.dot(side_A, side_A), -np.dot(side_A, side_B), -np.dot(side_A, side_B), np.dot(side_B, side_B)])
                matrix_1 = np.matrix(matrix_1.shape(2, 2))
                matrix_1_inverse = matrix_1.I
                
                matrix_2 = np.array([np.dot(side_A, side_B - side_A), np.dot(side_B, side_A -side_B)])
                matrix_2 = np.matrix(matrix_2.T)
                
                X = matrix_2 * matrix_1_inverse
                
                if X[0] > 1 or X[0] < 0 or X[1] > 1 or X[1] < 0 :
                    triangle_AB = 0.0
                    triangle_BA = 0.0
                    
                    for i in range(len(obstacle_B)):
                        temp_AB = obstacle_B[i] - obstacle_A[0]
                        temp = temp_AB / np.hypot(temp_AB[0], temp_AB[1])
                        triangle_AB += math.acos(temp)
                        
                    for j in range(len(obstacle_A)):
                        temp_BA = obstacle_A[i] - obstacle_B[0]
                        temp = temp_BA / np.hypot(temp_BA[0], temp_BA[1])
                        triangle_BA += math.acos(temp)
                        
                    triangle_AB = round(triangle_AB, 2)
                    triangle_BA = round(triangle_BA, 2)
                    
                    if triangle_AB == 3.14:
                        return obstacle_B
                    elif triangle_BA == 3.14:
                        return obstacle_A
                    else:
                        return obstacle_A, obstacle_B
                
    def barriers_circle_intersect(obstacle, circle):
        #circle = array(圆心， 半径)
        for i in np.array(len(obstacle)):
            if i != len(obstacle):
                vector_dis = obstacle[i + 1] - obstacle[i]
            else:
                vector_dis = obstacle[i] - obstacle[0]
            # 圆心到边的距离
            distances = np.linalg.norm(np.cross(vector_dis, circle[0])/np.linalg.norm(circle[0]))
            
            if distances < circle[1]:
                print("多边形与圆相交")
                
        print("没有")
    
    def circle_intersect(circle_A, circle_B):
            vector_circle = circle_A - circle_B
            dis = np.hypot(vector_circle[0], vector_circle[1])
            if dis < circle_A[1] + circle_B[1]:
                print("两圆相交")
                
    
            
                
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    