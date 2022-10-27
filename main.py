from sys import prefix
from flask import Flask
from routes.html import htmlTemplate
from routes.basic import basicRoutes

app = Flask(__name__)

@app.before_request
def beforeRequest():
  print("This is printing Before each request")
  # ? Can be used for * #
  # ? Opening database connections.
  # ? tracking user actions
  # ? determining user permissions, etc……
  pass

@app.after_request
def afterRequest(res):
  print("This is printing after each request")
  # ? close a database connection * #
  # ? To alert the user with changes in the application, etc…. * #
  # ! Always return response in after request
  return res

@app.route("/")
def index():
  return "Hello, World!"

@app.route("/", methods=['POST'] )
def postIndex():
  return "This is post request"

# Creating routes in different folder because we don't need to cluster here
app.register_blueprint(htmlTemplate, url_prefix="/api/v1/")
app.register_blueprint(basicRoutes, url_prefix="/api/v1/")

@app.teardown_appcontext
def teardown(self):
  print("Ending app context")
    
@app.errorhandler(404)
def page_not_found(error):
  return {
    "error": "Oops! This page doesn't exist."
  }, 404

@app.errorhandler(Exception)
def exception_handler(error):
  return {
    "error": "This is error caught in Error Handler"
  }, 500

app.debug = True
if __name__ == "__main__":
  app.run(port=1000, debug = True)
  # debug = True ==> Starts in development mode, restarts server when changes happen
  # port = 5000 ==> Starts on port : 5000 , default port is 5000
