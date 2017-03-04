import psycopg2


def db_connect():
    host = 'ec2-54-173-238-7.compute-1.amazonaws.com'
    conn = psycopg2.connect(host=host,
                            port=5432,
                            database='postgis',
                            user='postgres',
                            password='barrick')
    return conn

def execute_query(conn, query, data = False, multiple=False):
    """ Insert, update, delete statements
    ------
    """
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
    """ select statemtns
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
