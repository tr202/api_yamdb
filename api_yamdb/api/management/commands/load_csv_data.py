import sqlite3

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            import pandas as pd
        except Exception as e:
            print('Unable to import pandas', e)
        conn = sqlite3.connect('./db.sqlite3')
        conn.cursor()
        self.handle_1(conn, pd)
        self.handle_2(conn, pd)

    def handle_1(self, conn, pd):

        # ---------------------users---------------------------
        try:
            users = pd.read_csv('./static/rdata/users_yamdbuser.csv')
            users.to_sql('users_yamdbuser', conn, if_exists='append',
                         index=False, chunksize=10000)
        except Exception as e:
            print('users', e)
        # ---------------------category---------------------------
        try:
            category = pd.read_csv('./static/rdata/titles_category.csv')
            category.to_sql('reviews_category', conn, if_exists='append',
                            index=False, chunksize=10000)
        except Exception as e:
            print('category', e)

        # ---------------------genre---------------------------
        try:
            genre = pd.read_csv('./static/rdata/titles_genre.csv')
            genre.to_sql('reviews_genre', conn, if_exists='append',
                         index=False, chunksize=10000)
        except Exception as e:
            print('genre', e)

    def handle_2(self, conn, pd):
        # ---------------------title---------------------------
        try:
            titles = pd.read_csv('./static/rdata/titles_titles.csv')
            titles.to_sql('reviews_title', conn, if_exists='append',
                          index=False, chunksize=10000)
        except Exception as e:
            print('titles', e)
        # ---------------------genre_title---------------------------
        try:
            genre_title = pd.read_csv('./static/rdata/titles_genre_title.csv')
            genre_title.to_sql('reviews_genretitle', conn, if_exists='append',
                               index=False, chunksize=10000)
        except Exception as e:
            print('titles_genretitle', e)
        # ---------------------review---------------------------
        try:
            review = pd.read_csv('./static/rdata/titles_review.csv')
            review.to_sql('reviews_review', conn, if_exists='append',
                          index=False, chunksize=10000)
        except Exception as e:
            print('review', e)
        # ---------------------comment---------------------------
        try:
            comments = pd.read_csv('./static/rdata/titles_comments.csv')
            comments.to_sql('reviews_comment', conn, if_exists='append',
                            index=False, chunksize=10000)
        except Exception as e:
            print('comments', e)
