
# This module demonstrates the Visma Business NXT API-call to get a list of the available companies for the current context

# Imports

## Imports required Flask modules
from flask import Blueprint, redirect, render_template, session

## We us a component called gql to communicate with the Visma Business NXT GraphQL API (https://pypi.org/project/gql/)
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Creates a blueprint of this module to be used in app.py
getavailablecompanies = Blueprint('getavailablecompanies', __name__)

# Register route for function getavailablecustomers
@getavailablecompanies.route('/getavailablecompanies')
def getavailcompanies():

    # Select the transport with a defined url endpoint
    transport = AIOHTTPTransport(
        url="https://business.visma.net/api/graphql", # GraphQL endpoint
        headers={ 'Authorization': 'Bearer ' + session["token"] }) # Adds the Authorization HTTP header

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)    

    # Creates the GraphQL query
    query = gql(
        """
        {
            availableCompanies 
            {
                totalCount
                items {
                name
                vismaNetCompanyId
                }
            }
        }
    """
    )

    # Execute the query on the transport
    result = client.execute(query)

    # Extract the available companies list from the result, send this as a parameter to the html-template
    return render_template("getavailablecompanies.html", availcompanies = result["availableCompanies"])    

# Creates route for the function to set the companynumber in session
@getavailablecompanies.route('/setselectedcompany/<companyno>')
def setselectedcompany(companyno):
    session["companyno"] = companyno

    # Returns to index-page
    return redirect("/")