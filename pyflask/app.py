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

app = Flask(__name__)

html_root_path = str(Path('..', 'html').resolve())

jwt_secret = 'opensesame'

app.logger.setLevel(logging.DEBUG)

DBName = 'MovieList'

sql_host = os.getenv('DATABASE_HOST', default='localhost')
sql_port = int(os.getenv('DATABASE_PORT', default='3306'))

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        return obj.replace(tzinfo=datetime.timezone.utc).timestamp()

    raise TypeError ("Type %s not serializable" % type(obj))

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
    cast = request.args.get('cast')
    castid = request.args.get('castid')
    releaseyear = request.args.get('releaseyear')
    minruntime = request.args.get('minruntime')
    maxruntime = request.args.get('maxruntime')
    builder = []
    params = []
    if title is not None:
        builder.append('title LIKE %s')
        params.append(sql_like(title))
    if cast is not None:
        builder.append('titleid IN (SELECT titleid FROM Casts c JOIN Cast_Movie cm ON c.castid = cm.castid WHERE c.castname LIKE %s)')
        params.append(sql_like(cast))
    if castid is not None:
        builder.append('titleid IN (SELECT titleid FROM Cast_Movie WHERE castid = %s)')
        params.append(castid)
    if releaseyear is not None:
        builder.append('releaseyear = %s')
        try:
            params.append(int(releaseyear))
        except:
            raise AppError('Release year must be a number')
    if minruntime is not None:
        builder.append('runtimemin >= %s')
        try:
            params.append(int(minruntime))
        except:
            raise AppError('Minimum runtime must be a number')
    if maxruntime is not None:
        builder.append('runtimemin <= %s')
        try:
            params.append(int(maxruntime))
        except:
            raise AppError('Maximum runtime must be a number')
    with cnx() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Movies"
            if builder:
                query = query + ' WHERE ' + ' AND '.join(builder)
            cursor.execute(query, params)
            return json.dumps(cursor.fetchall())

@app.route('/api/comments')
def query_comments():
    titleid = request.args.get('titleid')
    if titleid is None:
        raise AppError('titleid cannot be None!')
    with cnx() as conn:
        with conn.cursor() as cursor:
            query = "SELECT comment, username, publishtime FROM Comments, Users WHERE titleid = %s AND Comments.userid = Users.userid;"
            cursor.execute(query, [titleid])
            return json.dumps(cursor.fetchall(), default=json_serial)

@app.route('/api/movieid')
def movie_id():
    titleid = request.args.get('titleid')
    if titleid is None: 
        raise AppError('titleid cannot be None!')
    with cnx() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Movies WHERE titleid = %s;"
            cursor.execute(query, [titleid])
            return json.dumps(cursor.fetchall(), default=json_serial)

@app.route('/api/cast')
def get_cast():
    titleid = request.args.get('titleid')
    if titleid is None:
        raise AppError('titleid cannot be None!')
    with cnx() as conn:
        with conn.cursor() as cursor:
            query = "SELECT castname, role FROM Cast_Movie, Casts WHERE Casts.castid = Cast_Movie.castid AND titleid = %s;"
            cursor.execute(query, [titleid])
            return json.dumps(cursor.fetchall(), default=json_serial)

@app.route('/api/comments', methods=['POST'])
def add_comment():
    try:
        userid = jwt.decode(bytes(request.json.get('token'), 'utf-8'), jwt_secret, algorithms="HS256")['userid']
    except:
        userid = None
    titleid = request.json.get('titleid')
    comment = request.json.get('comment')
    if userid is None:
        raise AppError('Need to be logged in!')
    if titleid is None:
        raise AppError('titleid cannot be None!')
    if comment is None or len(comment) <= 0:
        raise AppError('Comment cannot be empty!')
    commentid = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
    publishtime = datetime.datetime.now()
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Comments VALUES (%s, %s, %s, %s, %s)", (commentid, titleid, userid, comment, publishtime))
        conn.commit()
    return json.dumps({'commentid': commentid})

@app.route('/api/users')
def query_users():
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT userid, username FROM Users")
            return json.dumps(cursor.fetchall())

@app.route('/api/username')
def query_username():
    userid = request.args.get('userid')
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT username FROM Users WHERE userid = %s", (userid,))
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
    try:
        searcherid = jwt.decode(bytes(request.args.get('token'), 'utf-8'), jwt_secret, algorithms="HS256")['userid']
    except:
        searcherid = None

    builder = []
    params = [searcherid]
    userid = request.args.get('userid')
    name = request.args.get('name')
    subscribed = request.args.get('subscribed')
    if userid is not None:
        builder.append('E.userid = %s')
        params.append(userid)
    if name is not None:
        builder.append('E.listname LIKE %s')
        params.append(sql_like(name))
    if subscribed:
        builder.append('S.subscribeto IS NOT NULL')
    if builder:
        conditions = 'WHERE ' + ' AND '.join(builder)
    else:
        conditions = ""
    response = {}
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT listname, Movies.titleid, listid, subscribeto, U.userid, U.username FROM (SELECT Lists.listid AS listid, listname, titleid, userid FROM Lists LEFT JOIN List_Movie ON Lists.listid=List_Movie.listid {conditions}) AS E LEFT JOIN Movies on E.titleid=Movies.titleid LEFT JOIN Subscription ON Subscription.subscriber = %s AND Subscription.subscribeto = E.listid JOIN Users AS U ON E.userid = U.userid;", params)
            for row in cursor.fetchall():
                if (row[2] in response):
                    response[row[2]]['titles'].append(row[1])
                else:
                    response[row[2]] = {'name': row[0], 'subscribed': row[3] is not None, 'userid': row[4], 'username': row[5], 'titles': [row[1]] if row[1] else []} 
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
    
@app.route('/api/list-delete', methods=['POST'])
def delete_list():
    listid = request.json.get('listid')
    try:
        userid = jwt.decode(bytes(request.json.get('token'), 'utf-8'), jwt_secret, algorithms="HS256")['userid']
    except:
        userid = None
    if userid is None:
        raise AppError('Need to be logged in!')
    if listid is None or len(listid) <= 0:
        raise AppError('listid cannot be none!')
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Lists WHERE listid = %s AND userid = %s;", (listid, userid))
            if cursor.rowcount <= 0:
                raise AppError('List could not be found!')
        conn.commit()
    return json.dumps({})

@app.route('/api/subscriptions', methods=['POST'])
def add_subscription():
    try:
        userid = jwt.decode(bytes(request.json.get('token'), 'utf-8'), jwt_secret, algorithms="HS256")['userid']
    except:
        userid = None
    listid = request.json.get('listid')
    subscribe = request.json.get('subscribe')
    if listid is None or len(listid) <= 0:
        raise AppError('listid cannot be none!')
    if subscribe is None:
        raise AppError('subscribe cannot be none!')
    if userid is None:
        raise AppError('You must be logged in!')
    with cnx() as conn:
        with conn.cursor() as cursor:
            if subscribe:
                cursor.execute("INSERT INTO Subscription VALUES (%s, %s)", (userid, listid))
            else:
                cursor.execute("DELETE FROM Subscription WHERE subscriber = %s AND subscribeto = %s", (userid, listid))
        conn.commit()
    return json.dumps({})

@app.route('/api/genres', methods=['GET'])
def get_genres():
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT genre from Genre_Movie;")
            return json.dumps([x[0] for x in cursor.fetchall()])

@app.route('/api/suggest', methods=['POST'])
def suggest_movie():
    genre = request.json.get('genre')
    with cnx() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT M.* FROM Movies as M, Genre_Movie as G WHERE M.titleid = G.titleid AND genre = %s ORDER BY RAND() LIMIT 1;", [genre])
            return json.dumps(cursor.fetchone())
