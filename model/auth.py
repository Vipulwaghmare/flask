from model.Crypto import Crypto

class Authorization:
  def __init__(self):
    pass

  def set_password(self, password):
    crypto = Crypto()

    password_validation_errors = crypto.check_password_requirements(password)
    if (len(password_validation_errors) > 0):
      return { "error" : password_validation_errors }
    hashed_password = crypto.hash_password(password)
    decoded_hash_password = str(hashed_password.decode('utf8'))
    # save with db query
    
    return {"hash_password": decoded_hash_password}
  