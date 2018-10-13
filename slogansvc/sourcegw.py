from slogansvc.db import alter, fetch
from slogansvc.source import Source


def listall():
    return [to_src(res) for res in fetch(LIST)]


def get(src_id):
    results = fetch(GET, {'id': src_id})
    length = len(results)
    if length > 1:
        raise AssertionError(f'GET should have only retrieved 1 row. Rows: {len(results)}')
    elif length == 0:
        return None
    return to_src(results[0])


def upsert(src):
    return alter(UPSERT, {'source': src.source})[1][0][0]


def delete(src_id):
    return alter(DELETE, {'src_id': src_id})


def to_src(res):
    return Source(res[0], res[1], res[2])


LIST = """SELECT
    id,
    source,
    update_date_time
FROM SOURCE"""

GET = LIST + " WHERE id = %(id)s"

UPSERT = """INSERT INTO SOURCE(source, update_date_time)
VALUES(%(source)s, now()
ON CONFLICT DO SET
    source = excluded.source,
    update_date_time = excluded.update_date_time
RETURNING id"""

DELETE = "DELETE FROM SOURCE WHERE id = %(src_id)s"
