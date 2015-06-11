# @file   FiberSetup.py
"""
.. module:: FiberSetup
   :synopsis: Fiber Definition and fiber_stack definition
.. moduleauthor:: <sebastiana.giani@epfl.ch>
"""
import numpy as np
import math
import random
import ROOT
import Sipm
import MainSimulation


class Fiber(object):
    """Class to define the object fiber.

        Each object fiber is defined by the center coordinates (the attributes Xc and Yc), the
        diameter and the refraction index of the core material.
        All the method of this class are definide here:
               

          """
    def __init__(self, Xc=0, Yc=0, diameter=250e-06, core_index=1.59):

        """The init method is invoked to create a new class instance """ 
        self.Xc = Xc
        self.Yc = Yc
        self.diameter = diameter
        self.core_index = core_index
        self.photons = 0
     
    def getImpact(self, Theta, X0, Y0):
        """Method to calculate the impact parameter.
           Given the initial position of the particle (Theta, X0,Y0) and the coordinate
           of the fiber center, returns the impact parameter of the particle  with respect
           to the fiber axis. This method is invoked by the method :func:`producePhotons`."""
     
        Xp=X0 + math.sin(Theta)*math.sin(Theta)*(self.Xc-X0) + math.sin(Theta)*math.cos(Theta)*(self.Yc-Y0);
        Yp=Y0 + math.sin(Theta)*math.cos(Theta)*(self.Xc-X0) + math.cos(Theta)*math.cos(Theta)*(self.Yc-Y0);
        impact=math.sqrt((self.Xc-Xp)*(self.Xc-Xp)+(self.Yc-Yp)*(self.Yc-Yp))
        #print 'imp', impact,'xp', Xp, 'yp', Yp, self.Xc, self.Yc
        return impact

    def producePhotons(self, Theta, X0, Y0):
        """Generation of photons.
           According to the value of the impact parameter, calculated calling the method :func:`getImpact`,
           a certain number of photons is generetad randomly following the shape of some functions. These functions
           represent the photons distribution obtained by a Geant simulation.
           This function returns a number of photons greater than zero only if the impact parameter is lower
           than tha radius of the fiber"""

        impact=self.getImpact(Theta, X0,Y0)
        #print impact
        #impact=0.000123
        #print self.diameter
        if impact<=self.diameter/2:

           # print impact
            impact=impact*1000000
            if impact>=0 and impact<=25:
                f1=ROOT.TF1("f1","57.5095*exp(-0.5*pow((x-22.1398)/6.16924,2))",0,50)
                number=f1.GetRandom()
            elif impact>25 and impact<=50:
                f1=ROOT.TF1("f1","TMath::Landau(x,18.4867,2.66185,0)*341.192",0,50)
                number=f1.GetRandom()
                
            elif impact>50 and impact<=75:
                f1=ROOT.TF1("f1","TMath::Landau(x,17.9427,2.74043,0)*364.594",0,50)
                number=f1.GetRandom()
                
            elif impact>75 and impact<=100:
                f1=ROOT.TF1("f1","68.0951*exp(-0.5*pow((x-18.178)/4.91197,2))",0,50)
                number=f1.GetRandom()
                
            elif impact>100 and impact<=125:
                f1=ROOT.TF1("f1","59.8287*exp(-0.5*pow((x-12.1788)/4.54820,2))",0,40)
                number=f1.GetRandom()
                
             
            self.photons=int(round(number))
        else:
            self.photons=0

        #print self.photons
    def resetPhotons(self):
        self.photons=0
         


class Setup(object):
    """This class define the geometry of the setup.
       
        Given a certain number of layers, number of fiber per layers, the gap between two
        close fiber in the same layer,usint the class method __init__ a class instance is created
        with these caracheteristics.
        The most important attribute of this class is :attr:`fiber_stack` that representes one matrix of
        fiber objects. For each fiber, a position for the center is assigned in order to define the geometry
        of the simulated setup.
           
           
        All the method of this class are definide here """
    
   
    #def __init__(self, filename, layers=5, nfibers=128, diameter=250e-06, gap_diam=30e-06, ch_widht=0.25e-03, ch_height=1.5e-03):
    def __init__(self, parameter):
        #self.param=MainSimulation.Parameters(filename) 
        self.param = parameter
        self.layers = self.param.layers
        #self.nfibers = nfibers
        #self.diameter = diameter
        #self.gap = gap_diam
        #self.channel_widht = ch_widht
        #self.channel_height = ch_height
        self.nfibers =self.param.nfibers 
        self.diameter = self.param.diameter
        self.gap = self.param.fiber_gap
        self.channel_width = self.param.ch_width
        self.channel_height = self.param.ch_height
        self.channel_array = Sipm.ChannelArray(parameter)
        self.x = -random.random()*self.diameter/2
        self.y = math.sqrt(math.pow(self.diameter,2) - math.pow((self.diameter+self.gap)/2,2))
        self.y0 = self.diameter/2*math.cos(math.asin((self.diameter+self.gap)/2/self.diameter))
         
        self.fiber_stack = []
        """Matrix of fiber objects.

        This matrix represent a stack of fibers, our setup. For each fiber, a position for the center is assigned in order to define the geometry
        of the simulated setup.   """

        pro=[]
        x= self.x
        for i in range (self.nfibers): 
            temp = []               
            
            for j in range (self.layers):
                if j%2==0:
                    temp.append(Fiber(x, 2.0*(j-1.0)*self.y-j*self.y,self.diameter,1.59 ))
                else:
                    temp.append(Fiber(x+(self.diameter+self.gap),(-2.0+j)*self.y,self.diameter,1.59))
               
            x+= self.diameter+self.gap
            pro.append(temp)
        a=np.array(pro).T    #the list of list "pro" is transformed in a numpy array because we need to transpose it.
        self.fiber_stack=a
       
    def simulateParticle(self, Theta, X0,Y0):
        """This method simulates the particle passing through the stack of fibers.

        For each fiber in the stack, the :func:`producePhotons` in the class :class:`Fiber` is called.
        After the photons production,in oder to simulate the signal produced by photons in the detector
        the functions :func:`Sipm.ChannelArray.fillPixels`, :func:`Sipm.ChannelArray.fillChannelArray`, from :mod:`Sipm`, class :class:`Sipm.ChannelArray`
        are invoked."""
        print self.nfibers
        for layers in range(self.layers):
            
            for nfibers in range(self.nfibers):
            #for layers in range(self.layers):
                self.fiber_stack[layers][nfibers].producePhotons(Theta,X0,Y0)
                if self.fiber_stack[layers][nfibers].photons>0:
                    
                    print layers, nfibers, self.fiber_stack[layers][nfibers].Yc
                    print self.fiber_stack[layers][nfibers].photons
         
        for nfibers in range(self.nfibers):
            for layers in range(self.layers):
                 
                self.channel_array.fillPixels(self.fiber_stack[layers][nfibers])

        self.channel_array.fillChannelArray()

    def reset(self):

        self.channel_array.resetArray()
        for nfibers in range(self.nfibers):
            for layers in range(self.layers):
                self.fiber_stack[layers][nfibers].resetPhotons()
        
                 
     
    def checkFiberCrossTalk(self):
         
        pass

    def getObjectChannel(self):
        """This method retuns an object from :mod:`Sipm`, class :class:`ChannelArray`, used to get
        attributes of the class"""

        return self.channel_array    




