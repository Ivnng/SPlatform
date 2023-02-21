# SPlatform

Hello.
This is SPlatform project. Its purpose is to create an API (Application Programming Interface) called 'HPI01' to review some queries about a movie dataset.

The source dataset is composed of the following files:

* source_data:
  * amazon_prime_titles.csv
  * disney_plus_titles.csv
  * hulu_titles.csv
  * netflix_titles.csv
  * ratings:
    * 1.csv
    * 2.csv
    * 3.csv
    * 4.csv
    * 5.csv
    * 6.csv
    * 7.csv
    * 8.csv

An ETL (Extraction, Transformation and Load) process was done on the source files and the resulting files are:

* transform_ratings.py
* transform_titles.py

* transformed_data:
  * average_rating.csv
  * ratings.csv
  * title.csv

In this repository you can find the 'title.csv', 'transform_ratings.py' and 'transform_titles.py' files inside the data folder.
You can find the rest of the files, including the source data, here:
https://mega.nz/folder/umIgGLTb#GtdfJXpJJGORmujvGbJMZg

To create the API, FastAPI & Uvicorn were used to test locally. Then, Docker was used to create the Dockerfile and be able to deploy on render.

The API has four main queries:
1. /get_max_duration/
2. /get_score_count/{platform}
3. /get_count_platform/{platform}
4. /get_actor/{platform}

You can test it here:
https://hpi01.onrender.com

See the /docs for more guidance.

The next part of the project was made using the same source data, and it's called MPlatform:
https://github.com/Ivnng/MPlatform
