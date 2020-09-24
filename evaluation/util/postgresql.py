import psycopg2

GET_INDEX_NAME_QUERY = '''
SELECT
    indexname
FROM
    pg_indexes
WHERE
    schemaname = 'public' and
    tablename like '{}' and 
    indexdef like '%{}%'
ORDER BY
    tablename,
    indexname;
'''

DROP_INDEX_STATEMENT = 'DROP INDEX "{}"; commit;'


def remove_index(resource_id, column):
    connection = psycopg2.connect(user="ckan",
                                  password="ckan",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="datastore")

    curs = connection.cursor()
    curs.execute(GET_INDEX_NAME_QUERY.format(resource_id, column))
    idx_name = curs.fetchone()[0]
    print(idx_name)
    curs.execute(DROP_INDEX_STATEMENT.format(idx_name))