# sc_wrapper.py
# -*- coding: utf-8 -*-
# @Author: Samuel Ordonia | sordonia120446 | Sam O
# @Date:   2017-04-01 19:00:01
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-04-06 16:41:24




"""
Python wrapper for sc cpp code.

Created on 3/21/2017.

@author: sordonia120446 | Sam O
"""




# Python standard library imports
from ctypes import c_float
from ctypes import c_char_p
from sys import platform




# constants
__WIN__ = 'win32'
__OSX__ = 'darwin' 




#  Default shared object file path
# filepath = './simplicial_complex/cpp/SCExport.so'
class SimplicialComplex(object):
    '''
    The wrapper class for the C++ Simplical Complex implementation.
    '''

    def __init__(self, *, shared_obj_path = None, max_simplex = None, threshold = None, \
        cols = None, rows = None ):
        '''
        Initializes the wrapper for the simplical complex.

        :return: `None`
        '''

        if platform == __WIN__:
            from ctypes import windll
            self.__lib = windll.LoadLibrary(shared_obj_path)
        elif platform == __OSX__:
            from ctypes import CDLL
            self.__lib = CDLL(shared_obj_path)

        self.simplical_complex_instance = self.__lib.createInstance()
        self.num_of_rules = max_simplex
        self.threshold = threshold
        self.cols = cols
        self.rows = rows
        self.filepath = shared_obj_path

    # def __init__(self, num_of_rules, threshold, cols, rows, filepath=None):
    #     self.obj = lib.createInstance()
    #     self.num_of_rules = num_of_rules
    #     self.threshold = threshold
    #     self.cols = cols
    #     self.rows = rows
    #     self.filepath = filepath

    


    def initialize(self):
        '''
        Initializes the SimplicalComplex C++ object.

        Under the hood, it calls the 

        `void SimplicialCmplx::initialize(int rules, float threshold, int cols, int rows)`

        method of the SimplicalCmplx C++ class.

        :return: `None`
        '''

        self.__lib.initialize(self.simplical_complex_instance, self.num_of_rules,\
         c_float(self.threshold), self.cols, self.rows)

    


    def remove_instance(self):
        '''
        Deletes the SimplicalComplex C++ object from the heap.

        Under the hood:
          calls the `void removeInstance(SimplicialCmplx *p_instance)` of the SimplicialCmplx C++
          object.

        :return: `None`
        '''

        self.__lib.removeInstance(self.simplical_complex_instance)

    


    def set_bit_map_row(self, row_number, bit_vector):
        '''
        Sets the bitmap row

        Under the hood:
          calls the `void SimplicialCmplx::setBitMapRow(int cols, int rows, const char *row_data)`
          of SimplicalCmplx C++ object.

        :return: `None`
        '''

        self.__lib.setBitMapRow(self.simplical_complex_instance, self.cols, row_number, c_char_p(bit_vector))

    


    def process(self):
        '''
        Runs the simplical complex algorithm.

        Under the hood:
          calls the `void SimplicialCmplx::process()` of the SimplicalCmplx C++ object.

        :return: `None`
        '''

        self.__lib.process(self.simplical_complex_instance)

    


    def directProcess(self, num_of_rules, threshold, cols, rows, bit_vector):
        '''
        Runs the simplical complex algorithm.

        Under the hood:
          `void directProcess(int rules, float threshold, int cols, int rows, const char *data)`

        :return: `None`
        '''

        self.__lib.directProcess(num_of_rules, c_float(threshold), cols, rows, c_char_p(bit_vector))
