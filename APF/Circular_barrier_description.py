# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 15:57:57 2021

@author: Tom Wade
"""

import numpy as np


# 圆形单障碍
class Circular_barrier_description(object):
    def __init__(self, origin, circular_barrier_center, circular_barrier_radius):
        self.origin = origin
        self.circular_barrier_center = circular_barrier_center
        self.circular_barrier_distance = circular_barrier_radius

    def circular_barrier(self, origin, circular_barrier_center, circular_barrier_radius):
        vector_OC = circular_barrier_center - origin # O:origin   C:circular_barrier_center
        distance = np.hypot(vector_OC[0], vector_OC[1]) - circular_barrier_radius

        point = distance * vector_OC / np.hypot(vector_OC[0], vector_OC[1]) + origin

        return point
    
"""
circular_barrier_center = np.array([2.0,2.0])
circular_barrier_radius = 10
origin = np.array([0,0])

f = Circular_barrier_description(origin, circular_barrier_center, circular_barrier_radius)
f.circular_barrier(origin, circular_barrier_center, circular_barrier_radius)
"""