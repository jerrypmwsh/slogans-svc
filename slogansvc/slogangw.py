from slogansvc.db import fetch, alter
from slogansvc.slogan import Slogan

ID = 0
SLOGAN = 1
COMPANY = 2
CATEGORY_ID = 3
SOURCE_ID = 4
SOURCE_INFO = 5
UPDATE_DATE_TIME = 6


def listall(distinct: bool = False):
    results = fetch(LIST_DISTINCT) if distinct else fetch(LIST)
    return [_slogan(res) for res in results]


def get(s_id):
    results = fetch(GET, {'id': s_id})
    length = len(results)
    if length > 1:
        raise AssertionError(f'GET should have only retrieved 1 row. Rows retrieved: {length}')
    elif length == 0:
        return None

    return _slogan(results[0])


def upsert(slogan: dict):

    if 's_id' in slogan.keys():
        return alter(UPDATE, {
            's_id': slogan['s_id'],
            'slogan': slogan.get('slogan'),
            'company': slogan.get('company'),
            'category_id': slogan.get('category_id'),
            'source_id': slogan.get('source_id'),
            'source_info': slogan.get('source_info'),
        })[1][0][0]

    return alter(INSERT, {
        'slogan': slogan.get('slogan'),
        'company': slogan.get('company'),
        'category_id': slogan.get('category_id'),
        'source_id': slogan.get('source_id'),
        'source_info': slogan.get('source_info'),
    })[1][0][0]


def delete(s_id):
    return alter(DELETE, {'id': s_id})


def _slogan(res):
    return Slogan(
        res[ID],
        res[SLOGAN],
        res[COMPANY],
        res[CATEGORY_ID],
        res[SOURCE_ID],
        res[SOURCE_INFO],
        res[UPDATE_DATE_TIME]
    )


LIST = """SELECT
    s.id,
    s.slogan,
    s.company,
    c.category,
    src.source,
    s.source_info,
    s.update_date_time
FROM SLOGAN s LEFT OUTER JOIN CATEGORY c
ON s.category_id = c.id
LEFT OUTER JOIN SOURCE src
ON s.source_id = src.id"""

LIST_DISTINCT = """SELECT DISTINCT ON (s.slogan, s.company)
    s.id,
    s.slogan,
    s.company,
    c.category,
    src.source,
    s.source_info,
    s.update_date_time
FROM SLOGAN s LEFT OUTER JOIN CATEGORY c
ON s.category_id = c.id
LEFT OUTER JOIN SOURCE src
ON s.source_id = src.id"""

INSERT = """INSERT INTO SLOGAN (
    slogan, 
    company,
    category_id, 
    source_id, 
    source_info, 
    update_date_time) 
VALUES (%(slogan)s, %(company)s, %(category_id)s, %(source_id)s, %(source_info)s, now())
RETURNING id
"""

UPDATE = """UPDATE SLOGAN SET
    slogan = %(slogan)s,
    company = %(company)s,
    category_id = %(category_id)s,
    source_id = %(source_id)s,
    source_info = %(source_info)s,
    update_date_time = now()
WHERE id = %(s_id)s
RETURNING id"""

DELETE = "DELETE FROM SLOGAN WHERE id = %(id)s"

GET = LIST + " WHERE s.id = %(id)s"
