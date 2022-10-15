from flask import Blueprint, request, jsonify 
# Request:
# .method => to get method
# .json => to get request data 

# Response
# dict => will automatically converted JSON
# array => use jsonify to convert it to JSON

basicRoutes = Blueprint('basicRoutes', __name__)

@basicRoutes.before_request
def beforeBasicRequest():
  print("This is printing Before Basic route request")
  pass

@basicRoutes.after_request
def afterBasicRequest(res):
  print("This is printing after Basic route request")
  return res

@basicRoutes.route("/get-request")
def getRequest():
  return { "message": "This is GET request" }

@basicRoutes.route("/post-request", methods=['POST'])
def postRequest():
  try:
    return request.json
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
    request_data = request.json
  except Exception as e:
    return jsonify({"error": "Error getting json out of request"}), 400
  return { "your put request is" : request_data }

@basicRoutes.route("/delete-request", methods=['DELETE', "POST"])
def deleteRequest():
  try:
    method = request.method
    request_data = request.json
  except Exception as e:
    return jsonify({"error": "Error getting json out of request"}), 400
  return jsonify([{ f"your {method} request is" : request_data }])

@basicRoutes.route('/form-data', methods =["POST"])
def gfg():
  first_name = request.form.get("fname")
  last_name = request.form.get("lname") 
  # check if the post request has the file part
  if 'file' not in request.files:
    return { 'error': "no file found" }
  file = request.files['file']
  # If the user does not select a file, the browser submits an
  # empty file without a filename.
  if file.filename == '':
    return { 'error': 'file has no name :(' } 
  filename = file.filename
  if file:
    file.save(filename)
    return { 'success': 'downloaded file successfully' } 
  return { 'success': 'somehow execution ended' } 
  
@basicRoutes.route("/error-request")
def errorRequest():
  raise Exception("This is error route")
  return { "message": "This is Error request" }
