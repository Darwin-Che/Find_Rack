CREATE TABLE Movies (
    titleid     VARCHAR(11)  NOT NULL PRIMARY KEY,
    title       VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    releasedate    DATE,
    region      VARCHAR(30),
    lang        VARCHAR(30)
);

CREATE TABLE Users (
    userid     VARCHAR(11)  NOT NULL PRIMARY KEY,
    username   VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL 
);

-- CREATE TABLE Casts (
--     castid      VARCHAR(11) NOT NULL PRIMARY KEY,
--     titleid     VARCHAR(11) NOT NULL 
--     castname    VARCHAR(50) NOT NULL,
--     FOREIGN KEY (titleid) REFERENCES Movies(titleid)
-- );

CREATE TABLE Lists (
    listid      VARCHAR(11) NOT NULL PRIMARY KEY,
    userid      VARCHAR(11) NOT NULL,
    listname    VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    FOREIGN KEY (userid) REFERENCES Users(userid)
);

CREATE TABLE Comments (
    titleid     VARCHAR(11) NOT NULL,
    userid      VARCHAR(11) NOT NULL,
    comment     LONGTEXT    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    publishtime DATETIME    NOT NULL,
    PRIMARY KEY (titleid, userid, publishtime),
    FOREIGN KEY (userid) REFERENCES Users(userid),
    FOREIGN KEY (titleid) REFERENCES Movies(titleid)
);

CREATE TABLE List_Movie (
    listid      VARCHAR(11) NOT NULL,
    titleid     VARCHAR(11) NOT NULL,
    PRIMARY KEY (listid, titleid),
    FOREIGN KEY (titleid) REFERENCES Movies(titleid),
    FOREIGN KEY (listid) REFERENCES Lists(listid)
);

CREATE TABLE Genre_Movie (
    titleid      VARCHAR(11) NOT NULL,
    genre        CHAR(20) NOT NULL,
    PRIMARY KEY (titleid, genre),
    FOREIGN KEY (titleid) REFERENCES Movies(titleid)
);

CREATE TABLE Subscription (
    subscriber  VARCHAR(11) NOT NULL, -- this is userid
    subscribeto VARCHAR(11) NOT NULL, -- this is listid
    PRIMARY KEY (subscriber, subscribeto),
    FOREIGN KEY (subscriber) REFERENCES Users(userid),
    FOREIGN KEY (subscribeto) REFERENCES Lists(listid)
);


