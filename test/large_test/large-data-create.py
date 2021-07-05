import random
import os
import datetime
import mysql.connector
from pathlib import Path

#### 
print('load in the entries of Movies.scsv')
print('enter path to movies.scsv (e.g. input ../../realdata/movies.scsv)')
movies_path = input()
f = open(movies_path)
movies = f.readlines()
f.close()

def randmovieid():
	return movies[random.randint(1,len(movies)-1)].split(';')[0]

#### create user data

print('How many users you want? (user id starting from 0) ')
user_n = int(input())

print('creating users.scsv {}'.format(user_n))

f = open("users.scsv", "w")
f.write('userid;username;password\n');

for i in range(user_n):
	f.write('u{};user{};passwordfor{}\n'.format(i, i, i))

f.close()

#### create list data

print('How many lists you want? (list id starting from 0)')
list_n = int(input())

print('creating lists.scsv {}'.format(list_n))

f = open("lists.scsv", "w")
f.write('listid;userid;listname\n')

for i in range(list_n):
	f.write('l{};u{};list{}\n'.format(i, random.randint(0, user_n-1), i))

f.close()

#### create comments data

def randomtimes(start = "1900-01-01 00:00:00", end = "2020-01-01 00:00:00"):
    frmt = '%Y-%m-%d %H:%M:%S'
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    td = etime - stime
    return random.random() * td + stime

print('How many comments you want? (comment id starting from 0)')
com_n = int(input())

print('creating comments.scsv {}'.format(com_n))

f = open("comments.scsv", "w")
f.write('commentid;movieid;userid;text;publishtime\n')

for i in range(com_n):
	f.write('c{0};{1};u{2};"comment from user {2} to movie {1}";{3}\n'.format(i, randmovieid(), random.randint(0, user_n-1), randomtimes().strftime('%Y-%m-%d %H:%M:%S')))

f.close()

#### populate lists

print('populating lists')
print('max number of movies in a list? ')
max_movies = int(input())

f = open("list_movie.scsv", "w")
f.write('listid;titleid\n')

for i in range(list_n):
	l = random.randint(0,max_movies)
	sample = random.sample(movies, l)
	for j in range(l):
		f.write('l{};{}\n'.format(i, sample[j].split(';')[0]))

f.close()

#### subscription populate

print('subscription: per list or per user? 0 for list / 1 for user')
choice = int(input())

f = open("subscription.scsv", "w")
f.write('userid;listid\n')

if choice == 0:
	print('max users per list?')
	maxusers = int(input())
	for i in range(list_n):
		l = random.randint(0,maxusers)
		sample = random.sample(range(user_n), l)
		for j in range(l):
			f.write('u{};l{}\n'.format(sample[j], i))
else:
	print('max lists per user?')
	maxlists = int(input())
	for i in range(user_n):
		l = random.randint(0,maxlists)
		sample = random.sample(range(list_n), l)
		for j in range(l):
			f.write('u{};l{}\n'.format(i, sample[j]))

f.close()

#### do you want to write these data to the database?

print('do you want to write these data to the database? 0 for NO, 1 for Yes')
writedatabase = int(input())

if writedatabase != 0:
	sql_host = os.getenv('DATABASE_HOST', default='localhost')
	print('mysql host : ' + str(sql_host)) 
	sql_port = int(os.getenv('DATABASE_PORT', default='3306'))
	print('mysql port : ' + str(sql_port))
	DBName = 'MovieList'
	print('DBName : ' + str(DBName))
	
	cnx = mysql.connector.connect(host=sql_host, 
		port=sql_port, 
		user='348proj', 
		passwd='dev000000',
		database=DBName)

	sql_path = str(Path().absolute())
	data_path = sql_path
	cursor = cnx.cursor()
	print(sql_path)
	for a in cursor.execute(Path(sql_path, 'drop_large_test.sql').read_text().replace('path', data_path), multi=True):
		pass
	for a in cursor.execute(Path(sql_path, 'create_large_test.sql').read_text().replace('path', data_path), multi=True):
		pass
	for a in cursor.execute(Path(sql_path, 'populate_large_test.sql').read_text().replace('path', data_path), multi=True):
		pass
	

	cnx.commit()
	






