import json
from services.MongoDB import MongoDB

class UserModel(MongoDB):
  def __init__(self):
    self._collection_name = "users"
    super(UserModel, self).__init__(self._collection_name)

  def get_user_details(self, email):
    return self.find_one({ "email": email })
  
  def register_user(self, email, password):
    response = self.insert_one({
      "email": email,
      "password": password
    })
    return response

