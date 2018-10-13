from slogansvc.category import Category
from slogansvc.db import alter, fetch


def listall():
    return [to_category(res) for res in fetch(LIST)]


def get(c_id):
    results = fetch(GET, {'id': c_id})
    length = len(results)
    if length > 1:
        raise AssertionError(f'GET should have only retrieved 1 row. Rows: {len(results)}')
    elif length == 0:
        return None
    return to_category(results[0])


def upsert(category):
    return alter(UPSERT, {'category': category.category})[1][0][0]


def delete(c_id):
    return alter(DELETE, {'c_id': c_id})


def to_category(res):
    return Category(res[0],res[1], res[2])


LIST = """SELECT
    id,
    category,
    update_date_time
FROM CATEGORY"""

GET = LIST + " WHERE id = %(id)s"

UPSERT = """INSERT INTO CATEGORY(
    category, 
    update_date_time) 
VALUES (%(category)s, now())
ON CONFLICT DO SET
    category = excluded.category
    update_date_time = excluded.update_date_time
RETURNING id"""

DELETE = "DELETE FROM CATEGORY WHERE id = %(c_id)s"
