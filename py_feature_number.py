import sys
import os
import logging
import pyifeature
class feature(pyifeature.ifeature): 
    """
    """
    def __init__(self, dic): 
        pyifeature.ifeature.__init__(self, dic)
        self.__index = int(dic['index'])

    def neednorm(self):
        return True

    def range(self): 
        return 1

    def feature(self, ipt):
        level = ipt[self.__index]
        fea = [(0, float(level))]
        return fea

if __name__ == '__main__': 
    while True: 
        iput = raw_input()
        f = feature({})
        print f.range()
        print f.feature(iput)
