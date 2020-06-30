import psycopg2
from psycopg2 import extras


class DatabaseConnection:

    def __init__(self, connection):
        self.dsn = connection
        self._conn = None
        self._cur = None
        self._result = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, ctype, value, traceback):
        self.close()

    def connect(self):
        if self._conn is None:
            self._conn = psycopg2.connect(self.dsn)
            self._cur = self._conn.cursor(cursor_factory=extras.RealDictCursor)

    def close(self):
        self._cur.close()
        self._conn.close()

        self._conn = None
        self._cur = None
        self._result = None

    def query(self, sql_query, params=()):
        self._cur.execute(sql_query, params)
        self._result = self._cur.fetchall()
        return self._result

    def insert(self, sql_query, params=()):
        self._cur.execute(sql_query, params)
        self.commit()

    def commit(self):
        self._conn.commit()

    def get_last_result(self):
        return self._result

    def is_connected(self):
        return self._conn is not None
