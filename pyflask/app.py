import os
import sys
import datetime
import click
import uuid
import simplejson as json
import mysql.connector
from mysql.connector import errorcode

from flask import Flask, request

app = Flask(__name__) 

DBName = 'TestDB'

cnx = mysql.connector.connect(user='348proj', passwd='dev000000', database=DBName)


@app.route('/data', methods=['POST'])
def data():
    cursor = cnx.cursor()
    
    print(json.dumps(request.json, sort_keys=True, indent=4 * ' '))
    action = request.json.get('action')

    if not action:
        return '''<p>Error</p>'''
    # if action == 'get':
    #     return dbget(request.json)
    if action == 'put':
        return dbput(request.json, cursor)

def dbput(form, cursor):
    try:
        cursor.execute(
            (
                "INSERT INTO main "
                "(first_name, last_name) "
                "VALUES (%(first_name)s, %(last_name)s) "
            ),
            form
        )
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
    return 'Success!'

    
