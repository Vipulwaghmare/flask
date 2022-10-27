import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import json
import os

'''
Usage:
from services.Logger import Logger
logger = Logger.get_instance()
  logger.log.info('Info log')
  logger.log.error("Error Log")
'''

class Logger:
  __instance = None
  def __init__(self):
    self.load_config()

  def load_config(self):
    with open('settings/logger_config.json') as config_file:
      config_data = json.load(config_file)

    mail_config = config_data["mailer"]
    self._host = mail_config["host"]
    self._port = mail_config["port"]
    self._username = mail_config["username"]
    self._password = mail_config["password"]
    self._from_address = mail_config["from_address"]
    self._to_address = mail_config["to_address"]

    path_config = config_data["path"]
    self._path = path_config["path"]
    self._file_name = path_config["file_name"]

    
    slack_config = config_data["slack"]
    self._channel_token = slack_config["channel_token"]
    self._channel_name = slack_config["channel_name"]

    # Logger Setup
    logger_env = os.environ.get("API_ENV", default="LOCAL")
    extra = {"env" : logger_env}
    formatter = logging.Formatter('%(env)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('backend')
    logger.setLevel(logging.DEBUG)

    # File handler which logs debug messages
    fh = RotatingFileHandler('logs/{}.log'.format(self._file_name), maxBytes=100*1024*1024, backupCount=100)
    fh.setLevel(logging.DEBUG)

    # Printing in terminal
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    
    # Creating Formatter and Adding to the handler
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger = logging.LoggerAdapter(logger, extra)
    self.log = logger
    Logger.__instance = self
  
  @staticmethod 
  def get_instance(): 
    if Logger.__instance == None: 
        Logger() 
    return Logger.__instance