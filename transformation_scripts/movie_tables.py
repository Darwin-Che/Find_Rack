import pandas as pd

print('Reading original dataset...')
title_basics = pd.read_csv('title.basics.tsv', sep='\t').drop(columns=['primaryTitle', 'isAdult', 'endYear'])

print('Executing transform 1/6...')
title_basics = title_basics[title_basics.titleType == 'movie'].drop(columns=['titleType'])

print('Executing transform 2/6...')
movie_genre = title_basics.copy()

print('Executing transform 3/6...')
movie_genre = movie_genre[movie_genre.genres.notnull() & (movie_genre.genres != '\\N')]

print('Executing transform 4/6...')
movie_genre['genre'] = movie_genre['genres'].str.split(',')

print('Executing transform 5/6...')
movie_genre = movie_genre[['tconst', 'genre']]
movie_genre = movie_genre.explode('genre')

print('Executing transform 6/6...')
title_basics = title_basics.drop(columns=['genres']).rename(columns={'startYear': 'release_year', 'originalTitle': 'title'})

print('Writing outputs...')
title_basics.to_csv('movies.scsv', sep=';', index=False)
movie_genre.to_csv('movie_genre.scsv', sep=';', index=False)
