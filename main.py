from fastapi import FastAPI, Query
import pandas as pd
from enum import Enum

title = pd.read_csv('/project/data/transformed_data/title.csv')

class platform_op(str, Enum):
    amazon_prime = 'amazon'
    disney = 'disney'
    netflix = 'netflix'
    hulu = 'hulu'

class duration_type_op(str, Enum):
    film_minutes = 'min'
    seasons = 'season'

splatform = FastAPI()

@splatform.get('/')
def welcome():
    return 'Hello. Please go to the section /docs to know more.'

@splatform.get('/get_max_duration/')
def get_max_duration(
    year: int | None = Query(default = None, title = 'Release Year (number)'),
    platform: platform_op | None = Query(default = None, title = 'Streaming Platform (lower case)'),
    duration_type: duration_type_op | None = Query(default = None, title = 'Duration Type (min/season)')
    ):
    '''
    Movie with maximum duration and optional filters of year, platform & duration type.
    '''
    if platform == 'amazon':
        platform = 'a'
    if platform == 'disney':
        platform = 'd'
    if platform == 'netflix':
        platform = 'n'
    if platform == 'hulu':
        platform = 'h'

    if year:
        if platform:
            if duration_type:
                query = title.query('release_year == @year and id.str.startswith(@platform) == True and duration_type == @duration_type', inplace = False)
                subquery = query.query('duration_int == duration_int.max()', inplace = False)
                subquery = subquery[['title', 'duration_int', 'duration_type']].to_dict()
                return subquery                
            else:
                query = title.query('release_year = @year and id.str.startswith(@platform) == True', inplace = False)
                subquery = query.query('duration_int == duration_int.max()', inplace = False)
                subquery = subquery[['title', 'duration_int', 'duration_type']].to_dict()
                return subquery
        if duration_type:
            query = title.query('release_year == @year and duration_type == @duration_type', inplace = False)
            subquery = query.query('duration_int == duration_int.max()', inplace = False)
            subquery = subquery[['title', 'duration_int', 'duration_type']].to_dict()
            return subquery
        else:
            query = title.query('release_year == @year', inplace = False)
            subquery = query.query('duration_int == duration_int.max()', inplace = False)
            subquery = subquery[['title', 'duration_int', 'duration_type']].to_dict()
            return subquery
    if platform:
        if duration_type:
            query = title.query('id.str.startswith(@platform) == True and duration_type == @duration_type', inplace = False)
            subquery = query.query('duration_int == duration_int.max()', inplace = False)
            subquery = subquery[['title', 'duration_int', 'duration_type']].to_dict()
            return subquery
        else:
            query = title.query('id.str.startswith(@platform) == True', inplace = False)
            subquery = query.query('duration_int == duration_int.max()', inplace = False)
            subquery = subquery[['title', 'duration_int', 'duration_type']].to_dict()
            return subquery
    if duration_type:
        query = title.query('duration_type == @duration_type', inplace = False)
        subquery = query.query('duration_int == duration_int.max()', inplace = False)
        subquery = subquery[['title', 'duration_int', 'duration_type']].to_dict()
        return subquery
    else:
        query = title.query('duration_int == duration_int.max()', inplace = False)
        query = query[['title', 'duration_int', 'duration_type']].to_dict()
        return query

@splatform.get('/get_score_count/{platform}')
def get_score_count(platform: platform_op, score: float, year: int):
    '''
    How many movies are better rated than the score the user inputs, and the year.
    '''
    if platform == 'amazon':
        platform = 'a'
    if platform == 'disney':
        platform = 'd'
    if platform == 'netflix':
        platform = 'n'
    if platform == 'hulu':
        platform = 'h'
    
    query = title.query('id.str.startswith(@platform) == True and rating > @score and release_year == @year', inplace = False)
    subquery = query['id'].to_dict()
    return len(subquery)

@splatform.get('/get_count_platform/{platform}')
def get_count_platform(platform: platform_op):
    '''
    How many movies are in the selected platform.
    '''
    if platform == 'amazon':
        platform = 'a'
    if platform == 'disney':
        platform = 'd'
    if platform == 'netflix':
        platform = 'n'
    if platform == 'hulu':
        platform = 'h'

    query = title.query('id.str.startswith(@platform) == True', inplace = False)
    subquery = query['id'].to_dict()
    return len(subquery)

@splatform.get('/get_actor/{platform}')
def get_actor(platform: platform_op, year: int):
    '''
    Which is the actor or actors that appear more in movies of that platform and year.
    '''
    if platform == 'amazon':
        platform = 'a'
    if platform == 'disney':
        platform = 'd'
    if platform == 'netflix':
        platform = 'n'
    if platform == 'hulu':
        platform = 'h'

    query = title.query('id.str.startswith(@platform) == True and release_year == @year', inplace = False)

    #Cleaning
    subquery01 = query['cast'].to_string(index = False)
    subquery01 = subquery01.strip()
    subquery01 = subquery01.replace('...', '')
    subquery01 = subquery01.replace('\n', ', ')

    #Separating
    subquery01 = subquery01.split(',')

    #To DataFrame
    subquery01 = pd.DataFrame(subquery01)
    subquery01 = subquery01.rename(columns = {0: 'actor'})

    #More Cleaning
    subquery01['actor'] = subquery01['actor'].str.strip()
    subquery01 = subquery01.replace(r'^\s*$', 'unknown', regex=True)
    subquery01.fillna(value = 'unknown', axis = 0, inplace = True)
    subquery01 = subquery01.replace('NaN', 'unknown', regex = True)
    subquery01 = subquery01[subquery01['actor'] != 'unknown']

    #Counting
    subquery02 = subquery01.groupby(['actor'])['actor'].count().reset_index(name = 'count')
    subquery03 = subquery02.nlargest(1, 'count', keep = 'all')
    subquery03 = subquery03.to_dict()

    return subquery03