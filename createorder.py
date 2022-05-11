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
        mutation create_order($companyno : Int!, $customerNo : Int!, $orderName : String)
        {
            useCompany(no : $companyno)
            {
                    order_create(values:[{
                        orderDate : 20220511
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

    params = {"companyno": int(session["companyno"]), 'customerNo' : int(request.form['customerNo']), 
    'orderName': request.form['orderName']}

    # Execute the query on the transport
    result = client.execute(query, variable_values=params)

    return render_template("createorder.html", orders=result["useCompany"]["order_create"]["items"] )
