# %%
#Import libraries.
import pandas as pd

# %%
#Read each file.
one = pd.read_csv('source_data/ratings/1.csv')
two = pd.read_csv('source_data/ratings/2.csv')
three = pd.read_csv('source_data/ratings/3.csv')
four = pd.read_csv('source_data/ratings/4.csv')
five = pd.read_csv('source_data/ratings/5.csv')
six = pd.read_csv('source_data/ratings/6.csv')
seven = pd.read_csv('source_data/ratings/7.csv')
eight = pd.read_csv('source_data/ratings/8.csv')

# %%
#Unite files.
data = [one, two, three, four, five, six, seven, eight]
ratings = pd.concat(data)

# %%
#Modify timestamp.
ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit = 's')


# %%
#Change titles.
ratings['id'] = ratings['movieId']
del ratings['movieId']
ratings['user_id'] = ratings['userId']
del ratings['userId']
ratings = ratings[['id', 'user_id', 'rating', 'timestamp']]

# %%
#Add year column.
ratings['rating_year'] = ratings['timestamp'].dt.year
ratings.head()

# %%
#Export 'ratings'.
ratings.to_csv('transformed_data/ratings')

# %%
#Export 'average_rating'.
mean = ratings.groupby('id')['rating'].mean()
mean.to_csv('transformed_data/average_rating')


