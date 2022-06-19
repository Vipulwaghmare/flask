from flask import Flask 
from routes.htmlTemplate import htmlTemplate
from routes.basicRoutes import basicRoutes

app = Flask(__name__)

@app.route("/")
def index():
  return "Hello, World!"

# Creating routes in different folder because we don't need to cluster here
app.register_blueprint(htmlTemplate)
app.register_blueprint(basicRoutes)


if __name__ == "__main__":
  app.run(port=1000, debug=True)
  # debug = True ==> Starts in development mode, restarts server when changes happen
  # port = 1000 ==> Starts on port : 1000 , default port is 5000
