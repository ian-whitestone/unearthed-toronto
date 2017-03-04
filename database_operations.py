import psycopg2


def db_connect():
    host = 'some_host'
    conn = psycopg2.connect(host=host,
                            port=5432,
                            database='dfs',
                            user=login['user'],
                            password=login['password'])
    return conn

def insert_query(conn, query, data = False, multiple=False):
    cur = conn.cursor()
    if multiple and data:  # data is a list of tuples
        cur.executemany(query, data)
    elif data:  # data is a single tuple
        cur.execute(query, data)
    else:
        cur.execute(query)
    conn.commit()
    cur.close()
    return


def select_query(conn, query, data=False, cols=False):
    """
    -------
    param
        data <tuple> :

    """
    cur = conn.cursor()
    if data:  # data is a single tuple
        cur.execute(query, data)
        resultset = cur.fetchall()
    else:
        cur.execute(query)
        resultset = cur.fetchall()
    if cols:
        colnames = tuple([desc[0] for desc in cur.description])
        return [colnames]+resultset
    cur.close()
    return resultset
