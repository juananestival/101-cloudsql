from flask import Flask
from flask import Response, request
import requests
import json
import os
import sqlalchemy


def main(initial_request):

    # Assign Variables to Pass
    connection_name = "hospitality-demo-361210:us-central1:dfcxlabs"
    table_name = "customers"
    db_name = "retail"
    db_user = "postgres"
    db_password = "Al0h0m0ra!"
    driver_name = 'postgresql+pg8000'
    query_string = dict(
        {"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

    stmt1 = sqlalchemy.text('select * from {}'.format(table_name))
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
            results = conn.execute(stmt1)
            for result in results:
                print(result)
            print('after execute')
            msg = 'Sample response'
            WebhookResponse=answer_webhook(msg)
            return WebhookResponse
            
    except Exception as e:
        return 'Error: {}'.format(str(e))

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