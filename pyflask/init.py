import os
import sys
import datetime
import click
import uuid
import simplejson as json
import mysql.connector
from mysql.connector import errorcode

from flask import Flask, request



cnx = mysql.connector.connect(user='348proj', passwd='dev000000')

DBName = 'TestDB'

TABLES = {}
TABLES['main'] = (
    'CREATE TABLE main ('
    'first_name varchar(14), '
    'last_name varchar(15) '
    ')'
)
 
"""Initialize the database."""
cursor = cnx.cursor()
if i:  
    cm = 'USE %(DBName)s; SOURCE test.sql'
else:
    cm = 'CREATE DATABASE {}'.format(DBName)
try:
    cursor.execute(cm, {'DBName': DBName})
    cnx.commit()
    click.echo('Initialized database.') 
    cnx.database = DBName
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)

if i:
    return

"""Initialize Table"""
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")