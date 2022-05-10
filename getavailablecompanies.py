import json
from flask import Blueprint, render_template, session
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

getavailablecompanies = Blueprint('getavailablecompanies', __name__)

@getavailablecompanies.route('/getavailablecompanies')
def getavailcompanies():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://business.visma.net/api/graphql", headers={ 'Authorization': 'Bearer ' + session["token"] })

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
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

    # parsed = client.parse_results(result)

    return render_template("getavailablecompanies.html", availcompanies = result["availableCompanies"])    