"""
huyifeng@baidu.com
"""
import numpy as np
from scipy.sparse import csr_matrix
import logging
import paddle.v2 as paddle
import cPickle as pickle
import time
import interval
#from interval import Interval,IntervalSet
class normal(object): 
    """
    normal
    """
    def __init__(self, max_idx, norm=None, norpar=None): 
        """
        __init__
        """
        self.__label = []
        self.__m = None
        self.__min = None
        self.__max = None
        self.__range = None
        self.__nor_interval = None
        self.__max_idx = max_idx - 1
        if norm is None: 
            self.__nor_interval = interval.IntervalSet([])
        else: 
            self.__nor_interval = norm
            print self.__nor_interval

        if norpar is None: 
            self.__load = self.__load_train
        else: 
            self.__min = norpar['min'] 
            self.__max = norpar['max']
            self.__range = norpar['range']
            self.__load = self.__load_test
            print norpar
        self.__log = logging.getLogger('paddle')

    def load(self, reader):
        """
        load
        """
        return self.__load(reader)

    def __load_test(self, reader): 
        """
        load_test
        """
        if len(self.__min) != self.__max_idx + 1\
            or len(self.__max) != self.__max_idx + 1\
            or len(self.__range) != self.__max_idx + 1:
            raise Exception('range of min|max|range is not match')
        row_cnt = 0
        row = []
        col = []
        data = []
        last_time = time.time()
        for fea, lbl in reader():
            for idx, val in fea:
                row.append(row_cnt)
                col.append(idx)
                if idx in self.__nor_interval: 
                    if val < self.__min[idx]: 
                        self.__log.warning('val[%d,%d](%f) < min(%f),set val to %f' % (row_cnt, idx,
                            val, self.__min[idx], self.__min[idx]))
                        val = self.__min[idx] 
                    if val > self.__max[idx]: 
                        self.__log.warning('val[%d,%d](%f) > max(%f),set val to %f' % (row_cnt, idx, 
                            val, self.__max[idx], self.__max[idx]))
                        val = self.__max[idx]
                data.append(val)
            self.__label.append(lbl)
            row_cnt += 1
            if time.time() - last_time > 10:
                self.__log.info('Data processed %d' % (row_cnt))
                last_time = time.time()
        self.__m = csr_matrix((data, (row, col)), shape=(row_cnt, self.__max_idx + 1))
        self.__log.info("csr_matrix created:%d %d" % (self.__m.shape[0], self.__m.shape[1]))
        #return par
        
    def __load_train(self, reader): 
        """
        load_train
        """
        row_cnt = 0
        row = []
        col = []
        data = []
        last_time = time.time()
        for fea, lbl in reader():
            for idx, val in fea:
                row.append(row_cnt)
                col.append(idx)
                data.append(val)
            self.__label.append(lbl)
            row_cnt += 1
            if time.time() - last_time > 10:
                self.__log.info('Data processed %d' % (row_cnt))
                last_time = time.time()
        self.__m = csr_matrix((data, (row, col)), shape=(row_cnt, self.__max_idx + 1))
        self.__log.info("csr_matrix created:%d %d" % (self.__m.shape[0], self.__m.shape[1]))
        self.__min = np.array([self.__m[..., col].min() if col in self.__nor_interval else -1 
                                    for col in xrange(self.__m.shape[1])])
        print 'min: ', self.__min
        self.__log.info('min created')
        self.__max = np.array([self.__m[..., col].max() if col in self.__nor_interval else -1 
                                    for col in xrange(self.__m.shape[1])])
        print 'max: ', self.__max
        self.__log.info('max created')
        self.__range = np.array([1 if i == 0.0 else i for i in self.__max - self.__min])
        print 'range: ', self.__range
        self.__log.info('range created')
        return {'min': self.__min, 'max': self.__max, 'range': self.__range}, self.__nor_interval
    
    def normalize(self, fea, par): 
        """
        normalize
        """
        self.__min = par['min'] 
        self.__max = par['max']
        self.__range = par['range']
        if len(self.__min) != self.__max_idx + 1\
            or len(self.__max) != self.__max_idx + 1\
            or len(self.__range) != self.__max_idx + 1:
            raise Exception('range of min|max|range is not match')
        data = []
        for idx, val in fea: 
            if val < self.__min[idx]: 
                self.__log.warning('val[%d](%f) < min(%f),set val to %f' % (idx,
                    val, self.__min[idx], self.__min[idx]))
                val = self.__min[idx] 
            if val > self.__max[idx]: 
                self.__log.warning('val[%d](%f) > max(%f),set val to %f' % (idx, 
                    val, self.__max[idx], self.__max[idx]))
                val = self.__max[idx]
            val = (val - self.__min[idx])/self.__range[idx]
            if val != 0.0: 
                data.append((idx, val))
        return data

    def reader(self): 
        """
        reader
        """
        def data_reader():
            """
            data_reader
            """
            for nrow in xrange(self.__m.shape[0]): 
                fea = []
                for i in xrange(self.__m.shape[1]): 
                    if i in self.__nor_interval: 
                        val = (self.__m[nrow,i] - self.__min[i]) / self.__range[i]
                        if val != 0.0: 
                            fea.append((i, val))
                    else: 
                        if self.__m[nrow, i] != 0.0: 
                            fea.append((i, self.__m[nrow, i]))
                yield fea, self.__label[nrow]
        return data_reader

if __name__ == '__main__': 
    def reader(): 
        """
        """
        fea = [
            [(0, 1.0), (1, 2.0), (2, 3.0), (3, 4.0), (4, 3.0)],
            [(0, 2.0), (4, 2.0)],
            [(0, 3.0), (4, 3.0)],
            [(0, 4.0), (4, 4.0)],
            [(0, 5.0), (4, 5.0)],
            [(0, 6.0), (1, 2.0), (2, 3.0), (3, 4.0), (4, 5.0)],
        ]
        for i in fea:
            yield i, len(i)
    def reader2(): 
        """
        """
        fea = [
            [(0, 8.0), (1, 10.0), (2, 3.0), (3, 4.0), (4, 3.0)],
            [(0, 7.0), (4, 2.0)],
            [(0, 6.0), (4, 3.0)],
            [(0, 5.0), (4, 4.0)],
            [(0, 4.0), (4, 5.0)],
            [(0, 3.0), (1, 2.0), (2, 3.0), (3, 4.0), (4, 5.0)],
        ]
        for i in fea:
            yield i, len(i)

    normal_range  = interval.IntervalSet([interval.Interval(1,10,low_closed=True,upper_closed=False)])
    print normal_range
    nor = normal(7, normal_range)
    norpar, interval= nor.load(reader)
    print 'norpar:', norpar
    print 'interval:', interval
    with open('temp_norm.pki', 'wb') as f: 
        pickle.dump({'norpar': norpar, 'interval': interval}, f)
    print '*' * 50
    for fea,lbl in nor.reader()(): 
        print fea, lbl
    print '*' * 50
    
    #print '%' * 50
    #for fea,lbl in reader2():
    #   print '{', nor.normalize(fea, out), '}'
    #print '%' * 50

    test_nor = normal(7,norm=interval, norpar=norpar)
    test_nor.load(reader2)
    print '+' * 50
    for i in test_nor.reader()():
        print i
    print '+' * 50

