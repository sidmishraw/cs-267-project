from ctypes import *

lib = CDLL('test.so')

class Test(object):

    def __init__(self):
        self.obj = lib.CreateInstance()

    def DoSomething(self):
        lib.DoSomething()

    def DoSomethingHello(self):
        return c_int(lib.DoSomethingHello(self.obj))

    def InputTestInteger(self):
        lib.InputInteger(c_int(404))

    def InputTestFloat(self):
        lib.InputFloat(c_float(7.8))

    def InputTestString(self):
        lib.InputString(c_char_p(b"GoGoPowerRanger!"))

t = Test()
i = t.DoSomethingHello()
print(i.value)
print("stop")

t.InputTestInteger()
t.InputTestFloat()
t.InputTestString();


