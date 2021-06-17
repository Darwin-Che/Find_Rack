# Movie_List

## Features
- Simple web UI
- Search for movies by title
- List all users
- Create a new user
- Login to user account

## Setting up with docker
1. `cd` into the `docker` directory.
2. Execute `docker-compose up`
3. The application is now running.

You can now connect to the application here: http://127.0.0.1:5000. If you need to debug the database, connect to it here: `127.0.0.1:13306` (see `create_user.txt` for the credentials).

The application stores it's state/data in two docker volumes:

- `cs348_movielist_database`: The SQL database
- `cs348_movielist_app_context`: Misc files

Note that the application will automatically create the required tables and populate the database with data on first start. If you need to reset the database and bring the application to it's initial state, you must `docker-compose down` and delete the 2 volumes above.

## Setting up manually

### Install prerequisites
1. Install Python 3
2. Install the dependencies with: `pip install -r pyflask/requirement.txt`

### Create User
Execute the content of create_user.txt in mysql root user to have user "348proj" and passwd "dev000000".

### Init db and load sample data
Run in the following in the project directory (the folder where this README is):

```
python pyflask/init.py
```

Will create the database called 'MovieList' and load in some sample data.

### Start the application
Run: `flask run --host=0.0.0.0` inside the `pyflask` directory.

You can now connect to the application here: http://127.0.0.1:5000.

## Testing
- The testing code for task 5 is in the `pyflask/test-sample.py`
- Some sample output of running the above test program can be found here: `test/test-sample.out`

## Loading in real data
Tools for transforming and loading the IMDB database can be found in the `transformation_scripts` folder.

Additionally, if you use docker you can run `USE_REAL_DATA=true docker-compose up` instead of the normal `docker-compose up` command to automatically fetch, transform and load the IMDB dataset. Note that this is a very slow process however (several hours).
