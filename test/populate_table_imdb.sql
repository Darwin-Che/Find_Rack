LOAD DATA INFILE "path/movies.scsv"
INTO TABLE Movies
CHARACTER SET utf8mb4
COLUMNS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA INFILE "path/casts.scsv"
INTO TABLE Casts
CHARACTER SET utf8mb4
COLUMNS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- LOAD DATA INFILE "path/users.scsv"
-- INTO TABLE Users
-- CHARACTER SET utf8mb4
-- COLUMNS TERMINATED BY ';'
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES;

-- LOAD DATA INFILE "path/lists.scsv"
-- INTO TABLE Lists
-- CHARACTER SET utf8mb4
-- COLUMNS TERMINATED BY ';'
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES;

-- LOAD DATA INFILE "path/comments.scsv"
-- INTO TABLE Comments
-- CHARACTER SET utf8mb4
-- COLUMNS TERMINATED BY ';'
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES;

LOAD DATA INFILE "path/cast_movie.scsv"
INTO TABLE Cast_Movie
CHARACTER SET utf8mb4
COLUMNS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- LOAD DATA INFILE "path/list_movie.scsv"
-- INTO TABLE List_Movie
-- CHARACTER SET utf8mb4
-- COLUMNS TERMINATED BY ';'
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES;

LOAD DATA INFILE "path/genre_movie.scsv"
INTO TABLE Genre_Movie
CHARACTER SET utf8mb4
COLUMNS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- LOAD DATA INFILE "path/subscription.scsv"
-- INTO TABLE Subscription
-- CHARACTER SET utf8mb4
-- COLUMNS TERMINATED BY ';'
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 LINES;
