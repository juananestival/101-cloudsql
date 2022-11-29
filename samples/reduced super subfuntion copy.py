from flask import Flask
from flask import Response, request
import requests
import json
import os
import sqlalchemy


def main(initial_request):
    request_json = initial_request.get_json()
    tag = request_json['fulfillmentInfo']['tag']
    
    # Evaluate webhook tag
    if tag == 'get-pin':
        print("Tag flow for: {tag}")
        msg = db_getpin(initial_request)
    elif tag == 'update-order':
        msg = "update-order"
        update_orders()
    elif tag == 'empty-orders-table':
        empty_orders_table()
        msg = "empty-table"
    else:
        msg = "Unknown tag"
    
    WebhookResponse=answer_webhook(msg)
    return WebhookResponse

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

def db_getpin(req):
    connection_name = "hospitality-demo-361210:us-central1:dfcxlabs"
    table_name = "customers"
    db_name = "retail"
    db_user = "postgres"
    db_password = "Al0h0m0ra!"
    driver_name = 'postgresql+pg8000'
    query_string = dict(
        {"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

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
            #results = conn.execute(stmt1)
            result = conn.execute(stmt1).fetchone()
            #results = conn.execute(stmt1).fetchall()
            data = result[0]
            print(f'after execute data returnned {data}')
            return f'after execute data returnned {data}'
            
    except Exception as e:
        return 'Error: {}'.format(str(e))
    
def update_orders():
    print ('Updating')
    connection_name = "hospitality-demo-361210:us-central1:dfcxlabs"
    table_name = "orders"
    db_name = "retail"
    db_user = "postgres"
    db_password = "Al0h0m0ra!"
    driver_name = "postgresql+pg8000"
    productName = "pixel", 
    customerPhone = "+1555", 
    quantity = 1
    query_string = dict(
        {"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

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
    connection_name = "hospitality-demo-361210:us-central1:dfcxlabs"
    table_name = "orders"
    db_name = "retail"
    db_user = "postgres"
    db_password = "Al0h0m0ra!"
    driver_name = 'postgresql+pg8000'
    query_string = dict(
        {"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

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

    