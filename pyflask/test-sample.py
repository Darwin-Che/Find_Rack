import os
import mysql.connector
from mysql.connector import errorcode
from pathlib import Path
import init

cursor.execute("SELECT * FROM Movies")
for r in cursor.fetchall():
    print(r)

