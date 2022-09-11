import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import json
import os
# Logs in Slack
from slacker_log_handler import SlackerLogHandler
# Logs in AWS CloudWatch
import watchtower

'''
Usage:
from model.Logger import Logger
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

    # Logging to cloudwatch
    if logger_env != "LOCAL":
      log_group = logger_env + "_Backend_Apis"
      cwh = watchtower.CloudWatchLogHandler(log_group = log_group)
      logger.addHandler(cwh)
    
    # Email 
    if logger_env == "PROD":
      eh = SMTPHandler(self._host, self._from_address, self._to_address, "# Backend Error #", (self._username, self._password), (), timeout=1.0)
      eh.setLevel(logging.ERROR)
      eh.setFormatter(formatter)
      logger.addHandler(eh)
    
    # Errors on Slack
    if logger_env == "PROD":
      try:
        sh = SlackerLogHandler(self._channel_token, self._channel_name, stack_trace=True)
        sh.setLevel(logging.ERROR)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
      except Exception as e:
        print(e)
        raise e
    
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