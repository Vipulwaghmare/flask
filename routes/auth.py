import json
from flask import Blueprint, request, Response, jsonify, session
from model.Crypto import Crypto
from model.Auth import Authorization
from utils.requestValidation import  validate_request_body, validate_request_properties, validate_request_schema

authRoutes = Blueprint('authRoutes', __name__)

# ! TO DO
@authRoutes.route("/register", methods=["POST"])
@validate_request_body
@validate_request_properties(['email', 'password'])
@validate_request_schema("jsonSchemas/login.json")
def register():
  try:
    request_data = request.get_json()
    return request_data
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

@authRoutes.route("/requestPasswordReset", methods=["POST"])
@validate_request_body
@validate_request_properties(['email'])
def requestPasswordReset():
  try:
    request_data = request.get_json()
    email = request_data["email"]

    # Create Token
    crypto = Crypto()
    token = crypto.generate_random()
    hash_for_session = crypto.create_api_key(token)
    session['reset_hash'] = hash_for_session
    # ! Send email
    return { "token" : token }  
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

@authRoutes.route("/validatePasswordResetToken", methods=["POST"])
@validate_request_body
@validate_request_properties(['email'])
def validatePasswordResetToken():
  try:
    request_data = request.get_json()
    token = request_data["token"]
    session_token_hash = session.get('reset_hash', False)
    # Create Token
    crypto = Crypto()
    valid = crypto.validate_hash(token, session_token_hash)
    if valid:
      return jsonify({"status": "Ready for new password"}), 200
    return jsonify({"status": "Invalid token"}), 412
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

@authRoutes.route("/resetPassword", methods=["POST"])
@validate_request_body
@validate_request_properties(['password'])
def resetPassword():
  try:
    request_data = request.get_json()
    password = request_data['password']
    authorization = Authorization()
    response = authorization.set_password(password)
    if "error" in response:
      return jsonify({"password_validation_error": response["error"] }), 415
    session['hashedpass'] = response["hash_password"]
    return { 'status': "Password set successfully "}
  except Exception as e:
    print("ERRO",e)
    return jsonify({"error": "Some error occured and figure it out" }), 400

# ! TO DO
@authRoutes.route("/login", methods=['POST'])
@validate_request_body
@validate_request_properties(['email', 'password'])
@validate_request_schema("jsonSchemas/login.json")
def login():
  try:
    request_data = request.get_json()
    # session['email'] = request_data['email']
    (email, password) = (request_data["email"], request_data["password"])
    # * Validate password
    hashed_password = session.get('hashedpass')
    bytes_hashed_password = hashed_password.encode("utf8")
    crypto = Crypto()
    valid = crypto.validate_hash(password, bytes_hashed_password)
    if valid:
      return f"logged in with email { request_data['email']}"
    return { "error": "Error" }
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400

# ! TO DO
@authRoutes.route("/logout", methods=['POST', "GET"])
def logout():
  try:
    email = session.get('email', 'not set')
    if (email == 'not set'):
      return "User is not logged in"
    session.pop('email')
    return f"User logged out successfully with email {email}"
  except Exception as e:
    print(e)
    return jsonify({"error": "Error getting json out of request"}), 400