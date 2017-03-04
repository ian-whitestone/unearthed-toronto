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
        cols <boolean> : if True, return list of dicts where keys are column names
                         if False, return list of tuples
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
        resultset = [{colnames[col_index]:value
            for col_index, value in enumerate(result)} for result in resultset]

    cur.close()
    return resultset
