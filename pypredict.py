#coding:utf-8
import os
import sys
import numpy
import paddle.v2 as paddle
def get(name, x): 
    if name == 'softmax': 
        return __softmax_predict(x) 
    elif name == 'nn': 
        return __nn_predict(x)
def __softmax_predict(x): 
    """
    model_predict
    """
    #Softmax
    y_predict = paddle.layer.fc(input=x, 
        size=2, act=paddle.activation.Softmax())
    return y_predict
def __nn_predict(x): 
    """
    model_predict
    """
    #NN
    hidden = paddle.layer.fc(input=x, size=16,act=paddle.activation.Sigmoid(), 
                             param_attr=paddle.attr.Param(sparse_update=True))
    y_predict = paddle.layer.fc(input=hidden, size=1,act=paddle.activation.Sigmoid())
    return y_predict
