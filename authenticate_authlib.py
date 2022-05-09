from flask import Blueprint, redirect, session, url_for, request, json
import os, uuid, requests
from authlib.integrations.flask_client import OAuth

authenticate_authlib = Blueprint('authenticate.authlib', __name__)

oauth = OAuth(authenticate_authlib)

vismaconnect = oauth.register(
    name='Visma Connect',
    client_id=os.environ.get('CONNECT_CLIENT_ID'),
    client_secret=os.environ.get('CONNECT_CLIENT_SECRET'),
    access_token_url='https://connect.visma.com/connect/token',
    access_token_params=None,
    authorize_url='https://connect.visma.com/connect/authorize',
    authorize_params=None,
    api_base_url='https://connect.visma.com/connect/',
    client_kwargs={'scope': 'openid profile email business-graphql-api:access-group-based'}  
)


# The login-function reachable at route /login
@authenticate_authlib.route('/login')
def login():

    # Creates the Visma Connect OAuth Client
    vismaconnect = oauth.create_client('Visma Connect')
    # Generates the authorize redirect-uri (must be registered with the application in Visma Developer Portal) 
    redirect_uri = url_for('authorize', _external=True)
    # Starts the authorization and redirect-process
    return vismaconnect.authorize_redirect(redirect_uri)

@authenticate_authlib.route("/authorize")
def authorize():

    # Creates the Visma Connect OAuth Client
    vismaconnect = oauth.create_client('Visma Connect')
    # Collects the access-token
    token = vismaconnect.authorize_access_token()

    # Makes a call the get the user-information for the current user
    resp = vismaconnect.get('userinfo', token = token)
    # Checks for valid response-code (200-series)
    resp.raise_for_status()
    # Gets the user-info object from the response
    user_info = resp.json()

    # Sets the users name and email in the session
    session["name"] = user_info["name"]
    session["email"] = user_info["email"]

    # Redirects to the main-function
    return redirect('/')
