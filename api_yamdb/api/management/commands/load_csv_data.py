import sqlite3
import pandas as pd
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = sqlite3.connect('./db.sqlite3')
        c = conn.cursor()
        try:
            category = pd.read_csv('./static/data/category.csv')
            category.to_sql('titles_category', conn, if_exists='append', index = False, chunksize = 10000)
        except Exception as e:
            print(e)
        try:
            genre = pd.read_csv('./static/data/genre.csv')
            genre.to_sql('titles_genre', conn, if_exists='append', index = False, chunksize = 10000)
        except Exception as e:
            print(e)
        try:  
            comments = pd.read_csv('./static/data/genre.csv')
            comments.to_sql('titles_comments', conn, if_exists='append', index = False, chunksize = 10000)
        except Exception as e:
            print('comments', e)
        try:
            genre_title = pd.read_csv('./static/data/genre_title.csv')
            genre_title.to_sql('titles_genre_title', conn, if_exists='append', index = False, chunksize = 10000)
        except Exception as e:
            print('genre_title', e)
        try:
            review = pd.read_csv('./static/data/review.csv')
            review.to_sql('titles_review', conn, if_exists='append', index = False, chunksize = 10000)
        except Exception as e:
            print('review', e)
        try:
            titles = pd.read_csv('./static/data/titles.csv')
            titles.to_sql('titles_titles', conn, if_exists='append', index = False, chunksize = 10000)
        except Exception as e:
            print('titles', e)
        try:
            users = pd.read_csv('./static/rdata/users_yamdbuser.csv')
            users.to_sql('users_yamdbuser', conn, if_exists='append', index = False, chunksize = 10000)
        except Exception as e:
            print('users', e)
