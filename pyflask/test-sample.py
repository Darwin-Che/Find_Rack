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


