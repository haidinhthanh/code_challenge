import logging
from logging import handlers
import datetime
import os
"""
@Desc: Ham ghi log
"""


class LogAction(object):

    def __init__(self, name='logger', level=logging.INFO):
        # Create the Logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.info("init logger success!")

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def init_log(self, level=logging.INFO, path_folder_logs="../logs/"):
        formatter = logging.Formatter(
            '%(asctime)s|%(levelname)s|%(filename)30s|%(funcName)40s| %(lineno)3d| %(message)s'
        )
        if not os.path.exists(path_folder_logs):
            os.makedirs(path_folder_logs)
        log_file = path_folder_logs + str(datetime.date.today()) + ".log"

        # log_file = "logs/service.log"
        self.logger.setLevel(level)
        file_handler = handlers.TimedRotatingFileHandler(log_file, when='d', interval=1, backupCount=100,encoding='utf-8')
        console_handler = logging.StreamHandler()
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.info("init logger success!")
        return self.logger

