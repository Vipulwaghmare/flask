from flask import g 
from pymongo import MongoClient
from pymongo import errors

from utils.helpers import bson_to_json

class MongoDB:
  def __init__(self, collection_name, database_name = "firstApp"):
    self.connection = None
    self._database = database_name
    self.set_db_connection()
    self.collection = self.db[collection_name]
  
  def set_db_connection(self,):
    db = getattr(g, 'db', None)
    if db is None:
      self.create_connection()
    else:
      self.db = db

  def create_connection(self):
    try:
      self.connection = MongoClient('mongodb://localhost:27017/')
      g.db = self.connection
      self.db = self.connection[self._database]
    except Exception as e:
      print("ERROR - Cannot connect to db")

  def close(self):
    print('closing-connection')
    if self.connection is not None:
      self.connection.close()
  
  # CRUD Queries
  def find_one(self, condition = {}, select = {} ):
    data = self.collection.find_one(condition, select)
    return bson_to_json(data)

  def insert_one(self, insert_data):
    try:
      self.collection.insert_one(insert_data)
      return { "success": "Successfully inserted data" }
    except errors.DuplicateKeyError as de:
      return { "error" : "Duplicate entry found" }
    except Exception as e:
      return { "error": "Some error occured" }

  def update_one(self, filter_data, updated_values):
    try:
      self.collection.update_one(filter_data, updated_values)
      return { "success": "Successfully inserted data" }
    except errors.DuplicateKeyError as de:
      return { "error" : "Duplicate entry found" }
    except Exception as e:
      return { "error": "Some error occured" }
