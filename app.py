# The Visma Busniess NXT API uses OAuth 2.0 for authentication. 
# Two different flows are supported:
#   - Authentication Code Flow for applications that has user interaction, this flows requires that the user logs in with a username and 
#     password. The integration will impersonate this user when makong API-calls.
#   - Client Credentials Flow for non-interactive integrations, this flows authenticates without requiring a user, the integration will 
#     identify as itself and not a user. Ideal for machine-to-machine type integrations.
# Both scenarios requires that the application/integration is known by Visma, therefore the application must be created in Visma Developer Portal
# and request access to the Visma Business NXT API before authentication.  

# https://docs.business.visma.net/docs/authentication/overview

from flask import Flask, render_template

from authenticate import authenticate
# from authenticate_authlib import authenticate_authlib
from listorders import listorders
from getavailablecompanies import getavailablecompanies

import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') 

app.register_blueprint(authenticate)
# app.register_blueprint(authenticate_authlib)
app.register_blueprint(listorders)
app.register_blueprint(getavailablecompanies)

@app.route("/")
def index():
    return render_template("index.html")