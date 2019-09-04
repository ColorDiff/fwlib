#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:46:25 2019

@author: Luca Michael Reeb
"""
import numpy as np

def mask_ellipse(shape, position, radii):
    '''Parameters expected in y, x order'''
    a, b = radii
    y, x = position
    yy, xx = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]))
    yy_shifted = yy - y
    xx_shifted = xx - x
    return (yy_shifted ** 2 / a ** 2 + xx_shifted ** 2 / b ** 2 < 1).T
    
def mask_annulus(shape, position, radii_inner, radii_outer):
    '''Parameters expected in y, x order'''
    inner = mask_ellipse(shape, position, radii_inner)
    outer = mask_ellipse(shape, position, radii_outer)
    return outer & ~inner

def mask_rect(shape, position, size):
    '''Parameters expected in y, x order, position is the center'''
    mask = np.zeros(shape)
    width, height = size
    c_y, c_x = position
    mask[int(c_y - width / 2) : int(c_y + width / 2),
         int(c_x - height / 2) : int(c_y + height / 2)] = 1
    return mask

def tukeywin2d(shape, alpha=0.3):
    wnd_y = tukeywin(shape[0], alpha=alpha)
    wnd_x = tukeywin(shape[1], alpha=alpha)
    xx, yy = np.meshgrid(wnd_x, wnd_y)
    return (xx * yy)


def normalize_spec(spectrum):
    return 20 * np.log(1 + np.abs(spectrum))
    

def tukeywin(window_length, alpha=0.3):
    '''The Tukey window, also known as the tapered cosine window, can be regarded as a cosine lobe of width \alpha * N / 2
    that is convolved with a rectangle window of width (1 - \alpha / 2). At \alpha = 1 it becomes rectangular, and
    at \alpha = 0 it becomes a Hann window.
 
    We use the same reference as MATLAB to provide the same results in case users compare a MATLAB output to this function
    output
 
    Reference
    ---------
    http://www.mathworks.com/access/helpdesk/help/toolbox/signal/tukeywin.html
 
    '''
    # Special cases
    if alpha <= 0:
        return np.ones(window_length) #rectangular window
    elif alpha >= 1:
        return np.hanning(window_length)
 
    # Normal case
    x = np.linspace(0, 1, window_length)
    w = np.ones(x.shape)
 
    # first condition 0 <= x < alpha/2
    first_condition = x<alpha/2
    w[first_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[first_condition] - alpha/2) ))
 
    # second condition already taken care of
 
    # third condition 1 - alpha / 2 <= x <= 1
    third_condition = x>=(1 - alpha/2)
    w[third_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[third_condition] - 1 + alpha/2))) 
 
    return w

if __name__ == '__main__':
    #mask = mask_ellipse((100, 100), (50, 50), (10, 25))
    mask = mask_annulus((100, 100), (50, 50), (10, 25), (20, 30))
    #mask = mask_rect((100, 100), (50, 50), (50, 80))
    import matplotlib.pyplot as plt
    plt.imshow(mask)
    plt.show()