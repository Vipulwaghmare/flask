from datetime import datetime, timedelta, timezone
from dao.UserDao import UserDao
from model.UserModel import UserModel 
from services.Crypto import Crypto
from services.Logger import Logger

logger = Logger.get_instance() 

class User(UserModel):
  def __init__(self):
    super(User, self).__init__()
  
  def set_password(self, password):
    crypto = Crypto()
    password_validation_errors = crypto.check_password_requirements(password)

    if (len(password_validation_errors) > 0):
      return { "error" : password_validation_errors }

    hashed_password = crypto.hash_password(password)
    decoded_hash_password = str(hashed_password.decode('utf8'))
    
    return { "hash_password": decoded_hash_password }

  def register_user(self, user_data):
    hash_password = self.set_password(user_data['password'])
    if "error" in hash_password:
      return { "error": hash_password["error"] }
    user_data['password'] = hash_password["hash_password"]
    try:
      return self.save_user(user_data)
    except Exception as e:
      return { "error": 'Failed to add user' }

  def get_user_register_data(self, request_data):
    # validate schema 
    return {
      "email": request_data["email"],
      "password": request_data["password"]
    }

  def validate_password(self, password, bytes_hashed_password):
    bytes_hashed_password = bytes_hashed_password.encode('utf8')
    crypto = Crypto()
    valid = crypto.validate_hash(password, bytes_hashed_password)
    return valid
  
  def get_access_token(self, payload):
    crypto = Crypto()
    payload['exp'] =  datetime.now(tz=timezone.utc) + timedelta(minutes=30)
    access_token = crypto.encode(payload)
    return access_token 
  
  def get_refresh_token(self, payload):
    crypto = Crypto()
    payload['exp'] =  datetime.now(tz=timezone.utc) + timedelta(days=1)
    refresh_token = crypto.encode(payload)
    return refresh_token
  
  def get_login_response(self, user_details):
    try:
      email = user_details["email"]
      access_token = self.get_access_token(user_details)
      refresh_token = self.get_refresh_token(user_details)
      self.update_refresh_token(email, refresh_token)
      return { "access_token": access_token, "refresh_token": refresh_token, "email": email } 
    except Exception as e:
      logger.log.error(f"[get_login_response] {str(e)}")
      return {"error": "Some Error occured." }

  def generate_password_reset_token(self, email):
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
    self.update_password_reset_token(email, jwt_token_for_db)
    return token

  def validate_access_token(self, hash_string):
    try:
      crypto = Crypto()
      user_details = crypto.decode(hash_string)
      return user_details 
    except Exception as e:
      return None
  
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