# %%
#Import libraries.
import pandas as pd

# %%
#Read files.
prime = pd.read_csv('source_data/amazon_prime_titles.csv')
disney = pd.read_csv('source_data/disney_plus_titles.csv')
hulu = pd.read_csv('source_data/hulu_titles.csv')
netflix = pd.read_csv('source_data/netflix_titles.csv')

# %%
#Add id column
prime.insert(0, 'id', 'a' + prime['show_id'], allow_duplicates = False)
disney.insert(0, 'id', 'd' + disney['show_id'], allow_duplicates = False)
hulu.insert(0, 'id', 'h' + hulu['show_id'], allow_duplicates = False)
netflix.insert(0, 'id', 'n' + netflix['show_id'], allow_duplicates = False)

# %%
#Replace NaN for 'G' (General for all audiences) on 'rating'.
prime['rating'] = prime['rating'].fillna('G')
disney['rating'] = disney['rating'].fillna('G')
hulu['rating'] = hulu['rating'].fillna('G')
netflix['rating'] = netflix['rating'].fillna('G')

# %%
#Change 'date_added' to datetime format.
prime['date_added'] = pd.to_datetime(prime['date_added'])
disney['date_added'] = pd.to_datetime(disney['date_added'])
hulu['date_added'] = pd.to_datetime(hulu['date_added'])
netflix['date_added'] = pd.to_datetime(netflix['date_added'])

# %%
#All to lower case.
strings = ['type', 'title', 'director', 'cast', 'country', 'listed_in', 'description']

for string in strings:
    try:
        prime[string] = prime[string].str.lower()
        disney[string] = disney[string].str.lower()
        netflix[string] = netflix[string].str.lower()
        hulu[string] = hulu[string].str.lower()
    except AttributeError:
        continue

# %%
#Split 'duration' into 'duration_int' (integer) & 'duration_type' (string).
prime[['duration_int', 'duration_type']]= prime['duration'].str.split(" ", expand = True)
del prime['duration']
prime = prime[['id', 'show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added', 'release_year', 'duration_int', 'duration_type', 'listed_in', 'description']]

disney[['duration_int', 'duration_type']]= disney['duration'].str.split(" ", expand = True)
del disney['duration']
disney = disney[['id', 'show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added', 'release_year', 'duration_int', 'duration_type', 'listed_in', 'description']]

hulu[['duration_int', 'duration_type']] = hulu['duration'].str.split(" ", expand = True)
del hulu['duration']
hulu = hulu[['id', 'show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added', 'release_year', 'duration_int', 'duration_type', 'listed_in', 'description']]

netflix[['duration_int', 'duration_type']] = netflix['duration'].str.split(" ", expand = True)
del netflix['duration']
netflix = netflix[['id', 'show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added', 'release_year', 'duration_int', 'duration_type', 'listed_in', 'description']]

# %%
#Change missing values on 'duration_int' for 0.
prime['duration_int'] = prime['duration_int'].fillna(0)
disney['duration_int'] = disney['duration_int'].fillna(0)
hulu['duration_int'] = hulu['duration_int'].fillna(0)
netflix['duration_int'] = netflix['duration_int'].fillna(0)

# %%
#Turn datatype to int.
prime['duration_int'] = prime['duration_int'].astype('int')
disney['duration_int'] = disney['duration_int'].astype('int')
hulu['duration_int'] = hulu['duration_int'].astype('int')
netflix['duration_int'] = netflix['duration_int'].astype('int')

# %%
#Unite the DataFrames.
platforms = [prime, disney, hulu, netflix]
titles = pd.concat(platforms)

# %%
#Import 'average_rating'.
average_rating = pd.read_csv('transformed_data/average_rating')

# %%
#Join 'average_rating' with 'title'.
title = titles.set_index('id').join(average_rating.set_index('id'))

# %%
#Final changes on 'duration_type'.
title['duration_type'] = title['duration_type'].replace(['Seasons', 'seasons', 'Season'], 'season')

# %%
#Export 'title'.
title.to_csv('transformed_data/title')


