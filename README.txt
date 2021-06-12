# Movie_List


## Prerequisite

- Python3

```
pip install -r pyflask/requirement.txt
```

## Setting up with docker
1. `cd` into the `docker` directory.
2. Execute `docker-compose up`
3. The application is now running.

You can now connect to the application here: http://127.0.0.1:5000. If you need to debug the database, connect to it here: `127.0.0.1:13306`.

The application stores it's state/data in two docker volumes:

- `cs348_movielist_database`: The SQL database
- `cs348_movielist_app_context`: Misc files

Note that the application will automatically create the required tables and populate the database with data on first start. If you need to reset the database and bring the application to it's initial state, you must `docker-compose down` and delete the 2 volumes above.

## Demo Usage


### Create User

execute the content of create_user.txt in mysql root user to have user "348proj" and passwd "dev000000"



### Init db

Run in the pyflask directory
```
python init.py
```
Will create the database called 'TestDB' and a table 'main'



### Put data in db

Run in the pyflask directory
```
flask run
```

Send POST request to the '/data' with format
```
{
    "action": "put",
    "first_name" : "fnxxx",
    "last_name" : "lnxxx"
}
```
Will register the name into the table main


### Query data in db

Run in the pyflask directory
```
flask run
```

Send POST request to the '/data' with format
```
{
    "action": "get"
}
```
Will return a list of entries in JSON form

Send POST request to the '/data' with format
```
{
    "action": "get", 
    "first_name" : "fnxxx"
}
```
Will return a list of entries satisfying "first_name"="fnxxx" in JSON form, "last_name" option is also available, can be combined. 

