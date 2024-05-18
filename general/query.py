from django.db import connection

def add_query(query):
  connection.cursor().execute(query)
  connection.close()



def query_select(query, param):
  with connection.cursor() as cursor:
    cursor.execute(query, param)
    result = cursor.fetchall()
    return result
  
def query_delete(query):
  with connection.cursor() as cursor:
    cursor.execute(query)

def parse(result):
    data = result[0][0]
    return data