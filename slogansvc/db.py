from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import OperationalError, ProgrammingError, Error
from time import sleep
import os

DB_KEYS = [
    'dbname',
    'user',
    'password',
    'host',
    'port',
    'minconn',
    'maxconn',
]


def _db_conf():
    conf = {}
    for key in DB_KEYS:
        conf[key] = os.environ[key]
    return conf


def fetch(query, args=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args if args else ())
            res = cur.fetchall()
    return res


def alter(query, args=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            count = cur.rowcount
            rows = []
            try:  # Not all alters return a row
                rows = cur.fetchall()
            except ProgrammingError:
                pass
    return count, rows


@contextmanager
def get_conn():
    conn = POOL.getconn()
    try:
        yield conn
    except Error as e:
        try:
            conn.rollback()
        except Error as e:
            raise OperationalError("Error while attempting to rollback", e)
        raise e
    try:
        conn.commit()
    except Error as e:
        raise OperationalError("Error while attempting to commit", e)
    POOL.putconn(conn)


def init():
    connected = False
    tries = 0
    while not connected and tries < 5:
        try:
            global POOL
            POOL = ThreadedConnectionPool(**_db_conf())
            connected = True
        except OperationalError:
            print(f'Retrying connection to db: {tries}')
            tries += 1
            sleep(5)
    if not connected:
        raise Exception("could not connect to db")


init()
