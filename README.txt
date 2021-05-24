# Movie_List


## Prerequisite

- Python3

```
pip install -r pyflask/requirement.txt
```


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

