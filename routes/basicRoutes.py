from flask import Blueprint, request, Response, jsonify

basicRoutes = Blueprint('basicRoutes', __name__)

@basicRoutes.route("/get-request")
def getRequest():
  return { "message": "This is GET request" }

@basicRoutes.route("/post-request", methods=['POST'])
def postRequest():
  try:
    request_data = request.get_json()
  except Exception as e:
    return jsonify({"error": "Error getting json out of request"}), 400
  
  if "send_facts" in request_data:
    if request_data['send_facts']:
      return  "Taarak Mehta Ka oolta chashma is the worst show ever" 
    return "You don't need any facts"
  return { "your request is" : request_data }

@basicRoutes.route("/put-request", methods=['PUT'])
def putRequest():
  try:
    request_data = request.get_json()
  except Exception as e:
    return jsonify({"error": "Error getting json out of request"}), 400
  return { "your put request is" : request_data }

@basicRoutes.route("/delete-request", methods=['DELETE', "POST"])
def deleteRequest():
  try:
    method = request.method
    request_data = request.get_json()
  except Exception as e:
    return jsonify({"error": "Error getting json out of request"}), 400
  return { f"your {method} request is" : request_data }