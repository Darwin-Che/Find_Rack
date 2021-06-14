import os
import mysql.connector
from mysql.connector import errorcode
from pathlib import Path
from init import *

query1 = '''
SELECT title,releaseyear,runtimemin FROM Movies
WHERE title LIKE "%Back to the Future%"
'''
cursor.execute(query1)
for r in cursor.fetchall():
    print(r)

