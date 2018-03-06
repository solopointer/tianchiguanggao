#coding:utf-8
import os
import sys
import gzip
import numpy
import logging
import datetime
import time
import logging.handlers
import cPickle as pickle
import paddle.v2 as paddle
import pynormalization
import pyconfig
import pyreaders
import pypaddlelog
import pyformater
import pypredict
def softmax_trainer(x):
    y = paddle.layer.data(name='y', type=paddle.data_type.integer_value(1))
    y_predict = pypredict.get('softmax', x)
    cost = paddle.layer.cross_entropy_cost(input=y_predict, label=y)
    parameters = paddle.parameters.create(cost)
    optimizer = paddle.optimizer.Momentum(momentum = 0)
    return  paddle.trainer.SGD(
            cost=cost, 
            parameters=parameters,
            update_equation=optimizer)
def nn_trainer(x): 
    y = paddle.layer.data(name='y', type=paddle.data_type.dense_vector(1))
    y_predict = pypredict.get('nn', x)
    cost = paddle.layer.square_error_cost(input=y_predict, label=y)
    parameters = paddle.parameters.create(cost)
    optimizer = paddle.optimizer.Momentum(momentum = 0)
    return  paddle.trainer.SGD(
            cost=cost, 
            parameters=parameters,
            update_equation=optimizer)
    
MODEL_NAME = 'nn'
TRAINERS = {
    'softmax': softmax_trainer,
    'nn': nn_trainer
}
if __name__ == '__main__': 
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    FEATURE_RANGE = sum([m.range() for m in pyconfig.FEATURE_CONFIG])
    pypaddlelog.initlogger(logging.INFO, 'trainer')
    with_gpu = os.getenv('WITH_GPU', '0') != 0 
    paddlelog = logging.getLogger('paddle')
    localtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    modelpath = '%s/models/%s/' % (BASE_DIR, localtime)
    if os.path.exists(modelpath) is False: 
        os.mkdir(modelpath)
    paddlelog.info('model output path: %s' % (modelpath))
    paddle.init(use_gpu=0, trainer_count=1)
    x = paddle.layer.data(name='x', 
        type=paddle.data_type.sparse_float_vector(FEATURE_RANGE))
    trainer = TRAINERS[MODEL_NAME](x)
    sample_formater = pyformater.get_sample_formater(MODEL_NAME)
    #TRAIN
    rd, intv = pyreaders.file(sample_formater, '/home/work/huyifeng/train.txt')
    train_normal = pynormalization.normal(FEATURE_RANGE, norm=intv)
    normalpar, intv = train_normal.load(rd)
    train_reader = paddle.batch(
        paddle.reader.shuffle(
            train_normal.reader(), buf_size=1000),
        batch_size=2000)
    with open('%s/normal.pki' % (modelpath), 'wb') as f: 
        pickle.dump({'interval': intv, 'normalpar': normalpar}, f)
    #TEST
    rd, intv = pyreaders.file(sample_formater, '/home/work/huyifeng/test.txt')
    test_normal = pynormalization.normal(FEATURE_RANGE, norm=intv, norpar=normalpar)
    test_normal.load(rd)
    test_reader = paddle.batch(
        paddle.reader.shuffle(
            test_normal.reader(), buf_size=1000),
        batch_size=320)
    logging.getLogger('paddle').info('Load data done!')
    def _event_handler(event):
        """
        Define end batch and end pass event handler
        """
        if isinstance(event, paddle.event.EndIteration):
            logging.getLogger('paddle').info("Pass %d, Batch %d, Cost %f\n" % (
                event.pass_id, event.batch_id, event.cost))
            result = trainer.test(reader=test_reader)
            logging.getLogger('paddle').info("Test at Pass %d, cost: %f" % (event.pass_id, result.cost))
        if isinstance(event, paddle.event.EndPass):
            with gzip.open('%s/model.%s.tar' % (modelpath, event.pass_id), "w") as f:
                trainer.save_parameter_to_tar(f)
    #-------------------------------Train---------------------------------------------
    trainer.train(
        reader=train_reader,
        event_handler=_event_handler,
        num_passes=3)
    FINAL_MODEL_FILE = '%s/model.final.tar' % (modelpath)
    with gzip.open(FINAL_MODEL_FILE, "w") as f:
        trainer.save_parameter_to_tar(f)
    logging.getLogger('paddle').info('Train Done:%s' % (FINAL_MODEL_FILE))
    #-------------------------------Test----------------------------------------------
    #logging.getLogger('paddle').info('Begin Test')
    #with gzip.open(FINAL_MODEL_FILE, 'r') as f:
    #    final_parameters = paddle.parameters.Parameters.from_tar(f)
    #test_data = []
    #test_label = []
    #for fea, lbl in test_normal.reader()():
    #    test_data.append((fea,))
    #    test_label.append(lbl)
    #probs = paddle.infer(
    #    output_layer=y_predict, 
    #    parameters=final_parameters, 
    #    input=test_data)
    #right = 0
    #result_formater = pyformater.get_result_formater(MODEL_NAME)
    #for i in xrange(len(probs)):
    #    print 'output:', probs[i]
    #    if (probs[i][0] > probs[i][1] and test_label[i] == 0) or\
    #        (probs[i][0] < probs[i][1] and test_label[i] == 1): 
    #        right += 1
    #        print probs[i],test_label[i],'\033[1;35m Right \033[0m'
    #    else: 
    #        print probs[i],test_label[i]
    #logging.getLogger('paddle').info("All: %d Right:%d %f%%" % (len(probs), right, float(right)*100/float(len(probs))))
    #-------------------------------Test----------------------------------------------

