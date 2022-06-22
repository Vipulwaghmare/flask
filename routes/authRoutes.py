from flask import Blueprint, request, Response, jsonify, session


authRoutes = Blueprint('authRoutes', __name__)

@authRoutes.route("/login", methods=['POST'])
def login():
  try:
    request_data = request.get_json()
    session['email'] = request_data['email']
    return f"logged in with email { request_data['email']}"
  except Exception as e:
    return jsonify({"error": "Some error occured and figure it out" }), 400


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