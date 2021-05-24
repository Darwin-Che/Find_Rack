import mysql.connector
from mysql.connector import errorcode

DBName = 'TestDB'

TABLES = {}
TABLES['main'] = (
    'CREATE TABLE main ('
    'first_name varchar(14), '
    'last_name varchar(15) '
    ')'
)

cnx = mysql.connector.connect(user='348proj', passwd='dev000000')
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


# Initialize Table

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")