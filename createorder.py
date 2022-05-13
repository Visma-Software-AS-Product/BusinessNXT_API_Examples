from datetime import date
from flask import Blueprint, render_template, session, request
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

createorder = Blueprint('createorder', __name__)


@createorder.route('/createorder', methods=['GET'])
def getOrderData():

    return render_template('createorder.html')

    
@createorder.route('/createorder', methods=['POST'])
def postorder():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://business.visma.net/api/graphql",
                                 headers={'Authorization': 'Bearer ' + session["token"]})

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        mutation create_order($companyno : Int!, $customerNumber : Int!, $orderName : String, $orderDate : Int)
        {
            useCompany(no : $companyno)
            {
                    order_create(values:[{
                        orderDate : $orderDate
                        customerNo : $customerNo
                        name : $orderName
                        }
                        ])
                    {
                        affectedRows
                            items{
                                orderNo
                                orderDate
                                customerNo
                                }
                        }
                }
        }
        """
    )

    params = {"companyno": int(session["companyno"]),
     'customerNumber' : int(request.form['customerNo']), 
    'orderName': request.form['orderName'], 
    'orderdate' : int(request.form['orderDate'])}

    # Execute the query on the transport
    result = client.execute(query, variable_values=params)

    return render_template("createorder.html", orders=result["useCompany"]["order_create"]["items"] )
