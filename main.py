from flask import Flask, g
from routes.auth import authRoutes

from flask_session import Session

from services.Logger import Logger

logger = Logger.get_instance() 

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

Session(app)

@app.route("/")
def index():
  return "Hello, World!"

app.register_blueprint(authRoutes, url_prefix="/api/v1/")

@app.teardown_appcontext
def teardown(self):
  db = g.pop('db', None)
  try:
    if db is not None:
      db.close()
  except Exception as e:
    logger.log.error(f"[Login] {str(e)}")
    
@app.errorhandler(404)
def page_not_found(error):
  return {
    "error": "You are lost dude!"
  }, 404

@app.errorhandler(Exception)
def exception_handler(error):
  return {
    "error": "We have failed you. Apologies. :("
  }, 500

app.debug = True
if __name__ == "__main__":
  app.run(port=1000)
  # debug = True ==> Starts in development mode, restarts server when changes happen
  # port = 1000 ==> Starts on port : 1000 , default port is 5000
