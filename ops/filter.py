#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 00:26:42 2019

@author: Luca Michael Reeb
"""
import numpy as np
from scipy.signal import convolve2d, gaussian

class GaussianBlur:
    
    def __init__(self, ksize=3, sigma=1):
        self.ksize=ksize
        self.sigma=sigma
        gkern1d = gaussian(ksize, std=sigma).reshape(ksize, 1)
        self.kernel = np.outer(gkern1d, gkern1d)
        
        
    def __str__(self):
        return "GaussianBlur(ksize={0}, sigma={1})".format(self.ksize, self.sigma)
    
    def __call__(self, im):
        return convolve2d(im, self.kernel, mode='same')
    
if __name__ == '__main__':
    g = GaussianBlur(ksize=21, sigma=5)