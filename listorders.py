from flask import Blueprint
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

listorders = Blueprint('listorders', __name__)

@listorders.route('/listorders/<companyno>')
def getorderlist(companyno):
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://business.visma.net/api/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True, headers={ 'Authorization': 'Bearer ' + token })

    # Provide a GraphQL query
    query = gql(
            """
            {
                useCompany(no:3538773)
                {
                    order{
                        items{
                            orderNo
                            name
                            transactionType
                            orderDate
                            customerNo
                            supplierNo
                        }
                    }
                }
            }
        """
        )

    # Execute the query on the transport
    result = client.execute(query)
    print(result)