#Angular distribution module
"""
.. module:: GenerateEvent
   :synopsis: Definition of Angular Distribution functions for the photons
.. moduleauthor:: Sebastiana Giani <sebastiana.giani@epfl.ch>
"""

import math
from ROOT import TF1
import unittest


def function_1 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=27:
        return -0.7367+5.0550*x[0]-0.0554*x[0]*x[0]


def function_2 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=27:
        return -0.2846+13.3962*x[0]-0.0838*x[0]*x[0]


def function_3 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=27:
        return -1.9196+25.6074*x[0]-0.2702*x[0]*x[0]


def function_4 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=27:
        return -1.2325+34.1110*x[0]-0.3271*x[0]*x[0]
    
def function_5 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=27:
        return -6.7858+44.746*x[0]-0.4284*x[0]*x[0]


def function_6 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<= 27:
        return -8.5570+56.2115*x[0]-0.5866*x[0]*x[0]
    else:
        return 7451.11-335.88*x[0]+3.6112*x[0]*x[0]


def function_7 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=27:
        return -6.0329+62.0612*x[0]-0.4463*x[0]*x[0]
    else:
        return 6296.19-257.260*x[0]+2.5809*x[0]*x[0]


def function_8 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=27:
        return -2.3125+71.1939*x[0]-0.4842*x[0]*x[0]
    else:
        return 4405.57-141.793*x[0]+1.1392*x[0]*x[0]


def function_9 (x):

    if x[0]<=0.25:
        return 0.0
    if x[0]<=27:
        return -18.2144+82.3692*x[0]-0.9137*x[0]*x[0]
    else:
        return 2221.03-40.1972*x[0]+0.1705*x[0]*x[0]


def function_10 (x):

    if x[0]<=0.2:
        return 0.0
    if x[0]<=16:
        return -0.4247+18.1516*x[0]+0.4020*x[0]*x[0]
    else:
        return 1473.86*math.exp(-x[0]/11.7009)

    
def choose_angle_from_distribution(radius):

    """

     Given the position of the photon rispect to the center of the fiber(radius), this function return us the emission angle
     of the photons.Depending by the radius, a random number is returned from the distributions obtained by a Geant Simulation"""
    #print radius
    
    angle=0
    if radius>=0 and radius<=12.5:
        f1=TF1("f1",function_1,0,27) 
        angle=f1.GetRandom()
    elif radius>12.5 and radius<=25:
        f2=TF1("f2",function_2,0,27)
        angle=f2.GetRandom()
    elif radius>25 and radius<=37.5:
        f1=TF1("f1",function_3,0,27) 
        angle=f1.GetRandom()
    elif radius>37.5 and radius<=50:
        f1=TF1("f1",function_4,0,27) 
        angle=f1.GetRandom()
    elif radius>50 and radius<=62.5:
        f1=TF1("f1",function_5,0,27) 
        angle=f1.GetRandom()
    elif radius>62.5 and radius<=75:
        f1=TF1("f1",function_6,0,37) 
        angle=f1.GetRandom()
    elif radius>75 and radius<=87.5:
        f1=TF1("f1",function_7,0,44) 
        angle=f1.GetRandom()
    elif radius>87.5 and radius<=100:
        f1=TF1("f1",function_8,0,60) 
        angle=f1.GetRandom()
    elif radius>100 and radius<=112.5:
        f1=TF1("f1",function_9,0,86) 
        angle=f1.GetRandom()
    elif radius>=112.5 and radius<=125:
        f1=TF1("f1",function_10,0,70) 
        angle=f1.GetRandom()
   
    #print angle
    return math.radians(angle)

       





