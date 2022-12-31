import datetime
from configs.log import logger

def printCurTime(param):
    current_time = datetime.datetime.now()
    logger.info(param + " " + str(current_time))
