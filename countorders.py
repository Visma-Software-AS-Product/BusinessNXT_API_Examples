from flask import Blueprint, render_template, session
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

countorders = Blueprint('countorders', __name__)

@countorders.route('/countorders')
def gettotalorders():
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
                    order_aggregate{
                        count{
                            orderNo
                            }
                        }
                }            
            }
        """
        )
    
    params = {"companyno": int(session["companyno"])}

    # Execute the query on the transport
    result = client.execute(query, variable_values=params)
    
    return render_template("countorders.html", orders = result["useCompany"]["order_aggregate"]["count"])   