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

def get_pins_db():
    try:
        sql = """
            SELECT pin_number FROM sensors;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error occured : {e}")
        return None

def get_chosen_plants(plant_id):
    try:
        sql = "SELECT * FROM default_plants WHERE id IN %s"
        cursor.execute(sql, (plant_id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def new_plant(user_id, plant_id, sensor_name, sensor_pin):
    try:
        sql = "INSERT INTO user_plants(user_id, plant_id, sensor_name, sensor_pin) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, plant_id, sensor_name, sensor_pin))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return {'status' : False}
    
def get_reserved_pins():
    try:
        sql = "SELECT plant_id, sensor_pin FROM user_plants"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def remove_pin(plant_id):
    try:
        sql = "DELETE FROM user_plants WHERE plant_id = %s"
        cursor.execute(sql, (plant_id,))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def user_reserved_pins(user_id):
    try:
        sql = "SELECT sensor_pin FROM user_plants WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return {"status" : False}

def get_user_plants(user_id):
    try:
        sql = """
         SELECT default_plants.*, custom_plants.*, user_plants.*
         FROM user_plants
         LEFT JOIN default_plants ON user_plants.plant_id = default_plants.id
         LEFT JOIN custom_plants  ON user_plants.plant_id = custom_plants.id
         WHERE user_plants.user_id = %s
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return None

def update_plant_moisture(moisture_level, user_id, plant_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = "UPDATE user_plants SET moisture_level = %s WHERE user_id = %s AND plant_id = %s"
        cursor.execute(sql, (moisture_level, user_id, plant_id))
        connection.commit()
        return {'status' : True}
    except Exception as e:
        print(f"Error : {e}")
        return None