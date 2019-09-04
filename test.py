# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 19:32:31 2019

@author: Luca Michael Reeb
"""



from pipeline import Pipeline
from ops.transform import *
from ops.parallel import *
from ops.masks import *
import numpy as np

pipe = Pipeline()
#pipe.add(ToGreyscale())

pipe.add(CropRectangle(64, 0, 512, 480))
pipe.add(FFT())
#pipe.add(TukeyWin(512, 480))

pipe_a = Pipeline()
pipe_a.add(AlignedEllipse((480, 512), 1/7, invert=True))
pipe_a.add(IFFT())

pipe_b = Pipeline()
pipe_b.add(AlignedAnnulus((480, 512), 1/20, 1/15, invert=True))
pipe_b.add(IFFT())
pipe_b.add(Clip(0, 255))

pipe_c = Pipeline()
pipe_c.add(Rectangle((480, 512), (240, 0), (480, 420)))
pipe_c.add(IFFT())

pipe_d = Pipeline()
pipe_d.add(Rectangle((480, 512), (0, 256), (350, 512)))
pipe_d.add(IFFT())

pipe.split(CopySplit(4), [pipe_a, pipe_b, pipe_c, pipe_d], MergeGrid(2, 2))
pipe.add(np.uint8)

import cv2

try:
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False
    while rval:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("preview", pipe(gray))
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: 
            break
finally:
    vc.release()
    cv2.destroyWindow("preview")