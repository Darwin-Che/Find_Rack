DELETE FROM Cast_Movie
    WHERE castid NOT IN (SELECT castid FROM Casts);
DELETE FROM Cast_Movie
    WHERE titleid NOT IN (SELECT titleid FROM Movies);

DELETE FROM Genre_Movie
    WHERE titleid NOT IN (SELECT titleid FROM Movies);
