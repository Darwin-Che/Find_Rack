# For loading the txt data into mysql database

## Mysql configuration

add the following lines to `~/.my.cnf`
```
[mysqld]
secure-file-priv=""
```

## Python code

I have updated the code block in flask/init.py

So that we can execute 'python flask/init.py' in the root directory to restore the original data to the desired database

```
def loaddata():

    path_table_sql = 'test'   # the path for the .sql files
    path_data = str(Path('test/datapath').absolute())   # replace 'path' in the script with path_data

    
    for a in cursor.execute(Path(path_table_sql, 'drop_table.sql').read_text().replace("path", path_data), multi=True):
        pass
    for a in cursor.execute(Path(path_table_sql, 'create_table.sql').read_text().replace("path", path_data), multi=True):
        pass
    
    only_imdb = True  # are we only loading the four tables provided by ivan, or we are loading all 9 tables
    if only_imdb:
        for a in cursor.execute(Path(path_table_sql, 'populate_table_imdb.sql').read_text().replace("path", path_data), multi=True):
            pass
    else:
        for a in cursor.execute(Path(path_table_sql, 'populate_table_all.sql').read_text().replace("path", path_data), multi=True):
            pass
            
    cnx.commit()
```

