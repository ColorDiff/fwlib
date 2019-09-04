#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 19:37:26 2019

@author: Luca Michael Reeb
"""
import numpy as np

class CopySplit():
    
    def __init__(self, copy_n):
        self.copy_n = copy_n
        
    def __call__(self, x):
        return [x.copy() for _ in range(self.copy_n)]
    
class MergeGrid():
    
    def __init__(self, grid_w, grid_h):
        self.grid_w = grid_w
        self.grid_h = grid_h
        
    def __call__(self, *args):
        xs = np.array([*args])
        res = np.concatenate((*xs[:self.grid_w],), axis=1)
        for y in range(1, self.grid_h):
            row = np.concatenate((*xs[y * self.grid_w : (y+1) * self.grid_w],), axis=1)
            res = np.concatenate((res, row), axis=0)
        return res