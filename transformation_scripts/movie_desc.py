import sys
import os
import pandas as pd
import mysql.connector

print('Reading dataset...', flush=True)
title_basics = pd.read_csv(sys.argv[1], sep='\t', header=None)

print('Filtering out invalid rows...', flush=True)
title_basics = title_basics[pd.notnull(title_basics[1])]

print('Connecting to DB...', flush=True)
DBName = 'MovieList'
sql_host = os.getenv('DATABASE_HOST', default='localhost')
sql_port = int(os.getenv('DATABASE_PORT', default='3306'))
cnx = mysql.connector.connect(host=sql_host, port=sql_port, user='348proj', passwd='dev000000', database=DBName)
cnx.autocommit = False
cursor = cnx.cursor()

print('Connected to DB, executing queries...', flush=True)

i = 1
for x in title_basics.itertuples():
    if i % 1000 == 0:
        print('Executed {} queries so far...'.format(i), flush=True)
    if i % 10000 == 0:
        cnx.commit()
        print('Commited {} entries so far...'.format(i), flush=True)
    cursor.execute('UPDATE Movies SET summary = %s WHERE titleid = %s;', (x[2], x[1]))
    i = i + 1
cnx.commit()

print('OK!', flush=True)
