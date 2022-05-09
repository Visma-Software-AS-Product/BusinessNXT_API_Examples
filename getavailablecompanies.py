from flask import Blueprint
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

getavailablecompanies = Blueprint('getavailablecompanies', __name__)

@getavailablecompanies.route('/getavailablecompanies')
def getavailcompanies():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://business.visma.net/api/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True, headers={ 'Authorization': 'Bearer ' + token })

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
    print(result)