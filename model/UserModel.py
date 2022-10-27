from services.MongoDB import MongoDB

class UserModel(MongoDB):
  def __init__(self):
    self._collection_name = "users"
    super(UserModel, self).__init__(self._collection_name)

  def get_user_details(self, email):
    return self.find_one({ "email": email } )
  
  def save_user(self, user_data):
    email = user_data['email']
    password = user_data['password']
    response = self.insert_one({
      "email": email,
      "password": password
    })
    return response
  
  def get_password_reset_token(self, email):
    return self.find_one({ "email": email }, {'password_reset_token': 1, "_id": 0})
  
  # ! TODO: Add below details in single update user function
  def update_refresh_token(self, email, token):
    self.update_one({ "email": email }, {'refresh_token': token })
    return { "Success": "Successfully updated user" }
  
  def update_password_reset_token(self, email, jwt_token_for_db):
    self.update_one({ "email": email }, {'password_reset_token': jwt_token_for_db })
  
  def update_password(self, email, password):
    hash_password = self.set_password(password)
    if "error" in hash_password:
      return { "error": hash_password["error"] }
    hash_password = hash_password["hash_password"]

    self.update_one({ "email": email }, {'password_reset_token': hash_password })
    return { "Success": "Successfully updated user" }
