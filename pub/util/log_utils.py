import logging
import logstash
import sys
import os
from logging.handlers import RotatingFileHandler

class SingleLineFormatter(logging.Formatter):
    # def formatException(self, exc_info):
    #     result = super().formatException(exc_info)
    #     return repr(result)
 
    def format(self, record):
        result = super().format(record)
        result = result.replace("\n", "\\n")+'\n'
        # if record.exc_text:
        #     result = result.replace("\n", "")
        return result

logger = logging.getLogger('app')
# logger.setLevel(logging.DEBUG)
logger.propagate = False
handler = RotatingFileHandler('log/app.log', maxBytes=100*1024*1024, backupCount=2)
formatter = logging.Formatter('[%(asctime)s] [p%(process)s] [%(funcName)s] [%(pathname)s:%(lineno)d] [%(levelname)s] - %(message)s','%m-%d %H:%M:%S')
# formatter = SingleLineFormatter('[%(asctime)s] [p%(process)s] [%(funcName)s] [%(pathname)s:%(lineno)d] [%(levelname)s] - %(message)s','%m-%d %H:%M:%S')
handler.setFormatter(formatter)
handler.terminator = "\n"
logger.addHandler(handler)

def trace_log():
    import traceback
    just_the_string = traceback.format_exc().replace('\n','!!').replace('\r', '!!!')
    logger.error(just_the_string)