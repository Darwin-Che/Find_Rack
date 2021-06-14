import os
import uuid
import datetime
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
show_result(cursor)

print('Searching by year')

input_year = '2016'

query2 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE releaseyear=%s
'''
cursor.execute(query2, (input_year,))
show_result(cursor)


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
show_result(cursor)

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
show_result(cursor)


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
show_result(cursor)



print('Create new list')

print('Original lists')
cursor.execute('SELECT * FROM Lists')
show_result(cursor)

userid = 'e74e269da2494fe594f55bad7c21b651'
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

print('Add a new movie to a list')

listid = new_listid
titleid = 'mn07'
new_entry = (listid, titleid)

print('Original list')
cursor.execute('SELECT * FROM List_Movie WHERE listid=%s', (listid,))
show_result(cursor)

query7='''
INSERT INTO List_Movie
(listid,titleid)
VALUES(%s, %s)
'''

cursor.execute(query7, new_entry)

print('Updated list')
cursor.execute('SELECT * FROM List_Movie WHERE listid=%s', (listid,))
show_result(cursor)

print('New Subscription')

subscriber = '607cc790aa6046bcb6bd1ef91ba21b9d' 
subscribeto = 'f5766a1b2bbf47548e6df15c165b2589' 
new_subscription = (subscriber, subscribeto)

print('Original Subscriptions')
cursor.execute('SELECT * FROM Subscription')
show_result(cursor)

query8='''
INSERT INTO Subscription
(subscriber,subscribeto)
VALUES(%s, %s)
'''

cursor.execute(query8, new_subscription)

print('Updated Subscriptions')
cursor.execute('SELECT * FROM Subscription')
show_result(cursor)


print('Create new comment')

print('Original comments')
cursor.execute('SELECT * FROM Comments')
show_result(cursor)

commentid = uuid.uuid4().hex
titleid = 'mn08'
userid = 'e74e269da2494fe594f55bad7c21b651'
comment = "J'aime Elle !"
publishtime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

new_comment = (commentid, titleid, userid, comment, publishtime)

query9='''
INSERT INTO Comments
(commentid,titleid,userid,comment,publishtime)
VALUES(%s, %s, %s, %s, %s)
'''

cursor.execute(query9, new_comment)

print('Updated comments')
cursor.execute('SELECT * FROM Comments')
show_result(cursor)
