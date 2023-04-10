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





    '''
    def handle(self, *args, **options):
        convert('./static/data/category.csv', './db.sqlite3', 'titles_category')
        convert('./static/data/comments.csv', './db.sqlite3', 'titles_comments')
        convert('./static/data/genre_title.csv', './db.sqlite3', 'titles_genre_title')
        convert('./static/data/genre.csv', './db.sqlite3', 'titles_genre')
        convert('./static/data/review.csv', './db.sqlite3', 'titles_review')
        convert('./static/data/titles.csv', './db.sqlite3', 'titles_titles')
        convert('./static/data/users.csv', './db.sqlite3', 'users_yamdbuser')
    '''
    
    '''
    def handle(self, *args, **options):
        options = csv_to_sqlite.CsvOptions(typing_style="full") 
        input_files = ['./static/rdata/titles_category.csv',
                       './static/rdata/titles_comments.csv',
                       './static/rdata/titles_genre_title.csv',
                       './static/rdata/titles_genre.csv',
                       './static/rdata/titles_review.csv',
                       './static/rdata/titles_titles.csv',
                       './static/rdata/users_yamdbuser.csv']
        csv_to_sqlite.write_csv(input_files, './db.sqlite3', options)
    '''
        