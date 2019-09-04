#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 19:53:18 2019

@author: Luca Michael Reeb
"""
import numpy as np
from scipy import ndimage
from .util import tukeywin2d

class TukeyWin:
    
    def __init__(self, width, height, alpha=0.3, inverse=False):
        self.window = tukeywin2d((height, width), alpha=alpha)
        self.inverse = inverse
        if inverse:
            self.window = 1 - self.window
        
    def __call__(self, x):
        return x * self.window
    
    
class FFT:
    
    def __init__(self):
        pass
    
    def __call__(self, x):
        return np.fft.fftshift(np.fft.fft2(x))
    
class IFFT:
    
    def __init__(self):
        pass
    
    def __call__(self, x):
        return np.fft.ifft2(np.fft.fftshift(x)).real
    
class Clip:
    
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        
    def __call__(self, x):
        return np.clip(x, self.lower, self.upper)
    
class ToGreyscale:
    
    def __call__(self, x):
        return np.dot(x[...,:3], [0.2989, 0.5870, 0.1140])
    
class CropRectangle:
    
    def __init__(self, pos, w, h):
        self.y, self.x = pos
        self.w = w
        self.h = h
        
    def __call__(self, x):
        return x[self.y : self.y + self.h, self.x : self.x + self.w]
    
    
class Zoom:
    
    def __init__(self, fac):
        self.fac = fac
        
    def __call__(self, x):
        return ndimage.zoom(x, self.fac)