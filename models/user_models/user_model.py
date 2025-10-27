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
    
def get_number_of_plants(user_id):
    try:
        sql = "SELECT COUNT(*) FROM user_plants WHERE user_id = %s"
        cursor.execute(sql, (user_id))
        result = cursor.fetchone()["COUNT(*)"]
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def update_photo(image, user_id):
    try:
        sql = "UPDATE user_details SET profile_photo = %s WHERE id = %s"
        cursor.execute(sql, (image, user_id))
        connection.commit()
        print(image)
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None

def update_user(first_name, last_name, email, phone_number, birthdate, user_id):
    try:
        sql_update = """
            UPDATE user_details SET first_name = %s, last_name = %s, birthdate = %s, email = %s, phone_number = %s WHERE id = %s;
        """
        cursor.execute(sql_update, (first_name, last_name, birthdate, email, phone_number, user_id))
        connection.commit()
        return {"successful" : True}
    except Exception as e:
        print(f"Error : {e}") 
        return {"successful" : False}