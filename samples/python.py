from google.cloud import secretmanager
from flask import Flask
from flask import Response, request
import requests
import json
import os
import sqlalchemy

def main(initial_request):
    try:
        request_json = initial_request.get_json()
        print("Request received: {}".format(request_json))    
        product = request_json['sessionInfo']['parameters']['product']
        quantity = request_json['sessionInfo']['parameters']['quantity']
        pool = db_login(product, quantity)
        tag = request_json['fulfillmentInfo']['tag']
        
        print("tag : {}".format(tag))      
        if tag == 'phoneLookup':
            print("Tag flow for: {tag}")
        else:
            print("Else: ")           
        msg = 'Sample response'
        WebhookResponse=answer_webhook(msg)
        return WebhookResponse

    except Exception as error:
        print('Error at main: ' + repr(error))    

def answer_webhook(msg):
    message= {"fulfillment_response": {
        "messages": [
        {
          "text": {
            "text": [msg]
          }
        }
      ]
    }
    }
    return Response(json.dumps(message), 200)
    #return Response(json.dumps(message), 200, mimetype='application/json')

def db_login(product, quantity) -> sqlalchemy.engine.base.Engine:
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Organize the Secret Keys
    db_user_prod = "DB_USER_PROD"
    db_pass_prod = "DB_PASS_PROD"

    # Pass in the GCP Project ID
    project_id = os.environ["gcp_project_id"]
    
    # Obtain the Secret Name Path
    db_user_prod_name = f"projects/{project_id}/secrets/{db_user_prod}/versions/latest"
    db_pass_prod_name = f"projects/{project_id}/secrets/{db_pass_prod}/versions/latest"
    
    # Obtain the Latest Secret Version
    db_user_prod_response = client.access_secret_version(db_user_prod_name)
    db_pass_prod_response = client.access_secret_version(db_pass_prod_name)

    # Parse the Secret Response & Decode Payload
    db_user_prod_secret = db_user_prod_response.payload.data.decode('UTF-8')  
    db_pass_prod_secret = db_pass_prod_response.payload.data.decode('UTF-8') 

    # Assign Variables to Pass 
    connection_name = os.environ["gcp_connection_name"]
    table_name = os.environ["gcp_table_name"]
    table_field1 = os.environ["gcp_table_field1"]
    #table_field_value1 = "'From cf name2'"
    table_field_value1 = product
    table_field2 = os.environ["gcp_table_field2"]
    #table_field_value2 = "'front cf content2'"
    table_field_value2 = quantity
    db_name = os.environ["gcp_db_name"]
    db_user = db_user_prod_secret
    db_password = db_pass_prod_secret

    # If your database is MySQL, uncomment the following two lines:
    #driver_name = 'mysql+pymysql'
    #query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

    driver_name = 'postgresql+pg8000'
    query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})
    stmt = sqlalchemy.text('insert into {} ({}, {}) values ({}, {})'.format(table_name, table_field1, table_field2, table_field_value1, table_field_value2))
        
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    try:
        with db.connect() as conn:
            print('before execute')
            print(stmt)
            conn.execute(stmt)
            print('after execute')
    except Exception as e:
        return 'Error: {}'.format(str(e))
    return 'ok'