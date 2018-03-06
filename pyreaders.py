"""
huyifeng@baidu.com
"""
import os
import sys
import py_feature_number
import py_feature_map
import numpy
import logging
import logging.handlers
import pyconfig
import interval
#from interval import Interval,IntervalSet


def file(formater, fname):
    """
    file reader creator
    """
    par = pyconfig.FEATURE_CONFIG
    ifealen = [m.range() for m in par]
    ifeabase = [sum(ifealen[0:x]) for x in xrange(len(ifealen) + 1)]
    iset = []
    for idx in xrange(len(par)):
        if par[idx].neednorm(): 
            iset.append(interval.Interval(ifeabase[idx], 
                ifeabase[idx + 1], lower_closed=True, upper_closed=False))
    def reader():
        """
        reader
        """
        with open(fname, 'r') as f: 
            for l in f.readlines(): 
                sample = l.strip().split(' ')
                fea = []
                for idx in xrange(len(par)):
                    for k, v in par[idx].feature(sample):
                        if v != 0: 
                            fea.append((k + ifeabase[idx], float(v)))
                yield formater(fea, int(sample[-1]))
    return reader, interval.IntervalSet(iset)

if __name__ == '__main__': 
    file(None, '')
