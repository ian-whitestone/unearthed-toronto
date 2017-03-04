import src.database_operations as dbo



conn = dbo.db_connect()

f = open('data/mines.txt', encoding='latin-1')

lines = f.readlines()
data = [tuple(line.strip().split('\t')) for line in lines]

# for x in data:
#     if len(x[2])>200:
#         print (len(x[2]), x[2])

try:
    query = "INSERT INTO public.mines VALUES (%s, %s, %s, %s, %s, %s, %s)"
    dbo.execute_query(conn, query, data[1:], multiple = True)
except Exception as e:
    print (e)

conn.close()
