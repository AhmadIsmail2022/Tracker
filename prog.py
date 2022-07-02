#!/usr/bin/python
# -*- coding: latin-1 -*-
#--------------------------------------------------------------------------------
#  Program : Application for microcontroller system to implmenet 
#            Algorithm for estimation center corrdinates in Sub-Pixel Accuracy.
#
#  Created : 08.05.2022
#  Version : 1.3.1
#  Date    : 06.06.2022

#-------------------------------------------------------------------------------


import CResolver
#import picamera
#import picamera.array
from time import sleep
#from picamera import PiCamera
#from PIL import Image
from io import BytesIO
import time
import cv2
#-------------------------------------------------------------------------------
PathFile="gg.png"
Resolver = CResolver.CRelover()
Resolver.__init__()
img=cv2.imread(PathFile)
Resolver.Reset()
Resolver.setImage(img)
Resolver.ProcessImg()
t0=time.time()
Resolver.Print()

# --------------------------------------------------- 
