from datetime import datetime, timedelta, timezone
from services.Crypto import Crypto
from services.MySQL import MySQL

class UserDao(MySQL):
  def __init__(self):
    super(UserDao, self).__init__()

  def get_user_details(self, email): 
    cursor = self.connection.cursor(dictionary=True)
    query = "SELECT * from user where email = %s "
    cursor.execute(query, (email, ))
    user = cursor.fetchone()
    return user

  def register_user(self, email, password):
    hash_password = self.set_password(password)
    if "error" in hash_password:
      return { "error": hash_password["error"] }
    hash_password = hash_password["hash_password"]
    try:
      query = ("INSERT INTO user ( email, password)  VALUES (%s , %s ) ") 
      cursor = self.connection.cursor() 
      cursor.execute(query, (email, hash_password,))
      self.connection.commit()
      return { "Success": "Successfully created user" }
    except Exception as e:
      return { "error": "Some error occurred" }

  def get_password_reset_token(self, email):
    cursor = self.connection.cursor(dictionary=True)
    query = "SELECT password_reset_token from user where email = %s "
    cursor.execute(query, (email, ))
    user = cursor.fetchone()
    if user is None:
      return user
    return user["password_reset_token"]
    
  # ! TODO: Add below details in single update user function
  def update_refresh_token(self, email, token):
    query = "UPDATE user SET refresh_token = %s WHERE email = %s" 
    cursor = self.connection.cursor() 
    cursor.execute(query, (token, email,))
    self.connection.commit()
    return { "Success": "Successfully updated user" }
  
  def update_password_reset_token(self, email, jwt_token_for_db):
    query = "UPDATE user SET password_reset_token = %s WHERE email = %s" 
    cursor = self.connection.cursor() 
    cursor.execute(query, (jwt_token_for_db, email,))
    self.connection.commit()
  
  def update_password(self, email, password):
    hash_password = self.set_password(password)
    if "error" in hash_password:
      return { "error": hash_password["error"] }
    hash_password = hash_password["hash_password"]

    query = "UPDATE user SET password = %s, password_reset_token = null WHERE email = %s" 
    cursor = self.connection.cursor() 
    cursor.execute(query, (hash_password, email,))
    self.connection.commit()
    return { "Success": "Successfully updated user" }

