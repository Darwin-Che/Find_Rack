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

    print(json.dumps(request.json, sort_keys=True, indent=4 * ' '))
    action = request.json.get('action')


    ret = ""
    if not action:
        ret = '''<p>Error</p>'''
    if action == 'get':
        ret = dbget(request.json)
    if action == 'put':
        ret = dbput(request.json)
    
    return ret
    

def dbget(form):
    ret = ""
    cursor = cnx.cursor()

    try:
        q = []
        cond = ""
        if form.get('first_name'):
            cond += 'AND first_name=%(first_name)s'
        if form.get('last_name'):
            cond += 'AND last_name=%(last_name)s'
        
        cursor.execute(
            (
                "SELECT * FROM main WHERE true " + cond
            ),
            form
        )
        for (first_name, last_name) in cursor:
            print("first_name : {}; last_name : {}".format(first_name,last_name))
            q.append({"first_name" : first_name, "last_name" : last_name})

        ret = json.dumps(q, indent=4 * ' ')
    except mysql.connector.Error as err:
        print(err)
    
    cursor.close()
    return ret

def dbput(form):
    cursor = cnx.cursor()

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

    cursor.close()
    return 'Success Put!'

    

