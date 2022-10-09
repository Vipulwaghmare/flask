from flask import request, jsonify
from services.User import User
from utils.requestValidation import  validate_request_body, validate_request_properties, validate_request_schema
from model.Logger import Logger

logger = Logger.get_instance() 

@validate_request_body
@validate_request_properties(['email', 'password'])
@validate_request_schema("jsonSchemas/login.json")
def register():
  try:
    request_data = request.json
    (email, password) = (request_data["email"], request_data["password"])

    user = User()
    user_found = user.get_user_details(email)
    
    if user_found is not None:
      return jsonify({ "error" : "User already exists" }), 401

    response = user.register_user(email, password)

    if "error" in response:
      return jsonify({ "error" : response["error"] }), 401

    return jsonify({ "success": f"Successfully created user with Email: {email}" })
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

@validate_request_body
@validate_request_properties(['email', 'password'])
@validate_request_schema("jsonSchemas/login.json")
def login():
  try: 
    request_data = request.json 
    (email, password) = (request_data["email"], request_data["password"])

    user = User()
    user_details = user.get_user_details(email)
    
    if user_details is None:
      return jsonify({ "error" : "User not found" }), 401

    valid = user.validate_password(password, user_details["password"])
    
    if not valid:
      return jsonify({ "error" : "Invalid Email or Password" }), 401

    user_details = {
      "name": user_details["name"],
      "email": user_details["email"]
    }
    access_token = user.get_access_token(user_details)
    refresh_token = user.get_refresh_token(user_details)
    user.update_refresh_token(email, refresh_token)

    return { "success": "Logged in successfully", "access_token": access_token, "refresh_token": refresh_token }

  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

def getAccessToken():
  try: 
    refresh_token = request.args.get('refresh_token')

    if refresh_token is None:
      return { "error" : "refresh_token missing in query" }

    user = User()
    user_details = user.validate_access_token(refresh_token)
    
    if user_details is None:
      return jsonify({ "error" : "Invalid Access token" }), 401
    
    if "email" not in user_details:
      return jsonify({ "error" : "Invalid Access token" }), 401

    db_user_details = user.get_user_details(user_details["email"])

    if not db_user_details:
      return jsonify({ "error" : "Invalid access token" }), 401
    
    if db_user_details["refresh_token"] != refresh_token:
      return jsonify({ "error" : "Invalid Access token" }), 401

    user_details = {
      "name": user_details["name"],
      "email": user_details["email"]
    }
    access_token = user.get_access_token(user_details)
    refresh_token = user.get_refresh_token(user_details)
    user.update_refresh_token(user_details["email"], refresh_token)

    return { "access_token": access_token, "refresh_token": refresh_token }

  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

def logout():
  try:
    # email = session.get('email', 'not set')
    # if (email == 'not set'):
    #   return "User is not logged in"
    
    # ! TODO : Remove session or Clear jwt token
    # session.pop('email')

    return f"User logged out successfully"
  except Exception as e:
    return jsonify({"error": "Error getting json out of request"}), 400

@validate_request_body
@validate_request_properties(['email'])
def requestPasswordReset():
  try:
    request_data = request.json
    email = request_data["email"]

    user = User()
    # saves token hash in db & returns token for user
    token = user.generate_password_reset_token(email)

    # ! Send email and remove token from response 
    return { "token" : token }  
    # return { "Success": "Email sent. Please check and validate" }
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

@validate_request_body
@validate_request_properties(['email', 'token'])
def validatePasswordResetToken():
  try:
    request_data = request.json
    token = request_data["token"]
    email = request_data["email"]

    user = User()
    valid = user.validate_password_reset_token(email, token)

    if "error" in valid:
      return jsonify({"status": "Invalid token"}), 412

    if valid:
      return jsonify({"status": "Ready for new password"}), 200

    return jsonify({"status": "Invalid token"}), 412
  except Exception as e: 
    print("E", e)
    return jsonify({"error": "Some error occured and figure it out" }), 400

@validate_request_body
@validate_request_properties(['password', 'email', 'token'])
def resetPassword():
  try:
    request_data = request.json
    email = request_data['email']
    password = request_data['password']
    token = request_data['token']

    user = User()
    valid = user.validate_password_reset_token(email, token)

    if "error" in valid:
      return jsonify({"status": "Invalid token"}), 412

    response = user.update_password(email, password)

    if "error" in response:
      return jsonify({"password_validation_error": response["error"] }), 415
      
    return { 'status': "Password set successfully" }
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400
