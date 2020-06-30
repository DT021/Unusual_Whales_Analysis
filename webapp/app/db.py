from data.database.db_api import DatabaseConnection

from flask import Flask
from flask import current_app, g
from psycopg2.extras import RealDictCursor

def get_db():
    """

    :return: DatabaseConnection
    """
    if 'db' not in g:
        g.db = DatabaseConnection(current_app.config['PSYCOPG2_URL'])

    return g.db


def close(e=None):
    db: DatabaseConnection = g.pop('db', None)

    if db is not None:
        db.close()


def query_db(sql_query, params=()):
    """

    :param sql_query:
    :param params:
    :return:
    """
    db = get_db()

    if not db.is_connected():
        db.connect()

    return db.query(sql_query, params)


def insert(sql_query, params=()):

    db = get_db()

    if not db.is_connected():
        db.connect()

    db.insert(sql_query, params)


def init_app(app: Flask):
    app.teardown_appcontext(close)