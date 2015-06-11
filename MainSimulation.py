import numpy as np
import sys
import ROOT
import FiberSetup
import Sipm
import GenerateEvent
import AngularDistribution
#import TestModule



import unittest




            


class Parameters:
    """This class has as attributes all the parameters used in the simulation.

       These parameter are stored in a config.py file that has to be passed when
       the execution comand is given.
       Es: python MainSimulation.py config.py"""
    def __init__(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                exec 'self.'+line
        


if __name__== "__main__":

    """In this main an object of the class Parameter is instanced. """

    parameter = Parameters(sys.argv[1])
    simul=GenerateEvent.Event(parameter)

    simul.writeDataRoot()
