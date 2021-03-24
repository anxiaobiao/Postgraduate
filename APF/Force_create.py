# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:46:04 2021

@author: Tom Wade
"""

import numpy as np
import math

class Force_create(object):
    def __init__(self, origin, destination, missile, obstacle, range_of_action, obstacle_size):
        self.origin = origin                    #起始位置
        self.destination = destination          #终点位置
        self.missile = missile                  #导弹位置
        self.obstacle = obstacle                #障碍物位置
        self.range_of_action = range_of_action  #斥力作用距离
        
        self.obstacle_size = obstacle_size
    # 引力场  
    def gravitational(self, origin, missile , destination):
        dis_or_des = destination - origin
        distance = np.hypot(dis_or_des[0], dis_or_des[1])
        
        distance_SE = destination - missile     # S:Start   E:End
        k_max = 2
        U_max = k_max * distance
        
        
        
        return distance_SE / U_max
    # 斥力场
    def repulsion(self, missile, obstacle, range_of_action, obstacle_size): 
        obstacle_XY = np.array([0.0, 0.0])
        repulsion_force = np.array([0.0] * int(obstacle_size))
        repulsion_field = np.array([0.0] * 2)
        
        for i in range(obstacle_size) :
            obstacle_XY[0] = obstacle[i][0]
            obstacle_XY[1] = obstacle[i][1]
            vector_MO = missile - obstacle_XY   # M:missile   O:obstalce
            distance_MO = np.hypot(vector_MO[0], vector_MO[1])
            # 确定单位向量
            # modulus = np.hypot(vector_MO[0], vector_MO[1])
            MO_unit_verctor = vector_MO / distance_MO
            
            if distance_MO <= range_of_action:
                t = - math.pow(distance_MO / range_of_action/3, 2)
                repulsion_force[i] = math.exp(t)
            else:
                repulsion_force[i] = 0.0
                
            repulsion_field[0] = repulsion_field[0] + repulsion_force[i] * MO_unit_verctor[0]
            repulsion_field[1] = repulsion_field[1] + repulsion_force[i] * MO_unit_verctor[1]
            
            #i = i + 1
        return repulsion_field
    

    # 合力长
    def join_force_field(self):
        gravitational_field = self.gravitational(self.origin, self.missile, self.destination)
        repulsion_field = self.repulsion(self.missile, self.obstacle, self.range_of_action, self.obstacle_size)
        
        # print(gravitational_field + repulsion_field)
        return gravitational_field + repulsion_field

"""
origin = np.array([0, 0])  # 起点
obstacle = np.array([[34.45, 51.67], [51.05, 25.52], [20, 20]])   # 障碍物
obstacle_size = int(len(obstacle) / 2) # 障碍物个数
# obstacle = obstacle.reshape(obstacle_size,2)
destination = np.array([100.0, 100.0])   # 终点
missile = np.array([35.0, 50.0])   # 导弹位置
f = Force_create(origin, destination, missile, obstacle, 10, obstacle_size)
result = f.join_force_field()
print(result)
"""