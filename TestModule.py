import unittest
import numpy
import FiberSetup
import MainSimulation


class FiberclassTestCase (unittest.TestCase):

    def test
    pass

class SetupclassTestCase (unittest.TestCase):
    
    def setUp(self):
        parameter=MainSimulation.Parameters('config.py')
        self.layers_t=FiberSetup.Setup(parameter).layers
        self.nfibers_t=FiberSetup.Setup(parameter).nfibers
        #self.nfibers_t=200
        #self.layers_t=0
        self.stack_t=FiberSetup.Setup(parameter).fiber_stack
        self.y_t=FiberSetup.Setup(parameter).y
        


    #def test_minimum_stack_dimensions(self):
    #    number_layers=[3,4,5,6] #number of possible layers you can choose
    #    self.assertIn (self.layers_t, number_layers, msg='number of layers out of possible values: define it as a integer number between 3 and 6')
            

    def test_matrix_size(self):
        expected_size=(self.layers_t,self.nfibers_t)
        value=self.stack_t.shape
        self.assertTupleEqual(expected_size,value , msg='fiber_stack matrix dimensions are wrong')

    def test_stack_geometry(self):
        if(self.layers_t==5):
            expected_Yc_coordinates={'fiber0_0':-2*self.y_t,'fiber2_3':0.0,'fiber3_20':self.y_t}
            actual_Yc_coordinates={'fiber0_0':self.stack_t[0][0].Yc,'fiber2_3':self.stack_t[2][3].Yc,'fiber3_20':self.stack_t[3][20].Yc}
            self.assertDictEqual(expected_Yc_coordinates,actual_Yc_coordinates, msg='stack geometry is wrong')
            actual_Xc_coordinates0_0=self.stack_t[0][0].Xc
            max_expected_Xc_0_0=0.000125
            self.assertLessEqual(actual_Xc_coordinates0_0,max_expected_Xc_0_0,msg='Xc coordinate of fiber[0][0] is out of range')


if __name__== "__main__":
    unittest.main()      

	    
