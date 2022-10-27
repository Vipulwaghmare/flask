from flask import Blueprint, request 
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

@basicRoutes.route("/get")
def getRequest():
  return { "message": "This is GET request" }

@basicRoutes.route("/post", methods=['POST'])
def postRequest():
  # return { "success" : "This is default 200" }
  # raise Exception("HI")
  # return {"error": "This is throwing some error"}, 400
  return [1,2,3,4,5] 

@basicRoutes.route("/put-request", methods=['PUT'])
def putRequest():
  try:
    request_data = request.json
  except Exception as e:
    return {"error": "Error getting json out of request"}, 400
  return { "your put request is" : request_data }

@basicRoutes.route("/delete-put-request", methods=['DELETE', "PUT"])
def deleteRequest():
  method = request.method
  if method == "PUT":
    return { "Success": "You sent a PUT request" }
  if method == "DELETE":
    return { "Success": "You sent a DELETE request" }
  return f"This is method: {method}"

@basicRoutes.route('/form-data', methods =["POST"])
def formData():
  name = request.form.get("name") 
  # check if the post request has the file part
  if 'file' not in request.files:
    return { 'error': "no file found" }, 400
  file = request.files['file']
  if file.filename == '':
    return { 'error': 'file has no name :(' } , 400
  filename = file.filename
  if file:
    file.save(filename)
    return { 'success': 'downloaded file successfully' }
  
@basicRoutes.route('/query-request')
def queryRequest():
  name = request.args.get("name")
  profession = request.args.get("profession")
  print("ARGS", request.args)
  return {
    "name": name,
    "profession": profession
  }

@basicRoutes.route('/search/<name>')
def my_view_func(name):
  return { "Success": f"You searched for {name}"}