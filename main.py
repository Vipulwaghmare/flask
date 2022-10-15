from flask import Flask, g
from model.Email import Email 
from routes.html import htmlTemplate
from routes.basic import basicRoutes
from routes.auth import authRoutes
from routes.test import testRoutes

from flask_session import Session

from model.Logger import Logger

logger = Logger.get_instance() 

app = Flask(__name__)

# secret key and type to use session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

Session(app)

@app.before_request
def beforeRequest():
  print("This is printing Before each request")
  # ? Can be used for * #
  # ? Opening database connections.
  # ? tracking user actions
  # ? adding a “back button” feature by remembering the last page the user visited before loading the next
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

# Creating routes in different folder because we don't need to cluster here
app.register_blueprint(htmlTemplate)
app.register_blueprint(basicRoutes)
app.register_blueprint(testRoutes)
app.register_blueprint(authRoutes, url_prefix="/api/v1/")

@app.teardown_appcontext
def teardown(self):
  db = g.pop('db', None)
  try:
    if db is not None:
      db.close()
  except Exception as e:
    logger.log.error(f"[Login] {str(e)}")

if __name__ == "__main__":
  app.run(port=1000, debug=True)
  # debug = True ==> Starts in development mode, restarts server when changes happen
  # port = 1000 ==> Starts on port : 1000 , default port is 5000
