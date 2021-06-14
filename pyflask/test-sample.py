import os
import uuid
import mysql.connector
from mysql.connector import errorcode
from pathlib import Path
from init import *


def format_input(inp):
    return f'%{inp}%'

def show_result(cursor):
    for r in cursor.fetchall():
        print(r)


print('Searching by title')

input_title = 'Back to the Future'
input_title = format_input(input_title)

query1 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE title LIKE %s
'''
cursor.execute(query1, (input_title,))
for r in cursor.fetchall():
    print(r)

print('Searching by year')

input_year = '2016'

query2 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE releaseyear=%s
'''
cursor.execute(query2, (input_year,))
for r in cursor.fetchall():
    print(r)


print('Searching by actor/actress')

input_actor = 'Fox'
input_actor = format_input(input_actor)

query3 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE titleid IN
(SELECT titleid FROM Casts c JOIN Cast_Movie cm ON c.castid=cm.castid
WHERE castname LIKE %s AND (role="actor" OR role="actress"))
'''
cursor.execute(query3, (input_actor,))
for r in cursor.fetchall():
    print(r)

print('Searching by director')

input_director = 'James Cameron'
input_director = format_input(input_director)

query4 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE titleid IN
(SELECT titleid FROM Casts c JOIN Cast_Movie cm ON c.castid=cm.castid
WHERE castname LIKE %s AND role="director")
'''
cursor.execute(query4, (input_director,))
for r in cursor.fetchall():
    print(r)

print('Searching by genre')

input_genre = 'Drama'
input_genre = format_input(input_genre)

query5 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE titleid IN
(SELECT titleid FROM Genre_Movie
WHERE genre LIKE %s)
'''
cursor.execute(query5, (input_genre,))
for r in cursor.fetchall():
    print(r)


print('Create new list')

print('Original lists')
cursor.execute('SELECT * FROM Lists')
for r in cursor.fetchall():
    print(r)

userid = ''
new_listid = uuid.uuid4().hex
new_listname = "Darwin's favourite"

new_list = (new_listid, userid, new_listname)

query6='''
INSERT INTO Lists
(listid,userid,listname)
VALUES(%s, %s, %s)
'''

cursor.execute(query6, new_list)

print('New lists')
cursor.execute('SELECT * FROM Lists')
show_result(cursor)
