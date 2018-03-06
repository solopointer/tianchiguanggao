import pynormalization
import pyconfig
import pyformater 
import paddle.v2 as paddle  
import pyreaders
MODEL_NAME = 'nn'
FEATURE_RANGE = sum([m.range() for m in pyconfig.FEATURE_CONFIG])
train_normal = pynormalization.normal(FEATURE_RANGE)
sample_formater = pyformater.get_sample_formater(MODEL_NAME)
for i in pyreaders.file(sample_formater, '/home/work/huyifeng/train.txt')(): 
    print i
quit()
normalpar = train_normal.load(pyreaders.file(sample_formater, '/home/work/huyifeng/train.txt'))
train_reader = paddle.batch(
    paddle.reader.shuffle(
        train_normal.reader(), buf_size=1000),
    batch_size=2000)

for i in train_reader():
    print i
