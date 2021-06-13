# For loading the txt data into mysql database

## Mysql configuration

add the following lines to `~/.my.cnf`
```
[mysqld]
secure-file-priv=""
```

## Python code

```
# get the absolute path of the data txt/csv files
p = str(Path('.').absolute())
# replace 'path' in the script with p
for a in cursor.execute(Path('..', 'drop_table.sql').read_text().replace("path", p), multi=True):
    pass
for a in cursor.execute(Path('..', 'create_table.sql').read_text().replace("path", p), multi=True):
    pass
for a in cursor.execute(Path('..', 'populate_table.sql').read_text().replace("path", p), multi=True):
    pass
cnx.commit()
```

