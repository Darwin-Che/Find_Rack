import pandas as pd

print('Reading original dataset...', flush=True)
title_crew = pd.read_csv('title.crew.tsv', sep='\t').drop(columns=['directors'])
name = pd.read_csv('name.basics.tsv', sep='\t')[['nconst', 'primaryName']]

print('Executing transform 1/5...', flush=True)
filtered_title_crew = title_crew[title_crew.writers.notnull() & (title_crew.writers != '\\N')]
print('Executing transform 2/5...', flush=True)
filtered_title_crew['writers'] = filtered_title_crew['writers'].str.split(',')
print('Executing transform 3/5...', flush=True)
filtered_title_crew = filtered_title_crew.explode('writers')
filtered_title_crew = filtered_title_crew.rename(columns={"writers":"nconst"})
filtered_title_crew['category'] = 'writer'
                
print('Executing transform 4/5...', flush=True)
title_principals = pd.read_csv('title.principals.tsv', sep='\t').drop(columns=['ordering', 'job', 'characters']).append(filtered_title_crew)

print('Executing transform 5/5...', flush=True)
cast_table = title_principals.rename(columns={'category': 'role'})[['nconst','tconst','role']]

print('Writing outputs...', flush=True)
cast_table.to_csv('cast.scsv', sep=';', index=False)
name.to_csv('name.scsv', sep=';', index=False)
