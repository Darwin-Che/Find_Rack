
CREATE TABLE Users (
    userid     VARCHAR(32)  NOT NULL PRIMARY KEY,
    username   VARCHAR(20)  NOT NULL UNIQUE,
    password   BINARY(64)   NOT NULL /* 32 bytes SHA256, 32 bytes salt*/
);


CREATE TABLE Lists (
    listid      VARCHAR(32) NOT NULL PRIMARY KEY,
    userid      VARCHAR(32) NOT NULL,
    listname    VARCHAR(20) NOT NULL,
    FOREIGN KEY (userid) REFERENCES Users(userid) ON DELETE CASCADE,
    UNIQUE (userid, listname)
);

CREATE TABLE Comments (
    commentid   VARCHAR(32) NOT NULL PRIMARY KEY,
    titleid     VARCHAR(11) NOT NULL,
    userid      VARCHAR(32) NOT NULL,
    comment     LONGTEXT    NOT NULL,
    publishtime DATETIME    NOT NULL,
    FOREIGN KEY (userid) REFERENCES Users(userid) ON DELETE CASCADE,
    FOREIGN KEY (titleid) REFERENCES Movies(titleid) ON DELETE CASCADE
);

CREATE TABLE List_Movie (
    listid      VARCHAR(32) NOT NULL,
    titleid     VARCHAR(11) NOT NULL,
    PRIMARY KEY (listid, titleid),
    FOREIGN KEY (titleid) REFERENCES Movies(titleid) ON DELETE CASCADE,
    FOREIGN KEY (listid) REFERENCES Lists(listid) ON DELETE CASCADE
);


CREATE TABLE Subscription (
    subscriber  VARCHAR(32) NOT NULL, -- this is userid
    subscribeto VARCHAR(32) NOT NULL, -- this is listid
    PRIMARY KEY (subscriber, subscribeto),
    FOREIGN KEY (subscriber) REFERENCES Users(userid) ON DELETE CASCADE,
    FOREIGN KEY (subscribeto) REFERENCES Lists(listid) ON DELETE CASCADE
);



