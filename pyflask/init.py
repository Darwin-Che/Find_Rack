import os
import mysql.connector
from mysql.connector import errorcode
from pathlib import Path

DBName = 'MovieList'

#TABLES = {}
#TABLES['main'] = (
#    'CREATE TABLE main ('
#    'first_name varchar(14), '
#    'last_name varchar(15) '
#    ')'
#)

sql_host = os.getenv('DATABASE_HOST', default='localhost')
sql_port = int(os.getenv('DATABASE_PORT', default='3306'))
cnx = mysql.connector.connect(host=sql_host, port=sql_port, user='348proj', passwd='dev000000')
cnx.autocommit = True # For better performance
cursor = cnx.cursor()

# Init Database
cm = 'CREATE DATABASE IF NOT EXISTS {}'.format(DBName)

try:
    cursor.execute(cm, {'DBName': DBName})
    cnx.database = DBName
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)

print("Success creating database: {}, now inserting data...".format(DBName), flush=True)


# Initialize Table
# For now just execute test script
def loaddata():

    path_table_sql = 'test'   # the path for the .sql files
    path_data = str(Path('test/datapath').absolute())   # replace 'path' in the script with path_data

    cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
    
    for a in cursor.execute(Path(path_table_sql, 'drop_table.sql').read_text().replace("path", path_data), multi=True):
        pass
    for a in cursor.execute(Path(path_table_sql, 'create_table.sql').read_text().replace("path", path_data), multi=True):
        pass
    
    only_imdb = False  # are we only loading the four tables provided by ivan, or we are loading all 9 tables
    if only_imdb:
        for a in cursor.execute(Path(path_table_sql, 'populate_table_imdb.sql').read_text().replace("path", path_data), multi=True):
            pass
    else:
        for a in cursor.execute(Path(path_table_sql, 'populate_table_all.sql').read_text().replace("path", path_data), multi=True):
            pass

    print("Repairing foreign keys...", flush=True)
    for a in cursor.execute(Path(path_table_sql, 'repair_foreign_keys.sql').read_text().replace("path", path_data), multi=True):
        pass
    cursor.execute('SET FOREIGN_KEY_CHECKS=1;')

loaddata()

#for table_name in TABLES:
#    table_description = TABLES[table_name]
#    try:
#        print("Creating table {}: ".format(table_name), end='')
#        cursor.execute(table_description)
#        cnx.commit()
#    except mysql.connector.Error as err:
#        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#            print("already exists.")
#        else:
#            print(err.msg)
#    else:
#        print("OK")
