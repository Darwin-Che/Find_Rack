import os
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.constants import ClientFlag
from pathlib import Path

DBName = 'TestDB'

sql_host = os.getenv('DATABASE_HOST', default='localhost')
sql_port = int(os.getenv('DATABASE_PORT', default='3306'))
cnx = mysql.connector.connect(host=sql_host, port=sql_port, user='348proj', passwd='dev000000')
cursor = cnx.cursor()

# Init Database
cm = 'CREATE DATABASE IF NOT EXISTS {}'.format(DBName)

try:
    cursor.execute(cm, {'DBName': DBName})
    cnx.commit()
    cnx.database = DBName
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)

print("Success creating database: {}".format(DBName))


# test functions
def querySQL(table, outcol, orderby, cond = {}):
    condclause = " WHERE 1=1 "
    for (k,v) in cond:
        condclause += ( " AND " + k + " LIKE " + v )
    print("SELECT %s FROM %s " , outcol, table  )
    return cursor.execute( "SELECT %s FROM %s " , outcol, table)

def insertSQL(table, values):
    valstr = ",".join([str(s) for s in values])
    cursor.execute( "INSERT INTO %s VALUES ( %s )", table, valstr)
    cnx.commit()

def loadSample():
    p = {"path" : str(Path('.').absolute())}
    print(Path('..', 'populate_table.sql').read_text().replace("path", p["path"]))
    for a in cursor.execute(Path('..', 'drop_table.sql').read_text().replace("path", p["path"]), multi=True):
        pass
    for a in cursor.execute(Path('..', 'create_table.sql').read_text().replace("path", p["path"]), multi=True):
        pass
    for a in cursor.execute(Path('..', 'populate_table.sql').read_text().replace("path", p["path"]), multi=True):
        pass
    cnx.commit()

# -------------
# Check data is correctly loaded
# -------------

loadSample()
cnx.commit()

cursor.execute("show tables")
# cnx.close()
# for s in cursor.execute("show tables").fetchall():
#     print(s)
# for moviename in querySQL("Movies", "*", "titleid"):
#     print(moviename)
