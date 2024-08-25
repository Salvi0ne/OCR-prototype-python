import psycopg2
from psycopg2 import sql


db_params = {
    'dbname': 'hello_world',        
    'user': 'wan_afnan_hariz',      
    'password': '',    
    'host': 'localhost',            
    'port': '5432'                  
}

# Establish the connection
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    
    print("Connection successful")

    # Example query
    query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier('hello_table'))
    cursor.execute(query)

    # Fetch results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
