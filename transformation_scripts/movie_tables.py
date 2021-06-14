import pandas as pd

print('Reading original dataset...', flush=True)
title_basics = pd.read_csv('title.basics.tsv', sep='\t')

print('Removing invalid data...', flush=True)
# Sometimes rows are parsed incorrectly (due to movie titles having quotation marks)
# We detect these rows by checking whether or not the row has the correct amount of columns
# We then discard these rows
title_basics = title_basics[title_basics[title_basics.columns[-1]].notnull()]
# Discard rows movies with crazy long titles
title_basics = title_basics[title_basics.originalTitle.str.len() <= 400]
title_basics = title_basics.drop(columns=['titleType', 'primaryTitle', 'isAdult', 'endYear'])

print('Executing transform 1/5...', flush=True)
movie_genre = title_basics.copy()

print('Executing transform 2/5...', flush=True)
movie_genre = movie_genre[movie_genre.genres.notnull() & (movie_genre.genres != '\\N')]

print('Executing transform 3/5...', flush=True)
movie_genre['genre'] = movie_genre['genres'].str.split(',')

print('Executing transform 4/5...', flush=True)
movie_genre = movie_genre[['tconst', 'genre']]
movie_genre = movie_genre.explode('genre')

print('Executing transform 5/5...', flush=True)
title_basics = title_basics.drop(columns=['genres']).rename(columns={'startYear': 'release_year', 'originalTitle': 'title'})

print('Writing outputs...', flush=True)
title_basics.to_csv('movies.scsv', sep=';', index=False)
movie_genre.to_csv('movie_genre.scsv', sep=';', index=False)
