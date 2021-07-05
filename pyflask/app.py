import os
import re
import sys
import datetime
import click
import uuid
import simplejson as json
import mysql.connector
import logging
import random
import string
import hashlib
import jwt
from mysql.connector import errorcode
from pathlib import Path

from flask import Flask, request, send_from_directory, make_response

html_root_path = str(Path('..', 'html').resolve())

jwt_secret = 'opensesame'

app = Flask(__name__) 
app.logger.setLevel(logging.DEBUG)

DBName = 'MovieList'

sql_host = os.getenv('DATABASE_HOST', default='localhost')
sql_port = int(os.getenv('DATABASE_PORT', default='3306'))

def sql_like(like):
    return '%' + like.replace('%', '\\%').replace('_', '\\_') + '%'

def patch_function(old_function, function):
    return lambda *a, **kw: function(old_function, *a, **kw)

def cnx():
    new_cnx = mysql.connector.connect(pool_name="pool",
            pool_size=10,
            host=sql_host,
            port=sql_port,
            user='348proj',
            passwd='dev000000',
            database=DBName)
    new_cnx.cursor = patch_function(new_cnx.cursor, extended_cursor)
    return new_cnx


# Extends: https://github.com/mysql/mysql-connector-python/blob/85e7e9a1934ecbdd426bd478fb657922464a7644/lib/mysql/connector/cursor.py#L170
def verbose_execute(self, operation, params=(), multi=False):
    app.logger.debug('Executing query: %s, params: %s', operation, params)
    self(operation, params, multi)

# Extends: https://github.com/mysql/mysql-connector-python/blob/85e7e9a1934ecbdd426bd478fb657922464a7644/lib/mysql/connector/connection.py#L992
def extended_cursor(self, buffered=None, raw=None, prepared=None, cursor_class=None,
                    dictionary=None, named_tuple=None):
    new_cursor = self()
    new_cursor.execute = patch_function(new_cursor.execute, verbose_execute)
    return new_cursor


def hash_password(password, salt=os.urandom(32)):
    hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hash

def verify_password(unihash, password):
    salt = unihash[:32]
    new_unihash = hash_password(password, salt)
    return unihash == new_unihash

class AppError(Exception):
    pass

@app.route('/')
def serve_index():
    return send_from_directory(html_root_path, 'index.html')

@app.route('/<path:path>')
def serve_ui(path):
    return send_from_directory(html_root_path, path)


@app.errorhandler(AppError)
def handle_app_error(e):
    resp = make_response(json.dumps({"error":str(e)}), 500)
    resp.headers['Error-Type'] = 'handled'
    return resp

@app.errorhandler(mysql.connector.DatabaseError)
def handle_app_error(e):
    resp = make_response(json.dumps({"error":"Database error: " + str(e)}), 500)
    resp.headers['Error-Type'] = 'handled'
    return resp


# /api/movies: List all movies
# /api/movies?title=whatever: Search for all movies with 'whatever' in the title
@app.route('/api/movies')
def query_movies():
    title = request.args.get('title')
    builder = []
    params = []
    if title is not None:
        builder.append('title LIKE %s')
        params.append(sql_like(title))
    with cnx() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Movies"
            if builder:
                query = query + ' WHERE ' + 'AND'.join(builder)
            cursor.execute(query, params)
            return json.dumps(cursor.fetchall())

@app.route('/api/users')
def query_users():
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT userid, username FROM Users")
            return json.dumps(cursor.fetchall())

@app.route('/api/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None:
        raise AppError('Username cannot be None!')
    if password is None:
        raise AppError('Password cannot be None!')
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
    hash = hash_password(password)
    with cnx() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Users VALUES (%s, %s, %s)", (id, username, hash))
            conn.commit()
        except mysql.connector.IntegrityError as err:
            raise AppError('A user with this username already exists!')
    return json.dumps({"userid":id})

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None:
        raise AppError('Username cannot be None!')
    if password is None:
        raise AppError('Password cannot be None!')
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT userid, password FROM Users WHERE username = %s", (username,))
            row = cursor.fetchone()
    if row is None:
        raise AppError('User could not be found!')
    if verify_password(row[1], password):
        return json.dumps({"token":jwt.encode({"userid": row[0]}, jwt_secret, algorithm="HS256")})
    else:
        raise AppError('Bad password!')

@app.route('/api/lists', methods=['GET'])
def get_lists():
    userid = request.args.get('userid')
    if not userid:
        raise AppError('No user id supplied!')
    response = {}
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT listname, title, listid FROM (SELECT Lists.listid, listname, titleid FROM Lists LEFT JOIN List_Movie ON Lists.listid=List_Movie.listid WHERE Lists.userid=%s) AS E LEFT JOIN Movies on E.titleid=Movies.titleid;", (userid,))
            for row in cursor.fetchall():
                if (row[2] in response):
                    response[row[2]]['titles'].append(row[1])
                else:
                    response[row[2]] = {'name': row[0], 'titles': [row[1]] if row[1] else []} 
            return json.dumps(response)
            
@app.route('/api/lists', methods=['POST'])
def create_list():
    try:
        userid = jwt.decode(bytes(request.json.get('token'), 'utf-8'), jwt_secret, algorithms="HS256")['userid']
    except:
        userid = None
    listname = request.json.get('listname')
    if userid is None:
        raise AppError('Need to be logged in!')
    if listname is None or len(listname) <= 0:
        raise AppError('List name cannot be None!')
    listid = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
    with cnx() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Lists VALUES (%s, %s, %s)", (listid, userid, listname))
            conn.commit()
        except mysql.connector.IntegrityError as err:
            raise AppError('A list with this name already exists!')
    return json.dumps({'listid': listid})

@app.route('/api/list-add', methods=['POST'])
def add_to_list():
    listid = request.json.get('listid')
    titleid = request.json.get('titleid')
    if listid is None or len(listid) <= 0:
        raise AppError('listid cannot be none!')
    if titleid is None or len(titleid) <= 0:
        raise AppError('titleid cannot be none!')
    with cnx() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO List_Movie VALUES (%s, %s)", (listid, titleid))
            conn.commit()
        except mysql.connector.IntegrityError as err:
            raise AppError('A list with this name already exists!')
    return json.dumps({'listid': listid})
    
