from db import get_connection
from services.entity_services import newUser

connection = get_connection()
cursor = connection.cursor()

def get_users():
    sql_fetch = "SELECT * FROM user_details"
    cursor.execute(sql_fetch)
    result = cursor.fetchall()
    return result

def get_user_data(id):
    sql_user = "SELECT * FROM user_details WHERE id = %s"
    cursor.execute(sql_user, (id, ))
    user_data = cursor.fetchone()
    return user_data

def update_user_process(first_name, last_name, birthdate, email, phone_number, id):
    try:
        sql_update = """
            UPDATE user_details SET first_name = %s, last_name = %s, birthdate = %s, email = %s, phone_number = %s WHERE id = %s;
        """
        cursor.execute(sql_update, (first_name, last_name, birthdate, email, phone_number, id))
        connection.commit()
        return {"successful" : True}
    except Exception as e:
        print(f"Error : {e}") 
        return {"successful" : False}

def delete_user_process(id):
    try:
        sql_delete = "DELETE FROM user_details WHERE id = %s"
        cursor.execute(sql_delete, (id, ))
        connection.commit()
        return {"successful" : True}
    except Exception as e:
        print(f"Error : {e}")
        return {"successful" : False}