import pandas as pd

title_crew = pd.read_csv('title.crew.tsv', sep='\t').drop(columns=['directors'])
writer_dict = {'tconst': [], 'nconst': [], 'category': []}

for index, row in title_crew.iterrows():
    if type(row['writers']) is str and row['writers'] != '\\N':
            for writer in row['writers'].split(','):
                writer_dict['tconst'].append(row['tconst'])
                writer_dict['nconst'].append(writer)
                writer_dict['category'].append('writer')

writer_df = pd.DataFrame(data=writer_dict)
                
title_principals = pd.read_csv('title.principals.tsv', sep='\t').drop(columns=['ordering', 'job', 'characters']).append(writer_df)

name = pd.read_csv('name.basics.tsv', sep='\t')[['nconst', 'primaryName']]

cast_table = title_principals.rename(columns={'category': 'role'})
cast_table.to_csv('cast.scsv', sep=';', index=False)
name.to_csv('name.scsv', sep=';', index=False)
