from datetime import date
from flask import Blueprint, render_template, session, request
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

addorderlines = Blueprint('addorderlines', __name__)


@addorderlines.route('/addorderlines', methods=['GET'])
def getOrderData():

    return render_template('addorderlines.html')

    
@addorderlines.route('/addorderlines', methods=['POST'])
def postorderLines():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://business.visma.net/api/graphql",
                                 headers={'Authorization': 'Bearer ' + session["token"]})

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        mutation create_order_line($companyno : Int!, $orderNumber : Int!, $productNumber: String, $quantity : Decimal)
        {
            useCompany(no : $companyno)
            {
                    orderLine_create(values:[{
                        orderNo : $orderNumber
                        productNo : $productNumber
                        quantity : $quantity
                        }
                        ])
                    {
                        affectedRows
                            items{
                                lineNo
                                orderNo
                                }
                        }
                }
        }
        """
    )

    params = {"companyno": int(session["companyno"]), 
    'orderNumber' : int(request.form['orderNo']), 
    'productNumber': request.form['productNo'], 
    'quantity' : int(request.form['quantity'])}

    # Execute the query on the transport
    result = client.execute(query, variable_values=params)

    return render_template("addorderlines.html", orders=result["useCompany"]["orderLine_create"]["items"] )
