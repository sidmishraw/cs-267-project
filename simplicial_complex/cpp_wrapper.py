"""
Python wrapper for basic cpp test file in shared object "test.so"

Created on 3/12/2017.

@author: sordonia120446, skycckk
"""
from ctypes import *

lib = CDLL('test.so')

class Test(object):

    def __init__(self):
        self.obj = lib.CreateInstance()

    def DoSomething(self):
        """Deprecated test fnc"""
        lib.DoSomething()

    def DoSomethingHello(self):
        """
        Test fnc to return int.
        """
        return c_int(lib.DoSomethingHello(self.obj))


my_test = Test()
my_int = my_test.DoSomethingHello()
print(my_int.value)
