import pymongo

# try:
#   mongo = pymongo.MongoClient(
#     host="localhost",
#     post= 27017,
#     serverSelectionTimeoutMS = 1000
#   )
#   mongo.server_info()
# except:
#   print("ERROR - Cannot connect to db")

class MongoDB:
  def __init__(self):
    self.create_connection()

  def create_connection(self):
    try:
      mongo = pymongo.MongoClient(
        host="localhost",
        post= 27017,
        serverSelectionTimeoutMS = 1000
      )
      mongo.server_info()
    except Exception as e:
      print("ERROR - Cannot connect to db")
