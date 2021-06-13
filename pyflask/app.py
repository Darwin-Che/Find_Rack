import os
import sys
import datetime
import click
import uuid
import simplejson as json
import mysql.connector
import logging
import random
import string
from mysql.connector import errorcode
from pathlib import Path

from flask import Flask, request, send_from_directory

html_root_path = str(Path('..', 'html').resolve())

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


@app.route('/')
def serve_index():
    return send_from_directory(html_root_path, 'index.html')

@app.route('/<path:path>')
def serve_ui(path):
    return send_from_directory(html_root_path, path)

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

@app.route('/api/users', methods=['POST'])
def create_user():
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
    username = request.json.get('username')
    if username is None:
        raise RuntimeError('Title cannot be None!')
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Users VALUES (%s, %s)", (id, username))
        conn.commit()

    return json.dumps({"userid":id})
