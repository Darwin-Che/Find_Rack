# basic test strategy

Load in sample data

## Check the database is correctly loaded by doing global queries

Query all movie sorted by increasing movie_id
Query all users sorted by increasing user_id
Query all lists sorted by increasing list_id
Query all comments sorted by increasing timestamp 

## Check the ability to correctly retrieve data (evolve as the application grows)

Query all lists titles containing "l0"
Query all users subscribed to list_id "l01"
Query all comments of the movie "m04"

## Check the movie searching features

Query all movie_id with genre "genre1"
Query all movie_id with title containing " of "
Query all movie_id with actor 
Query all movie_id with director 
Query all movie_id with release date in 2005

## Check new movies can be inserted

Insert new movie
(m05, M movie 05, 2021-06-09, Mars, Alien Language)

## Check list can be created 

Create a new list 
(l21, 5, Zhaocheng's l21)

Add movie m01, m02 to it

## Check new subscription can be made

## Check new actors can be added
