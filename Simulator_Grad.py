# Project: Accurate Measurment system
# Program: Simulator with more reality fueatures
#          + Adding gradiant illumination 
#          + Adding normal noise 

# version : 1.3
# date    : 18.05.2022
#---------------------------------------------------------------
from os import system
import cv2
import numpy as np
import time as T
import math


#-------------------------------
# path
path = "D:\ImageSubPixles.png"           # path to sub pixels image file
pathPixels="D:\IMGS\ImgePixels_19_05_3.png"    # path to output pixel image file


#--------- init
system('cls')   
# Create a black image
N_sp_X=3280*16
N_sp_Y=2464*16
Mat=np.zeros((N_sp_Y,N_sp_X),np.uint8)
#img=Image.new('RGB',(N_sp_X,N_sp_Y))


#----------------  input DATA

# real sub pixels information
# center corrdinates in pixles
x0=2483
y0=1401
r0=150

# sub pixles corrdinates
x1=2  #  0 ---> 16
y1=4  #  0 ---> 16                                  
r1=1

# final system corrdinates
Xc=float( x0*16 + x1 )    # Xc=2483 +  2/16  = 2483. 1250
Yc=float( y0*16 + y1 )    # Yc=1401  +  4/16  = 1401.2500
Rc=float( r0*16 + r1 )    # Rc=97   + 1/16   = 97  . 0625

#---- circum points in subpixles representation

#(Xi - Xc)^2 + (Yi - Yc)^2 = Rc^2, 

Fi=float(0.0)

Xi = Rc * math.cos (Fi) + Xc 	
Yi = Rc * math.sin (Fi) + Yc 

#-------------------------------------------
# build circle in sub pixle accuracy
xt=float(Xc-Rc)
yt=float(Yc-Rc)
subpixlesInside=0
c=math.pow(Rc,2)
while xt  <=  Xc+Rc :
    yt=float(Yc-Rc)
    a=math.pow((xt - Xc),2)
    while  yt <= Yc+Rc:
        b=math.pow((yt - Yc),2)
        if(  a + b  <= c  ):
            Mat[math.ceil(yt),math.ceil(xt)]=150
            subpixlesInside+=1
            #print(xt,yt)
        yt+=1
    xt+=1
    print("Sub-Pixles:",subpixlesInside, " Out of 7743641")

#print("Number of Sub-Pixles inside circle",subpixlesInside)
#----------------------------------------------------------------------
#--------------- convert now to pixle resolution ----------------------
def CalcPixelValue(M,xf,yf):
    val=0
    u=xf*16
    v=yf*16
    NoColoredSubPixles=0
    while u<= (xf+1)*16:
        v=yf*16
        while v<= (yf+1)*16:
            if(M[v,u]>20):
                NoColoredSubPixles+=1
            v+=1
        u+=1
    
    if(NoColoredSubPixles> 128 ):
        val=150
    return val
#----------------------------------------------------------------------
# 18.05.2022
def CalcPixelValue_Gradient(M,xf,yf):
    val=0
    u=xf*16
    v=yf*16
    NoColoredSubPixles=0
    while u<= (xf+1)*16:
        v=yf*16
        while v<= (yf+1)*16:
            if(M[v,u]>20):
                NoColoredSubPixles+=1
            v+=1
        u+=1
    val=NoColoredSubPixles
    if(val>255):
        val=255
    return val
#----------------------------------------------------------------------
def CalcPixelValue_Gradient_Noise(M,xf,yf):
    val=0
    u=xf*16
    v=yf*16
    NoColoredSubPixles=0
    while u<= (xf+1)*16:
        v=yf*16
        while v<= (yf+1)*16:
            if(M[v,u]>20):
                NoColoredSubPixles+=1
            v+=1
        u+=1
    #val=NoColoredSubPixles                          # Gradient 0 % noise
    #val=NoColoredSubPixles+ np.random.normal(0,5,1)  # Gradient 10% noise 
    val=NoColoredSubPixles+ np.random.normal(0,10,1)  # Gradient 20% noise 
    if(val>255):
        val=255
    if(val<0):
        val=0
    return val
#----------------------------------------------------------------------
# pixle index
px=x0-r0-1
py=y0-r0-1
# sub-pixle index
sx=0 
sy=0
# pixle value
pv=0
# Pixles Matrix
Mp=np.zeros((2464,3280),np.uint8)
print("Converting to Pixels......")
#
r=0
while( px<x0+r0+1 ):
    py=y0-r0-1
    while( py <  y0+r0+1 ):
        Mp[py,px]=CalcPixelValue_Gradient_Noise(Mat,px,py)
        #print(px,py,Mp[py,px])
        py+=1
    px+=1
print("*** Finish Converting ***")   
#---------------------
# saving section
output=Image.fromarray(Mp)
output.save(pathPixels)
#output=Image.fromarray(Mat)
#print(output)
#output.save(path)

#print("Angle Step Value:",Fs)
#print("Number of steps for each angle step:",j)
#print("Number of Angle steps:",i)
#print(i)




