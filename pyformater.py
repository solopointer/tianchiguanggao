#coding:utf-8
def get_sample_formater(name):
    def __softmax_formater(fea, label): 
        return fea, int(label)
    def __nn_formater(fea,label): 
        return fea, [float(label)]
    if name == 'softmax': 
        return __softmax_formater
    elif name == 'nn': 
        return __nn_formater
def get_result_formater(name): 
    def __softmax(lbl):
        if lbl[0] > lbl[1]:
            return 0
        else: 
            return 1
    def __nn(lbl): 
        if lbl[0] > 0.5: 
            return 1
        else: 
            return 0 
    if name == 'softmax': 
        return __softmax
    elif name == 'nn': 
        return __nn
