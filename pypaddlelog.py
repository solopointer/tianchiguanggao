#coding:utf-8
import os
import sys
import logging
import datetime
import time
import logging.handlers
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
def initlogger(loglevel,logo): 
    """ 
    init the logginger
    """
    logfmt = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    log_path = BASE_DIR + '/log/'
    if os.path.exists(log_path) is False: 
        os.mkdir(log_path)
    logging.basicConfig(level = loglevel, format = logfmt)
    Rthandler = logging.handlers.RotatingFileHandler(log_path + '/%s.%d.%s.log' % 
            (os.path.basename(str(sys.argv[0])), os.getpid(), logo), 
            maxBytes = 300 * 1024 * 1024, backupCount = 20)
    Rthandler.setLevel(loglevel)
    formatter = logging.Formatter(logfmt)
    Rthandler.setFormatter(formatter)
    logging.getLogger('paddle').addHandler(Rthandler)
