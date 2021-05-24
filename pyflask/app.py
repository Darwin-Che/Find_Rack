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


    ret = ""
    if not action:
        ret = '''<p>Error</p>'''
    if action == 'get':
        ret = dbget(request.json, cursor)
    if action == 'put':
        ret = dbput(request.json, cursor)
    
    cursor.close()
    return ret
    
def dbget(form, cursor):
    ret = ""

    try:
        q = []
        cursor.execute(
            (
                "SELECT * FROM main "
            ),
            form
        )
        for (first_name, last_name) in cursor:
            print("first_name : {}; last_name : {}".format(first_name,last_name))
            q.append({"firstname" : first_name, "lastname" : last_name})

        ret = json.dumps(q, indent=4 * ' ')
    except mysql.connector.Error as err:
        print(err)
    
    return ret

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

    return 'Success Put!'

    

