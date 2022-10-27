from flask import Blueprint, render_template

htmlTemplate = Blueprint('htmlTemplate', __name__)

@htmlTemplate.route("/basic-html")
def basicHTML(): 
  return render_template("basic.html")

@htmlTemplate.route("/jinja-html")
def jinjaHTML():
  return render_template("index.html")

@htmlTemplate.route("/jinja-html-2")
def jinjaHTML2():
  return render_template("index2.html")