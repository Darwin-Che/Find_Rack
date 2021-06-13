import pandas as pd

title_basics = pd.read_csv('title.basics.tsv', sep='\t').drop(columns=['titleType', 'primaryTitle', 'isAdult', 'endYear'])
genre_dict = {'tconst': [], 'genre': []}

for index, row in title_basics.iterrows():
    if type(row['genres']) is str:
        for genre in row['genres'].split(','):
            genre_dict['tconst'].append(row['tconst'])
            genre_dict['genre'].append(genre)

movie_genre = pd.DataFrame(data=genre_dict)
title_basics = title_basics.drop(columns=['genres']).rename(columns={'startYear': 'release_year', 'originalTitle': 'title'})

title_basics.to_csv('movies.scsv', sep=';', index=False)
movie_genre.to_csv('movie_genre.scsv', sep=';', index=False)

