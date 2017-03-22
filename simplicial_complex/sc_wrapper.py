"""
Python wrapper for sc cpp code.

Created on 3/21/2017.

@author: sordonia120446 | Sam O
"""
from ctypes import *
import os

# Temp hack to make import to main file work
filepath = './simplicial_complex/cpp/SCExport.so'
lib = CDLL(filepath)

class SimplicialComplex(object):

    def __init__(self, num_of_rules, threshold, cols, rows, filepath=None):
        self.obj = lib.createInstance()
        self.num_of_rules = num_of_rules
        self.threshold = threshold
        self.cols = cols
        self.rows = rows
        self.filepath = filepath

    def remove_instance(self):
        lib.removeInstance(self.obj)

    def set_bit_map_row(self, row_number, bit_vector):
        lib.setBitMapRow(self.obj, self.cols, row_number, c_char_p(bit_vector))

    def process(self):
        lib.process(self.obj)
