from pymongo import MongoClient

class MongoDB:
  def __init__(self):
    self.connection = None
    self.create_connection()

  def create_connection(self):
    try:
      self.connection = MongoClient(
        host="localhost",
        post= 27017,
        serverSelectionTimeoutMS = 1000
      )
      test = self.connection.server_info()
      print("TEST", test)
    except Exception as e:
      print("ERROR - Cannot connect to db")

  def close(self):
    self.connection.close()

