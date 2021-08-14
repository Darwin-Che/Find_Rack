# For loading the txt data into mysql database

## Mysql configuration

add the following lines to `~/.my.cnf`
```
[mysqld]
secure-file-priv=""
```

Or if it doesn't work by still showing permission error, try these 
```
/etc/my.cnf
/etc/mysql/my.cnf
$MYSQL_HOME/my.cnf
[datadir]/my.cnf
~/.my.cnf
```

## Python code

We can execute 'python flask/init.py' in the root directory to repopulate the database with desired data

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

As shown in the code segments, we have two options: 

1. load fake sample dataset for all 9 tables. 

	- don't change path_data, since `test/datapath` is where the fake sample data locates. 
	- change only_imdb to False. 


1. load real imdb data for the four tables: to do 
	1) modify "path\_data" where 'test/datapath' points to the real imdb datasets with file names "movies.scsv", "cast\_movie.scsv", "movie\_genre.scsv", and "casts.scsv"; 
	2) modify "only_imdb" to True
	3) notice that there are no available imdb data for others, so we generate fake user/comments/list data. This can be done by first knowing the path to "movies.scsv" and then go to subdirectory `cd test/large_test` and call `python large-data-create.py` and follow the interactive procedure to specify the size of fake data. This generated fake data depends on the movies given in the "movies.scsv".






