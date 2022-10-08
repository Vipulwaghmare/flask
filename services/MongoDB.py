from flask import g 
from pymongo import MongoClient

class MongoDB:
  def __init__(self):
    self.connection = None
    self.set_db_connection()
    self.create_connection()
  
  def set_db_connection(self,):
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = self.create_connection()
    return db

  def create_connection(self):
    try:
      self.connection = MongoClient(
        host="localhost",
        post= 27017,
        serverSelectionTimeoutMS = 1000
      )
      test = self.connection.server_info()
    except Exception as e:
      print("ERROR - Cannot connect to db")

  def close(self):
    if self.connection is not None:
      self.connection.close()

