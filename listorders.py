from flask import Blueprint, render_template, session
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

listorders = Blueprint('listorders', __name__)

@listorders.route('/listorders')
def getorderlist():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://business.visma.net/api/graphql", headers={ 'Authorization': 'Bearer ' + session["token"] })

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
            """
            query getorders ($companyno: Int!)
            {                
                useCompany(no: $companyno)
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
    
    params = {"companyno": int(session["companyno"])}

    # Execute the query on the transport
    result = client.execute(query, variable_values=params)
    
    return render_template("listorders.html", orders = result["useCompany"]["order"])    