# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 11:05:15 2021

@author: Tom Wade
"""

import numpy as np


# 凸多边形单障碍
class Convex_polygon_barrier_description(object):
    def __init__(self, origin, convex_polygon_barrier_point):
        self.origin = origin
        self.convex_polygon_barrier_point = convex_polygon_barrier_point
    
    def convex_polygon_barrier(self, origin, convex_polygon_barrier_point):
        point = np.array([0.0] * len(convex_polygon_barrier_point) * 2).reshape(len(convex_polygon_barrier_point), 2)
        distance_min = np.hypot((origin - convex_polygon_barrier_point[0])[0], (origin - convex_polygon_barrier_point[0])[1])
        indix = 0
        for i in range(len(convex_polygon_barrier_point)):
            if i == len(convex_polygon_barrier_point)-1:
                j = 0
            else:
                j = i+1
            
            vector_OI = origin - convex_polygon_barrier_point[i]  # O:origin   I:i
            vector_OJ = origin - convex_polygon_barrier_point[j]  # O:origin   J:j
            barrier_distance = convex_polygon_barrier_point[j] - convex_polygon_barrier_point[i]
            Tau = (np.dot(origin, barrier_distance) - np.dot(convex_polygon_barrier_point[i], barrier_distance)) / (np.dot(barrier_distance, barrier_distance))
            extreme_point = convex_polygon_barrier_point[i] + Tau * barrier_distance
            
            if Tau >= 0 and Tau <= 1:
                point[i] = extreme_point.T
            elif np.hypot(vector_OI[0], vector_OI[1]) <= np.hypot(vector_OJ[0], vector_OJ[1]):
                point[i] = convex_polygon_barrier_point[i]
            else:
                point[i] = convex_polygon_barrier_point[j]

            distance = np.hypot((origin - point[i])[0], (origin - point[i])[1])
            if distance < distance_min:
                indix = i
            
            
            
        # print(point[indix])
        return point[indix]
    
"""
origin = np.array([0,0])
# convex_polygon_barrier_point = np.array([3.0,2.0, 2.0,3.0, 3.0,4.0, 4.0,3.0, 4.0,2.0]).reshape(5,2)
convex_polygon_barrier_point = np.array([[20,20], [20,30], [30,40], [40,30], [40,20]])

f = Convex_polygon_barrier_description(origin, convex_polygon_barrier_point)
f.convex_polygon_barrier(origin, convex_polygon_barrier_point)
"""











           