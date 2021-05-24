# Movie_List

## Prerequisite

- Python3

```
pip install -r pyflask/requirement.txt
```

## Demo Usage

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

