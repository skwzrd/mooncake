import os
import sqlite3
from flask import current_app, g
from config import init_sql_path, db_path, translations_path
import pandas as pd


def init_db_schema():
    """https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#initial-schemas"""
    with current_app.app_context():
        db = get_db()
        with current_app.open_resource(init_sql_path, mode='r') as f:
            sql_string = f.read()
            db.cursor().executescript(sql_string)
        db.commit()


def init_db_data():
    df = pd.read_csv(translations_path)
    with get_db() as conn:
        df.to_sql('character', conn, 'main', if_exists='append', index_label='id')


def is_db_initialized():
    return os.path.exists(db_path)


def init_db_sequence():
    print('initializing db...')
    init_db_schema()
    init_db_data()


def get_db():
    """https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#using-sqlite-3-with-flask
    https://www.reddit.com/r/flask/comments/5ggh7j/what_is_flaskg/
    """
    with current_app.app_context():
        db = getattr(g, 'database', None)
        if db is None:
            db_initialized = is_db_initialized()
            g.database = sqlite3.connect(db_path)
            if not db_initialized:
                init_db_sequence()
            db = g.database

        # Make using dictionary syntax available with:
        db.row_factory = sqlite3.Row
        return db


def query_db(query, args=(), one=False, one_one=False):
    """https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying"""
    with current_app.app_context():
        try:
            with get_db() as conn:
                print(query.replace('?', '{}').format(*args))
                cur = conn.execute(query, args)
                r = cur.fetchall()
                if 'select' not in query:
                    conn.commit()
                cur.close()
            if r == []:
                return None
            if one:
                return r[0] if r else None
            if one_one:
                return r[0][0] if r else None
            return r
        except Exception as e:
            raise Exception(e)


def query_db_df(sql_string, params=None):
    with current_app.app_context():
        try:
            with get_db() as conn:
                df = pd.read_sql(sql_string, conn, params=params)
        except Exception as e:
            print(sql_string, params, sep='\n')
            raise Exception(e) from None
    return df
