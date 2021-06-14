import os
import mysql.connector
from mysql.connector import errorcode
from pathlib import Path
from init import *


def format_input(in):
    return f'%{in}%'


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

print('Searching by actor')

input_actor = ''
input_title = format_input(input_actor)

query2 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE titleid IN
(SELECT titleid FROM Casts c JOIN Cast_Movie cm ON c.castid=cm.castid
WHERE castname LIKE %s AND (role="actor" OR role="actress"))
'''
cursor.execute(query2, (input_actor,))
for r in cursor.fetchall():
    print(r)

