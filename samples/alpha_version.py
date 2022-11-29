from flask import Flask
from flask import Response, request
import requests
import json
import os
import sqlalchemy
import time

### Global Variables
db_name = "retail"
db_user = "postgres"
db_password = "Al0h0m0ra!"
connection_name = "hospitality-demo-361210:us-central1:dfcxlabs"
driver_name = 'postgresql+pg8000'
query_string = dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})
#---------------#

def main(initial_request):
    
    print(initial_request)
    request_json = initial_request.get_json()
    tag = request_json['fulfillmentInfo']['tag']
    ver = os.environ.get('K_REVISION')
    print(f"Python Function version: {ver}")
    print("main - print: {}".format(request_json))
    
    # Evaluate webhook tag
    if tag == 'validate-pin':
        print("Tag flow for: {tag}")
        msg, params = db_validate_pin(initial_request)
    elif tag == 'update-order':
        msg, params = "update-order"
        update_orders()
    elif tag == 'empty-orders-table':
        empty_orders_table()
        msg, params = "empty-table"
    else:
        msg = "Unknown tag"
        params = {}
    
    WebhookResponse=answer_webhook(msg)
    return WebhookResponse

#---------------#
def answer_webhook(msg):
    message = {
        "session_info": {
            "parameters" : {
                "wh_execution_time":time.time()
            }    
        },
        "fulfillment_response": {
            "messages": [
                {   
                    "text": {
                        "text": [msg]
                    }
                }
            ]
        }
    }
    message_temp =  {
        "session_info": {
            "parameters" : {
                "wh_execution_time":time.time()
            }    
        },
        "fulfillment_response": {
            "messages": [
                {   
                    "text": {
                        "text": [msg]
                    }
                }
            ]
        }
    }
    message_temp["session_info"]["parameters"]["p1"]=1
    
    print (f'El tipo de respuesta es {type(message_temp)}')
    return Response(json.dumps(message_temp), 200)

def db_validate_pin(req):
    request_json = req.get_json()
    print (f'the type of request is {type(request_json)}')
    typed_pin_param = request_json['sessionInfo']['parameters']['pin_number']
    # The param is received like a list. Let's extract the value
    typed_pin = typed_pin_param[0]
    print (f'the number typed is {typed_pin} of type {type(typed_pin)}')
    table_name = "customers"

    stmt1 = sqlalchemy.text(f'select customerPIN from {table_name}')
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
            print(stmt1)
            result = conn.execute(stmt1).fetchone()
            stored_pin = result[0]
            
            if (str(stored_pin) == str(typed_pin)):
                print ("same pin")
            else:
                print ("wrong pin")
            print (f'after execute data returnned {stored_pin}')
            return f'after execute data returnned {stored_pin}'
            
    except Exception as e:
        return 'Error: {}'.format(str(e))
    
def update_orders():
    print ('Updating')
    table_name = "orders"
    productName = "pixel", 
    customerPhone = "+1555", 
    quantity = 1
    stmt1 = sqlalchemy.text(f'insert into {table_name} (productName, customerPhone, quantity) values ({productName}, {customerPhone}, {quantity})')
    stmt2 = sqlalchemy.text('insert into {} ({}, {}, {}) values ({}, {}, {})'.format(table_name, "productName", "customerPhone", "quantity",  productName, customerPhone, quantity))

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
            print('before update')
            print(stmt1)
            conn.execute(stmt1)
            return "updated"
            
    except Exception as e:
        return 'Error: {}'.format(str(e))

def empty_orders_table():
    table_name = "orders"

    stmt1 = sqlalchemy.text('delete from {}'.format(table_name))
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
            print('before delete')
            print(stmt1)
            results = conn.execute(stmt1)
            for result in results:
                print(result)
            print('after execute')
            return "deleted"
            
    except Exception as e:
        return 'Error: {}'.format(str(e))

    