# Imports

## Import required Flask modules
from flask import Flask, render_template

## Import OS-module to access environment-variables
import os

## Import the blueprints for the functionality in this application
## We have chosen to use Flask blueprints so that we can separated the funtionality in smaller, more readable modules 
from authenticate import authenticate
from listorders import listorders
from getavailablecompanies import getavailablecompanies
from countorders import countorders
from createorder import createorder
from addorderlines import addorderlines
from createassociate import createassociate

# Creates the Flask application
app = Flask(__name__)

# Sets the secret key for the Flask application, to be able to store values in session
app.secret_key = os.environ.get('SECRET_KEY') 

# Register the blueprints containing all the funtionality of the application
app.register_blueprint(authenticate)
app.register_blueprint(listorders)
app.register_blueprint(getavailablecompanies)
app.register_blueprint(countorders)
app.register_blueprint(createorder)
app.register_blueprint(addorderlines)
app.register_blueprint(createassociate)

# Defines the default route of the application, this will serve the index-page
@app.route("/")
def index():
    # Returns the template index.html
    return render_template("index.html")