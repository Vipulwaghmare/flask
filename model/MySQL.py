from flask import g 
import mysql.connector
import json
from settings.environment import config_folder

class MySQL:
  def __init__(self, database_name = "test", config_file_name = "db", **opts):
    self.connection = None
    self._database = database_name
    self.load_config(config_file_name) 
    self.create_connection(opts) 

  def load_config(self, config_file_name):
    # config_folder not available in global variables
    if not 'config_folder' in globals():
      raise NameError("[MySql] config_folder is not set")
    file_path = f"settings/{config_folder}/{config_file_name}.json"
    with open(file_path) as config_file:
      config_data = json.load(config_file)
      self._host = config_data["host"]
      self._user = config_data["user_name"]
      self._password = config_data["password"]

  def create_connection(self, opts):
    self.connection = mysql.connector.connect(
      host = self._host,
      database = self._database,
      user = self._user,
      password = self._password,
      **opts
    )
    self.connection = self.get_connection()
  
  def get_connection(self):
    if not self.connection.is_connected():
      self.connection.reconnect(attempts = 4, delay = 5)
    return self.connection
  
  def close(self):
    if self.connection is not None:
      self.connection.close()