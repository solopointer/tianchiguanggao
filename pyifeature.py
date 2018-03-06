"""
huyifeng@baidu.com
"""
import os
class ifeature(object): 
    """
    interface of feature
    """
    def __init__(self, dic): 
        """
        ___init___
        """
        pass
    def neednorm(self): 
        """
        neednorm
        """
        return False
    def range(self): 
        """
        range
        """
        return 0
    def feature(self, obj):
        """
        feature
        """
        pass
