import os
import mysql.connector
from mysql.connector import errorcode
from pathlib import Path
from init import *

input_title = 'Back to the Future'

query1 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE title LIKE "%%s%"
'''
cursor.execute(query1 % input_title)
for r in cursor.fetchall():
    print(r)

