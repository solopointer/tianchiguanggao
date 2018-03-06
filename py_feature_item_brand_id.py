import sys
import os
import logging
import pyifeature
class feature(pyifeature.ifeature): 
    """
    """
    def __init__(self, dic): 
        pyifeature.ifeature.__init__(self,dic)
        if os.path.exists(dic['file']) is False: 
            raise Exception('File %s does not exists' % (dic['file']))
        cnt = 1
        self.__m = {}
        with open(dic['file'], 'r') as f: 
            for l in f.readlines(): 
               l = l.strip()
               if l not in self.__m: 
                   self.__m[l] = cnt
                   cnt += 1

    def range(self): 
        return len(self.__m) + 1

    def feature(self, id):
        if id in self.__m: 
            fea = [(self.__m[id], 1.0)]
        else: 
            fea = [(0, 1.0)]
        #return sorted(fea,cmp=lambda x,y:cmp(x[0], y[0]))
        return fea

if __name__ == '__main__': 
    while True: 
        iput = raw_input()
        f = feature({'file': '/home/work/huyifeng/item_brand_id.txt'})
        print f.range()
        print f.feature(iput)
