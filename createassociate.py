from flask import Blueprint, render_template, session, request
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

createassociate = Blueprint('createassociate', __name__)


@createassociate.route('/createassociate', methods=['GET'])
def getData():

    return render_template('createassociate.html')

    
@createassociate.route('/createassociate', methods=['POST'])
def postAssociate():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://business.visma.net/api/graphql",
                                 headers={'Authorization': 'Bearer ' + session["token"]})

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        mutation create_associate($companyno : Int!, $name : String, $shortName : String, $customerNumber : Int, $supplierNumber : Int)
        {
            useCompany(no : $companyno)
            {
                    associate_create(values:[{
                        name : $name
                        shortName : $shortName
                        customerNo : $customerNumber
                        supplierNo : $supplierNumber
                        }
                        ])
                    {
                        affectedRows
                            items{
                                associateNo
                                customerNo
                                name
                                shortName
                                }
                        }
                }
        }
        """
    )
    

    params = {"companyno": int(session["companyno"]), 
    'name' : request.form['name'], 
    'shortName': request.form['shortName'], 
    'customerNumber' : int(request.form['customerNo']) if request.form['customerNo'] != '' else None, 
    'supplierNumber' : int(request.form['supplierNo']) if request.form['supplierNo'] != '' else None}

    # Execute the query on the transport
    result = client.execute(query, variable_values=params)

    return render_template("createassociate.html", associates=result["useCompany"]["associate_create"]["items"])
