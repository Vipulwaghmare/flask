from datetime import datetime, timedelta, timezone 
from services.Crypto import Crypto
from services.MySQL import MySQL

class User():
  def __init__(self):
    pass

  def get_user_details(self, email):
    mysql = MySQL()
    cursor = mysql.connection.cursor(dictionary=True)
    query = "SELECT * from user where email = %s "
    cursor.execute(query, (email, ))
    user = cursor.fetchone()
    return user
  
  def set_password(self, password):
    crypto = Crypto()
    password_validation_errors = crypto.check_password_requirements(password)

    if (len(password_validation_errors) > 0):
      return { "error" : password_validation_errors }

    hashed_password = crypto.hash_password(password)
    decoded_hash_password = str(hashed_password.decode('utf8'))
    
    return { "hash_password": decoded_hash_password }

  def register_user(self, email, password):
    hash_password = self.set_password(password)
    if "error" in hash_password:
      return { "error": hash_password["error"] }
    hash_password = hash_password["hash_password"]

    mysql = MySQL()
    query = ("INSERT INTO user ( email, password)  VALUES (%s , %s ) ") 
    cursor = mysql.connection.cursor() 
    cursor.execute(query, (email, hash_password,))
    mysql.connection.commit()

    return { "Success": "Successfully created user" }

  def validate_password(self, password, bytes_hashed_password):
    bytes_hashed_password = bytes_hashed_password.encode('utf8')
    crypto = Crypto()
    valid = crypto.validate_hash(password, bytes_hashed_password)
    return valid
  
  def get_access_token(self, payload):
    crypto = Crypto()
    payload['exp'] =  datetime.now(tz=timezone.utc) + timedelta(seconds=30)
    access_token = crypto.encode(payload)
    return access_token 
  
  def get_refresh_token(self, payload):
    crypto = Crypto()
    payload['exp'] =  datetime.now(tz=timezone.utc) + timedelta(days=1)
    refresh_token = crypto.encode(payload)
    return refresh_token 

  def validate_access_token(self, hash_string):
    try:
      crypto = Crypto()
      user_details = crypto.decode(hash_string)
      return user_details 
    except Exception as e:
      return None

  def get_password_reset_token(self, email):
    mysql = MySQL()
    cursor = mysql.connection.cursor(dictionary=True)
    query = "SELECT password_reset_token from user where email = %s "
    cursor.execute(query, (email, ))
    user = cursor.fetchone()
    if user is None:
      return user
    return user["password_reset_token"]
  
  def validate_password_reset_token(self, email, token):
    # gets jwt password reset token from DB
    jwt_db_token = self.get_password_reset_token(email)
    if jwt_db_token is None:
      return { "error": "Token is not valid" }

    try:
      crypto = Crypto()
      # Decode token_hash from jwt_db_token, also checks for expiry time
      token_hash = crypto.decode(jwt_db_token)
    except Exception as e:
      return {"error": "Invalid token"}

    if token_hash is None:
      return {"error": "Invalid token"}

    # compare user token and db token
    token_hash = token_hash["token_hash"].encode("utf-8")
    valid = crypto.validate_hash(token, token_hash)
    if valid:
      return { "success": "Successfully validated token" }
    return {"error": "Invalid token"}
    
  # ! TODO: Add below details in single update user function
  def update_refresh_token(self, email, token):
    mysql = MySQL()
    query = "UPDATE user SET refresh_token = %s WHERE email = %s" 
    cursor = mysql.connection.cursor() 
    cursor.execute(query, (token, email,))
    mysql.connection.commit()
    return { "Success": "Successfully updated user" }
  
  def update_password_reset_token(self, email):
    # generate token 
    # token: for user 
    # jwt_token : to save in DB : 
    # jwt_token : { expiry: 1 day, hash_token: compare with user token to validate }
    crypto = Crypto()
    token = crypto.generate_random()
    token_hash = crypto.create_api_key(token) 
    payload = {
      'token_hash': token_hash.decode("utf-8"), 
      'exp':  datetime.now(tz=timezone.utc) + timedelta(days=1)
    }
    jwt_token_for_db = crypto.encode(payload)

    mysql = MySQL()
    query = "UPDATE user SET password_reset_token = %s WHERE email = %s" 
    cursor = mysql.connection.cursor() 
    cursor.execute(query, (jwt_token_for_db, email,))
    mysql.connection.commit()
    return token
  
  def update_password(self, email, password):
    hash_password = self.set_password(password)
    if "error" in hash_password:
      return { "error": hash_password["error"] }
    hash_password = hash_password["hash_password"]

    mysql = MySQL()
    query = "UPDATE user SET password = %s, password_reset_token = null WHERE email = %s" 
    cursor = mysql.connection.cursor() 
    cursor.execute(query, (hash_password, email,))
    mysql.connection.commit()
    return { "Success": "Successfully updated user" }