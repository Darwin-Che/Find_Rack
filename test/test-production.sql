
select 'all movies %Back to the Future%' AS '';

SELECT title,releaseyear,runtimemin FROM Movies
WHERE title LIKE "%Back to the Future%"
ORDER BY titleid
;

select '---------------------------------' AS '';
select 'all movies at year 2016' AS '';

SELECT title,releaseyear,runtimemin FROM Movies
WHERE releaseyear="2016"
ORDER BY titleid
LIMIT 10
;

select '---------------------------------' AS '';
select 'all movies by %Jim Carrey%' AS '';

SELECT title,releaseyear,runtimemin FROM Movies
WHERE titleid IN
(SELECT titleid FROM Casts c JOIN Cast_Movie cm ON c.castid=cm.castid
WHERE castname LIKE "%Jim Carrey%" AND (role="actor" OR role="actress"))
ORDER BY titleid
LIMIT 10
;

select '---------------------------------' AS '';
select 'all lists by user5 or user0' AS '';


SELECT * FROM Lists
WHERE userid = "u5" OR userid = "u0"
ORDER BY listid
;
select '---------------------------------' AS '';
select 'add a list (lNEW, u0, u0 new list)' AS '';

INSERT INTO Lists
(listid,userid,listname)
VALUES("lNEW", "u0", "u0's new list")
;
select '---------------------------------' AS '';
select 'all lists by user5 or user0' AS '';


SELECT * FROM Lists
WHERE userid = "u5" OR userid = "u0"
ORDER BY listid
;

select '---------------------------------' AS '';
select 'delete movie tt0000502 from list lNEW' AS '';

DELETE FROM List_Movie
where listid="lNEW" AND titleid="tt0000502"
;

select '---------------------------------' AS '';
select 'add movie tt0000502 from list lNEW' AS '';

INSERT INTO List_Movie
(listid,titleid)
VALUES ("lNEW", "tt0000502")
;

select '---------------------------------' AS '';
select 'all movies in list lNEW' AS '';

SELECT * FROM List_Movie
WHERE listid="lNEW"
;

select '---------------------------------' AS '';
select 'all comments by user5 or user0' AS '';

SELECT comment, publishtime FROM Comments
WHERE userid = "u5" OR userid = "u0"
ORDER BY publishtime DESC
LIMIT 10
;

select '---------------------------------' AS '';
select 'u5 has a new comment on tt0000502' AS '';

INSERT INTO Comments
(commentid, titleid, userid, comment, publishtime)
VALUES ("cNEW", "tt0000502", "u5", "u5 has a new comment on tt0000502", "2021-07-05 11:00:00")
;

select '---------------------------------' AS '';
select 'all comment on movie tt0000502' AS '';

SELECT comment, publishtime FROM Comments
WHERE titleid="tt0000502"
;

select '---------------------------------' AS '';
select 'all comment on movie id < tt0001000' AS '';

SELECT comment, publishtime FROM Comments
WHERE titleid<"tt0001000"
ORDER BY publishtime DESC
LIMIT 10
;

select '---------------------------------' AS '';
select 'all comment by user5 or user0' AS '';

SELECT comment, publishtime FROM Comments
WHERE userid = "u5" OR userid = "u0"
ORDER BY publishtime DESC
LIMIT 10
;

select '---------------------------------' AS '';
select 'all lists user0 subscribed' AS '';

SELECT * FROM Subscription
WHERE subscriber="u0"
LIMIT 10
;

select '---------------------------------' AS '';
select 'all users subscribed to list0' AS '';

SELECT * FROM Subscription
WHERE subscribeto="l0"
LIMIT 10
;

select '---------------------------------' AS '';
select 'all users subscribed to lNEW' AS '';

SELECT * FROM Subscription
WHERE subscribeto="lNEW"
LIMIT 10
;

select '---------------------------------' AS '';
select 'user0 subscribe to lNEW' AS '';

INSERT INTO Subscription
(subscriber, subscribeto)
VALUES ("u0", "lNEW")
;

select '---------------------------------' AS '';
select 'all users subscribed to lNEW' AS '';

SELECT * FROM Subscription
WHERE subscribeto="lNEW"
LIMIT 10
;















