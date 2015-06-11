# Sipm module

"""
.. module:: Sipm
   :synopsis: Detector definition
.. moduleauthor:: Sebastiana Giani <sebastiana.giani@epfl.ch>
"""
import numpy as np
import math
import random
import ROOT
from AngularDistribution import choose_angle_from_distribution
#import AngularDistribution
import FiberSetup



class ChannelArray(object):
    """Class to describe the detector

         The SiPM detector is described as an array of channels. The number of channel is given by the attribute
         channel_number.For each channel the dimentions are defined. Each channel consists of a certain number of pixels,
         whose dimensions are defined also with some class attributes. The most important attibutes of the class are:
         the list self.pixels, a matrix of boolean value. All the elements, by default, are assigned as False. The
	 value becames True if a pixel is fired by the photon.
	 the array pixel_lit_per_channel,an array with a size given by the total number oh channel. The elements, equal to zero by default,
         are filled with the nymber of pixels fired per channel.
    """
      
    #def __init__(
    #        self, name="Sipm", channel_number=128, channel_width=250e-06,
    #        channel_height=1.5e-03, dead_zone=5e-06, epoxy=120e-06, pixel_x_size=4, pixel_y_size=20,
    #        prob_pde=0.25):
    def __init__(self, parameter):
        
        self.param=parameter
        
        #self.channel_number = channel_number
        self.channel_number = self.param.channel_number
      
        # Note these are values shared by all the channels inside this channel array
        self.channel_width = self.param.ch_width
        self.channel_height = self.param.ch_height
        #self.channel_width = channel_width
        #self.channel_height = channel_height
        #self.dead_zone = dead_zone
        #self.epoxy = epoxy
        #self.prob_pde = prob_pde
        #self.pixel_x_size = pixel_x_size
        #self.pixel_y_size = pixel_y_size
        self.dead_zone = self.param.dead_zone
        self.epoxy = self.param.epoxy
        self.prob_pde = self.param.prob_pde
        self.pixel_x_size =self.param.pixel_x_size
        self.pixel_y_size = self.param.pixel_y_size
        self.pixel_width = self.channel_width/self.pixel_x_size
        self.pixel_height = self.channel_height/self.pixel_y_size
        self.epoxy_index = self.param.epoxy_index
        

        self.pixels = [[ False for j in range(self.pixel_y_size)] for i in range(self.pixel_x_size*self.channel_number)]
        #print len( self.pixels)
        #print self.pixel_x_size*self.channel_number
        #self.pixels = [[ False for j in range(4)] for i in range(3)]
        # containing all the pixels

        self.pixel_lit_per_channel = np.zeros(self.channel_number, dtype=int)
        #print self.channel_number
    def fillPixels(self, Fiber):
        """
        Given a fiber , this method return the position of the pixel fired by photons

        This method, calculating the position of the photon when it arrives at the SiPM. According to the position,
        the correspondant pixel in the channel is fired, with a probability given by the Photon Detection Efficiency (pde),
        A random number is generated ( between 0 an 1 uniformly); if this number is lower than the pde value, the pixel is
        fired and the correspondant element in the list pixels is assigned as True. This method is called in the function :func:`simulateParticle`,
        from :mod:`FiberSetup`, :class:`Setup`.
        
        """
        # Recover number of photons produced by the fiber        
        photons =Fiber.photons
        # For all the produced photons, generate a random position in the fiber
        for i in range (photons):
            
            position = self.getPhotonPosition(Fiber) 
            # beware this position is in coordinates, the following step is to find the corresponding pixel
            
            x_pixel = int(position[0]/self.pixel_width)
            y_pixel = int(position[1]/self.pixel_height)

           # print  x_pixel,  y_pixel
            if x_pixel<(self.pixel_x_size*self.channel_number) and x_pixel>=0 and  y_pixel<self.pixel_y_size and y_pixel>=0:
                if random.random > self.prob_pde:
                    self.pixels[x_pixel][y_pixel]= True

    def getPhotonPosition(self, Fiber):
        """
        Given a Fiber, returns  a  position for the photon. 

        .. warning::

                This method is not part of the Fiber class because it also takes into account the epoxy 
                thickness between the fiber and  the channel, so an additionnal diffraction effects has to be taken 
		into account.
        The position of the photon in the fiber surface is generated randomly. In order to  calculate the position in the space
        the angle of emission is computed calling the function :func:`getThetaPrime`.
	     

        """
        # Recover values of the current fiber
        FCx, FCy, diameter = Fiber.Xc, Fiber.Yc, Fiber.diameter

        phi=random.random()*math.pi
        phi_prime=random.random()*math.pi
        radius=random.random()*diameter/2.
        theta_prime=self.getThetaPrime(radius)
        xp=FCx+radius*math.cos(phi)+math.cos(phi_prime)*math.sin(theta_prime)*self.epoxy
        yp=FCy+radius*math.sin(phi)+self.channel_height/2.0+math.sin(phi_prime)*math.sin(theta_prime)*self.epoxy

        return [xp, yp]

    def getThetaPrime(self,radius): #it has to be modified using a module?
        """The emission angle of photons is calculated.

	   The angle is calculated calling the function :func:`AngularDistribution.choose_angle_from_distribution`, from :mod:`AngularDistribution`.
	   The angle of emission is then recalculated taking into account the different refraction index between fiber and the epoxy layer,
	   used to fix the Sipm detector"""
        core_index = FiberSetup.Fiber().core_index
        angle_emission = choose_angle_from_distribution(radius)
        theta_prime = math.asin(core_index/ self.epoxy_index*math.sin(angle_emission)) # The angle of emission after the epoxy layer calculated with the Snell law.
        return theta_prime

    def fillChannelArray(self):
        """
        Method to interface with the C++ class

        It fills the pixel_lit_per_channel array according to the pixels array.If a pixel is fired (an element of the pixels matrix has the value 'True',
        the corresponding channel is calculated and the number of pixels fired of that channel is incremented by one.
        """
        for j in range (self.pixel_y_size):
            for i in range (self.pixel_x_size*self.channel_number):
                if self.pixels[i][j]==True:
                    self.pixel_lit_per_channel[i/4] += 1  
        #print self.pixel_lit_per_channel
        #print self.pixel_x_size*self.channel_number 

    def resetArray(self):
        """
        Method to reset the pixel and channel array for each event """

        print 'reset of the matrix'
        
        for j in range (self.pixel_y_size):
            for i in range (self.pixel_x_size*self.channel_number):
                self.pixels[i][j]= False
                self.pixel_lit_per_channel[i/4]=0  

        



 
        




    

     
        
    
       
    



