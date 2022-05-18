# The Visma Busniess NXT API uses OAuth 2.0 for authentication. 
# Two different flows are supported:
#   - Authentication Code Flow for applications that has user interaction, this flows requires that the user logs in with a username and 
#     password. The integration will impersonate this user when makong API-calls.
#   - Client Credentials Flow* for non-interactive integrations, this flows authenticates without requiring a user, the integration will 
#     identify as itself and not a user. Ideal for machine-to-machine type integrations. 
# Both scenarios requires that the application/integration is known by Visma, therefore the application must be created in Visma Developer Portal
# and request access to the Visma Business NXT API before authentication.  

# *: Not released yet

# https://docs.business.visma.net/docs/authentication/overview

# This examples demonstrates the Authentication Code flow (user interactive). The the required steps in the flow are:
# 1. The user is redirected to the Visma Connect login-screen (this is done in method "login()")
# 2. When the user has benn authenticated, Visma Connect as the user for this applications permission to access their 
#    data on behalf of the user.
# 3. When the permission/conscent is given Visma Connect redirects the browser back to the application using the redirectURI
# 4. The application receives the redirect-call including a code.
# 5. The application exchanges the received code with a token that can be used to access the API. 

# --------------------------------------------------------------------------------------------------

# Imports

## OS imports
import os, uuid, requests
from datetime import datetime, timedelta

## Required Flask modules
from flask import Blueprint, redirect, session, url_for, request, json

# Creates a blueprint of this module to be used in app.py
authenticate = Blueprint('authenticate', __name__)

# The login-function reachable at route /login. 
# The task of this method is to redirect the user to the Visma Connect login-page
@authenticate.route('/login')
def login():

    # The redirectURI is the URL that Visma Connect uses to redirect the user back to this application.
    # The method "authorize" is our redirect, we use url_for to get the external url to this method.
    # NB! The redirectURI needs to be registered in Visma Developer Portal before use.
    redirect_uri = url_for('authenticate.authorize', _external=True)

    # We vuild the URL to redirect the user to   
    vnurl = "https://connect.visma.com/connect/authorize" # BaseURL for Visma Connect authorization
    vnurl += "?response_type=code" # Defines that we would like to have a code back to our redirectURI
    vnurl += "&client_id=" + os.environ.get('CONNECT_CLIENT_ID') # We need to provide this applications ClientID (application must be registered in Visma Developer Portal)
    vnurl += "&redirect_uri=" + redirect_uri # The redirectURI where we expect the user to be redirected to after login/conscent
    vnurl += "&scope=openid profile email business-graphql-api:access-group-based" # The scopes (API access rights) this application requires                

    # Redirects the browser to the created URL
    return redirect(vnurl)

# The authorize-function (redirect-uri). Visma Connect will redirect the browser to this URL after the login/conscent process
@authenticate.route('/authorize')
def authorize():

    # The request contains an argument called code, which contains the code that can exchanged for a token
    code = request.args['code']
    
    # Build the request-data to be sent to the token-request, since this data conatins the client_secret this information 
    # must be sent in the request payload (encrypted via HTTPS).
    reqdata = "grant_type=authorization_code" # The grant_type to use
    reqdata += "&code=" + code # The code received in the request
    reqdata += "&client_id=" + os.environ.get('CONNECT_CLIENT_ID') # The applications ClientID
    reqdata += "&client_secret=" + os.environ.get('CONNECT_CLIENT_SECRET') # The applications ClientSecret
    reqdata += "&redirect_uri=" + url_for('authenticate.authorize', _external=True) # The redirectUri used
    
    # We use the requests module to send a POST-request to Visma Connect to exchange the code for a token
    response = requests.post("https://connect.visma.com/connect/token",
                             data=reqdata,
                             headers={'Content-Type': 'application/x-www-form-urlencoded'}
                             )

    # Check the response from the API-call, we expect HTTP status 200 (Success)
    if response.status_code == 200:
        # The data is returned as JSON, we use the json-module to parse into a JSON-object
        json_data = json.loads(response.text)

        # Sets the token in the browser session
        session["token"] = json_data["access_token"] 

        # We also set session-value with the expiretime of the token to display this to the user (Optional)   
        session["expiretime"] = datetime.now() + timedelta(seconds=json_data["expires_in"])

        # Redirects the browser back to the index-page
        return redirect("/")   