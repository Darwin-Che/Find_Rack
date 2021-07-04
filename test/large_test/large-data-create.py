import random
import datetime

#### 
print('load in the entries of Movies.scsv')
f = open("realdata/movies.scsv")
movies = f.readlines()
f.close()

def randmovieid():
	return movies[random.randint(1,len(movies)-1)].split(';')[0]

#### create user data

print('How many users you want? (user id starting from 0) ')
user_n = int(input())

print('creating Users.scsv {}'.format(user_n))

f = open("Users.scsv", "w")
f.write('userid;username;password\n');

for i in range(user_n):
	f.write('u{};user{};passwordfor{}\n'.format(i, i, i))

f.close()

#### create list data

print('How many lists you want? (list id starting from 0)')
list_n = int(input())

print('creating Lists.scsv {}'.format(list_n))

f = open("Lists.scsv", "w")
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

print('creating comments.scsv {}'.format(list_n))

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









