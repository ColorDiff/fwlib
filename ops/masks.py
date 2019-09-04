#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 23:04:09 2019

@author: Luca Michael Reeb
"""


from abc import ABC
from ops.util import mask_annulus, mask_ellipse, mask_rect

class MaskOperation(ABC):
    
    def __call__(self, im):
        im[self.mask] = 0
        return im

class Annulus(MaskOperation):
    
    def __init__(self, shape, position, radii_inner, radii_outer, invert=False):
        self.shape = shape
        self.position = position
        self.radii_inner = radii_inner
        self.radii_outer = radii_outer
        self.invert = invert
        self.mask = mask_annulus(self.shape, 
                                 self.position, 
                                 self.radii_inner, 
                                 self.radii_outer)
        if not self.invert:
            self.mask = ~self.mask
        
    def __str__(self):
        s = "Annulus(shape={0}, position={1}, radii_inner={2}"
        s += "radii_outer={3}, invert={4})"
        return s.format(self.shape, self.position,
                        self.radii_inner, self.radii_outer,
                        self.invert)
    
class AlignedAnnulus(MaskOperation):
    
    def __init__(self, shape, ratio_inner, ratio_outer, invert=False):
        radii_inner = (shape[0] * ratio_inner, shape[1] * ratio_inner)
        radii_outer = (shape[0] * ratio_outer, shape[1] * ratio_outer)
        position = (int(shape[0] / 2), int(shape[1] / 2))
        self.annulus = Annulus(shape, position, radii_inner, radii_outer, invert=invert)
        
    def __str__(self):
        return str(self.annulus)
    
    def __call__(self, im):
        return self.annulus(im)
    
    

class Ellipse(MaskOperation):
    
    def __init__(self, shape, position, radii, invert=False):
        self.shape = shape
        self.position = position
        self.radii = radii
        self.invert = invert
        self.mask = mask_ellipse(shape, position, radii)
        if not invert:
            self.mask = ~self.mask
            
    def __str__(self):
        s = "Ellipse(shape={0}, position={1}, radii={2}, invert={3})"
        return s.format(self.shape, self.position,
                        self.radii, self.invert)
        
class AlignedEllipse(MaskOperation):
    
    def __init__(self, shape, radii_ratio, invert=False):
        radii = (shape[0] * radii_ratio, shape[1] * radii_ratio)
        position = (int(shape[0] / 2) , int(shape[1] / 2))
        self.ellipse = Ellipse(shape, position, radii, invert=invert)
        
    def __str__(self):
        return str(self.ellipse)
    
    def __call__(self, im):
        return self.ellipse(im)
    
class Rectangle(MaskOperation):
    
    def __init__(self, shape, position, size, invert=False):
        self.shape = shape
        self.position = position
        self.size = size
        self.invert = invert
        self.mask = mask_rect(shape, position, size)
        if not invert:
            self.mask = ~self.mask
    
    def __str__(self):
        s = "Rectangle(shape={0}, position={1}, size={2}, invert={3})"
        return s.format(self.shape, self.position,
                        self.size, self.invert)
        
class AlignedRectangle(MaskOperation):
    
    def __init__(self, shape, size_ratio, invert=False):
        size = (shape[0] * size_ratio, shape[1] * size_ratio)
        position = (int(shape[0] / 2) , int(shape[1] / 2))
        self.rect = Rectangle(shape, position, size, invert=invert)
        
    def __str__(self):
        return str(self.rect)
    
    def __call__(self, im):
        return self.rect(im)
    
class MaskWrapper:
    
    def __init__(self, mask_cls, *init_args, **init_kwargs):
        self.mask_cls = mask_cls
        self.set_params(*init_args, **init_kwargs)
        
    def __call__(self, im):
        return self.inst(im)
    
    def __str__(self):
        return str(self.inst)
        
    def set_params(self, *args, **kwargs):
        self.inst = self.mask_cls(*args, **kwargs)
    
    
if __name__ == '__main__':
    shape = (1000, 1200)
    position = (int(shape[0] / 2), int(shape[1] / 2))
    a = AlignedAnnulus(shape, 1/15, 1/7, invert=True)
    import numpy as np
    import matplotlib.pyplot as plt
    im = np.ones(shape)
    plt.imshow(a(im))
    plt.show()
    print(a)