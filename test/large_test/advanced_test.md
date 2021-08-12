# create fake user data

Step 1 : 

In this directory, execute

```
python large-data-create.py
```

And follow the guide to generate data saved in files in this directory. 

Step 2 :

If you want to get the files into a remote mysql server, make sure that 

1. connect with this option `'--local-infile=1'`
2. run this in mysql `SET GLOBAL local_infile=1;`

And then do 

```
source drop_large_test.sql
source create_large_test.sql
source populate_large_test.sql
```



