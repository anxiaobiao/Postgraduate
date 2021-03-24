# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 17:03:19 2021

@author: Tom Wade
"""

import numpy as np
import math
from Force_create import Force_create as FC

class Circle_APF(object):
    def __init__(self, origin, destination, missile, obstacle, range_of_action, obstacle_size):
        self.origin = origin                    #起始位置
        self.destination = destination          #终点位置
        self.missile = missile                  #导弹位置
        self.obstacle = obstacle                #障碍物位置
        self.range_of_action = range_of_action  #斥力作用距离
        
        self.obstacle_size = obstacle_size
        
    def repulsion(self, missile, obstacle, range_of_action, obstacle_size):
        obstacle_XY = np.array([0.0, 0.0])
        repulsion_force = np.array([0.0] * int(obstacle_size))
        repulsion_field = np.array([0.0] * 2 * int(obstacle_size)).reshape(int(obstacle_size), 2)
        
        for i in range(obstacle_size) :
            obstacle_XY[0] = obstacle[i][0]
            obstacle_XY[1] = obstacle[i][1]
            vector_MO = missile - obstacle_XY   # M:missile   O:obstalce
            distance_MO = np.hypot(vector_MO[0], vector_MO[1])
            # 确定方向向量
            # modulus = np.hypot(vector_MO[0], vector_MO[1])
            MO_unit_verctor = vector_MO / distance_MO
            
            if distance_MO <= range_of_action:
                t = - math.pow(distance_MO / range_of_action/3, 2)
                repulsion_force[i] = math.exp(t)
            else:
                repulsion_force[i] = 0.0
                
            repulsion_field[i][0] = repulsion_force[i] * MO_unit_verctor[0]
            repulsion_field[i][1] = repulsion_force[i] * MO_unit_verctor[1]
            
            #i = i + 1
        return repulsion_field
        
    def circle_APF(self, origin, destination, missile, obstacle, range_of_action, obstacle_size):
        repulsion_field = self.repulsion(missile, obstacle, range_of_action, obstacle_size)
        repulsion_field_postive = repulsion_field_negative = repulsion_field
        force_circle = np.array([0.0] * 2)
        
        for i in range(len(repulsion_field)):
            repulsion_field_postive[i][0] = -repulsion_field[i][1]
            repulsion_field_postive[i][1] = repulsion_field[i][0]
            
            repulsion_field_negative[i][0] = repulsion_field[i][1]
            repulsion_field_negative[i][1] = -repulsion_field[i][0]
        
        # 确定航行方向单位向量
        vector = FC(origin, destination, missile, obstacle, range_of_action, obstacle_size).join_force_field()
        #vector = FC(origin, destination, missile, obstacle, range_of_action, obstacle_size).join_force_field()

        
        vector = vector / np.hypot(vector[0], vector[1])
        
        # 确定环流方向
        for i in range(len(repulsion_field)):
            if np.dot(vector, repulsion_field_postive[i]) > 0 or (np.dot(vector, repulsion_field_postive[i]) == 0 and -np.dot(vector,repulsion_field[i]) < 0):
                force_circle += repulsion_field_postive[i]
            elif np.dot(vector, repulsion_field_negative[i]) > 0 or (np.dot(vector, repulsion_field_negative[i]) == 0 and -np.dot(vector,repulsion_field[i]) > 0):
                force_circle += repulsion_field_negative[i]
        
        force_traditional = FC(origin, destination, missile, obstacle, range_of_action, obstacle_size).gravitational(origin, missile, destination)
        force_repulsion = FC(origin, destination, missile, obstacle, range_of_action, obstacle_size).repulsion(missile, obstacle, range_of_action, obstacle_size)
        # 确定参数
        distance_XY = obstacle - missile
        distance = np.hypot(distance_XY[0], distance_XY[1])
        parameter = 1 / distance
        
        join_repulsion = parameter * force_circle + (1 - parameter) * force_repulsion
        
        # print(parameter * force_circle + (1 - parameter) * force_traditional)
        return join_repulsion + force_traditional
        
        
"""
origin = np.array([0, 0])  # 起点
obstacle = np.array([[34.45, 51.67], [51.05, 25.52], [20, 20]])   # 障碍物
obstacle_size = int(len(obstacle) / 2) # 障碍物个数
# obstacle = obstacle.reshape(obstacle_size,2)
destination = np.array([100.0, 100.0])   # 终点
missile = np.array([0.0, 0.0])   # 导弹位置
f = Circle_APF(origin, destination, missile, obstacle, 1, obstacle_size)
result = f.circle_APF(origin, destination, missile, obstacle, 1, obstacle_size)  
print(result)
"""