# GenerateEvent module


"""
.. module:: GenerateEvent
   :synopsis: Simulation of the event
.. moduleauthor:: Sebastiana Giani <sebastiana.giani@epfl.ch>
"""
import numpy as np
import math
import random
import ROOT
import FiberSetup
import Sipm




class Event:
    """The class Event is the most important class of the simulation. In this class, using the method :func:`writeDataRoot``,
    inside a loop that defines the number of events to generate in the simulation, the function :func"`generateSignalEvent` is invoked.
    ."""

    #def __init__(self, theta_max, spare_channel, method, nEvents, parameter):
    def __init__(self,parameter):
        self.param=parameter
        self.theta_max=self.param.theta_max
        self.spare_channel=self.param.spare_channel 
        self.method=self.param.method
        self.setup=FiberSetup.Setup(parameter)
        self.therarray=[]
        self.events=self.param.nevents
        
    def generateTheta(self):
        """This method generates randomly the theta angle for the particle """
        if self.method==0:
            theta=random.random()*(self.theta_max)*math.pi/180.0
            self.therarray.append(theta)
        return theta

    def generateSignalPosition(self):
        """ This function generates a random position for the particle"""
        
        X0=random.random()*((self.setup.getObjectChannel().channel_number-2*self.spare_channel)*(self.setup.getObjectChannel().channel_width)+self.spare_channel*(self.setup.getObjectChannel().channel_width))
        #print self.setup.getObjectChannel().channel_width
        #print self.setup.getObjectChannel().channel_number 
        return X0    

    def generateSignalEvent(self):
        """This method generates the single event of a particle passing trough a stack of fiber

            given by the theta angle and the x0 position for the particle, the event is generated calling the function
            :func:`FiberSetup.Setup.simulateParticle`. This function is a method of the class Setup. Fot this reason it is called using self.setup
            that is an object of that class.

            """
        
        theta=self.generateTheta()
        self.therarray.append(theta)
        X0=self.generateSignalPosition()
        #print theta, X0
        self.setup.simulateParticle(theta,X0,Y0=0)
        
        

    def writeDataRoot(self):
        """A shorter explanation

        In this method inside a loop,the simulation runs calling the method :func:`generateSignalEvent`

        The events generated are stored in a Tree of a Root file.
        """

        file_result=ROOT.TFile("Result.root","recreate")
        tree=ROOT.TTree("Simul","SimulTree")
        n=np.zeros(self.events,dtype=float)
        p=np.zeros(self.events,dtype=float)
        l=[]
        tree.Branch('theta',n,'theta/D')
        tree.Branch('sig_position',p,'sig_position/D')
       # tree.Branch('photon_angle',l,'photon_angle/D')
        for event in range (self.events):
            print 'event', event
            
            self.generateSignalEvent()
            #ch=self.setup.getObjectChannel().setNChannel(
            print 'end_event'	
            n[event]=self.generateTheta()
            
            
            p[event]=self.generateSignalPosition()
            #print n[event],p[event]
         #return self.generateSignalEvent()
        
            tree.Fill()
            self.setup.reset()
        file_result.Write()
        file_result.Close()
        self.plotResults(p,n)
    def plotResults(self,p,n):
        pass






