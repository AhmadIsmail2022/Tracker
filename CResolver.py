
import math
import time as t
import Constants as CONST
import numpy as np

#-----------------------------------------------------------------------
class CResults:
    def __init__(self):
        self.Xc=0
        self.Yc=0
        self.Rc=0
        self.ProcessingTime=0
        self.NumberofCircumPoints=0

    def Print(self):
        print("Results Circle Parameters:")
        print ("                Xc     {:0.4f}".format( self.Xc))
        print ("                Yc     {:0.4f}".format( self.Yc))
        print ("                Rc     {:0.4f}".format( self.Rc))
        print ("                Points {}"   .format( self.NumberofCircumPoints))
        print ("                Time   {:0.9f}".format( self.ProcessingTime))

#-----------------------------------------------------------------------
class CRelover:
    def __init__(self):
        self.name= "Camera Resolver Class"
        self.version="1.3.2"
        self.date="06.06.2022"
        self.Reset()
        self.Results=CResults()
    
    def Reset(self):
        self.Xp =[]
        self.Yp =[]
        self.Xp.append(0)
        self.Yp.append(0)
        self.NXp=[]
        self.NYp=[]
        self.Nn=0
    
    def Filter(self):
        i=1
        self.Nn=0
        while(i<self.Cp):
            if(self.Xp[i]%2==1 and self.Yp[i]%2==1):  # take only even columns
                self.NXp.append(self.Xp[i])
                self.NYp.append(self.Yp[i])
                self.Nn+=1
            i+=1
        self.Results.NumberofCircumPoints=self.Nn
        return 0
    
    
    def Print(self):
        print("Program: ",self.getName())  
        print("Version: ",self.version)
        print("Update_: ",self.date)  
        self.Results.Print() 

    def getName(self):
        return self.name
      
    def ProcessImg(self):
        t0=t.time()
        self.FirstPoint=self.Find_FirstPoint()
        self.find_circumferencePoints()
        self.Filter()  # 20.06.2022
        self.do_Calcs_Filtered()
        t1=t.time()
        self.Results.ProcessingTime=t1-t0

    def setImage(self,ImageInput):
         # since the lazer in system is red color
        self.Img = ImageInput[:, :, 0] # get the red layer of image
  
    def Find_FirstPoint(self):
        x=0
        while x<CONST.W:
            y=0
            while y<CONST.H:
                if self.Img[y,x] > CONST.Black_th:
                    return x,y  
                y+=CONST.Rc
            x+=CONST.Rc 
        return 0,0

    #------------------------------------
    # check if new point is not repeated in last three points found array
    def IsUnique(self, x,y):
        i=0
        j=self.Cp
        while i<2 and j>2:
            if( x == self.Xp[j-i-1] and y==self.Yp[j-i-1]):
                return 0 # not unique
            i+=1
        return 1 # case unique
    #------------------------------------
    def IsPointCircumference(self,x,y):
        # assum point at circum
        res=0
        NoColoredCells=0
        if  self.Img[y,x]  > CONST.Black_th:
            NoColoredCells+=1
        else:
            return 0
        if  self.Img[y+1,x] > CONST.Black_th:
            NoColoredCells+=1
        if  self.Img[y,x+1] > CONST.Black_th:
            NoColoredCells+=1
        if self.Img[y-1,x] > CONST.Black_th:
            NoColoredCells+=1
        if self.Img[y,x-1] > CONST.Black_th:
            NoColoredCells+=1
        if (NoColoredCells<5 and  NoColoredCells >1):
            res=1;                       
        return res
    #------------------------------------
    def find_circumferencePoints(self):
        x0,y0=self.FirstPoint
       
        r=self.IsPointCircumference(x0,y0)
        #print("start point circumference:")
        #print(r)
        xs=x0
        ys=y0
        if( not r==1):
            while not self.IsPointCircumference(xs,ys) :
                ys-=1
        # corrdinates of base circum point
        #print(xs,ys)
        # xs,ys  start point of calculation !! no change
        # current point
        self.Xp.append(xs)
        self.Yp.append(ys)
        self.Cp=2
        xt=xs
        yt=ys
        # indicator to finish all point
        State=0
        while State==0:
            # move up y-1
            if(self.IsPointCircumference(xt,yt-1) and self.IsUnique(xt,yt-1)):
                yt=yt-1
            else:
                # move right x+1
                if(self.IsPointCircumference(xt+1,yt) and self.IsUnique(xt+1,yt)):
                    xt=xt+1
                else:
                    #move  y up and x right
                    if(self.IsPointCircumference(xt+1,yt-1) and self.IsUnique(xt+1,yt-1)):
                        xt=xt+1
                        yt=yt-1
                    else:
                        # move down y+1
                        if(self.IsPointCircumference(xt,yt+1) and  self.IsUnique(xt,yt+1)):
                            yt=yt+1
                        else:
                            #move  y down and x right
                            if(self.IsPointCircumference(xt+1,yt+1) and self.IsUnique(xt+1,yt+1)):
                                xt=xt+1
                                yt=yt+1
                            else:
                                #move  y down and x left
                                if(self.IsPointCircumference(xt-1,yt+1) and self.IsUnique(xt-1,yt+1)):
                                    xt=xt-1
                                    yt=yt+1 
                                else:
                                    #move left
                                    if(self.IsPointCircumference(xt-1,yt)and self.IsUnique(xt-1,yt)):
                                        xt=xt-1
                                    else:
                                    #move  y up and x left
                                        if(self.IsPointCircumference(xt-1,yt-1) and self.IsUnique(xt-1,yt-1)):
                                            xt=xt-1
                                            yt=yt-1 
                                        else:
                                            State=-1
                                            return -1
            if (State==0): # check normal search,check no error
                if (xt==xs and yt==ys): # finish loop , find all points circum
                    State=1
                else: # found new point 
                    self.Xp.append(xt)
                    self.Yp.append(yt)
                    self. Cp+=1
        self.Results.NumberofCircumPoints=self.Cp
        return self.Cp
    #-----------------------------------
    def Min(self,n):
        j=1
        mx=self.Xp[1]
        my=self.Yp[1]
        while(j<=n):
            if(self.Xp[j]<mx):
                mx=self.Xp[j]
            if(self.Yp[j]<my):
                my=self.Yp[j]
            j+=1
        return mx,my
    
    def Min_Filter(self,n):
        j=0
        mx=self.NXp[0]
        my=self.NYp[0]
        while(j<n):
            if(self.NXp[j]<mx):
                mx=self.NXp[j]
            if(self.NYp[j]<my):
                my=self.NYp[j]
            j+=1
        return mx,my
    #-----------------------------------
    def Offest(self,n,xo,yo):
        j=1
        while(j<=n):
            self.Xp[j]=float(self.Xp[j]-xo)
            self.Yp[j]=float(self.Yp[j]-yo)
            j+=1
    
    def Offest_Filter(self,n,xo,yo):
        j=0
        while(j<n):
            self.NXp[j]=float(self.NXp[j]-xo)
            self.NYp[j]=float(self.NYp[j]-yo)
            j+=1

#-----------------------------------
    def do_Calcs_Filtered(self):
        n=self.Results.NumberofCircumPoints
        if(n<=0):
             return -1,-1,-1
        #n-=1
        xo,yo=self.Min_Filter(n)
        #xo,yo= np.min(self.Xp),np.min(self.Yp)
        self.Offest_Filter(n,xo,yo)
                
        sx=float(sum(self.NXp))
        sx2=float(sum(np.power(self.NXp,2)))       
        sx3=float(sum(np.power(self.NXp,3)))
        sy=float(sum(self.NYp))
        sy2=float(sum(np.power(self.NYp,2)))       
        sy3=float(sum(np.power(self.NYp,3)))
        sxy= float(sum(np.multiply(self.NXp,self.NYp)))
        sx2y= float(sum(np.multiply(np.power(self.NXp,2),self.NYp)))
        sxy2= float(sum(np.multiply(self.NXp,np.power(self.NYp,2))))
        a1=float(sx*sx)
        tmp=float(n*sx2)
        a1=float(a1-tmp)
        a1=float(a1*2) #----a1
        b1=float(sx*sy)
        tmp=float(n*sxy)
        b1=float(b1-tmp)
        b1=float(2*b1) #------b1
        a2=b1
        b2=float(sy*sy)
        tmp=float(n*sy2)
        b2=float(b2-tmp)
        b2=float(b2*2) #-------b2
 
        c1=float(sx2*sx) 
        t1=float(n*sx3)
        t2=float(sx*sy2)
        t3=float(n*sxy2)
        c1=float(c1-t1)
        c1=float(c1+t2)
        c1=float(c1-t3) #----c1

        c2=float(sx2*sy)
        t1=float(n*sy3)
        t2=float(sy*sx2)
        t3=float(n*sx2y)
        c2=float(c2-t1)
        c2=float(c2+t2)
        c2=float(c2-t3) #-----c2

        xc=float(c1*b2)
        xc=float(xc-c2*b1) 
        t=float(a1*b2)
        t=float(t-a2*b1)
        xc=float(xc/t)

        yc=float(a1*c2 - a2*c1) 
        yc=float(yc/(a1*b2-a2*b1))

        #--- calc radius
        rc=sx2-2*xc*sx+n*xc*xc+sy2-2*yc*sy+n*yc*yc
        rc=math.sqrt(rc/n)
        self.Results.Xc=xc+xo+CONST.Calib_X
        self.Results.Yc=yc+yo+CONST.Calib_Y
        self.Results.Rc=rc+CONST.Calib_R
        
    def do_Calcs(self):
        n=self.Results.NumberofCircumPoints
        if(n<=0):
             return -1,-1,-1
        n-=1
        xo,yo=self.Min(n)
        #xo,yo= np.min(self.Xp),np.min(self.Yp)
        self.Offest(n,xo,yo)
                
        sx=float(sum(self.Xp))
        sx2=float(sum(np.power(self.Xp,2)))       
        sx3=float(sum(np.power(self.Xp,3)))
        sy=float(sum(self.Yp))
        sy2=float(sum(np.power(self.Yp,2)))       
        sy3=float(sum(np.power(self.Yp,3)))
        sxy= float(sum(np.multiply(self.Xp,self.Yp)))
        sx2y= float(sum(np.multiply(np.power(self.Xp,2),self.Yp)))
        sxy2= float(sum(np.multiply(self.Xp,np.power(self.Yp,2))))
        a1=float(sx*sx)
        tmp=float(n*sx2)
        a1=float(a1-tmp)
        a1=float(a1*2) #----a1
        b1=float(sx*sy)
        tmp=float(n*sxy)
        b1=float(b1-tmp)
        b1=float(2*b1) #------b1
        a2=b1
        b2=float(sy*sy)
        tmp=float(n*sy2)
        b2=float(b2-tmp)
        b2=float(b2*2) #-------b2
 
        c1=float(sx2*sx) 
        t1=float(n*sx3)
        t2=float(sx*sy2)
        t3=float(n*sxy2)
        c1=float(c1-t1)
        c1=float(c1+t2)
        c1=float(c1-t3) #----c1

        c2=float(sx2*sy)
        t1=float(n*sy3)
        t2=float(sy*sx2)
        t3=float(n*sx2y)
        c2=float(c2-t1)
        c2=float(c2+t2)
        c2=float(c2-t3) #-----c2

        xc=float(c1*b2)
        xc=float(xc-c2*b1) 
        t=float(a1*b2)
        t=float(t-a2*b1)
        xc=float(xc/t)

        yc=float(a1*c2 - a2*c1) 
        yc=float(yc/(a1*b2-a2*b1))

        #--- calc radius
        rc=sx2-2*xc*sx+n*xc*xc+sy2-2*yc*sy+n*yc*yc
        rc=math.sqrt(rc/n)
        self.Results.Xc=xc+xo+CONST.Calib_X
        self.Results.Yc=yc+yo+CONST.Calib_Y
        self.Results.Rc=rc+CONST.Calib_R
        
    #-----------------------------------
    
