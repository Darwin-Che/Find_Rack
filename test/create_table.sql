CREATE TABLE Movies (
    titleid     VARCHAR(11)  NOT NULL PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    releaseyear    YEAR
);

CREATE TABLE Users (
    userid     VARCHAR(11)  NOT NULL PRIMARY KEY,
    username   VARCHAR(20)  NOT NULL UNIQUE,
    password   BINARY(64)   NOT NULL /* 32 bytes SHA256, 32 bytes salt*/
);

CREATE TABLE Casts (
    castid      VARCHAR(11) NOT NULL PRIMARY KEY,
    castname    VARCHAR(50) NOT NULL
);

CREATE TABLE Cast_Movie (
    castid      VARCHAR(11)  NOT NULL,
    titleid     VARCHAR(11)  NOT NULL,
    role        VARCHAR(20)  NOT NULL,
    PRIMARY KEY (castid, titleid, role),
    FOREIGN KEY (castid) REFERENCES Casts(castid),
    FOREIGN KEY (titleid) REFERENCES Movies(titleid)
);

CREATE TABLE Lists (
    listid      VARCHAR(11) NOT NULL PRIMARY KEY,
    userid      VARCHAR(11) NOT NULL,
    listname    VARCHAR(20) NOT NULL,
    FOREIGN KEY (userid) REFERENCES Users(userid)
);

CREATE TABLE Comments (
    commentid   VARCHAR(11) NOT NULL PRIMARY KEY,
    titleid     VARCHAR(11) NOT NULL,
    userid      VARCHAR(11) NOT NULL,
    comment     LONGTEXT    NOT NULL,
    publishtime DATETIME    NOT NULL,
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
    genre        VARCHAR(20) NOT NULL,
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


