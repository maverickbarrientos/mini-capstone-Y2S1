from db import get_connection

connection = get_connection()
cursor = connection.cursor()

def get_user(user_id):
    try:
        sql = "SELECT * FROM user_details WHERE id = %s"
        cursor.execute(sql, (user_id, ))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None