import pandas as pd

print('Reading original dataset...')
title_basics = pd.read_csv('title.basics.tsv', sep='\t').drop(columns=['titleType', 'primaryTitle', 'isAdult', 'endYear'])

print('Executing transform 1/5...')
movie_genre = title_basics.copy()

print('Executing transform 2/5...')
movie_genre = movie_genre[movie_genre.genres.notnull() & (movie_genre.genres != '\\N')]

print('Executing transform 3/5...')
movie_genre['genre'] = movie_genre['genres'].str.split(',')

print('Executing transform 4/5...')
movie_genre = movie_genre[['tconst', 'genre']]
movie_genre = movie_genre.explode('genre')

print('Executing transform 5/5...')
title_basics = title_basics.drop(columns=['genres']).rename(columns={'startYear': 'release_year', 'originalTitle': 'title'})

print('Writing outputs...')
title_basics.to_csv('movies.scsv', sep=';', index=False)
movie_genre.to_csv('movie_genre.scsv', sep=';', index=False)
