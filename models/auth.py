from db import get_connection

connection = get_connection()
cursor = connection.cursor()

def validate_login(email, password):
    try:
        sql = "SELECT * FROM user_accounts WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None