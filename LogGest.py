#!/usr/bin/env python
import envConfig
import logging.handlers, sys

try:
    logger = logging.getLogger(__name__)
    loggerHandler = logging.handlers.TimedRotatingFileHandler(filename=envConfig.FILELOG , interval=1)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
    logger.setLevel(logging.DEBUG)
    loggerHandler.setFormatter(formatter)
    logger.addHandler(loggerHandler)
except Exception as error:
    print ("Error with logs: %s" % (str(error)))
    sys.exit()

def ErrorMSG(msg):
    logger.error(msg)

def WarningMSG(msg):
    logger.warning(msg)

def DebugMGS(msg):
    logger.debug(msg)

def InfoMGS(msg):
    logger.info(msg)