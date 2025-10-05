from db import get_connection

connection = get_connection()
cursor = connection.cursor()

def get_default_plants():
    try:
        sql = "SELECT * FROM default_plants"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None