from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

@app.route("/")
def index():
  return "Hello, World!"

# ! Rendering HTML Templates
@app.route("/basic-html")
def basicHTML():
  # To return html template: it automatically picks from templates folder 
  return render_template("basic.html")

@app.route("/jinja-html")
def jinjaHTML():
  # To return html template: it automatically picks from templates folder 
  return render_template("index.html")

@app.route("/jinja-html-2")
def jinjaHTML2():
  # To return html template: it automatically picks from templates folder 
  return render_template("index2.html")

if __name__ == "__main__":
  app.run(port=1000, debug=True)
  # debug = True ==> Starts in development mode, restarts server when changes happen
  # port = 1000 ==> Starts on port : 1000 , default port is 5000
