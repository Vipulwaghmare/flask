import json
import secrets
import bcrypt
import re

class Crypto:
  def __init__(self):
    self._load_config()
  
  def _load_config(self):
    with open('settings/crypto_config.json') as config_file:
      config_data = json.load(config_file)
    self._secret = config_data["secret"]
    self._algorithm = config_data["algorithm"]
    self._lifespan = config_data["lifespan"] # hours
  
  def hash_password(self, password):
    salt = bcrypt.gensalt(rounds=6)
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed_password

  def generate_random(self):
    return secrets.token_hex(32)

  def create_api_key(self, api_key):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(api_key.encode('utf8'), salt)
    return hash

  def validate_hash(self, value, hash):
    try:
      valid = bcrypt.checkpw(value.encode('utf8'), hash)
    except Exception as e:
      raise e
    if valid:
      return True
    else:
      return False

  # def check_password_requirements(self, pwd):
  #   results = {
  #     "Password should include at least 1 lower case character": False,
  #     "Password should Include at least one number": False,
  #     "Password should between 7 and 32 characters long": False
  #   }
  #   password_validation_errors = []
  #   if len(pwd) not in range(7, 32):
  #     results["Password should between 7 and 32 characters long"] = True
  #   if not bool(re.search(r'\d', pwd)):
  #     results["Password should Include at least one number"] = True
  #   if not bool(re.search(r'[a-z]', pwd)):
  #     results["Password should include at least 1 lower case character"] = True
  #   return results
  
  def check_password_requirements(self, pwd):
    password_validation_errors = []
    if len(pwd) not in range(7, 32):
      password_validation_errors.append("Password should between 7 and 32 characters long")
    if not bool(re.search(r'\d', pwd)):
      password_validation_errors.append("Password should Include at least one number") 
    if not bool(re.search(r'[a-z]', pwd)):
      password_validation_errors.append("Password should include at least 1 lower case character")
    return password_validation_errors