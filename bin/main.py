import configparser
from utils.logUtils import LogAction

config = configparser.RawConfigParser()
config.read('config.properties')
log = LogAction(__file__).init_log(path_folder_logs=config.get("Logger", "log_path"))
