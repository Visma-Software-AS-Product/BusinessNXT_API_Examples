from datetime import datetime, timedelta
from flask import Blueprint, redirect, session, url_for, request, json
import os, uuid, requests

authenticate = Blueprint('authenticate', __name__)

# The login-function reachable at route /login
@authenticate.route('/login')
def login():

    redirect_uri = url_for('authenticate.authorize', _external=True)

    # URL for new token   
    vnurl = "https://connect.visma.com/connect/authorize"
    vnurl += "?response_type=code"
    vnurl += "&client_id=" + os.environ.get('CONNECT_CLIENT_ID')
    vnurl += "&redirect_uri=" + redirect_uri
    vnurl += "&scope=openid profile email business-graphql-api:access-group-based"
    vnurl += "&state=" + str(uuid.uuid4())                

    return redirect(vnurl)

    # # Creates the Visma Connect OAuth Client
    # vismaconnect = oauth.create_client('Visma Connect')
    # # Generates the authorize redirect-uri (must be registered with the application in Visma Developer Portal) 
    # redirect_uri = url_for('authorize', _external=True)
    # # Starts the authorization and redirect-process
    # return vismaconnect.authorize_redirect(redirect_uri)

# The authorize-function (redirect-uri)
@authenticate.route('/authorize')
def authorize():

    code = request.args['code']
    
    reqdata = "grant_type=authorization_code"
    reqdata += "&code=" + code
    reqdata += "&client_id=" + os.environ.get('CONNECT_CLIENT_ID')
    reqdata += "&client_secret=" + os.environ.get('CONNECT_CLIENT_SECRET')
    reqdata += "&redirect_uri=https://127.0.0.1:5000/authorize"
    
    response = requests.post("https://connect.visma.com/connect/token",
                             data=reqdata,
                             headers={'Content-Type': 'application/x-www-form-urlencoded'}
                             )

    if response.status_code == 200:
        json_data = json.loads(response.text)

        # Sets the token in the browser session
        session["token"] = json_data["access_token"]    
        session["expiretime"] = datetime.now() + timedelta(seconds=json_data["expires_in"])

        return redirect("/")    
